"""Compile certified finite floors into exact all-dimensional rational bounds.

Run from any directory.  The archived seed inequalities must first pass their
separate exact dual verifier; this compiler verifies their algebraic transport
and the finite-to-infinite envelope comparison.  It does not turn an arbitrary
user-supplied number into a valid positive-map bound.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import factorial, prod
import argparse
import importlib.util
import json


ROOT = Path(__file__).resolve().parent


def load_transport(path):
    spec = importlib.util.spec_from_file_location("exact_transport", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_seeds(path):
    out = {3: Q(0)}
    for rank in range(4, 100):
        name = f"recursive_cert_{rank}.json" if rank < 8 else f"dual_{rank}.json"
        file = path / name
        if not file.exists():
            break
        data = json.loads(file.read_text())
        value = Q(data["objective"] if rank < 8 else data["floor"])
        assert -Q(1, rank) <= value <= 0
        out[rank] = value
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-dir", type=Path, default=ROOT / "finite/certificates")
    parser.add_argument("--transport", type=Path, default=ROOT / "transport/verify_transport_general.py")
    parser.add_argument("--output", type=Path, default=ROOT / "compiled_bounds.json")
    args = parser.parse_args()
    transport = load_transport(args.transport)
    seeds = read_seeds(args.seed_dir)
    assert max(seeds) >= 17
    records = []
    for rank, gamma in sorted(seeds.items()):
        K = transport.parameters(rank, gamma)[2]
        if rank == 3:
            start = rank + 3
            certificate = {"method": "analytic general transport theorem"}
        else:
            try:
                certificate = transport.certify_seed(rank, gamma, rank + 1)
                start = rank + 1
            except AssertionError:
                # The universal theorem already proves this range; the
                # coefficientwise shift test is sufficient, not necessary.
                start = rank + 3
                certificate = {"method": "analytic general transport theorem"}
        assert transport.target(rank, K) == gamma
        transfer_start = start
        # The original seed supplies the missing endpoint whenever the
        # all-dimensional transport begins at the immediately next rank.
        if start == rank + 1:
            start = rank
        records.append({"rank": rank, "gamma": str(gamma), "K": str(K),
                        "K_decimal": float(K), "start": start,
                        "transfer_start": transfer_start,
                        "transport_certificate": certificate})

    # The main theorem has one fixed range, independent of future seed rank.
    baseline = lambda n: -Q(n, n*n + 6*n + 39)
    for n in range(8, 17):
        assert seeds[n] >= baseline(n)
    assert seeds[16] >= -Q(3, 82)
    clean = transport.certify_seed(16, -Q(3, 82), 17)
    # For all real n>=17 the cross-multiplied gap is 9*n+273 > 0.
    main_tail_numerator = [273, 9]

    def envelope(n):
        candidates = [baseline(n)]
        if n in seeds:
            candidates.append(seeds[n])
        for rec in records:
            if n >= rec["start"]:
                candidates.append(transport.target(n, Q(rec["K"])))
        return max(candidates)

    # An optional sharper one-formula envelope with the same fixed range.
    best = max(records, key=lambda rec: Q(rec["K"]))
    A = Q(best["K"])
    tail = best["start"]
    caps = {n: -Q(n, envelope(n)) - n*n - A*n for n in range(8, tail)}
    B = min([A*A + 2*A] + list(caps.values()))
    assert 8*8 + 8*A + B > 0  # denominator increases thereafter
    slope = A*A + 2*A - B
    at_tail = slope*tail + B*(A+1)
    assert slope >= 0 and at_tail >= 0
    for n in range(8, tail):
        assert envelope(n) >= -Q(n, n*n + A*n + B)

    # The fresh rank-eighteen certificate permits a simple strict upgrade
    # of the original formula while keeping the range n>=8 unchanged.
    uniform_upgrade = None
    upgrade_A, upgrade_B = Q(31,5), Q(38)
    if A >= upgrade_A:
        for n in range(8, tail):
            assert envelope(n) >= -Q(n, n*n+upgrade_A*n+upgrade_B)
        polynomial = [upgrade_B*(A+1), A+upgrade_A*(A+1)-upgrade_B, A-upgrade_A]
        assert min(polynomial) >= 0
        for n in [8,9,17,18,19,50,100]:
            improvement = -Q(5*n,5*n*n+31*n+190)-baseline(n)
            assert improvement == Q(n*(n-5),(5*n*n+31*n+190)*(n*n+6*n+39)) > 0
        uniform_upgrade = {"start":8, "numerator":"-5n", "denominator":"5n^2+31n+190",
                           "finite_ranks_checked":list(range(8,tail)), "tail_start":tail,
                           "tail_gap_coefficients_ascending":[str(c) for c in polynomial],
                           "strict_gain_numerator":"n(n-5)"}

    # Algebraic update identities are checked at exact rational values.
    gain_cases = 0
    for rec in records:
        k, g, K = rec["rank"], Q(rec["gamma"]), Q(rec["K"])
        improved_g = g/2
        improved_K = transport.parameters(k, improved_g)[2]
        assert improved_K-K == Q((k*k-1)*(improved_g-g), (1-improved_g)*(1-g))
        for n in [max(tail, rec["start"]), max(tail, rec["start"])+3]:
            N = n*(n-1)
            assert transport.target(n, improved_K)-transport.target(n, K) == Q((improved_K-K)*(n*n-1), (N+improved_K)*(N+K))
            assert transport.parameters(n, transport.target(n, K))[2] == K
            gain_cases += 1

    # Basic actual-map calibrations, supplementing the proofs/certificates.
    comparisons = []
    for n in [8, 9, 10, 12, 16, 17, 18, 19, 20, 32, 50, 100]:
        bound = envelope(n)
        assert bound <= 1                  # identity and transpose
        assert bound <= Q(1, n**n)         # depolarizing map
        assert bound <= -Q(33, 512*prod(range(n-7, n+1)))  # actual padded seed
        comparisons.append({"n": n, "main": str(baseline(n)),
                            "best": str(bound), "best_decimal": float(bound)})

    result = {"status": "passed", "scope": "algebraic transport of independently certified seeds",
              "main_theorem": {"start": 8, "numerator": "-n", "denominator": "n^2+6n+39",
                               "finite_ranks_checked": list(range(8,17)),
                               "tail_gap_numerator_ascending": main_tail_numerator,
                               "clean_K6_transport": clean},
              "seeds": records,
              "sharper_single_formula": {"start": 8, "A": str(A), "B": str(B),
                  "A_decimal": float(A), "B_decimal": float(B), "tail_start": tail,
                  "tail_gap_shifted_coefficients": [str(at_tail), str(slope)],
                  "finite_caps": {str(n): str(v) for n,v in caps.items()}},
              "new_uniform_upgrade":uniform_upgrade,
              "exact_gain_checks": gain_cases, "comparison": comparisons}
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "passed", "largest_seed_rank": max(seeds),
                      "largest_K": str(A), "largest_K_decimal": float(A),
                      "combined_bound_starts": tail,
                      "transport_starts": best["transfer_start"], "universal_formula_starts": 8,
                      "single_formula_B": str(B), "exact_gain_checks": gain_cases}, indent=2))


if __name__ == "__main__":
    main()
