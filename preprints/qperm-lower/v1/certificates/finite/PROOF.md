# Schur differential inequalities and dimension-uniform quantum-permanent lower bounds

**Research supplement — 11 October 2026**

## 1. Results and their scope

Let \(H:M_n(\mathbb C)\to M_n(\mathbb C)\) be complex linear, ordinary positive, unital, and trace preserving. Put
\[
\Gamma_n(H)=\det(\partial_X)\det H(X),\qquad
\Phi_n(H)=\Gamma_n(H)/n!,\qquad
\mu_n=\min_H\Phi_n(H).
\]
The matrix entries in the differential are independent complex variables. Complete positivity is not assumed.

The earlier elementary bound was
\[
L_n=\frac{(n+1)!}{n^{n+1}}-\frac1n.
\]
Its proof retains a probability distribution of monomial shapes and one mixed-discriminant coefficient bound. It is not sharp for any fixed \(n\ge3\). This supplement produces improvements with an algebraic, rather than exponentially small, correction to \(-1/n\).

### Theorem A. Closed dimension-uniform bounds

Every ordinary positive **unital** map satisfies
\[
\boxed{\Phi_n(H)\ge-\frac{n-3}{n^2-n+2}\qquad(n\ge6).}
\tag{1.1}
\]
Using the previously certified rank-seven bound, one obtains
\[
\boxed{\Phi_n(H)\ge-\frac{19n-85}{19n(n-1)+66}\qquad(n\ge8).}
\tag{1.2}
\]
The new finite-dimensional certificates below imply the stronger formulas
\[
\boxed{\Phi_n(H)\ge-\frac{n-5}{n^2-n+4}\qquad(n\ge10),}
\tag{1.3}
\]
\[
\boxed{\Phi_n(H)\ge-\frac{n-6}{n^2-n+5}\qquad(n\ge13).}
\tag{1.4}
\]
Trace preservation is not needed in the transport step: it is used to establish the seed bounds, which then extend to unnormalized compatible maps by capacity normalization. All these conclusions therefore apply, in particular, to the original bistochastic problem.

The last bound has expansion
\[
-\frac{n-6}{n^2-n+5}
=-\frac1n+\frac5{n^2}+\frac{10}{n^3}+O(n^{-4}).
\tag{1.5}
\]
This improves the old exponentially small positive correction to \(-1/n\). It does **not** improve the leading \(O(1/n)\) order of the known negative-part bound or determine the asymptotics of \(\mu_n\).

### Theorem B. New finite-dimensional lower certificates

Every ordinary positive bistochastic map satisfies the following rational lower bounds:

| Dimension | Certified lower bound |
|---:|---:|
| 8 | \(-5274023/100000000=-0.05274023\) |
| 9 | \(-2532141/50000000=-0.05064282\) |
| 10 | \(-4791679/100000000=-0.04791679\) |
| 11 | \(-4573151/100000000=-0.04573151\) |
| 12 | \(-1084543/25000000=-0.04338172\) |

These are exact rational **dual lower certificates**, rounded downward for readability. No exact-optimum claim is made for the new linear programs. The exact, slightly larger dual values are included in the certificate files. The older rank-four through rank-seven certificates remain unchanged and are rebuilt in the verifier.

Neither theorem proves nonnegativity in ranks four through seven. No new negative map, global minimizer, or sharpness assertion for the full positive-map cone is supplied here.

## 2. What hyperbolicity and Lorentzian theory do and do not supply

For a fixed orthonormal input frame \(U=(u_1,\ldots,u_n)\), put
\[
A_i=H(u_i u_i^*),\qquad p_U(x)=\det\Big(\sum_i x_iA_i\Big).
\]
Here \(A_i\succeq0\) and \(\sum_iA_i=I\). The polynomial is homogeneous, has nonnegative coefficients, and is real stable: if every \(\operatorname{Im}z_i>0\), then
\[
\operatorname{Im}\sum_i z_iA_i
=\sum_i(\operatorname{Im}z_i)A_i\succ0,
\]
so the matrix is invertible. Such homogeneous real-stable polynomials belong to the Lorentzian class [BH20]. Stable determinant polynomials, polarization, and preservation operators are developed in [BBL09].

The difficulty is the operation we actually need: Haar averaging these polynomials and then applying a **signed** exterior coefficient functional. Neither step may be replaced by an unverified positivity-preserving operation.

