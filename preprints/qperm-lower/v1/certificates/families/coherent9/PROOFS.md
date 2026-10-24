# Extremal quantum permanents: a metric obstruction and a stronger rank-nine witness

8 October 2026

## Scope and normalization

For a complex-linear map H:M_r(C)->M_r(C), write

\[
\Gamma_r(H)=\det(\partial_X)\det H(X),\qquad
\Phi_r(H)=\Gamma_r(H)/r!.
\]
Let B_r^+ be the ordinary positive, unital, trace-preserving maps, and
mu_r=min_{H in B_r^+} Phi_r(H). The minimum exists by compactness. The
results here do not determine mu_9 or characterize its global minimizers.
They establish (i) a metric-independent obstruction to geodesic convexity,
(ii) an explicit feasible improvement over the normalized Du seed,
(iii) an exact minimum and fixed-q envelope in a two-parameter family.

The baseline seed is the version of Yun-Heng Du's counterexample already
recorded and audited in the project. No first-priority claim is made for
the present deformation. The original counterexample is Du's result:
Y.-H. Du, *Griffiths positivity does not imply positivity of the top Chern
form*, arXiv:2610.05931 (2026).

## 1. A stationary negative-curvature obstruction, independent of the metric

For odd r>=3 define

\[
T_s(X)=\frac{\operatorname{tr}(X)I_r-sX}{r-s},\qquad 0<s<1.
\]
This is unital and trace preserving. On a unit rank-one input its eigenvalues
are (1-s)/(r-s) once and 1/(r-s) with multiplicity r-1. Thus it is strictly
positive and lies in the relative interior of B_r^+.

The determinant differential gives

\[
f_r(s):=\Phi_r(T_s)
=\frac{\sum_{k=0}^r(-s)^k}{(r-s)^r}
=\frac{1-s^{r+1}}{(1+s)(r-s)^r}.
\]
For example, the formula follows by expanding det(b tr(X)I+aX); its
normalized determinant contraction is sum_{k=0}^r a^k b^{r-k}.
Differentiation yields

\[
f'_r(s)=\frac{(r+1)s[1-rs^{r-1}-(r-1)s^r]}
{(1+s)^2(r-s)^{r+1}}.
\]
There is exactly one s_r in (0,1) satisfying

\[
rs_r^{r-1}+(r-1)s_r^r=1,
\]
because the left side is strictly increasing from zero to 2r-1. At this point

\[
f''_r(s_r)=-\frac{r(r-1)(r+1)s_r^{r-1}}
{(1+s_r)(r-s_r)^{r+1}}<0.
\]

This is a stationary point on the *whole affine bistochastic space*, not
just the displayed curve. The functional Phi_r is invariant under
H -> Ad_U H Ad_{U^*}, and T_s is fixed by this action. Averaging any tangent
map K satisfying K(I)=K^*(I)=0 over U(r) gives c(Id-Delta_r). This follows
from the irreducibility of conjugation on traceless matrices. The derivative
of Phi at T_s therefore depends only on this scalar c. Since the derivative
in the T_s direction vanishes at s_r, the derivative in every tangent
direction vanishes there.

At a critical point the Riemannian Hessian, for any smooth Riemannian metric,
agrees with the coordinate Hessian as a quadratic form: the connection term
is multiplied by the vanishing first derivative. The negative second
variation above consequently excludes local geodesic convexity for *every*
smooth Riemannian metric on the interior of B_r^+ near T_{s_r}.

In rank three, s_3=1/2,

\[
T_{1/2}(X)=(2\operatorname{tr}(X)I-X)/5,
\quad \Phi_3(T_{1/2})=1/25,\quad f''_3(1/2)=-64/625.
\]
In rank nine s_9=0.7145377271673349... (the decimal is illustrative; the
algebraic characterization and the sign proof are exact).

This excludes a globally geodesically convex reformulation of Phi_r itself
on the full interior in odd rank. It does not exclude useful metrics on a
smaller stratum, on a negative sublevel component, or for another objective.

## 2. Geometry that does remain valid

### 2.1 Positive-definite Choi matrices

For C positive definite, Phi_r(C)=<w,C^{tensor r}w>, where w is the normalized
input/output determinant vector. Along the affine-invariant geodesic
C_t=C_0^{1/2}exp(tA)C_0^{1/2}, tensoring and diagonalizing the Hermitian sum
of copies of A shows that Phi_r(C_t) is a sum of exponentials with nonnegative
coefficients. It is strictly positive; log Phi_r is geodesically convex.
This is a statement on the CP Choi cone, not on the ordinary-positive cone
containing the negative witnesses.

### 2.2 Capacity variables, not the map objective

For a strictly positive map H, the capacity objective

\[
X\longmapsto \log\det H(X)-\log\det X
\]
is geodesically convex on positive definite X. Along X_t=X_0^{1/2}e^{tA}X_0^{1/2},
spectral decomposition gives H(X_t)=sum_i e^{t lambda_i}H(v_iv_i^*).
Every coefficient matrix is PSD. Factoring them and applying Cauchy--Binet
expresses det H(X_t) as a nonzero sum of exponentials with nonnegative
coefficients; log det X_t is affine. This proof uses ordinary positivity.

