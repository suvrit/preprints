# Certified finite and bounded-projection improvements, 22 October 2026

This standalone release keeps both earlier certificate releases untouched.
It includes exact feasible duals for the full projection-spectral and mixed
coefficient relaxation, their complete dependency chain, and an exact finite
bounded-projection certificate in dimension 24. No LP or map optimality is
claimed.

The new finite LP seeds are:

| Dimension | Certified lower bound | Transport parameter K |
| --- | --- | --- |
| 8 | −52740227999/10¹² | dependency of dimension 21 |
| 19 | −8262359897/250000000000 | 558090971742/86087453299 |
| 20 | −8047057661/250000000000 | 564039362940/86015685887 |
| 21 | −6271336687/200000000000 | 1366038591460/206271336687 |
| 24 | −649/22351 | 271/40 |

Dimension 24 uses the finite analytic certificate below. Its unrounded value
is slightly stronger. With h_n(K)=−(n−1−K)/(n(n−1)+K), exact shifted-polynomial
certificates give h_n(K_k) for every n≥k, for k=18,19,20,21,24. The seed
identity handles n=k; the polynomial checks handle every real n≥k+1.

In particular, for every integer n≥8,

    Phi_n >= -3*n/(3*n*n + 20*n + 103).

This equals the previous release's simple formula at 8 and is strictly
stronger for n≥9. The stronger finite seeds and transported tails remain
available; the single formula is not claimed to dominate them.

A stronger smooth envelope is

    Phi_n >= -n/(n*n + (271/40)*n + B),
    B = -8/gamma_8 - 64 - 8*(271/40).

It equals this release's improved dimension 8 bound at 8. The verifier checks
all finite comparisons and the positive linear numerator controlling the
tail. It strictly improves the earlier release's smooth envelope for n≥8.

## Verification

From the repository root, run:

```sh
python3 certificates-2026-10-22-push/verify.py
```

Only Python's standard library is required. The verifier rebuilds every
full rational model, checks every dual inequality and the complete seed
dependency chain, verifies the archived primal vectors in dimensions 4–7,
then checks the analytic 24 coefficient identity, exact infinite-tail
polynomials, both envelopes, and the input checksums. It writes
`verification.json`. Dimensions 20–21 dominate runtime; allow several minutes.

For a quick arithmetic check after full verification, `--tails-only` checks
the analytic 24 step, transport, envelopes, and checksums while explicitly
skipping LP dual verification. Its output is not a full verification report.

`SHA256SUMS` covers all input files and excludes generated `verification.json`.
`PROVENANCE.json` records copied inputs. The model builders are unchanged
copies from the prior release. Their mathematical applicability uses the
paper's mixed determinant and projection-spectrum arguments.

## Exact dimension 24 certificate

Set n=24, k=21, a=12, N=n(n−1), gamma=gamma_21,
K=(k−1)(1+k*gamma)/(1−gamma), h=h_n(K),
t=(n²−1)/((1−gamma)(N+K)), eta=1/n+h,
v=a(n−a)/N, Delta=a(n−a)/(N+K)−1/4, and A=4nv/(n+1).

For each partition lambda of n, let r_lambda be its signed score,
J_lambda the selected mixed coefficient from seed gamma, and R_lambda
the rank 2 row (−1 at (n), 1/(n−1) at (n−1,1), zero elsewhere).
The nonnegative transport residual is

    c_lambda = r_lambda - h - t*J_lambda - eta*R_lambda.

Let psi(0)=1, psi(±1)=−1, psi(other)=C. Define b_lambda as its exact uniform
subset average at rank 12. The smallest C valid on the finite spectral hull is

    C = 49038552465408/22017942472189.

The verifier checks all 145 spectral vertices. Thus B=sum b_lambda*w_lambda
is a valid nonnegative row. Set

    q_lambda = b_lambda - 1 + A*(1-r_lambda),
    q_star = q_(n),
    M = max_(c_lambda>0) (q_lambda + q_star*R_lambda)/c_lambda.

The maximum occurs at (6,1^18), and

    M = 35977984552366996045762853848991272
        /327848126478907158293371233405225.

The two leading partitions and (n) have zero residual. Their adjusted q
coefficients are zero. Every other partition has positive residual. The
verifier checks all 1,575 coefficient inequalities and the exact identity

    (A+M)*(r_lambda-gamma_star)
      = b_lambda + M*t*J_lambda + (M*eta+q_star)*R_lambda
        + [M*c_lambda - q_lambda - q_star*R_lambda],

where gamma_star=h+4*Delta/(A+M). Every bracket and row multiplier is
nonnegative. Summing against the orbital weights proves the bound.

The exact result is

    gamma_star = -9167110563519855245922921656813
                  /315707850865223035909120949619832,
    K_star = 19139439468149302001394165971264
             /2824999664597764270913424967623
           = 6.775023624958362... > 271/40.

Rounding K downward yields gamma_24=−649/22351. This certificate uses only
finite exact computations at dimension 24; it does not rely on a conjecture,
on a numerical optimum, or on the asymptotic separator theorem.

## Discovery and stopping point

The numerical proposals used moments through degree 10. A row-subset solve
found the dimension 21 dual; omitted row multipliers were zero and the final
dual was checked against the full original rational model. Dimension 19 and
20 accepted duals were similarly repaired and verified exactly.

Degree 12 and full probability-coordinate attempts encountered time limits
or solver errors. The bounded dimension 22 attempt hit its 45-second LP limit
after exact model construction and supplied no accepted certificate. These
are numerical limits, not a proof that stronger finite LP seeds do not exist.
Scratch discovery scripts and logs remain under `bounds-push/numerical/`
and `bounds-push/root/`; no numerical solver is needed for this release.