### 2.1 A genuine orbital average need not be hyperbolic

On \(M_4\), let \(P=\operatorname{diag}(1,1,0,0)\), \(Q=I-P\), and
\[
H(X)=\tfrac12\operatorname{tr}(PX)P+	frac12\operatorname{tr}(QX)Q.
\]
This is entanglement breaking and bistochastic. Put \(A=P-Q\) and
\[
a(U)=\tfrac12\operatorname{tr}(P UAU^*).
\]
Then
\[
\det H(U(tI+A)U^*)=(t^2-a(U)^2)^2.
\]
Writing \(m_2=\mathbb E a^2\), \(m_4=\mathbb E a^4\), the orbital average on this line is
\[
t^4-2m_2t^2+m_4.
\]
The random variable \(a^2\) is nonconstant: continuous choices of \(U\) give both \(a=1\) and \(a=0\). Hence \(m_4>m_2^2\). The quadratic in \(t^2\) has negative discriminant. Thus the full Haar-averaged determinant polynomial is not hyperbolic in the identity direction. Every individual integrand has all real roots on that line.

This example does not assert that the full orbital average fails every weaker Lorentzian property.

### 2.2 Even balanced permutation averaging can destroy Lorentzianity

The stable balanced polynomial
\[
p(x)=\frac{(x_1+x_2)^2(x_3+x_4)^2}{16}
\]
has \(p(1)=1\) and \(\partial_i p(1)=1\). Its full permutation average is
\[
q(x)=\frac1{24}m_{22}(x)+\frac1{24}m_{211}(x)+\frac14m_{1111}(x).
\]
The Hessian of \(\partial_1^2q\), on coordinates \(2,3,4\), has diagonal \(1/6\) and off-diagonal \(1/12\). Its eigenvalues are \(1/3,1/12,1/12\). This violates the defining at-most-one-positive-eigenvalue condition for the quadratic derivatives of a Lorentzian polynomial.

This is a permutation-average counterexample, not a claim that the preceding full Haar average is non-Lorentzian. It proves that stability of each summand and balancing alone do not justify a Lorentzian averaging step.

Accordingly, the usable mechanism below is not a conjectured closure of Lorentzian polynomials. It is **Schur diagonalization of a differential operator, combined with positivity of compatible mixed determinants before averaging**.

## 3. Orbital coefficients and the inherited mixed-differential inequality

For a positive unital map define
\[
f_H(x)=\mathbb E_U\det H(U\operatorname{diag}(x)U^*)
=\sum_{\lambda\vdash n}w_\lambda q_\lambda(x),\qquad
q_\lambda=\frac{m_\lambda}{m_\lambda(1^n)}.
\]
Positivity of the coefficient matrices in each frame gives
\[
w_\lambda\ge0,\qquad \sum_\lambda w_\lambda=1.
\tag{3.1}
\]
The normalized determinant differential extracts the column Schur coefficient of the invariant polynomial. Consequently
\[
\boxed{\Phi_n(H)=\sum_{\lambda\vdash n}r_\lambda w_\lambda,
\qquad r_\lambda=\frac{(-1)^{n-\ell(\lambda)}}{\binom n{\ell(\lambda)}}.}
\tag{3.2}
\]
For example,
\[
[s_{(1^n)}]m_\lambda
=(-1)^{n-\ell(\lambda)}\frac{\ell(\lambda)!}{\prod_jm_j(\lambda)!},
\quad
m_\lambda(1^n)=\frac{n!}{(n-\ell(\lambda))!\prod_jm_j(\lambda)!},
\]
and their ratio is (3.2).

For the first \(k\) variables let
\[
\Delta_k=\prod_{1\le i<j\le k}(x_i-x_j),\qquad
\mathscr D_k=\Delta_k^{-1}\partial_1\cdots\partial_k\Delta_k,
\quad
\mathscr T_k=(\partial_1+\cdots+\partial_k)^k.
\]
The radial determinant operator is exactly diagonal on the Schur basis, followed by removal of one column:
\[
\boxed{\mathscr D_ks_\lambda
=\prod_{i=1}^k(\lambda_i+k-i)s_{\lambda-(1^k)},}
\tag{3.3}
\]
with value zero when \(\lambda_k=0\). This follows immediately by differentiating the alternant \(\Delta_ks_\lambda\). The same formula for the matrix determinant differential follows from Fischer adjointness to multiplication by the determinant and the Schur norm formula. These are classical symmetric-function/differential identities, not claims of new machinery [Mac95, Gur04].