Capacity-based geodesic optimization is established in operator-scaling
literature; see Allen-Zhu, Garg, Li, Oliveira and Wigderson,
*Operator Scaling via Geodesically Convex Optimization, Invariant Theory
and Polynomial Identity Testing*, arXiv:1804.01076.

Under invertible input/output filtering, Phi and capacity acquire the same
factor |det A det B|^2. Thus Phi/capacity is constant on a filtering orbit.
Geodesic scaling removes normalization degrees of freedom; it does not by
itself improve the orbit's extremal ratio.

An exact instance: let

\[
P_t(\mathcal X)=t\,\operatorname{diag}(B_6(S),0_3)
+\operatorname{diag}(Z,Z^T,X+Y^T),\qquad t>0,
\]
with S the leading six-by-six input block and X,Y,Z its three diagonal
three-by-three blocks. Input filtering by diag(I_6,2sqrt(t) I_3) and output
filtering by diag((8t)^(-1/2)I_6,2^(-1/2)I_3) gives exactly the same normalized
Du map for every t. The combined determinant factor is 1/(32768 t^3).
Thus optimizing t in this family after exact balancing is vacuous.

## 3. Coherent completion of the seed's two bridges

Use three blocks of size three and define partial isometries

\[
A_1=E_{13}\otimes I_3,\quad B_1=E_{31}\otimes I_3,
\qquad A_2=E_{23}\otimes I_3,\quad B_2=E_{32}\otimes I_3.
\]
For real a,b define

\[
Q_a^{(1)}(X)=A_1XA_1^*+B_1XB_1^*
+a(A_1XB_1^*+B_1XA_1^*),
\]

\[
Q_b^{(2)}(X)=A_2X^TA_2^*+B_2X^TB_2^*
+b(A_2X^TB_2^*+B_2X^TA_2^*).
\]
Let J_6=[[0,I_3],[-I_3,0]], B_6(S)=tr(S)I_6-S-J_6 S^T J_6^*,
and let Btilde_6 be its pinched output embedding into the first six
coordinates, depending only on the leading six-by-six input block. Set

\[
H_{a,b}=\frac18\widetilde B_6+
\frac12(Q_a^{(1)}+Q_b^{(2)}).
\]
The map H_{0,0} is exactly the normalized seed with Phi=-1/7741440.

### 3.1 Exact feasibility region

The map H_{a,b} is ordinary positive exactly when |a|<=1 and |b|<=1.
For sufficiency,

\[
Q_a^{(1)}=
\frac{1+a}{2}\operatorname{Ad}_{A_1+B_1}
+\frac{1-a}{2}\operatorname{Ad}_{A_1-B_1},
\]
and the corresponding formula for Q_b^{(2)} is composed with transpose.
The Breuer--Hall part is positive: on xx^* its output is
||x||^2 I-xx^*-(J_6 bar x)(J_6 bar x)^*, with x perpendicular to J_6 bar x.
Thus the sum is positive.

Necessity follows from the rank-one input with block vector (e_1,0,e_1),
restricted to output directions (e_1,0,0) and (0,0,e_1): the resulting
principal two-by-two matrix is (1/2)[[1,a],[a,1]]. The other parameter is
tested on (0,e_1,e_1). These principal matrices require |a|,|b|<=1.

For all real a,b, both marginals of the raw tensor 8H_{a,b} are 8I_9.
Indeed all coherence terms have zero unital and adjoint-unital marginals,
Q_a^{(1)}(I)=P_1+P_3, Q_b^{(2)}(I)=P_2+P_3, and
Btilde_6(I)=4(P_1+P_2). The same identities hold for the adjoints.
Hence the whole feasible square is bistochastic.

### 3.2 Exact determinant polynomial

The complete contraction is

\[
\boxed{\Gamma_9(H_{a,b})=-\frac3{256}
\left[4+9(a^2+b^2)+a^4+b^4+16a^2b^2+a^4b^2+a^2b^4\right].}
\]
This is a polynomial identity for all real a,b; positivity is restricted
to the square above. Section 5 and the scripts give an exact finite
coefficient certificate, including all zero coefficients, rather than
an interpolation or Monte Carlo test.

Every nonconstant coefficient inside brackets is nonnegative, and it is
strictly increasing in each a^2,b^2 on [0,1]^2. Therefore

\[
\boxed{\min_{|a|,|b|\le1}\Gamma_9(H_{a,b})=-63/128,\qquad
\min_{|a|,|b|\le1}\Phi_9(H_{a,b})=-1/737280.}
\]
Equality within this family holds exactly at |a|=|b|=1. In particular, for
H_coh=H_{1,1},

\[
H_{\rm coh}=\frac18\widetilde B_6+
\frac12\operatorname{Ad}_{A_1+B_1}
+\frac12\operatorname{Ad}_{A_2+B_2}\circ\mathsf T.
\]
This is 21/2 times the negative magnitude of the normalized Du seed.
No global-minimum or best-published-value claim is made.

Along the valid two-sided path a=b=t,

