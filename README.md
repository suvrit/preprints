<div align="center">

# Preprints

**Preprints by Suvrit Sra, released version by version, every file timestamped.**

[![timestamps: OpenTimestamps](https://img.shields.io/badge/timestamps-OpenTimestamps-f7931a?logo=bitcoin&logoColor=white)](#checking-a-timestamp)
[![arXiv: Suvrit Sra](https://img.shields.io/badge/arXiv-Suvrit%20Sra-b31b1b?logo=arxiv&logoColor=white)](https://arxiv.org/search/?searchtype=author&query=Sra%2C+Suvrit)
[![format: PDF](https://img.shields.io/badge/format-PDF-4c566a)](#layout)
<!-- badges:start -->
[![papers](https://img.shields.io/badge/papers-4-0b7285)](#papers)
[![versions](https://img.shields.io/badge/versions-4-0b7285)](#papers)
<!-- badges:end -->

<sub>Every version stays available. Every released file carries an
OpenTimestamps proof made on the day it was released.</sub>

</div>

This repository contains the "initial public release" of my papers (from Oct 1, 2026 onwards) and supporting material for those papers. Not everything here will be on arXiv simultaneously (either due to their rate limits, or simply because the work was not arXiv-worthy yet); some works may eventually make it to conferences or journals if I find time to go through that process. My primary aim in sharing these works is the usual: dissemination of information in the hope that somebody else also finds it interesting and/or useful; and of course, sharing the joy of mathematics; merely because some of the work has AI assistance doesn't remove any of that joy or value. 

Each paper has its own folder under `preprints/`, and each release of it is a numbered version
(`v1`, `v2`, …) that stays in place when later ones appear. The paper's README
lists every version, newest first, with its abstract. When a version is also on
arXiv, the table links it; the version numbers here are this repository's own,
not arXiv's.



## Papers

<!-- release:start -->
| Paper | Latest | Released | PDF | arXiv |
|---|---|---|---|---|
| [**Monotonicity of Turán-ratios of symmetric polynomials**](preprints/sym-turan/) | v1 | 7 October 2026 | [![PDF](https://img.shields.io/badge/PDF-v1-0b7285)](preprints/sym-turan/v1/sym-turan-v1.pdf) | — |
| [**A Proof of McLeod's 1959 Conjecture on Complete Homogeneous Symmetric Ratios**](preprints/mcleod-hk/) | v1 | 5 October 2026 | [![PDF](https://img.shields.io/badge/PDF-v1-0b7285)](preprints/mcleod-hk/v1/mcleod-hk-v1.pdf) | — |
| [**Positive definite functions of noncommuting contractions, Hua-Bellman matrices, and a new distance metric**](preprints/hua/) | v1 | 2 October 2026 | [![PDF](https://img.shields.io/badge/PDF-v1-0b7285)](preprints/hua/v1/hua-v1.pdf) | [2112.00056v2](https://arxiv.org/abs/2112.00056v2) |
| [**A Koteljanskii inequality for permanents**](preprints/perm-m-matrix/) | v1 | 2 October 2026 | [![PDF](https://img.shields.io/badge/PDF-v1-0b7285)](preprints/perm-m-matrix/v1/perm-m-matrix-v1.pdf) | [2609.39979v1](https://arxiv.org/abs/2609.39979v1) |
<!-- release:end -->

## Checking a timestamp

Every released file `F` has an [OpenTimestamps](https://opentimestamps.org)
proof `F.ots` next to it. The proof shows that `F`, byte for byte, existed no
later than the Bitcoin block that confirms it.

```sh
pip install opentimestamps-client
ots verify preprints/perm-m-matrix/v1/perm-m-matrix-v1.pdf.ots
```

`ots verify` checks the proof against a local Bitcoin node. Without one, drop
the file and its `.ots` onto [opentimestamps.org](https://opentimestamps.org).

## Layout

```text
.
├─ README.md                    this file; the badges and the table are generated
└─ preprints/
   └─ <paper>/
      ├─ README.md              every version, newest first, with its abstract
      ├─ versions.json          the same, machine-readable
      └─ v1/, v2/, …            one folder per release
         ├─ <paper>-vN.pdf      the paper
         ├─ <paper>-vN.pdf.ots  its timestamp
         └─ …                   supporting PDFs and certificates, each with its .ots
```

## Citing

Cite the arXiv version where there is one; the table links it. For a version
released only here, cite the paper folder and version (for example
`perm-m-matrix` v1) with the repository URL. Versions are never replaced, so
the reference stays fixed.
