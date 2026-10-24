# Certificate release 2026.10.15.1

This frozen directory accompanies `../phi-lower-bounds-structural.tex`. It is a clean copy of the working certificate package, with all seven standard-library verification commands run successfully on 15 October 2026. Verifier sources and finite-certificate inputs are unchanged. `ARCHIVAL_README.md` preserves the working package's earlier instructions and provenance. The release has not yet been assigned a public deposit or stable public URL.

## Requirements and checksum identity

Python 3.10 or newer is sufficient for the required commands. They use exact rational arithmetic and the Python standard library. No optimizer, NumPy, SciPy, or network access is required. `finite/checks/sparse_extend.py` also contains optional discovery routines using NumPy/SciPy; those routines are not called by the finite checker. The optional `witnesses/asymptotic_agents/exterior/verify_stable_tuple.py` uses NumPy and is outside this seven-command clean run; its tuple construction is proved analytically in the manuscript.

Before verification, run from this directory:

```sh
shasum -a 256 -c SHA256SUMS
```

On systems providing GNU Coreutils, `sha256sum -c SHA256SUMS` is equivalent. `SHA256SUMS` lists every release file except itself, sorted by relative path; its SHA-256 identifies the whole frozen snapshot. Generated Python caches are excluded. The verification scripts write the result JSON files listed below. Keep this directory unchanged if retaining the frozen snapshot; run a copy when regenerating outputs.

## Required verification commands

Run from this directory, without Python's `-O` flag (assertions are part of the checks):

```sh
python3 -B finite/checks/verify_all.py
python3 -B compile_bounds.py
python3 -B structure/verify_rational.py --seeds
python3 -B structure/verify_fixed_core.py
python3 -B structure/verify_independent.py
```

Run the witness commands from the `witnesses/` subdirectory:

```sh
cd witnesses
python3 -B polarization_result/verify.py
python3 -B asymptotic_agents/padding/cp_summand_anisotropic.py
```

The `-B` flag suppresses bytecode caches. Every required command must exit with status zero. The `--seeds` run independently reconstructs the retained finite duals through rank 18 in addition to the structural identities; it intentionally repeats those dual checks.

## Expected summaries and generated files

| Command group | Expected summary | Generated file |
| --- | --- | --- |
| finite | `VERIFIED 18 -171460901/5000000000; ALL EXACT CHECKS PASSED 315 profile cases 154 derivative cases` | `finite/finite_verification_results.json` |
| transport | `"status": "passed"; "largest_seed_rank": 18; "largest_K": "32532964294/5171460901"; "exact_gain_checks": 32` | `compiled_bounds.json` |
| witness-seed | `"status": "passed"; "raw_Gamma8": "-540672"; "Phi8": "-11/6881280"` | `witnesses/polarization_result/verification.json` |
| witness-pencil | `coherent Qj formula passed 9 exact tests; general coefficient formula passed 6 exact tests; Three exact higher-dimensional contractions passed.; Rational limiting certificate at u=3/5: -4947/50000` | `witnesses/asymptotic_agents/padding/cp_summand_anisotropic.json` |
| structure-rational | `verified inherited seed 18; "status": "passed"; "coefficient_identity_parameter_cases": 315; "individual_coefficient_checks": 7029; "all_inherited_seeds_reverified": true` | `structure/rational_verification.json` |
| structure-fixed-core | `"status": "all exact assertions passed"; "number_of_dimension_checks": 16; reduction_2_noncentral_coefficients = ["1", "-2", "2"]` | `structure/fixed_core_verification.json` |
| structure-independent | `"status": "passed"; "exact_minor_Wick_antisymmetry_checks": 543; "exact_projection_polynomial_checks": 260; "signed_phase_and_square_checks": 24` | `structure/independent_verification.json` |

The finite checker verifies the exact primal and dual pair for ranks 4–7, dual feasibility and certified floors for ranks 8–18, recursion order, 315 independent projection-profile cases, and 154 radial-derivative cases. The compiler reconstructs the algebraic transport and compares the finite and infinite envelopes; it does not establish seeds without the separate finite verification. The rational structural checker verifies 7,029 individual coefficients in 315 parameter cases, 10,701 residual signs, and 2,229 all-proper-dimensional zero-seed coefficients, along with the inherited seeds. The fixed-core and independent checks are finite exact calibrations of the analytic formulas.

### Which commands verify Appendix B?

`polarization_result/verify.py` checks the eight-dimensional map's two bistochastic marginals, the raw contraction in both input and output orderings (`-540672`), the normalized value (`-11/6881280`), and the pinched direct-sum normalization. This is the witness-specific check for Appendix B.1.

`asymptotic_agents/padding/cp_summand_anisotropic.py` computes the complete degree-eight polynomial `Phi_8(Ad_Q+tH_8)` from nine exact values. Its coefficient vector, in ascending powers of `t`, must be

```text
['0', '0', '0', '1/1376256', '5/1376256', '41/6881280',
 '1/458752', '-17/6881280', '-11/6881280']
```

It also computes the shifted pencil, checks nine coherent and six general-corner identities, directly contracts the full extension in dimensions 9, 10, and 11, and checks the rational limiting value `P_*(3/5)=-4947/50000`. These are the witness-specific checks for the complete Appendix B.1 pencil and the coefficient used in Appendix B.2. The preparation harness additionally compared every computed coefficient with the manuscript's printed polynomial. The all-dimensional inequality is proved in Appendix B.2; the finite checks calibrate that proof.

## Recorded clean-run resource use

The run used Python 3.14.2 on macOS 15.3.1, ARM64. The seven commands together took 64.446467 seconds. Their maximum recorded resident memory was 404,946,944 bytes (approximately 405 MB, or 386 MiB). Wall time was measured with `time.perf_counter`; per-process resource use was measured with POSIX `os.wait4` and its child `rusage` (macOS reports `ru_maxrss` in bytes). The two finite-dual reconstructions dominate the run. These measurements describe this machine and run, rather than minimum requirements or performance guarantees.

`MANIFEST.json` records the version, dependency inventory, provenance, every exact command, exit status, output file, elapsed time and peak memory. `verification/` retains the complete logs, machine-readable run report, and copied input inventory. The release does not claim map realizability or solve the unrestricted asymptotic exponent. No archive, public upload, or public locator is implied by this local snapshot.
