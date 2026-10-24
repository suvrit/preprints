# Structural identities and coherent extensions

These checks accompany `../../phi-lower-bounds-structural.tex`.

- `verify_rational.py` comes from `phi_rational_structure.zip`, 15 October 2026. Only its inherited-certificate paths and output filename were adapted. It reuses `../finite/` rather than copying the unchanged certificates again.
- `verify_fixed_core.py` comes from `phi_fixed_core_development.zip`, 14 October 2026. Its output filename was changed to avoid collision with the rational verifier's output.
- `verify_independent.py` was added during integration. It independently expands minor Wick pairings and normalized antisymmetrization, checks the projection characteristic polynomial by elementary polynomial multiplication, and checks the signed cofactor/phase square estimates using rational reduction-map examples. It imports the fixed-core checker's exact example constructor only; it does not use the archived radial model or its mixed rows.

Run from the parent certificate directory:

```sh
python3 structure/verify_rational.py --seeds
python3 structure/verify_fixed_core.py
python3 structure/verify_independent.py
```

The first verifies 315 parameter cases and 7,029 individual mixed coefficients, 10,701 residual signs, 2,229 all-proper-dimensional zero-seed entries, finite comparisons, and (with `--seeds`) all inherited duals through rank 18. The second checks sixteen exact core/dimension combinations, direct ambient contractions for n=r,r+1, the Gamma normalization, coefficient/envelope controls, and the rank-two noncentral coefficients. The third checks 543 exact Wick/antisymmetrization entries, 260 projection substitutions, and 24 phase/square estimates. Finite checks calibrate the formulas; the manuscript contains the general proofs.

No script proves actual-map realizability, a quantitative strictness gap, or the unrestricted asymptotic exponent. All output JSON files identify their scope.
