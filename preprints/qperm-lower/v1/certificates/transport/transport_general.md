# General seed transport and its exact limitation

This note assumes the checked mixed-contraction inequality in the existing
Schur-transport package. All additional claims below are algebraic consequences
of that inequality.

## A universal transport theorem

Let k >= 3 and let gamma in [-1/k,0] be a valid universal lower bound for
ordinary positive bistochastic maps on M_k. Define

\[
\kappa=\frac{(k-1)(1+k\gamma)}{1-\gamma},\qquad
h_n(\kappa)=-\frac{n-1-\kappa}{n(n-1)+\kappa}.
\]

Then every ordinary positive unital map on M_n satisfies

\[
\boxed{\Phi_n(H)\ge h_n(\kappa)\qquad(n\ge k+3).}
\]

No additional polynomial check is required for this range. A finite exact
coefficient certificate can improve the threshold to n=k+1; this is checked for
the current finite-dimensional seeds in the accompanying verifier.

### Proof

Write N=n(n-1), a=1-gamma, b=(k-1)(1+k gamma), D=aN+b, and
t=(n^2-1)/D. The inherited coefficient row is

\[
J=\sum_{\mu\vdash k}
\frac{(k)_{\underline s}}{(n)_{\underline s}}
\left(\frac{(-1)^j}{\binom{k}{j}}-\gamma\right)
w_{\mu\cup1^{n-k}}\ge0,
\quad j=k-\ell(\mu),\quad s=k-m_1(\mu).
\]

Also 
\[R=w_{(n-1,1)}/(n-1)-w_{(n)}\ge0.\] We prove every residual in

\[
\Phi_n-h_n=tJ+\mathbf1_{n\text{ even}}(1/n+h_n)R
+\sum_\lambda c_\lambda w_\lambda
\]

is nonnegative. Multiplication by D makes each residual affine in gamma,
including the rank-two correction because

\[
D(1/n+h_n)=b(n+1)/n.
\]

It therefore suffices to check gamma=-1/k and gamma=0. The two leading shapes
(1^n),(2,1^(n-2)) have zero residual identically. For other selected shapes,
j>=2 and j+1 <= s <= min(2j,k).

At gamma=0, D=N+k-1 and h_n=-(n-k)/D. Since n>=k+3,

\[
-2/N\ge h_n.
\]

All unselected shapes except (n) in even dimension have r_lambda >= -2/N;
the positive square-free shape and selected j=1 shape were already handled.
For selected odd j>=3 the mixed-row coefficient is negative, so its subtraction
only increases the residual. For selected even j>=2, use

\[
\frac{(k)_{\underline s}}{(n)_{\underline s}\binom{k}{j}}
\le\frac{k-j}{n-j}\frac1{\binom n j},
\]

which follows from s>=j+1. Consequently

\[
Dc_\lambda\ge(n-k)+
\frac{D-(n^2-1)(k-j)/(n-j)}{\binom n j}
=(n-k)\left(1+\frac{N+j-1}{(n-j)\binom n j}\right)>0.
\]

At gamma=-1/k, b=kappa=0, h_n=-1/n, and
t=(n+1)k/[n(k+1)]. For a selected shape, c_lambda>=0 is equivalent to

\[
A_{j,s}(k)\le A_{j,s}(n),\qquad
A_{j,s}(x)=\frac{(x)_{\underline s}}{x+1}
\left(1+\frac{x(-1)^j}{\binom xj}\right).
\]

For j=0 and j=1 these are respectively constant 1 and constant 0.
For even j>=2,

\[
A_{j,s}(x)=\frac{(x)_{\underline s}}{x+1}
+\frac{j!x}{x+1}(x-j)_{\underline{s-j}},
\]

a sum of nonnegative increasing functions for x>=s. For odd j>=3,

\[
A_{j,s}(x)=\frac{(x)_{\underline s}}{x+1}
\left(1-\frac{j!}{(x-1)_{\underline{j-1}}}\right),
\]

a product of nonnegative increasing functions for x>=s>=j+1. Thus the required
monotonicity holds. Every unselected coefficient is >=-1/n.

In even dimension the rank-two row cancels the (n) coefficient. Its only other
affected shape, (n-1,1), is unselected because n>=k+3. Its final residual is

\[
\frac{(n+1)(n-\kappa)}{n(N+\kappa)}>0.
\]

This identity holds at both endpoints and throughout the parameter interval;
0<=kappa<=k-1<n. All coefficients are now covered. Interpolation proves the
theorem. The gamma=-1/k endpoint itself is the elementary -1/n floor.

## The envelope and its limitation

For any finite collection of valid seeds satisfying the transport conditions,
the best resulting lower bound is obtained by the largest kappa. Indeed