### Lemma 3.1. Transfer to unnormalized maps

If \(\gamma_k\le0\) is a universal lower bound for positive bistochastic maps on \(M_k\), then every ordinary positive \(K:M_k\to M_k\) satisfies
\[
\Phi_k(K)\ge\gamma_k\det K(I).
\tag{3.4}
\]

**Proof.** Regularize by \(K_\varepsilon=K+\varepsilon\operatorname{tr}(\cdot)I\). On \(X\succ0,\det X=1\), the function \(\det K_\varepsilon(X)\) has compact sublevel sets, since \(K_\varepsilon(X)\succeq\varepsilon\operatorname{tr}(X)I\). At its minimizer \(X_0\), with \(Y_0=K_\varepsilon(X_0)\), stationarity gives \(K_\varepsilon^*(Y_0^{-1})=X_0^{-1}\). Thus
\[
L(Z)=Y_0^{-1/2}K_\varepsilon(X_0^{1/2}ZX_0^{1/2})Y_0^{-1/2}
\]
is bistochastic. Filtering covariance gives
\[
\Phi_k(K_\varepsilon)=\det(Y_0)\Phi_k(L)
\ge\gamma_k\det(Y_0)\ge\gamma_k\det K_\varepsilon(I).
\]
The last inequality uses \(\gamma_k\le0\). Let \(\varepsilon\downarrow0\). ∎

### Lemma 3.2. Common-map mixed positivity

For every positive unital \(H\) on \(M_n\), \(k<n\), and seed \(\gamma_k\) as above,
\[
\boxed{(\mathscr D_k-\gamma_k\mathscr T_k)f_H
\text{ has nonnegative monomial coefficients}.}
\tag{3.5}
\]

**Proof.** In a fixed input frame, expand
\[
\det\left(\sum_i x_iH(E_{ii})+H(VZV^*)\right),
\]
where \(V\) embeds the active \(k\)-space. Decompose the PSD baseline matrices \(H(E_{ii})\) into rank-one terms. Selecting \(n-k\) baseline vectors gives a nonnegative Gram determinant times \(\det K(Z)\) for a compatible positive map \(K:M_k\to M_k\). The two derivatives give \(k![\Phi_k(K)-\gamma_k\det K(I)]\ge0\). Coefficientwise summation and averaging the input frame prove the claim, using (3.3) to identify the radial operator. All entries continue to come from the same \(H\). ∎

Lemmas 3.1–3.2 are restated from the earlier mixed-contraction supplement. The new use here extracts a small number of rows and transports finite-dimensional certificates to every larger dimension.

## 4. Two explicit rows that control the extreme negative shapes

Let \(\mu\vdash k\), \(m=m_1(\mu)\), \(j=k-\ell(\mu)\), and \(s=k-m\). Extract the coefficient of \(x_{k+1}\cdots x_n\) in (3.5), and divide by \(k!\). One obtains
\[
\boxed{J_{n,k,\gamma}:=
\sum_{\mu\vdash k}d_\mu(n)w_{\mu\cup1^{n-k}}\ge0,}
\tag{4.1}
\]
where
\[
\boxed{d_\mu(n)=
\frac{(k)_{\underline{s}}}{(n)_{\underline{s}}}
\left(\frac{(-1)^j}{\binom kj}-\gamma\right).}
\tag{4.2}
\]
Here falling factorials are used. The normalization factor is equivalently
\[
\frac{m_\mu(1^k)}{m_{\mu\cup1^{n-k}}(1^n)}
=\frac{k!(n-k+m)!}{n!m!}.
\]
In particular, the coefficients of \(w_{(1^n)}\) and \(w_{(2,1^{n-2})}\) are
\[
1-\gamma,
\qquad
-\frac{(k-1)(1+k\gamma)}{n(n-1)}.
\tag{4.3}
\]

