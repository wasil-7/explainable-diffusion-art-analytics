# Independent review after print-visibility improvements

22 November 2026. This follow-up independently reviewed the staged `print_polish/paper.pdf` through all twelve current page renders, its `latex/main.tex`, condensed comparison table, captions, appendix and current figure-generator settings. The main-page renders are 144 DPI; original figure assets/source were used to assess channel/scaling choices. This report builds on the previous independent manual/M1-M3 audit; it does not reclassify prior correctly planned quadrants, calibrated saturation cutoff or SD side-analysis as deviations. No paper edits or experimental pipeline reruns were performed by this reviewer.

## After-improvement rubric scorecard

| Category | Score | Independent assessment |
|---|---:|---|
| DAV visualization and graphical integrity | **29/30** | Atlas identity, centroid evidence, sign coding and reserved palette are clearer; final screenshot caption and gallery typography improved, with some inherent print density remaining |
| Manual/cross-milestone continuity | **18.5/20** | Required structure and all five comparison components survive shortening; T15 and holdout omissions remain disclosed; omitted promised experiments and lack of matched external-method reproduction still limit completeness |
| Numerical/citation precision | **Pending parent verification /20** | Existing `qa/final_checks.json` reports 464 checks passed, 38 references, 13 tables and 11 figures. This reviewer did not independently rerun the complete numerical/citation audit and does not award unearned points |
| Scientific rigor and honesty | **14/15** | Frozen-probe, attribution, common-support, exchangeability and G1-G3 qualifications retained; no stronger inference introduced by condensation |
| GitHub/GCR packaging | **Pending publication/package verification /15** | This is a staged print review. Clean canonical source migration, exact final ZIP contents and publication cannot be certified from local PDF appearance |

**Independently scored subtotal after the final corrections: 61.5/65**, versus the preceding corrected-version 60.5/65. A defensible full score is `61.5 + verified numeric/citation score + verified repository/package score`; this sub-audit does not assert a final /100 before those separate checks. A visual polish pass does not itself establish that the revised version is published.

## Initial print-review findings (subsequently corrected where noted below)

No new critical or moderate visual, continuity or scientific-honesty defect was found. The following remain minor:

1. **Paper p.12, top left:** The acknowledgements end with the orphan continuation “NUCES), Islamabad, for academic guidance.” The content is complete, but the spill from p.11 weakens the otherwise clean References opening. Moving the acknowledgement sentence intact or a small local spacing adjustment would improve the page if twelve pages are preserved. This does not justify reducing table text again.
2. **Figure 8, p.8:** The tiny light-gray selected-case caption remains faint at print size. Plot axes and origin legend are readable; main caption/Table XIII retain interpretive context.
3. **Figure 11, p.11:** The eight-row gallery retains roughly 4-5 point diagnostic text. High-resolution figures are sharp but still require enlargement for detailed reading. Shared scales, origin shapes and N/A are correct.
4. **Table IX, p.8:** At 7.5 points it is improved but inherently dense; the Metric and Limitation columns wrap heavily. No overlap, truncation or lost row was observed.

## Requested visualization checks

- **Figure 3, p.5:** FFT-only is now teal, keeping purple reserved for SD. Alternate C1 row keys remain separated; all ten rows survive in B1 order, as the caption now explains. C2 ticks `0` and `.0034` are separated. The former crossing-leader problem stays resolved.
- **Figure 4, p.6:** Open blue Human circles, higher drawing order and filled low-opacity orange LD squares improve simultaneous origin visibility. Ellipse/contour outlines and white-haloed dark centroid arrows are stronger. Source explicitly draws Human above LD, contours at z-order 4, ellipses at 5, centroids at 6 and arrows at 7. Arrows still terminate at LD from Human; there is no sign reversal or changed data. No clipped ellipse, legend overlap or obscuring text annotation was found. Overlaid clouds inherently retain point coincidence; this is not eliminated by styling.
- **Figure 5, p.6:** Wider heading separation is cleaner. The fidelity axis uses `Cont.(15)` while the prose uses mathematical continuity `mathcal C(15)`; the legend spells out Continuity. This reduces confusion with statistical complexity C_H and C_solver without changing values. Zoom and seed-range caveats remain explicit.
- **Figure 6, p.7:** SD remains purple with redundant triangle/line identity. Log axes, intervals and external legend remain intact.
- **Figure 7B, p.7:** Teal-negative/ochre-positive mapping has a white zero center, explicit plus/minus cell signs and symmetric source limits `vmin=-lim`, `vmax=lim`, where lim is the maximum absolute shift. W1 remains grayscale sequential with upper bound 1.05. Orange origin identity is not reused as an unrelated Lab category; the ochre quantitative diverging endpoint is distinct and sign-labeled.
- **Figure 9, p.10:** HSV brown, Lab gray and HSV+Lab green are distinct from SD purple. Interval visibility and zero-based crop bars remain; bar labels clear their tops.
- **Figure 10, p.11:** Resize factors are now plainly `0.75` and `0.50`, beneath “Resize factor.” AUROC changes retain measured intervals. B and C deliberately remain point estimates without computed intervals, and C says n=10. The caption states this explicitly rather than inventing statistical certainty.
- **Figure 11, p.11:** Shared FFT/Haar ranges, logarithmic labels and 0-1 color-summary ranges survive. No new bar/title/label overlap was observed.

