# Verification report for v2026.10.15.2

## Inherited controls

The original seven controls passed in v2026.10.15.1; they were not rerun for v2. Every inherited non-metadata file is unchanged against the original inventory (54 files). The original v1 snapshot also passes its complete SHA-256 inventory, confirming it was not altered. The v1 checksum manifest digest is `ab6b5ac6b630a3250e4e48e0c1d3ebd74ee91c15dc9cc1eb354d65f7fb881506`.

The complete original report, commands and measured resources are preserved as `verification/v1-VERIFICATION.md`; its machine-readable record is `verification/v1-MANIFEST.json`. The original logs and source/data files remain at their original relative paths.

## Fresh family checks

All five newly staged family programs exited with status zero. The full nine- and eight-dimensional coefficient dictionaries match their asserted exact tables. All copied family sources and proof notes retain their input hashes. The added harness also checks both exact improvement factors and base-member normalizations.

| Fresh check | Elapsed seconds | Peak resident bytes | Exit status |
| --- | ---: | ---: | ---: |
| nine-full-polynomial | 0.094338 | 20021248 | 0 |
| nine-input-order | 0.922530 | 28688384 | 0 |
| eight-full-polynomial | 0.056650 | 15204352 | 0 |
| eight-input-output-descent | 0.300989 | 17842176 | 0 |
| eight-endpoint | 0.058489 | 15859712 | 0 |

Fresh suite elapsed: 1.450361 s. Maximum recorded child resident memory: 28,688,384 bytes.

### nine-full-polynomial

Working directory: `families/coherent9`.

```sh
python3 -B verify_polynomial.py
```

Exit status: 0. Generated result: `families/coherent9/coherent_polynomial.json`. Full log: `verification/family-nine-full-polynomial.log`.

### nine-input-order

Working directory: `families/coherent9`.

```sh
python3 -B verify_input_order.py
```

Exit status: 0. Generated result: `families/coherent9/verify_input_order.json`. Full log: `verification/family-nine-input-order.log`.

### eight-full-polynomial

Working directory: `families/coherence_descent/checks`.

```sh
python3 -B rank8_family.py
```

Exit status: 0. Generated result: `families/coherence_descent/checks/rank8_family.json`. Full log: `verification/family-eight-full-polynomial.log`.

### eight-input-output-descent

Working directory: `families/coherence_descent/checks`.

```sh
python3 -B verify_descent.py
```

Exit status: 0. Generated result: `families/coherence_descent/checks/verify_descent.json`. Full log: `verification/family-eight-input-output-descent.log`.

### eight-endpoint

Working directory: `families/coherence_descent/checks`.

```sh
python3 -B rank8_certificate.py
```

Exit status: 0. Generated result: `families/coherence_descent/checks/rank8_certificate.json`. Full log: `verification/family-eight-endpoint.log`.

## Scope and coefficient tables

The complete tables and their normalization are in `families/README.md` and `verification/family-run-results.json`. Their exact attained family minima give upper bounds on the unrestricted `mu_9` and `mu_8`; no global-minimum assertion is made. Analytic positivity, exact parameter feasibility and square-wide minimization follow from the manuscript proofs; the programs verify the complete polynomial coefficients and finite independent contraction/marginal/norm/gap controls.

The `compression_scan.py` and `pinching_checks.py` files are necessary helper imports. Their standalone search/pinching entry points were not run. No new optimization, ZIP archive, PDF export, publication or public upload was performed.
