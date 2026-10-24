# Certificate release 2026.10.15.2

This local frozen directory accompanies `../phi-lower-bounds-structural.tex`. It extends v2026.10.15.1 with the exact coherent-family certificates in dimensions nine and eight. The earlier release and this one have not been publicly deposited or assigned a stable public URL.

## Verification history and scope

The seven original controls were run successfully for v2026.10.15.1 on 15 October 2026. Their verifier sources, finite-certificate data, recorded logs and outputs are inherited byte for byte: 54 original non-metadata files were checked against the v1 checksum inventory. Those seven controls were **not rerun** in preparing v2. Their original instructions and reports remain in `verification/v1-README.md`, `verification/v1-VERIFICATION.md` and `verification/v1-MANIFEST.json`.

Five added exact family programs were freshly run for v2. All passed. Full coefficient dictionaries, independent contraction orders at exact parameters, marginal and norm controls, and the eight-dimensional polynomial gap identity agree. See [families/README.md](families/README.md) for the coefficient tables and the exact distinction between attained family minima and unrestricted minima.

## Requirements and commands

Python 3.10 or newer and the standard library suffice for all required checks. Do not use `-O`; assertions form part of verification. No network or optimizer is required. The inherited optional discovery and matrix-calibration programs retain the dependency limitations documented in `verification/v1-README.md`.

First check integrity from this directory:

```sh
shasum -a 256 -c SHA256SUMS
```

GNU `sha256sum -c SHA256SUMS` is equivalent. `SHA256SUMS` lists every regular release file except itself, sorted by relative path, excluding caches. Its own SHA-256 identifies this frozen snapshot.

To reproduce the fresh family suite from the release root:

```sh
python3 -B families/verify_all.py
```

Expected final status: `all fresh family checks passed`. Its five individual commands and working directories are listed in `VERIFICATION.md` and `verification/family-run-results.json`. The expected family minima are `Phi9=-1/737280` and `Phi8=-11/6881280`; the negative-magnitude improvement factors over the stated base members are `21/2` and `33/5`.

To rerun the seven inherited controls from the release root:

```sh
python3 -B finite/checks/verify_all.py
python3 -B compile_bounds.py
python3 -B structure/verify_rational.py --seeds
python3 -B structure/verify_fixed_core.py
python3 -B structure/verify_independent.py
```

Run the two inherited witness commands from the `witnesses` subdirectory:

```sh
python3 -B polarization_result/verify.py
python3 -B asymptotic_agents/padding/cp_summand_anisotropic.py
```

Expected summaries and mathematical roles of the inherited commands are preserved in `verification/v1-README.md`. Their baseline includes the exact rank-eighteen floor `-171460901/5000000000` and transport parameter `32532964294/5171460901`.

The scripts write JSON outputs and logs. Run a copy to preserve this frozen directory unchanged; `-B` suppresses bytecode caches. Neither the old nor new verifiers prove a global actual-map minimum, a quantitative strictness gap, or the unrestricted asymptotic exponent. The analytic manuscript proofs supply the all-dimensional implications and the positivity/family minimization arguments.

## Provenance and recorded resources

`MANIFEST.json` binds the release version, v1 checksum identity, inherited verification record, fresh commands and scope. `verification/family-copied-inputs.json` identifies unchanged copies from the source archive, and `verification/family-run-results.json` records their clean run. The source archive's reproducibility proof notes are preserved under `families/` for context; their additional topics are outside this release's fresh check claims.

The fresh family suite took 1.450361 seconds and had a maximum recorded child resident memory of 28,688,384 bytes on the recorded macOS ARM64/Python 3.14.2 environment. The inherited seven-control run took 64.446467 seconds, with maximum resident memory 404,946,944 bytes. These are separate runs. Wall time uses `time.perf_counter`; child resident memory uses POSIX `os.wait4` where available, with macOS reporting bytes.
