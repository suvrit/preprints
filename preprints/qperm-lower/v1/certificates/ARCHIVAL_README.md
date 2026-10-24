# Certificates for Lower bounds for the signed quantum permanent

This directory accompanies the original manuscript and its latest revision, `../phi-lower-bounds-structural.tex`. The finite/transport files are copied from the `method` directory of `phi_asymptotic_search.zip`. The `witnesses` files are selected exact verifiers from the same archive. The original ZIP remains unchanged.

From this directory, run with Python 3.10 or newer:

```sh
python3 finite/checks/verify_all.py
python3 compile_bounds.py
```

These commands use exact rational arithmetic and no numerical optimizer. The first rebuilds all finite models through dimension 18; the second reconstructs the all-dimensional shifted-polynomial certificates and rational envelopes. They write their own result JSON files.

From the `witnesses` subdirectory:

```sh
python3 polarization_result/verify.py
python3 asymptotic_agents/padding/cp_summand_anisotropic.py
```

These use the standard library. They verify the rank-eight seed, normalization, corner identity, improved polynomial witness, and polarization controls. The optional full matrix check in `asymptotic_agents/exterior/verify_stable_tuple.py` additionally uses NumPy; the manuscript's stable-tuple construction has a complete analytic proof.

`finite/checks/sparse_extend.py` is optional numerical discovery code requiring SciPy. Discovery is not needed to verify any bound in the paper. A proposed numerical objective is not a certificate until its rational dual passes exact feasibility.

The `structure` directory adds exact checks for the 15 October structural revision:

```sh
python3 structure/verify_rational.py --seeds
python3 structure/verify_fixed_core.py
python3 structure/verify_independent.py
```

Its README identifies the new archives, local path adaptations, and independent controls. All three use the standard library; the first reuses the retained finite certificates. These checks do not replace the analytic proofs or identify actual-map minima.

The manuscript's notes and archive audits are in `../phi-lower-bounds-notes.md` and `../phi-lower-bounds-review/`. Original mathematical notes copied with this directory preserve their own titles and chronology. Earlier manuscript versions are preserved alongside the current source.
