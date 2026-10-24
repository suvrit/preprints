# Exact coherent-family verification

These unchanged verifier sources come from `quantum_permanents_adjoint_energies_note_source.zip`, extracted into the manuscript review sources. The added `verify_all.py` harness runs five exact programs, asserts the complete coefficient tables and improvement factors, and checks that every copied family source still matches its input hash.

Run from the release root with Python 3.10 or newer (standard library only):

```sh
python3 -B families/verify_all.py
```

Do not use `-O`. The harness writes logs and result JSON files; run a copy if retaining this frozen snapshot. Expected final status: `all fresh family checks passed`.

## Mathematical scope

The scripts establish algebraic identities and finite exact controls. The manuscript proves ordinary positivity on the exact feasible square `|a|,|b| <= 1`, the bistochastic normalization, and the family minimization consequences. The exact attained family minima give **upper bounds** on the unrestricted minima `mu_9` and `mu_8`; they are not global minima over all positive bistochastic maps. The nine-dimensional base member is the normalized Du seed. The eight-dimensional base member is its specified compression and exact output balancing.

The nine-dimensional polynomial is

```text
Gamma9(H[a,b]) = -3/256 * (4 + 9(a^2+b^2) + a^4+b^4
                           + 16a^2b^2 + a^4b^2+a^2b^4).
```

Its family minimum is `Gamma9=-63/128`, `Phi9=-1/737280`, attained exactly when `|a|=|b|=1`. The negative magnitude improves by `21/2` over `Phi9(H[0,0])=-1/7741440`.

The balanced eight-dimensional polynomial is

```text
Gamma8(T[a,b]) = (8a^4 - 9a^2 - 21b^2 - 34a^2b^2 - 10)/1024.
```

Its exact family gap identity is

```text
1024*(Gamma8(T[a,b])+33/512)
 = (1-b^2)*(21+34a^2) + 27*(1-a^2) + 8*(1-a^2)^2.
```

Thus its family minimum is `Gamma8=-33/512`, `Phi8=-11/6881280`, attained exactly when `|a|=|b|=1`. The negative magnitude improves by `33/5` over `Phi8(T[0,0])=-1/4128768`.

## Full coefficient tables

All unspecified coefficients vanish. These are complete polynomial contractions, rather than interpolated coefficient fits.

| powers (a,b) | coefficient of Gamma9(H[a,b]) | coefficient of Gamma8(T[a,b]) |
| --- | ---: | ---: |
| (0,0) | -3/64 | -5/512 |
| (2,0) | -27/256 | -9/1024 |
| (0,2) | -27/256 | -21/1024 |
| (4,0) | -3/256 | 1/128 |
| (0,4) | -3/256 | 0 |
| (2,2) | -3/16 | -17/512 |
| (4,2) | -3/256 | 0 |
| (2,4) | -3/256 | 0 |

`coherent9/verify_polynomial.py` contracts the full nine-dimensional polynomial by output rows, using bit masks. `coherent9/verify_input_order.py` uses input rows and explicit sorted tuples at seven exact parameter pairs, checks both marginals and the norm profile, and checks identity/trace normalizations. Checks outside the feasible square concern polynomial identities only.

`coherence_descent/checks/rank8_family.py` contracts the full eight-dimensional polynomial by output rows. `verify_descent.py` compares the output-row and input-row recurrences at seven exact pairs, checks the formula, norm and gap identities, diagonal marginal identities, low-dimensional pinching controls, and one strictly positive perturbation. `rank8_certificate.py` checks the coherent endpoint, both bistochastic marginals with the exact output filter, and both contraction orders.

The helpers `compression_scan.py` and `pinching_checks.py` are required imports; their separate search/pinching entry points were not run in this release. The source proof notes are preserved as provenance and mathematical context. Other claims discussed in those notes are not additions to the present clean run.

The individual commands, their working directories, logs, outputs and measured resource use are in `../verification/family-run-results.json` and `../VERIFICATION.md`.