\[
\frac{\partial h_n(\kappa)}{\partial\kappa}
=\frac{n^2-1}{[n(n-1)+\kappa]^2}>0.
\]

Combining their selected J rows cannot improve this envelope: the abstract
two-shape profile

\[
w_{(1^n)}=\frac{K}{N+K},\qquad
w_{(2,1^{n-2})}=\frac N{N+K},\qquad K=\max_i\kappa_i,
\]

satisfies every selected J row and R, and has value h_n(K). This is only a
coefficient-relaxation statement, not realizability by a positive map.

There is also no recursive amplification from transporting a transported bound:

\[
\gamma=h_k(K)\quad\Longrightarrow\quad
\frac{(k-1)(1+k\gamma)}{1-\gamma}=K.
\]

Thus genuine seed improvements increase the envelope; repetition of the same
transport does not. For fixed K,

\[
h_n(K)=-\frac1n+\frac K{n^2}+\frac{2K}{n^3}+O(n^{-4}).
\]

This improves the correction but retains the leading -1/n scale.

## Current unconditional improvement

The new finite-dimensional exact dual certificate proves

\[
\gamma_{16}=-\frac{14602983}{400000000}>-\frac3{82}.
\]

The exact seed has transport parameter

\[
K_{16}=\frac{2495284080}{414602983}=6.018490416891\ldots.
\]

All shifted residual polynomials at n=17 have nonnegative rational
coefficients, both for the exact seed and for the convenient weakening -3/82.
Together with the rank-two parity correction, this proves

\[
\boxed{\Phi_n(H)\ge-\frac{n-7}{n^2-n+6}\qquad(n\ge17),}
\]

and the slightly stronger bound h_n(K_16) on the same range. The full polynomial
coefficient lists are in `transport_kappa6.json` and
`transport_new_certificates.json`. The standard-library verifier
`verify_transport_general.py` reconstructs them. The finite-rank seed itself is
certified independently in the finite-optimization package; the transport
verifier does not purport to verify that LP dual.

## Structural refinement for k-positive maps

A map H is k-positive when id_(M_k) tensor H is positive. Call H k-copositive
when H composed with matrix transposition is k-positive. Suppose H is positive
and unital on M_n, k>=3, and n>=k+3. If H is k-positive or k-copositive, then

\[
\boxed{\Phi_n(H)\ge-\frac{n-k}{n^2-n+k-1}.}
\]

This does not assume an unrestricted rank-k sign theorem. In the proof of the
mixed-contraction inequality, the relevant compatible maps are of the form

\[
K(Z)=W^*H(VZV^*)W:M_k\longrightarrow M_k,
\]

for input/output embeddings V,W (together with nonnegative Gram weights).
Compression preserves k-positivity. A k-positive map M_k to M_k is completely
positive, so Phi_k(K)>=0 by the CP determinant/Gaussian identity. Therefore
the mixed row holds with gamma=0. For k-copositive H the compatible map is
coCP instead, and the same nonnegativity follows because Phi is invariant
under input transposition. Applying the general transport theorem with
kappa=k-1 gives the displayed bound.

To see the copositive compression directly, let L=H composed with transpose
be k-positive. Then

\[
K(Z)=W^*L(\overline V Z^{\mathsf T}V^{\mathsf T})W
=\widetilde K(Z^{\mathsf T}),
\]

where the k-dimensional compression tilde K of L is CP.

For k proportional to n this improves the leading coefficient of the
negative floor: k=floor(alpha n) gives -(1-alpha)/n+O(n^-2). In particular,
(n-3)-positivity or (n-3)-copositivity gives

\[
\Phi_n(H)\ge-\frac3{n^2-4}\qquad(n\ge6).
\]

For example, at n=20, 17-positivity gives -1/132, while the new unconditional
kappa=6 bound gives -13/386. These are lower certificates, not sharpness
claims for those subclasses.

As basic consistency checks, the identity and transpose maps have Phi=1.
The normalized reduction/depolarizing family

\[
H_c(X)=\frac{\operatorname{tr}(X)I-cX}{n-c},\qquad0\le c\le1/k,
\]

is k-positive: its Choi matrix is proportional to
I-c|Omega><Omega| and a Schmidt-rank-at-most-k vector v satisfies
|<Omega,v>|^2<=k||v||^2. Its invariant is

\[
\Phi_n(H_c)=\frac{\sum_{j=0}^n(-c)^j}{(n-c)^n}\ge0,
\]

consistent with the structural bound. This follows by expanding
det((tr X)I-cX) and extracting the column Schur coefficient of each
e_j(X)(tr X)^(n-j), which is one.