A second row is essential in even dimensions. Taking the coefficient of \(x_1^{n-2}\) in \(\mathscr D_2f_H\ge_{\rm coeff}0\) gives
\[
\boxed{R_n:=\frac{w_{(n-1,1)}}{n-1}-w_{(n)}\ge0\qquad(n\ge3).}
\tag{4.4}
\]
Indeed, the selected coefficients of \(\mathscr D_2m_{(n)}\) and \(\mathscr D_2m_{(n-1,1)}\) are respectively \(-n\) and \(n\); the coefficients for all other shapes vanish. Normalizing by their values at \(1^n\) gives (4.4).

This row prevents all occupancy mass at a single variable from creating a separate even-dimensional loss. No exponentially small correction or unjustified parity assumption is needed.

## 5. The dimension-transport certificate

For a seed \(k,\gamma\), put
\[
a=1-\gamma,\quad b=(k-1)(1+k\gamma),\quad
\kappa=b/a,
\]
\[
N=n(n-1),\quad D=aN+b,
\quad h_n=-\frac{n-1-\kappa}{N+\kappa},
\quad t_n=\frac{n^2-1}{D}.
\tag{5.1}
\]
Assume \(\kappa>0\). We will prove a coefficientwise identity
\[
\boxed{\Phi_n(H)-h_n
=t_nJ_{n,k,\gamma}
+\mathbf1_{\{n\text{ even}\}}\left(\frac1n+h_n\right)R_n
+\sum_{\lambda\vdash n}c_\lambda w_\lambda,\qquad c_\lambda\ge0.}
\tag{5.2}
\]
Thus the lower bound has a fully nonnegative certificate in terms of valid common-map inequalities.

By (4.3), the coefficients of the two shapes \((1^n)\) and \((2,1^{n-2})\) on the right residual are exactly zero. For a selected shape \(\lambda=\mu\cup1^{n-k}\), before the rank-two correction the residual is
\[
r_\lambda-h_n-t_nd_\mu(n).
\]
Multiplying by the positive denominator \(D(n)_{\underline s}\) gives the polynomial
\[
\begin{aligned}
F_\mu(n)={}&(-1)^j j!D(n-j)_{\underline{s-j}}\
&+[a(n-1)-b](n)_{\underline s}\
&-(n^2-1)(k)_{\underline s}
\left(\frac{(-1)^j}{\binom kj}-\gamma\right).
\end{aligned}
\tag{5.3}
\]
The exact finite certificate is
\[
\boxed{F_\mu(k+1+z)\in\mathbb Q_{\ge0}[z]
\quad\text{for every }\mu\vdash k}
\tag{5.4}
\]
for each of the four seeds in the following table:

| \(k\) | Seed \(\gamma\) | \(\kappa\) | Dimensions used |
|---:|---:|---:|---:|
| 3 | \(0\) | \(2\) | \(n\ge6\) |
| 7 | \(-1/18\) | \(66/19\) | \(n\ge8\) |
| 9 | \(-1/19\) | \(4\) | \(n\ge10\) |
| 12 | \(-6/137\) | \(5\) | \(n\ge13\) |

Every rational coefficient in (5.4) is supplied in `certificates/dimension_transport.json` and reconstructed from (5.3) by the standard-library verifier. The two canceled shapes give the zero polynomial. This is a finite algebraic certificate of an inequality for **all** dimensions in the range, not a check up to a numerical cutoff.

For every unselected shape other than \((n)\) in even dimension and \((n-1,1)\),
\[
r_\lambda\ge-\frac2N\ge h_n.
\]
The last inequality is equivalent to
\[
(n-3-\kappa)n(n-1)\ge2\kappa.
\tag{5.5}
\]
It holds at the minimum dimension in the table, and thereafter both positive factors on the left increase.

In even dimension the coefficient of \((n)\) is eliminated by subtracting \((1/n+h_n)R_n\). The only other affected shape is \((n-1,1)\). If \(n>k+1\), its residual becomes
\[
\frac{(n+1)(n-\kappa)}{n(N+\kappa)}>0.
\tag{5.6}
\]
If \(n=k+1\) is even, it also occurs in (4.1), and its final residual is
\[
\frac{n+1}{n(N+\kappa)}
\frac{1-\gamma(n^2-3n+3)}{1-\gamma}>0.
\tag{5.7}
\]
These identities follow by substituting (4.2); both are checked separately by the verifier. All coefficients in (5.2) are now accounted for. This proves Theorem A from the four seed inequalities.

### 5.1 A completely explicit rank-three version