## Continuity and semantic checks after shortening

All fifteen manual components remain in order across the twelve-page paper. Abstract metrics, six keywords and five contributions remain. Section VI retains summary, quantitative table, methodological comparison, absolute/relative differences and fairness/limitations. Table IX retains every designated base study and all seven required content columns. Its shortened ArtBrain text is still contextualized by generator attribution in the Problem column; FIRE remains Kandinsky3-trained and Table-2 scoped; VIB-Net still distinguishes 15 Table-1 columns from 17 overall generators; SIDWA remains abstract-scoped with A100 latency. No material meaning was lost through these cuts.

The revised contribution and comparison wording now uses explicit signed “handcrafted-minus-ResNet-50” and “handcrafted-minus-DINOv2” differences. Both remain negative, with the ResNet interval wholly negative. “Transparent probe” rhetoric is replaced by the more precise 104-feature logistic-probe description. Third-person prose and absence of stale “awaits push” language are appropriate for the known public base repository, but final staged-print publication must still be checked separately.

The original caveats remain substantive: metadata ranking does not prove pixel-probe reliance on encoding; zero eligible confirmations does not establish zero true effects; JPEG/ordinal mediation is untested; equal recompression does not restore common support; equal-encoding retraining was not run; artist/style/generator holdouts and SD gallery were not run; human usefulness/explanation faithfulness remain untested. G1 is implemented auditability/fidelity, G2 descriptive within-style contrasts and G3 unestablished under verified controls. Condensation introduces no causal or generalization overclaim.

## Release boundary

The staged paper is locally acceptable for the assigned visual/continuity/rigor checks, with minor limitations above. Canonical figure renaming, cross-platform source-build instructions, no-extra-file GCR packaging, audit-directory migration and final GitHub publication require independent final package/repository checks. Do not treat this report or an existing pre-polish remote commit as evidence that all staged improvements are already on the remote.

## Final follow-up: pages 8, 11 and 12

Independently inspected the updated `qa/renders/08.png`, `11.png` and `12.png` after the last print corrections. Figure 8's selected-artwork caption is now dark and larger, wraps clearly under the artwork, and does not intrude into either image or plot. Human, style and case identifier are legible at a materially improved size. This resolves the faint-caption finding.

Figure 11's larger diagnostic ticks and titles are clearer, with no observed overlap between row titles, FFT/Haar axis labels, bars, N/A annotation or adjacent rows. The eight-case grid remains information-dense and some glyphs remain physically small; magnification remains useful for detailed numerical reading, but there is no new occlusion. This partially resolves the gallery-typography finding and supports a half-point DAV improvement rather than a perfect score.

Page 12 now starts cleanly with References. The acknowledgements and complete institution name remain together on page 11, resolving the orphan continuation without an additional page or reduced literature-table type size.

**Final assigned-module scores: DAV 29/30, continuity 18.5/20, scientific rigor 14/15 = 61.5/65.** No critical or moderate defect remains in these reviewed modules. Remaining minor observations are dense Table IX wrapping, the inherently compact gallery, and the visually long title. Numerical/citation and repository/package scores still require their separate verifier; a provisional parent score of 19.5/20 plus 14/15 would yield **95/100**, conditional on those checks and the stated publication boundary.
