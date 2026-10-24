# Coherence descent, extremal structure, and a negative rank-eight map

8 October 2026

## Scope

This note continues the minimization of
\[
 \Phi_n(H)=\frac1{n!}\det(\partial_X)\det H(X)
\]
over complex-linear ordinary positive bistochastic maps. Write
\(\Gamma_n=n!\Phi_n\), \(\mathfrak B_n^+\) for that compact feasible set, and
\(\mu_n=\min_{H\in\mathfrak B_n^+}\Phi_n(H)\).

The results establish an exact one-dimensional coherence-descent rule; structural restrictions on global minimizers; an explicit negative positive bistochastic map in dimension eight obtained by compressing the previous rank-nine construction; an exact polynomial/SOS minimum in a two-parameter rank-eight family; and a finite outer polynomial-optimization scheme with a rigorous repair-error bound. They do not determine \(\mu_8\) or \(\mu_9\), prove that rank eight is minimal, or give an efficient global optimization algorithm. No new numerical global lower bound is claimed.

All references to matrix positivity of a map mean ordinary positivity unless CP is explicitly written. Coefficients in every determinant contraction are kept coupled. The exact programs are supplemental algebraic checks; no independent human or multi-agent audit is claimed.

## 1. Exact coherence polynomials

For an orthogonal projection \(P\) on \(\mathbb C^n\), put \(Q=I-P\),
\[
 \mathcal D_{P,t}(X)=PXP+QXQ+t(PXQ+QXP),\qquad H_t=H\mathcal D_{P,t}.
\]
Then \(H_1=H\). If \(|t|\le1\),
\[
 \mathcal D_{P,t}=\frac{1+t}{2}\operatorname{Id}
 +\frac{1-t}{2}\operatorname{Ad}_{P-Q}
\]
is CP and bistochastic. Hence \(H_t\) is ordinary positive and bistochastic whenever \(H\) is. Both marginal equalities hold for every real \(t\).

### Theorem 1: degree reduction

If \(\operatorname{rank}P=k\), then
\[
 \Phi_n(H_t)=F_{H,P}(t^2),\qquad
 \deg F_{H,P}\le\min(k,n-k).
\]
This holds for every complex-linear \(H\). In particular, for rank-one \(P\),
\[
 \boxed{\Phi_n(H_t)=a_P+b_Pt^2,\quad
 a_P=\Phi_n(H\mathcal D_{P,0}),\quad b_P=\Phi_n(H)-a_P.}
\tag{1}
\]

**Proof.** Choose a basis adapted to \(P\). In the determinant differential, an input permutation uses the same number \(j\) of entries from \(P\) to \(Q\) as from \(Q\) to \(P\). Its coefficient after applying \(\mathcal D_{P,t}\) is multiplied by \(t^{2j}\), with \(j\le\min(k,n-k)\). Summing proves the degree statement. At rank one the values at \(0,1\) identify the two coefficients. The argument is polynomial and requires no positivity.

The same statements hold for output pinching, either directly by output permutations or using \(\Phi_n(H^*)=\Phi_n(H)\) for Hermiticity-preserving maps.

More generally, let \(H_0\) satisfy \(H_0=H_0\mathcal D_{P,0}\), and let \(R\) vanish on the two diagonal input blocks, with zero trace marginal. Then \(H_0+tR\) obeys the same degree bound. Thus the identity applies to proposed coherence *completions*, not only to rescaling already present coherences, provided their positivity is separately certified.

### Pinched coefficient as a lower-dimensional average

