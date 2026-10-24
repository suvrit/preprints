# Frozen certificate clean-run report

Release: `phi-lower-bounds-certificates-v2026.10.15.1`. All seven commands exited with status zero. All verifier sources and finite-certificate inputs matched their copied input hashes after execution. The printed nine-coefficient witness pencil matches exactly.

| Check | Elapsed seconds | Peak resident bytes | Exit status |
| --- | ---: | ---: | ---: |
| finite | 35.834025 | 394248192 | 0 |
| transport | 0.451228 | 20217856 | 0 |
| witness-seed | 0.185811 | 14843904 | 0 |
| witness-pencil | 1.233189 | 20709376 | 0 |
| structure-rational | 26.339676 | 404946944 | 0 |
| structure-fixed-core | 0.055933 | 13631488 | 0 |
| structure-independent | 0.337346 | 14499840 | 0 |

Suite elapsed: 64.446467 s. Maximum resident memory: 404946944 bytes.

The release README and MANIFEST.json give requirements, exact commands and expected output. This package is a local accompanying snapshot; public deposit is pending. Mathematical scope: finite exact certificates and calibration of the manuscript's algebraic identities, with analytic proofs supplying the all-dimensional implications.

## Exact commands, summaries and output files

Commands use the release root unless the working directory is stated as `witnesses`. Python 3.10 or newer, standard library only; do not use `-O`. Complete console output is preserved in the linked log for each command.

### finite

Working directory: `.`.

```sh
python3 -B finite/checks/verify_all.py
```

Expected summary: `VERIFIED 18 -171460901/5000000000; ALL EXACT CHECKS PASSED 315 profile cases 154 derivative cases`.

Generated result: `finite/finite_verification_results.json`. Full output: [verification/release-finite.log](verification/release-finite.log).

### transport

Working directory: `.`.

```sh
python3 -B compile_bounds.py
```

Expected summary: `"status": "passed"; "largest_seed_rank": 18; "largest_K": "32532964294/5171460901"; "exact_gain_checks": 32`.

Generated result: `compiled_bounds.json`. Full output: [verification/release-transport.log](verification/release-transport.log).

### witness-seed

Working directory: `witnesses`.

```sh
python3 -B polarization_result/verify.py
```

Expected summary: `"status": "passed"; "raw_Gamma8": "-540672"; "Phi8": "-11/6881280"`.

Generated result: `witnesses/polarization_result/verification.json`. Full output: [verification/release-witness-seed.log](verification/release-witness-seed.log).

### witness-pencil

Working directory: `witnesses`.

```sh
python3 -B asymptotic_agents/padding/cp_summand_anisotropic.py
```

Expected summary: `coherent Qj formula passed 9 exact tests; general coefficient formula passed 6 exact tests; Three exact higher-dimensional contractions passed.; Rational limiting certificate at u=3/5: -4947/50000`.

Generated result: `witnesses/asymptotic_agents/padding/cp_summand_anisotropic.json`. Full output: [verification/release-witness-pencil.log](verification/release-witness-pencil.log).

### structure-rational

Working directory: `.`.

```sh
python3 -B structure/verify_rational.py --seeds
```

Expected summary: `verified inherited seed 18; "status": "passed"; "coefficient_identity_parameter_cases": 315; "individual_coefficient_checks": 7029; "all_inherited_seeds_reverified": true`.

Generated result: `structure/rational_verification.json`. Full output: [verification/release-structure-rational.log](verification/release-structure-rational.log).

### structure-fixed-core

Working directory: `.`.

```sh
python3 -B structure/verify_fixed_core.py
```

Expected summary: `"status": "all exact assertions passed"; "number_of_dimension_checks": 16; reduction_2_noncentral_coefficients = ["1", "-2", "2"]`.

Generated result: `structure/fixed_core_verification.json`. Full output: [verification/release-structure-fixed-core.log](verification/release-structure-fixed-core.log).

### structure-independent

Working directory: `.`.

```sh
python3 -B structure/verify_independent.py
```

Expected summary: `"status": "passed"; "exact_minor_Wick_antisymmetry_checks": 543; "exact_projection_polynomial_checks": 260; "signed_phase_and_square_checks": 24`.

Generated result: `structure/independent_verification.json`. Full output: [verification/release-structure-independent.log](verification/release-structure-independent.log).

The witness-pencil run returns the complete vector `['0', '0', '0', '1/1376256', '5/1376256', '41/6881280', '1/458752', '-17/6881280', '-11/6881280']` in ascending degree. Each entry was compared exactly with the manuscript's printed polynomial by the preparation harness. The README explains the separate roles of the seed and pencil commands in Appendices B.1 and B.2.

Measurement details and individual resource counters are in [verification/release-run-results.json](verification/release-run-results.json); copied input hashes are in [verification/copied-inputs.json](verification/copied-inputs.json). The verifier source inventory and provenance remain auditable independently of any future public deposit.