For \(k=3,\gamma=0\), (4.1) is
\[
J=w_{(1^n)}-\frac2{n(n-1)}w_{(2,1^{n-2})}
+\frac2{n(n-1)(n-2)}w_{(3,1^{n-3})}\ge0.
\]
The only additional selected shape has residual
\[
\frac{(n-3)(n+1)(n^2-2n+2)}
 {n(n-1)(n-2)(n^2-n+2)}\ge0.
\]
The other coefficients are covered by (5.5)–(5.7). This proves (1.1) without a large certificate table. Its inputs are the rank-three sign theorem and the inherited mixed-contraction argument, not a Lorentzian closure conjecture.

It strictly improves \(L_n\) for every \(n\ge6\): the required comparison is
\[
n!(n^2-n+2)<2n^n.
\]
It holds at six, and the ratio on the left to \(n^n\) decreases thereafter. For example, use \((1+1/n)^n>2\) and \(n^2+n+2<2(n^2-n+2)\) for \(n\ge3\).

### 5.2 Exact optimality with respect to the retained transport data

The profile supported on the first two shapes, with
\[
w_{(1^n)}=\frac\kappa{N+\kappa},\qquad
w_{(2,1^{n-2})}=\frac N{N+\kappa},
\]
has \(J=0\), \(R_n=0\), and signed value \(h_n\). Hence (5.2) is optimal for the relaxed simplex with these selected rows. It is **not** a claim that this profile arises from a positive map. The larger spectral and mixed systems can and do impose stronger constraints.

## 6. The finite-rank certificates supplying the stronger seeds

The construction extends the earlier recursive spectral/mixed linear program. In addition to (3.1), it retains the mixed-discriminant floor
\[
w_{(1^n)}\ge n!/n^n
\]
and the characteristic-coefficient hull of each projection image. Since
\[
0\preceq H(P)\preceq I,\qquad\operatorname{tr}H(P)=\operatorname{rank}P,
\]
that hull is generated by the spectra
\[
(1^{[k]},0^{[n-k]})
\quad\text{and}\quad
(1^{[a]},((k-a)/b)^{[b]},0^{[n-a-b]}).
\]
Here \(0\le a<k\), \(k-a<b\le n-a\). The spectral coefficient rows are
\[
B_{k,j,\lambda}
=\binom nk^{-1}\sum_{|I|=k}
\binom{\sum_{i\in I}\lambda_i}{j},
\]
where \(\lambda\) is padded with zeros. Joint coefficients at each projection rank are represented by nonnegative weights on the finite hull.

To these rows we add every coefficient inequality (3.5), using the already proved smaller-dimensional constants. This is exactly the earlier compatible-contraction relaxation, extended to higher dimensions; no extra hypothesis on actual maps is inserted.

### Exact arithmetic and the role of numerical discovery

SciPy/HiGHS is used only to locate a candidate dual vector. The vector is rounded to rational entries and then **repaired to exact dual feasibility**:

1. Dual entries attached to singleton negative slack columns are made nonnegative.
2. For each disjoint probability block, its normalization-row multiplier is decreased to the exact minimum of the residual column bounds.
3. Every entry of \(c-A^Ty\) is recomputed over \(\mathbb Q\) and required to be nonnegative.

The resulting rational \(b^Ty\) is a proved lower bound. It is rounded **down** to the decimal fractions in Theorem B, and that weaker rational number is used in the next dimension. Verification reconstructs the entire induction chain and every matrix entry. No claim that the new dual certificates attain the exact LP optimum is made.

The lower bounds imply the convenient seeds
\[
\gamma_7\ge-1/18,\qquad \gamma_9\ge-1/19,
\qquad \gamma_{12}\ge-6/137.
\]
The seven-dimensional inequality is inherited; the latter two use the new certificates. Theorem A then follows for all stated dimensions.

### Why the Schur basis matters computationally

A direct expanded Vandermonde computation becomes expensive. Instead, Pieri multiplication gives the complete-to-Schur matrix \(K\). Hall duality between complete and monomial functions makes the monomial-to-Schur transition the inverse transpose of \(K\). Apply (3.3), remove a column, and transform back. This uses exact integers and rational numbers.

The verifier compares the new implementation with separately expanded Vandermonde and directional derivatives in every feasible partition/variable case through total degree seven. Higher degrees rest on the proved Schur identity, with the full resulting dual inequalities checked exactly. The generated certificates do not require SciPy to verify.

