# Print readability and final packaging review

Reviewed 22 November 2026. **Provisional local score:95/100**, using the same 30/20/20/15/15 rubric as the preceding audit. This is a bounded editorial assessment, not the instructor's grade or an institutional originality certificate. The separate87-point estimate uses an unspecified earlier baseline and cannot be arithmetically combined with this score.

| Category | Score | Remaining limit |
|---|---:|---|
| DAV design and print visibility |29/30| Dense comparative tables and compact eight-case gallery remain small-format content; no universal accessibility/user-study claim. |
| Manual and cross-milestone continuity |18.5/20| Promised independent holdouts/subject matching/GAN arm remain unrun and disclosed; historical source versions remain distinct. |
| Numerical/citation precision |19.5/20|464 automated checks pass; literal provenance is supplemented by semantic review, not a fresh independent derivation of every interpretation. |
| Scientific rigor |14/15| Encoding/subject support and exchangeability remain unavailable; improved presentation does not change that negative conclusion. |
| Repository and GCR packaging |14/15| Lean ZIP follows actual manual; source rebuilds identically. Updated local formatting/reorganization still needs the authors' next Git push. |
| **Total** |**95/100**| **Ready local package; public revision check follows publication.** |

## Requirement decisions

The M4 manual, expected-outcome paragraph on p.5, requires a PDF and editable LaTeX. Its reproducibility component on p.2 accepts a code/repository link with sufficient setup details. It does not explicitly require Word, BUILD.md, src/, tests/, requirements.txt or results/ inside the upload ZIP. These extras are therefore not added. The lean ZIP retains the paper, complete editable source/assets, supplement referenced by the paper, and a short README. Word and the complete code/evidence remain in the repository. `paper/paper.docx` already existed publicly; no missing-Word penalty is justified.

| Suggestion | Decision and effect |
|---|---|
| ZIP versus checklist | Keep manual-sized package; earlier audit-specific release/ layout is superseded by the user's lean-package instruction. No score deduction for absent optional ZIP copies. |
| Root review clutter | Move seven process/review Markdown documents into audit/reviews/; root keeps README, BUILD and REPRODUCIBILITY. Prior reports are marked historical, with a current review pointer. |
| Fig.4 weak overlays and LD overplot | Stronger KDE/ellipse strokes, black displacement arrows with white outline, larger centroid marks, hollow Human circles drawn above low-opacity filled LD squares. Same coordinates, counts and confidence construction. |
| Fig.10 resize notation | Replace multiplication-like glyphs with explicit 0.75/0.50 factor labels. |
| Fig.10 B/C uncertainty and ten styles | Keep explicitly descriptive point estimates; caption states no computed intervals and panelC states n = 10 styles. No new inference or invented intervals. |
| Fig.7B sign visibility | Keep exact symmetric zero-centered normalization; use teal/ochre with distinct lightness, signed annotations and signed colorbar ticks. |
| Purple reuse | SD remains purple; FFT-only becomes teal and HSV+Lab green. Human blue and LD orange unchanged. Dashboard model palette matches static probes. |
| Double-negative comparison | State handcrafted-minus-comparator differences explicitly, including negative intervals; remove 'trails by a negative' wording. The abstract already gave comparator scores without that double negative. |
| Code identifier in prose | Remove metadata_gated from IV.B; the readable Metadata-only label suffices. Weight identifier IMAGENET1K_V2 remains for reproducibility. |
| Overloaded C | Keep standard complexity C_H / atlas C, explicit solver C_solver, and distinguish continuity with calligraphic C and Cont.(15)table/plot labels. No parameter meaning changes. |
| Cryptic algorithm map | Replace the slash-heavy mapping sentence with readable operation/line ranges. The twelve-step plan crosswalk remains in the released evidence. |
| Transparent/explainable wording | Replace transparent probe/shifts with named linear probe/measured shifts. Retain the established research title; existing G1 limitations explicitly reject untested faithfulness/usefulness claims. Changing the topic/title is unnecessary. |
| Source filename gaps | In the GCR source, number main figure wrappers/assets 1–11 to match printed figures. Preserve reference labels and validate identical text/pixels. Internal development asset IDs may remain stable in the code release. |
| Build portability | README gives the same Tectonic command for Windows PowerShell, macOS and Linux shells; no platform-specific shell syntax. Full experimental cross-platform replication is not claimed. |
| TablesI/IX small type | Increase both from 7 to 7.5 pt. Shorten repetitive TableIX wording/captions while preserving all ten studies, metric values, version markers and material protocol limits.8 pt trials exceeded 12 pages, so they were not shipped. No margins or body fonts shrunk. |
| First person | Replace both 'our' constructions in II.B; third-person scan passes. |
| Stale process/availability wording | Use public availability statements. Replace 'preceding report' with direct cached-summary provenance. Retain original cuDNN as unrecorded; remove revision-import narrative without inventing a version. |
| Additional print fixes | Gallery titles/ticks enlarged, actual dashboard case caption recaptured larger/darker, and the acknowledgement paragraph ends before References rather than orphaning its final phrase. |

## Scientific invariants and verification

No original empirical result, split, feature value, prediction, model, inferential test or research conclusion changed. The 104-feature probe still has AUROC 0.9824 / F1 0.9420; frozen ResNet/DINO remain stronger;542 of 1,040 exploratory passes still yield zero eligible confirmations under failed controls. No full pipeline or new CI analysis was run. Figure redraws use the same cached inputs; screenshot capture passed all six native views and preserved the required UI footer.

The final source has 12 IEEE pages, 38 references, 13 main tables and 11 main figures. Word has separate pagination. All 464 numerical/citation/source-build checks pass, including clean and CSV-rebuild text/pixel identity, source-group membership, cached interval arithmetic, all main metric cells and effective figure resolution. Both literature tables are larger, with no missing rows or values. Renamed slim-source figures are separately compiled, ZIP members/CRC/hashes checked, and process notes/code/results remain outside GCR.

The prior public baseline was verified at commit 15621c8fd07261501bed7ed9eba7902ac8b23930 with 558 matching artifacts and manifest. It is not described as missing/private. The current local print changes require a new commit; no new remote publication is claimed before the user pushes. Institutional similarity/AI-use checks, exact department-name confirmation and final author read-through remain author actions. No Zenodo DOI is required by the manual or the user's chosen repository route.

## Independent review

The fresh-context review is retained in print_readability/INDEPENDENT_PRINT_REVIEW.md. It independently awards 29/30 DAV, 18.5/20 continuity and 14/15 rigor after viewing the final caption/gallery/acknowledgement repairs. Numerical and packaging scores above are the parent verifier's assessment. No critical or moderate local defect remains observed in this revision; residual limits are dense print content and the original experimental limitations, not hidden new causal claims.
