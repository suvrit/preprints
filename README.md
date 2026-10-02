<div align="center">

# preprints

**Papers by Suvrit Sra, released version by version, every file timestamped.**

[![timestamps: OpenTimestamps](https://img.shields.io/badge/timestamps-OpenTimestamps-f7931a?logo=bitcoin&logoColor=white)](#checking-a-timestamp)
[![arXiv: Suvrit Sra](https://img.shields.io/badge/arXiv-Suvrit%20Sra-b31b1b?logo=arxiv&logoColor=white)](https://arxiv.org/search/?searchtype=author&query=Sra%2C+Suvrit)
[![format: PDF](https://img.shields.io/badge/format-PDF-4c566a)](#layout)
<!-- badges:start -->
[![papers](https://img.shields.io/badge/papers-2-0b7285)](#papers)
[![versions](https://img.shields.io/badge/versions-2-0b7285)](#papers)
<!-- badges:end -->

<sub>Every version stays available. Every released file carries an
OpenTimestamps proof made on the day it was released.</sub>

</div>

Each paper has its own folder, and each release of it is a numbered version
(`v1`, `v2`, …) that stays in place when later ones appear. The paper's README
lists every version, newest first, with its abstract. When a version is also on
arXiv, the table links it; the version numbers here are this repository's own,
not arXiv's.

## Papers

<!-- release:start -->
| Paper | Latest | Released | PDF | arXiv |
|---|---|---|---|---|
| [**Positive definite functions of noncommuting contractions, Hua-Bellman matrices, and a new distance metric**](hua/) | v1 | 2 October 2026 | [![PDF](https://img.shields.io/badge/PDF-v1-0b7285)](hua/v1/hua-v1.pdf) | [![arXiv](https://img.shields.io/badge/arXiv-2112.00056v2-b31b1b?logo=arxiv&logoColor=white)](https://arxiv.org/abs/2112.00056v2) |
| [**A Koteljanskii inequality for permanents**](perm-m-matrix/) | v1 | 2 October 2026 | [![PDF](https://img.shields.io/badge/PDF-v1-0b7285)](perm-m-matrix/v1/perm-m-matrix-v1.pdf) | [![arXiv](https://img.shields.io/badge/arXiv-2609.39979v1-b31b1b?logo=arxiv&logoColor=white)](https://arxiv.org/abs/2609.39979v1) |
<!-- release:end -->

## Checking a timestamp

Every released file `F` has an [OpenTimestamps](https://opentimestamps.org)
proof `F.ots` next to it. The proof shows that `F`, byte for byte, existed no
later than the Bitcoin block that confirms it.

```sh
pip install opentimestamps-client
ots verify perm-m-matrix/v1/perm-m-matrix-v1.pdf.ots
```

`ots verify` checks the proof against a local Bitcoin node. Without one, drop
the file and its `.ots` onto [opentimestamps.org](https://opentimestamps.org).

## Layout

```text
preprints/
├─ README.md                 this file; the badges and the table are generated
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