## 7. Interpretation, comparisons, and remaining gap

For \(n=20\), (1.4) gives
\[
\Phi_{20}(H)\ge-\frac2{55}=-0.036363636\ldots,
\]
compared with \(L_{20}=-0.0499999756\ldots\). At \(n=50\), it gives \(-44/2455=-0.0179226069\ldots\), compared with essentially \(-0.02\). At \(n=100\), it gives \(-94/9905=-0.0094901564\ldots\), compared with essentially \(-0.01\).

In rank eight, the new finite certificate improves the earlier \(-0.0817855026\ldots\) to \(-0.05274023\), about a 35.5 percent reduction in the allowed negative magnitude. In rank nine it improves \(-0.0803713921\ldots\) to \(-0.05064282\), about 37.0 percent. The old rank-six/rank-seven numerical floors remain stronger than the elementary closed formula (1.1); all bounds should be combined by taking their maximum.

The current rank-eight global bracket becomes
\[
-0.05274023\le\mu_8\le\nu_8<-6.83\times10^{-6},
\]
with the existing capacity-trial witness unchanged. The gap remains large. No claimed extremizer realizes the relaxed profiles of Section 5.2.

The symmetry literature contributes a usable coefficient calculus and a disciplined description of its preservation boundaries. Fixed-frame determinant polynomials are stable; full orbital averaging can lose hyperbolicity; signed differential extraction is not automatically positive. The successful step preserves the common map through mixed determinants and uses Schur calculus to transport the resulting information across dimensions.

The new positive correction is polynomial rather than exponential, but the leading negative scale remains \(-1/n\). Stronger all-dimensional behavior or sharp fixed-rank constants would require more compatible-map information or further certified seed improvements. The present work does not settle any of the unrestricted sign questions in ranks four through seven.

## 8. Verification and references

Run
```
python checks/verify.py
python checks/verify_boundaries.py
```
from the extracted package. Both programs use only the Python standard library. The optional `checks/discover.py` additionally requires SciPy, but is not part of the proof checker.

The exact checks rebuild the inherited rank-four through rank-seven primal–dual certificates, verify all new rank-eight through rank-twelve rational duals, verify the four all-dimensional polynomial coefficient certificates, test all partition residuals in finite dimensions as additional controls, and verify the averaging counterexample and scalar comparisons. The universal claims use the written proofs and the finite polynomial identities, not numerical searches or a finite dimension cutoff. No independent human or multi-agent review is claimed.

**References and attribution.**

[BH20] P. Brändén and J. Huh, *Lorentzian polynomials*, Annals of Mathematics **192** (2020), 821–891. arXiv:1902.03719. Stable homogeneous polynomials and the Hessian characterization are established inputs.

[BBL09] J. Borcea, P. Brändén, and T. M. Liggett, *Negative dependence and the geometry of polynomials*, Journal of the American Mathematical Society **22** (2009), 521–567. arXiv:0711.3496. Stability-preserving operations and determinant examples; no general closure under the averaging used here is inferred.

[Mac95] I. G. Macdonald, *Symmetric Functions and Hall Polynomials*, second edition, Oxford University Press, 1995. Schur/monomial/complete duality and Pieri identities.

[Gur04] L. Gurvits, *Classical complexity and quantum entanglement*, Journal of Computer and System Sciences **69** (2004), 448–484. arXiv:quant-ph/0303055. Quantum permanent, Fischer identities, and scaling framework.

[Gur06] L. Gurvits, *The Van der Waerden conjecture for mixed discriminants*, Advances in Mathematics **200** (2006), 435–454. arXiv:math/0406420. The mixed-discriminant floor and its equality theorem are substantial inputs to the finite relaxations.

[Wan26] X. Wan, arXiv:2601.10424, *Positivity of the third Chern form of a Griffiths positive vector bundle* (version-dependent title). The unrestricted rank-three sign theorem is the starting sign input. This note does not claim that result as new.

[Project] *Rank-six and rank-seven quantum-permanent bounds from mixed contractions*, and *Optimizing the signed quantum-permanent lower bound through projection spectra*. Their finite models and earlier certificates are included as identified inputs. The new contributions are the exact two-row dimension-transport certificate, the higher-rank dual bounds, and the resulting rational all-dimensional improvement. No exhaustive bibliographic priority claim is made.
