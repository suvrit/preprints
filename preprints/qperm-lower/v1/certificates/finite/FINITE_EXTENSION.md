# Exact finite-rank extensions, 11 October 2026

The new certificates in `certificates/dual_13.json` onward use the same projection-spectral and recursive mixed-differential relaxation as the archived n4--12 certificates. They are rational dual-feasible vectors, not assertions of exact LP optimality or sharpness over positive maps.

Run the standalone exact verifier:

```
python checks/verify_all.py
```

It rebuilds every rational model, verifies all dual inequalities, verifies inherited exact primal-dual equalities through n7, and checks the Schur derivative and fast projection-profile formulas against independent implementations in small degrees. It imports no numerical optimizer. Recorded results are in `finite_verification_results.json`.

New exact floors through n17:

| n | certified lower bound |
|---|---|
|13| -414257677/10000000000 |
|14| -197275413/5000000000 |
|15| -47409913/1250000000 |
|16| -14602983/400000000 |
|17| -176217579/5000000000 |

In particular gamma16 > -3/82. Thus its transport parameter `(15*(1+16*gamma16))/(1-gamma16)` is greater than 6. The independently checked transport certificate for the weaker seed -3/82 yields

\[
\Phi_n(H)\ge -\frac{n-7}{n^2-n+6},\qquad n\ge17.
\]

The stronger literal gamma16 gives kappa=2495284080/414602983 (about 6.01849) in the corresponding rational formula. The final n17 seed gives kappa=32068818512/5176217579 (about 6.19542); its independent all-dimensional certificate is supplied in the transport package.

## Numerical discovery and exact acceptance

`checks/sparse_extend.py` is optional discovery code requiring SciPy. It keeps an exact sparse model, proposes a floating-point dual, rounds that dual to rational numbers, repairs disjoint simplex blocks, then verifies all inequalities exactly. Its `start end degree` arguments select dimensions and the maximum spectral elementary degree used during numerical discovery. For n15--17, degree 10 was used. All mixed-differential rows remain available. The accepted dual is embedded in the complete model by zero coefficients on omitted spectral equations, and the verifier checks the complete model.

High-dimensional full spectral discovery becomes numerically ill-conditioned. Some floating-point duals near the reported LP optimum produce poor bounds after exact repair. Those failed candidates were discarded; they are not theorems. The restricted spectral discovery gives the useful and fully verified certificates supplied here. Different numerical solver versions can produce different feasible duals; discovery is not needed to verify the supplied ones.

## Implementation corrections to the original archive

The archived `verify.py` and `discover.py` expected a dictionary-returning `build_recursive()` interface, while the included model exposed a dataclass-returning `build()` interface; they also looked for a `value` key instead of the inherited certificates' `objective` key. This copy includes a compatibility adapter and fixes those field names. Every old certificate was then rebuilt and checked exactly. These are checker-packaging defects, not failures of the old rational inequalities.

The additional sparse builder retains exactly the original deterministic row and column ordering. The dynamic-programming projection profile computes the integer coefficients of `product_i (1+u*z^lambda_i)` and is compared with direct subset enumeration in 315 cases. No new mathematical relaxation is introduced by those implementation changes.
