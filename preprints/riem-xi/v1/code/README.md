# Verification code for "On some positivity properties of the Riemann Ξ function"

These four programs evaluate the numerical certificates described in
Appendix F of the paper. The analytic reductions are in the paper; the
programs check the finitely many scalar inequalities, the eleven real-zero
enclosures, and the compact interval cover that those reductions leave.
Published first-zero and finite-height verifications of the zeta zeros are
external inputs and are not recomputed.

## Run

Install `requirements-verification.txt` (`mpmath==1.3.0`, `sympy==1.14.0`)
in a Python 3 environment, then run from this folder

```sh
python reproduce.py --output-dir /tmp/riem-xi-verification-run
```

The output directory must be new. The runner snapshots this folder, runs the
four programs, stops on failure, and writes `run-summary.json` with one log
per program. To run one program, use `python PROGRAM.py`.

| Program | Checks | Reference output |
| --- | --- | --- |
| `verify_reciprocal_xi.py` | 8 directed interval checks: the counting bound from Bellotti–Wong, the two height-100 estimates, the high-anchor counting margin at U = 1000, and the total-variation bound at U = 3·10^12 (Appendix F.1) | `verification_intervals.txt` |
| `verify_laguerre_identities.py` | 44 exact finite algebraic checks for the Laguerre coefficient identities and sign conventions (Section 4) | `verification_algebra.txt` |
| `verify_reciprocal_logconcavity.py` | 2 directed scalar checks for the exponential-tilt proofs of log-concavity (Section 3.1) | `verification_reciprocal_logconcavity.txt` |
| `verify_lambda_pf_higher.py` | Eleven certified real-zero enclosures, the residual-moment inputs, closed interval covers through order ten, and the tail constants; certifies strict global PF_10 of Λ (Appendix F.2–F.3) | `verification_lambda_pf_higher.txt` |

Interval inputs are rational or decimal-string values. An inconclusive
interval comparison never counts as a certificate. `SHA256SUMS` covers the
programs and reference outputs; check it with `shasum -a 256 -c SHA256SUMS`.
