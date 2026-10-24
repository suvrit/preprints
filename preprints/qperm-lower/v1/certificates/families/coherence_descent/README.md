# Coherence descent and a negative rank-eight quantum permanent

Read `PROOFS.md` for all statements and exact scope. The parent manuscript has not been changed.

Run with Python 3 (standard library only):

```
cd checks
python verify_descent.py
python rank8_family.py
python rank8_certificate.py
python pinching_checks.py
```

The first program checks the general degree identities, two independently ordered determinant contractions, the complete rank-eight family formula at rational controls, the family SOS gap, exact bistochastic marginals, Choi norms, and an explicit strictly positive negative example. `rank8_family.py` constructs the full polynomial coefficient dictionary, including proof that no further terms occur; it does not infer the identity from interpolation. `rank8_certificate.py` tests the explicit minimizing family member. JSON results are included.

Optional bounded searches:

```
python compression_scan.py
python rank7_scan.py
```

The unsuccessful smaller-rank searches do not establish positivity in those ranks. All universal transformation, optimality-structure, and outer-approximation assertions rely on the written proofs rather than finite tests.

The two contraction orders are an algebraic cross-check, not an independent human or multi-agent audit. `verify_input_order.py` is retained from the previous coherent-rank-nine certificate; it constructs its tensor directly from Breuer--Hall and CP/coCP formulas. The original rank-nine seed is attributed to Du; no assertion about the latest literature priority of the rank-eight construction is made.