\[
\Phi_9(H_{t,t})=-\frac{2+9t^2+9t^4+t^6}{15482880}.
\]
Thus Phi'_9(0)=0 but Phi''_9(0)=-1/860160<0. In particular the normalized
Du seed is not a local minimum of the actual positive bistochastic problem.
The perturbation is not a filtering reparameterization: its invariant changes.

### 3.3 Exact norm profile inside the family

Directly from the coefficient tensor,

\[
q(H_{a,b})=\frac{81}{8}+\frac92(a^2+b^2).
\]
At H_coh this is 153/8. At fixed q in [81/8,153/8], the smallest value
within the family is attained when a^2=b^2. Put z=(q-81/8)/9. Then

\[
\boxed{\min_{\substack{|a|,|b|\le1\\q(H_{a,b})=q}}\Phi_9(H_{a,b})
=-\frac{2+9z+9z^2+z^3}{15482880},\quad0\le z\le1.}
\]
To verify the fixed-q minimization, write s=a^2+b^2 and p=a^2b^2. The
bracket above equals 4+9s+s^2+(14+s)p. At fixed s the coefficient of p is
positive, so p=s^2/4 is optimal. This is feasible throughout 0<=s<=2.
The formula is an upper bound for the unrestricted m_9(q), not an equality
claim for that global lower envelope.

## 4. Contact geometry of the new witness

For an input vector x=(u,v,z) in C^3 direct-summed three times, put w=(u,v).
At H_coh the output is

\[
H_{\rm coh}(xx^*)=
\frac18\operatorname{diag}
(\|w\|^2I_6-ww^*-(J_6\bar w)(J_6\bar w)^*,0_3)
+\frac12\ell\ell^*+\frac12mm^*,
\]
where ell=(z,0,u), m=(0,bar z,bar v). For w!=0 its kernel consists exactly
of vectors y=(y_1,y_2,y_3) satisfying

\[
(y_1,y_2)\in\operatorname{span}\{w,J_6\bar w\},\quad
\ell^*y=0,\quad m^*y=0.
\]
Every pure output has rank at most six. Rank six occurs, for example, at
u=e_1,v=e_2,z=e_3. The three-dimensional kernel there is spanned by
(e_1,e_2,0), (e_2,-e_1,0), and (0,0,e_3). These are concrete product-zero
contacts for a later optimality analysis, not a proved global KKT certificate.

## 5. Exact finite contraction certificate

Let c[a,b,i,j] be the coefficient of X_ij in the output cell (a,b).
The determinant differential is exactly the triple-alternating contraction

\[
\Gamma_n(H)=\sum_{\sigma,\pi,\tau\in S_n}
\operatorname{sgn}\sigma\operatorname{sgn}\pi\operatorname{sgn}\tau
\prod_{a=0}^{n-1}c[a,\sigma(a),\pi(a),\tau(a)].
\]
There is no extra factorial. For the differential input permutation,
sign(tau pi^{-1})=sign(tau)sign(pi), which proves this normalization.

An exact dynamic program starts with R_0(empty,empty,empty)=1. At step a,
add one unused b,i,j, multiply by c[a,b,i,j], and by (-1) raised to the
number of earlier indices exceeding b,i,j in the respective three lists.
The final value is R_n(full,full,full). Computing with polynomials in a,b
rather than numbers establishes every coefficient of the family identity.
For the raw tensor 8H_{a,b} its nonzero coefficients are:

| powers (a,b) | integer coefficient of Gamma_9(8H) |
|---|---:|
| (0,0) | -6291456 |
| (2,0), (0,2) | -14155776 each |
| (4,0), (0,4) | -1572864 each |
| (2,2) | -25165824 |
| (4,2), (2,4) | -1572864 each |

All other coefficients vanish. Dividing by 8^9 yields the displayed formula.
`verify_polynomial.py` computes this entire polynomial in output-row order.
`verify_input_order.py` separately contracts in input-row order, using
explicit sorted index tuples instead of bit masks, and checks multiple
parameter choices, both marginals, q, and identity/trace normalizations.
Checks outside the feasible square are polynomial checks only.
`verify_geodesic.py` checks the exact derivative numerator identities and
the rank-three critical data. All programs use only the Python standard
library. No independent human or multi-agent proof review is claimed.

## 6. Precisely what is now bounded

\[
\boxed{\mu_9\le-1/737280.}
\]
For r>=9, padding with the identity map on the complementary pinched block gives

\[
\boxed{\mu_r\le-\frac1{737280\binom r9}.}
\]
The normalized factor is exact because Gamma factors over pinched square
block sums, whereas Phi includes division by the total factorial.

The previous universal lower bound -1+2/r^r remains available. To recall
its proof, decompose det into its pure scalar-coordinate term and its
orthogonal remainder. Every positive bistochastic map is an HS contraction,
fixes the scalar coordinate, and preserves the traceless subspace. The
scalar component contributes r!/r^r and the residual pairing is bounded
below by minus its squared norm r!(1-r^{-r}). Division by r! gives the bound.
We have not improved this global lower certificate here; the resulting
bracket for mu_9 is still very wide. The exact minimization is only over the
coherent bridge family. No assertion identifies H_coh with H_star.