For rank-one \(P=ee^*\), let \(V:\mathbb C^{n-1}\to e^\perp\) be an isometry. Diagonalize
\[
 H(P)=\sum_{j=1}^n\lambda_j u_ju_j^*,\quad\lambda_j\ge0,\quad\sum_j\lambda_j=1,
\]
and let \(U_j\) identify \(u_j^\perp\) with \(\mathbb C^{n-1}\). Then
\[
 \boxed{a_P=\frac1n\sum_{j=1}^n\lambda_j
 \Phi_{n-1}\bigl(U_j^*H(V(\cdot)V^*)U_j\bigr).}
\tag{2}
\]
Indeed, the pinched output is \(x_{11}H(P)+H(VX'V^*)\). The surviving input determinant permutations fix the first input index. Differentiation once in \(x_{11}\), followed by cofactor expansion in the eigenbasis of \(H(P)\), gives the unnormalized sum of \(\lambda_j\Gamma_{n-1}\). Dividing by \(n!\) gives (2).

## 2. Exact positivity interval and a valid descent map

For a unit output vector \(y\), write the positive matrix \(H^*(yy^*)\) in the input decomposition \(P\oplus Q\):
\[
 H^*(yy^*)=\begin{pmatrix}A_y&B_y\\B_y^*&D_y\end{pmatrix}.
\]
Use Moore--Penrose inverse square roots on the supports, and put
\[
 c_P(H)=\sup_{\|y\|=1}\|A_y^{\dagger/2}B_yD_y^{\dagger/2}\|_{\rm op}.
\]
Every such block matrix is PSD, so \(0\le c_P(H)\le1\). Support inclusions needed for the inverse formula follow from block positivity of this matrix.

### Theorem 2: admissible amplification

If the off-diagonal component \(R=H-H\mathcal D_{P,0}\) is nonzero, then \(c_P(H)>0\), and
\[
 \boxed{H_t\text{ is positive}\iff |t|\le\tau_P(H),\qquad
 \tau_P(H)=c_P(H)^{-1}\ge1.}
\tag{3}
\]
If \(R=0\), the family is constant, and set \(\tau_P=\infty\).

**Proof.** By self-duality, positivity is equivalent to positivity of \(H_t^*(yy^*)\) for every \(y\). These matrices are exactly the displayed blocks with \(B_y\) replaced by \(tB_y\). The generalized Schur-complement criterion gives \(|t|\|A_y^{\dagger/2}B_yD_y^{\dagger/2}\|\le1\). Taking the supremum gives (3). If every cross block vanishes, polarization in \(y\) shows \(R=0\). Otherwise at least one ratio is nonzero. The endpoint map is valid by closedness, even when the supremum is not attained at a nondegenerate output vector. It is on the boundary, since any strictly positive endpoint could be extended slightly.

This is an exact characterization, not a claim that computing \(c_P(H)\) is easy. In particular, no Choi-PSD replacement is being made.

### Corollary 3: rank-one descent without a high-degree line search

For rank-one \(P\) with nonzero off-diagonal component, define
\[
 \operatorname{Trans}_P(H)=
 \begin{cases}
 H_0,&b_P\ge0,\\
 H_{\tau_P(H)},&b_P<0.
 \end{cases}
\]
Then it is a positive bistochastic map and
\[
 \boxed{\Phi_n(\operatorname{Trans}_P(H))\le\Phi_n(H).}
\tag{4}
\]
The decrease is \(b_P\) if \(b_P\ge0\), and
\((-b_P)(\tau_P^2-1)\) if \(b_P<0\). If the off-diagonal component vanishes, leave the map unchanged. A zero-curvature pinching is permitted and may reduce structural complexity.

For a general cut of rank \(k\), the same task reduces exactly to minimizing a polynomial of degree at most \(\min(k,n-k)\) on \([0,\tau_P^2]\). For rank two this is just a scalar quadratic minimization. This is a special degree reduction, not the tautology of minimizing the original map objective.

### A certified amplification step from a known positivity margin

Suppose \(H=\delta\Delta_n+(1-\delta)K\), where \(0<\delta<1\) and \(K\) is positive bistochastic. For every cut,
\[
 \boxed{\tau_P(H)\ge1+\frac{2\delta}{n(1-\delta)}.}
\tag{5}
\]
For \(t\ge1\), the reflection expression and \(K(xx^*)\preceq I\) for unit \(x\) give
\[
 H_t(xx^*)\succeq
 \left[\frac\delta n-\frac{(1-\delta)(t-1)}2\right]I.
\]
This proves (5). Thus, when \(b_P<0\), a *known* depolarizing slack supplies an explicit strict descent step without optimizing the positivity threshold. The estimate is attained for \(K=\operatorname{Id}\) and a rank-one cut, as seen on a vector equally supported across the cut. This sharpness concerns the feasibility estimate, not the sign of \(b_P\).

## 3. Structural restrictions on minimizers

### Theorem 4: a least-coherent minimizer is saturated

Among all global minimizers, choose \(H_*\) minimizing \(q(H)=\|C_H\|_F^2\). For every rank-one input or output projection \(P\), either the corresponding off-diagonal component is zero, or
\[
 \boxed{b_P(H_*)<0,\qquad \tau_P(H_*)=1.}
\tag{6}
\]

**Proof.** If \(b_P>0\), pinching improves the objective. If \(b_P=0\) and the off-diagonal component is nonzero, pinching preserves the minimum but lowers \(q\), because
\[
 q(H_t)=q(H_0)+t^2q(H-H_0).
\]
This orthogonality follows in a basis adapted to the cut; it also holds for output cuts. Thus \(b_P<0\). If \(\tau_P>1\), amplification improves the objective, a contradiction.

The term “least-coherent” refers only to the specified secondary objective \(q\). This is a necessary structural theorem, not a complete classification of the minimizers or a proof of sufficiency.

### Theorem 5: all global minimizers lie on the ordinary-positive boundary for n >= 3

There is a bistochastic CP map of size three with zero determinant correlation,
\(R_3(X)=(\operatorname{tr}X I_3-X^T)/2\): its Gaussian Kraus pencil is odd skew-symmetric. Padding it by a pinched identity block gives \(\mu_n\le0\) for all \(n\ge3\).

Suppose a global minimizer \(H\) were strictly positive. It has a uniform product-positivity margin, so both signs of a sufficiently small change from \(t=1\) in every rank-one-cut family are feasible. Equation (1) therefore forces \(b_P=0\). Pinching gives another global minimizer that is still strictly positive: \(H(X)\succeq\eta\operatorname{tr}(X)I\) is preserved under CP trace-preserving input pinching and unital output pinching.

Successively pinch the coordinate input and output directions. Each step is constant in objective, and the endpoint is the classical map
\[
 X\longmapsto\operatorname{diag}(A\operatorname{diag}X),
\]
where \(A\) is a strictly positive doubly stochastic matrix. Its normalized determinant correlation is \(\operatorname{per}(A)/n!>0\), contradicting \(\mu_n\le0\). Hence no global minimizer is strictly positive. This removes the extra sign assumption on the averaged \((n-1)\)-compression invariant from the earlier conditional boundary statement. It is a global-minimizer theorem, not a classification of all local minima.

## 4. A negative rank-eight map

Use the previous rank-nine family. On three blocks of size three, set
\[
 A_1=E_{13}\otimes I_3,\quad B_1=E_{31}\otimes I_3,\quad
 A_2=E_{23}\otimes I_3,\quad B_2=E_{32}\otimes I_3.
\]
Let
\[
 Q_a^{(1)}(X)=A_1XA_1^*+B_1XB_1^*+a(A_1XB_1^*+B_1XA_1^*),
\]
\[
 Q_b^{(2)}(X)=A_2X^TA_2^*+B_2X^TB_2^*+b(A_2X^TB_2^*+B_2X^TA_2^*).
\]
Define \(J_6=\left(\begin{smallmatrix}0&I_3\\-I_3&0\end{smallmatrix}\right)\),
\(B_6(S)=\operatorname{tr}(S)I_6-S-J_6S^TJ_6^*\), and let \(\widetilde B_6\) be its pinched embedding in the leading six-dimensional input/output block. Put
\[
 H_{a,b}=\tfrac18\widetilde B_6+\tfrac12(Q_a^{(1)}+Q_b^{(2)}).
\]
For \(|a|,|b|\le1\), the first bridge is CP, the second coCP, and the Breuer--Hall part is ordinary positive. Both marginals of \(H_{a,b}\) are the identity. These facts follow directly from
\[
 Q_a^{(1)}=\tfrac{1+a}2\operatorname{Ad}_{A_1+B_1}
 +\tfrac{1-a}2\operatorname{Ad}_{A_1-B_1},
\]
and the analogous transposed expression, together with
\(B_6(xx^*)=\|x\|^2I-xx^*-(J_6\bar x)(J_6\bar x)^*\succeq0\).

Let \(V:\mathbb C^8\to\mathbb C^9\) have columns \(e_1,\ldots,e_8\), and let \(U\) have columns
\[
 e_1,e_2,e_3,e_4,e_5,e_7,e_8,e_9.
\]
Set
\[
 K_{a,b}(X)=U^*H_{a,b}(VXV^*)U,
 \qquad D=\operatorname{diag}(1,1,\sqrt2,1,1,1,1,1),
\]
\[
 \boxed{T_{a,b}(X)=D K_{a,b}(X)D.}
\tag{7}
\]
This is ordinary positive, by rectangular CP compression and output congruence. It is exactly bistochastic. To verify this without a numerical scaling procedure, put
\(F=E_{11}+E_{22}+E_{44}+E_{55}\) on the eight-dimensional input. Direct diagonal evaluation gives
\[
 K_{a,b}(I_8)=I_8-\tfrac12E_{33},\quad
 K_{a,b}^*(I_8)=I_8-\tfrac18F,\quad
 K_{a,b}^*(E_{33})=\tfrac18F.
\]
Since \(D^2=I+E_{33}\), both marginal identities follow. All coherence terms vanish on the marginals, so these calculations hold for every real \(a,b\).

The parameter square is exact. The rank-one tests in the first and third coordinate blocks, and in the second and third coordinate blocks, using their first coordinate, survive the chosen compression and have output matrices congruent to \(\tfrac12\left(\begin{smallmatrix}1&a\\a&1\end{smallmatrix}\right)\) and its \(b\) analogue. Thus positivity requires \(|a|,|b|\le1\).

### Exact contraction and its certificate

The identity is
\[
 \boxed{\Gamma_8(T_{a,b})=
 \frac{8a^4-9a^2-21b^2-34a^2b^2-10}{1024}.}
\tag{8}
\]
For reproducibility, write \(N=8H_{a,b}\). Restrict input indices to \(0,\ldots,7\) and output indices to \((0,1,2,3,4,6,7,8)\), using zero-based indices. The complete nonzero coefficient list for the unnormalized contraction of the restricted tensor is

| monomial | integer coefficient |
|---|---:|
| 1 | -81920 |
| a^2 | -73728 |
| b^2 | -172032 |
| a^4 | 65536 |
| a^2 b^2 | -278528 |

All other monomial coefficients vanish. The output congruence multiplies \(\Gamma_8\) by \(|\det D|^2=2\); division by \(8^8\) yields (8).

The program `rank8_family.py` computes the entire coefficient dictionary, rather than interpolating. The recurrence fixes successive output rows, records used output columns, input rows and input columns, and appends each tensor coefficient with the three permutation parities. An independently ordered recurrence in `verify_input_order.py` fixes input rows instead. `verify_descent.py` compares the latter against (8) at exact rational parameters, including parameters outside the positive square as checks of the polynomial identity. The inherited degree-nine construction is reproduced as explicit coefficient arithmetic, not as an inaccessible numerical tensor.

The Choi norm is also exact:
\[
 q(T_{a,b})=\frac{31}{4}+3(a^2+b^2).
\tag{9}
\]
At \(a=b=1\),
\[
 \boxed{\Gamma_8(T_{1,1})=-\frac{33}{512},\quad
 \Phi_8(T_{1,1})=-\frac{11}{6881280},\quad q(T_{1,1})=\frac{55}{4}.}
\tag{10}
\]
Thus \(\mu_8\le-11/6881280\). This establishes failure in dimension eight, not that eight is the smallest failing dimension. Padding yields
\[
 \mu_n\le-\frac{11}{6881280\binom n8},\quad n\ge8.
\]
For \(n=9\), the earlier coherent witness \(-1/737280\) is a better bound.

The failure also occurs under strict ordinary positivity. The map
\[
 S_8=\frac{99}{100}T_{1,1}+\frac1{100}\Delta_8
\]
is bistochastic and satisfies \(S_8(X)\succeq\operatorname{tr}(X)I/800\) for \(X\succeq0\). An exact contraction gives
\[
 \Phi_8(S_8)=
 -\frac{7271299899816808843}{5872025600000000000000000}<0.
\]
For an integer certificate, conjugate by \(D^{-1}\) and multiply by 1600. The resulting tensor is 198 times the compressed tensor of \(8H_{1,1}\), plus diagonal trace coefficients 2 on every output diagonal except coefficient 1 on the third. Its unnormalized contraction is \(-1072196798027387364753408\); multiplication by \(2/(1600^8\,8!)\) gives the fraction above.

The uncompleted seed \(T_{0,0}\), already a compression and balancing of the original rank-nine seed, is negative too:
\(\Phi_8(T_{0,0})=-1/4128768\). The coherent completion improves its negative magnitude by the exact factor \(33/5\). No best-published-value or bibliographic-priority claim is made.

## 5. A polynomial optimality certificate and an ordered descent transformation

On the exact feasible square,
\[
\boxed{\begin{aligned}
1024\,8!\left(\Phi_8(T_{a,b})+\frac{11}{6881280}\right)
={}&(1-b^2)(21+34a^2)\\
 &+27(1-a^2)+8(1-a^2)^2\ge0.
\end{aligned}}
\tag{11}
\]
This is an explicit sum-of-squares certificate with the defining inequalities \(1-a^2\ge0\), \(1-b^2\ge0\). The multiplier \(21+34a^2\) is SOS, as are the constant multiplier and the final square. Equality holds exactly at \(|a|=|b|=1\). It certifies the global minimum in this family; it is not a global certificate over all positive bistochastic maps on \(M_8\).

There is also a specified descent order. With \(u=a^2,v=b^2\), the objective numerator is
\[
 8u^2-9u-21v-34uv-10.
\]
It decreases in \(v\), so first replace \(b\) by a number of modulus one. At \(v=1\), its derivative in \(u\) is \(16u-43<0\) on \([0,1]\), so then replace \(a\) by a number of modulus one. Both steps preserve positivity and bistochasticity and do not increase \(\Phi_8\).

The order matters. At \(b=0\), the minimizing \(a^2\) is \(9/16\); increasing \(|a|\) from \(3/4\) to one increases the objective. Thus “always maximize every coherence” is false even in this explicit family. Equation (11), not a general intuition about coherence, certifies the two-step procedure.

## 6. Finite polynomial optimization with a quantitative positivity repair

This gives a rigorous approximation framework, not an implemented fast solver.

Use an orthonormal Hermitian basis with first element \(I/\sqrt n\). A Hermiticity-preserving bistochastic map is represented by
\(\operatorname{diag}(1,T)\), with a real \((n^2-1)\)-square matrix \(T\). Every ordinary positive bistochastic map is Hilbert--Schmidt contractive: apply the unital positive-map Schwarz inequality to each Hermitian input, take traces, and split a general matrix into Hermitian real and imaginary parts. Therefore \(\|T\|_{\rm op}\le1\). The ambient affine dimension is \((n^2-1)^2\), equal to 3969 for \(n=8\).

Fix finite \(\delta\)-nets \(\mathcal N_\delta\) of the unit sphere of \(\mathbb C^n\). Define the compact outer feasible set
\[
 \mathcal O_\delta=\{H\text{ HP and bistochastic}:\|H\|_{\rm HS\to HS}\le1,
 \ y^*H(xx^*)y\ge0\ \forall x,y\in\mathcal N_\delta\}.
\]
All genuine feasible maps lie in \(\mathcal O_\delta\). Its sample inequalities are linear in the map coefficients, and its contraction condition is an LMI,
\(\left(\begin{smallmatrix}I&T\\T^T&I\end{smallmatrix}\right)\succeq0\).
It is therefore a finite semialgebraic polynomial-optimization problem with objective \(\Phi_n\) of degree \(n\). Matrix inequalities can be encoded by principal-minor inequalities if a scalar-polynomial presentation is needed.

Let
\(L_\delta=\min_{H\in\mathcal O_\delta}\Phi_n(H)\).
For unit \(x,y\), replacing each by a net point changes \(y^*H(xx^*)y\) by at most \(4\delta\): use \(\|xx^*-x'x'^*\|_F\le2\|x-x'\|\) and Hilbert--Schmidt contraction. Thus every outer-feasible \(H\) satisfies
\[
 H(xx^*)\succeq-4\delta I.
\]
Consequently
\[
 \boxed{\mathcal R_\delta(H)=\frac{H+4n\delta\Delta_n}{1+4n\delta}}
\tag{12}
\]
is genuinely positive and bistochastic.

Since \(H-\Delta_n\) is its traceless block and has operator norm at most one,
\[
 \|\mathcal R_\delta(H)-H\|\le\frac{4n\delta}{1+4n\delta}.
\]
Both maps are contractions. Telescoping their degree-\(n\) symmetric tensor powers in the normalized Fischer determinant pairing gives
\[
 |\Phi_n(\mathcal R_\delta(H))-\Phi_n(H)|
 \le\frac{4n^2\delta}{1+4n\delta}.
\]
Applying this to an outer minimizer proves
\[
 \boxed{L_\delta\le\mu_n\le L_\delta+
 \frac{4n^2\delta}{1+4n\delta}.}
\tag{13}
\]
Nested nets give monotone outer minima converging to \(\mu_n\). If an outer candidate has objective at most \(L_\delta+\eta\), its repaired value lies within \(\eta+4n^2\delta/(1+4n\delta)\) above the true minimum.

Standard moment/SOS relaxations can provide certified lower bounds for these finite polynomial problems, with a redundant ball inequality supplying an Archimedean description. Importantly, an SOS *inner* test for positivity of a candidate map and an SOS *lower bound* for minimization over an outer region have different directions. The former produces feasible witnesses; the latter can certify global lower bounds. No finite-degree SOS test is identified with all ordinary positive maps.

The number of net constraints and polynomial variables is large. No practical convergence rate for a chosen low-order SDP relaxation, no new numerical global lower bound, and no efficient rank-eight global minimization are claimed. Equation (13) supplies an explicit logical connection between the sampling error, a positivity repair, and the objective gap.

## 7. Verification and remaining questions

`verify_descent.py` checks the exact input/output rank-one quadratic identities on dense HP integer tensors in sizes 2, 3 and 4; the rank-two quartic identity in size 4; identity and trace-map normalizations; the rank-eight formula by two contraction orders; its exact marginals and Choi norm; and the SOS certificate.

`compression_scan.py` enumerates all coordinate input/output compressions of the coherent rank-nine map in sizes 8 through 4. It finds twelve negative size-eight compressions and none in the tested smaller coordinate sizes. `rank7_scan.py` also tests 6,272 specified two-coordinate-plane restrictions of four size-eight family members, finding none negative. These finite checks do not establish positivity on all seven-dimensional subspaces or for all rank-seven maps. The negative rank-eight certificate is analytic/exact and does not depend on the unsuccessful search.

The main remaining issues are the optimum value \(\mu_8\) (and \(\mu_9\)), the global contact geometry of an optimizer, whether a negative example exists below eight, and useful nontrivial global lower certificates. The rank-one transformation gives genuine descent or structural simplification, but a map fixed against those moves is not automatically a global minimizer.

## Sources and established inputs

- L. Gurvits, *Classical deterministic complexity of Edmonds' problem and quantum entanglement*, arXiv:quant-ph/0303055. The quantum-permanent/Fischer framework and odd skew-matrix zero example are established inputs.
- Y.-H. Du, *Griffiths positivity does not imply positivity of the top Chern form*, arXiv:2610.05931. The previously recorded rank-nine seed motivates the family. The present rank-eight statements are independently certified by the explicit coefficient tensors above. A fresh fetch of the public record was unavailable during this continuation; no new claim about the latest literature status is made.
- J. B. Lasserre, *Global Optimization with Polynomials and the Problem of Moments*, SIAM J. Optim. 11 (2001), 796--817, doi:10.1137/S1052623400366802. Standard moment/SOS hierarchy.
- J. Nie and X. Zhang, *Positive Maps and Separable Matrices*, SIAM J. Optim. 26 (2016), 1236--1256, doi:10.1137/15M1018514. Positivity testing through biquadratic optimization and semidefinite relaxations; their stated matrix-space setting is real symmetric.
- L. Skowronek and K. Zyczkowski, *Positive maps, positive polynomials and entanglement witnesses*, arXiv:0903.3042. The positive-map/block-positive polynomial viewpoint.

The Schur-complement criterion, elementary phase-pinching channel, and moment/SOS machinery are not claimed as new. The determinant-specific degree reduction, its extremal consequences, the rank-eight certificate, and the family descent and gap identities are the conclusions established here.
