# Supporting files for v1

The computational claims of the paper and its supplement are checked by the three frozen
certificate bundles in this folder. Each bundle has its own README with the commands to run and a
`SHA256SUMS` file; only Python's standard library is needed.

| Bundle | Supports |
|---|---|
| `certificates-2026-10-22-push/` | the finite seeds of Table 1 (dimensions 4–21, Proposition A.2), the dimension-24 certificate (Proposition A.3), and the transported tails behind the bound $-3n/(3n^2+20n+103)$; supplement Section S1.3 |
| `certificates-2026-10-22/` | the strengthened dimension-18 certificate of supplement Section S1.2 |
| `certificates/` (release 2026.10.15.2) | the exact computations for the negative families of Appendix C (Propositions C.1 and C.2) and the extension polynomial (C.4); the first certificate release of supplement Section S1.1 |

The bundles are frozen snapshots, unchanged since they were made, so their READMEs use the file
names of that time, including an earlier working title of the paper. Scripts that generated the
certificates are not included; the verifiers are.
