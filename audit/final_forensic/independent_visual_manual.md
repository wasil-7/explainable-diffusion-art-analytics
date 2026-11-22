# Independent DAV, continuity and scientific-honesty audit

Audited on 22 November 2026. This reviewer independently read the supplied audit instruction, all four supplied course manuals, actual M1/M2/M3 extracted submissions, current `m4_final/latex/main.tex`, comparison tables, figure-generator source and current PDF renders. All twelve paper pages and supplementary S1 were visually inspected; the newly generated 300-DPI pages in `final_audit_work/renders` were also inspected, with additional 288-DPI PDF crops for Figure 3C and Figure 4. This is a bounded sub-audit of Modules 1, 2 and 4; it does not certify numerical or repository/package modules.

## Scores before corrective patches

| Requested module | Score | Reason |
|---|---:|---|
| DAV graphical integrity | 27/30 | Broadly correct channels, scales and captions; one moderate leader/label defect, dense publication-size gallery and light/low-contrast screenshot text |
| Manual and milestone continuity | 18/20 | Required structure and comparison components present; T15 omission in main paper and promised holdouts remain unexecuted despite honest disclosure |
| Scientific rigor and anti-overclaiming | 14/15 | Strong inferential caveats; failed support and unverified exchangeability necessarily constrain strength of experimental conclusions |

These are professor-style judgment scores, not a prediction of an instructor's exact rubric. If the moderate visual and T15 disclosure findings are fixed and verified, suggested scores become 28/30 and 18.5/20 respectively. Do not award full continuity marks merely because omitted experiments are disclosed.

## Moderate findings requiring correction

1. **Figure 3C, paper p.5: leader lines cross the numbered style-key region.** The leader toward key 8 traverses the lower key 3 region; other long leaders cross one another. The two-row keyed placement makes tracing points needlessly ambiguous at printed size. Evidence: `final_audit_work/visual_crops/fig3c.png`; generating placement is `m4_final/release/src/regenerate_figures.py` in `baselines()`, the `ari.annotate` call. The labels are distinct text rows, but a blanket zero-annotation-occlusion pass is unjustified. Put keys in an external dedicated keyed strip, use a short disambiguated label layout, or enlarge this panel with collision-checked leaders. Verify the final rendered panel after correction.

2. **Optional equal-encoding retraining (T15) is not explicitly disclosed as unrun in the paper.** `m4_final/release/README.md:91` says it was not run; `results/changes.csv` records no equal-encoding retraining in this round. The manuscript explains frozen-probe recompression carefully, but never names the omitted retraining experiment. The user's requested continuity audit expressly calls for unrun holdouts/T15 disclosure in the paper. Add a sentence to III-D or VII-B that T15 was not run and frozen-probe equal-transformation tests do not replace controlled retraining. This is a requested completeness defect, not evidence of a false experimental claim.

## Minor remaining observations

- **Figure 11, paper p.11:** The eight-row, five-column gallery uses approximately 4-5 point plot text at final print width. High-DPI export preserves sharpness but does not cure small physical typography. Aggregate comparisons are readable; row-level inspection requires magnification. A landscape supplement or enlarged individual cases would improve practical legibility.
- **Figure 8, paper p.8:** The linked artwork caption under the screenshot is very light and small. The main plot axes/legend are visible, but the selected-case identifier is poorly legible at print size. Main caption and Table XIII mitigate this; no data occlusion was observed.
- **Figure 5, paper p.6:** Adjacent B/C panel headings are closely spaced. They do not overlap in the inspected rendering, but extra separation would improve scanability.
- **Title, p.1:** The 15-word, three-line title is informative but visually long against the manual's request for a concise title. This is editorial rather than a compliance blocker.

## Module 1: figure-by-figure graphical checks

| Figure/location | Observed result |
|---|---|
| 1 p.2 architecture | Boxes, arrows and text are clear; no clipping/overlap; descriptive and failed-gate branches are honest |
| 2 p.5 dataset/metadata | Count bars start at zero; source identity uses hue plus hatch; count/native-size labels sit above bars; ROC legend is outside data; caption does not infer pixel-probe reliance |
| 3 p.5 probes/clustering | Position and interval marks support quantitative comparison; model markers/linestyles are redundant; legends outside data; insets are disclosed; C keyed leaders need correction as above |
| 4 p.6 H-C atlas | Ten styles use named facets and shared axes rather than an ordinal color ramp; Human/LD use hue and circle/square identity; ellipse and contour legend is below plots; arrows intentionally connect centroids; no ellipse clipping found |
| 5 p.6 PCA/t-SNE/fidelity | Full PCA and labeled zoom are separate; equal-coordinate PCA aspect retained; hollow t-SNE markers expose origins; fidelity zoom explicit; intervals correctly called seed ranges rather than confidence intervals |
| 6 p.7 FFT/Haar | Explicit log-scale labels; Haar intervals visible around small open markers; three origins use color/shape/line redundancy; legend below data |
| 7 p.7 heatmaps | Position in matrix identifies nominal style/family; sequential grayscale for nonnegative W1; diverging signed map is exactly symmetric in source (`vmin=-lim`, `vmax=lim`); numeric cell values and contrasting text retained; 1.013 lies within 1.05 W1 bound |
| 8 p.8 dashboard | Two-origin color and shape mapping retained; labels and legend outside data; no nominal luminance ramp; selected-case caption too faint/small |
| 9 p.10 ablations | Forest intervals, zero-reference lines, no bars on truncated axes; saturation axis explicitly marked zoom and retains whiskers; crop bars start at zero and labels sit above bars; Lab gray, HSV brown, combined magenta |
| 10 p.11 stress tests | Separate AUROC/silhouette/rank panels avoid dual-axis ambiguity; AUROC confidence intervals visible; originals treated as reference; no invented uncertainty on descriptive silhouette/rank values |
| 11 p.11 gallery | Every FFT row uses same 0.0001-1 logarithmic y-range, every Haar row 0.00001-0.1; color bars share 0-1 x-range; N/A is explicit; no title/bar/axis annotation overlap observed, but typography very small |
| S1 supplementary p.S1 | Human/LD violin+jitter and ECDF views clear; hue/shape/line redundancy; raw units and KS D shown; development-based selection and descriptive status plainly disclosed |

The locked map in current `results/color_map.json` is Human `#2563EB`, LD `#F97316`, SD `#8458B3`. Purple SD is authorized; the prompt's teal was an example. Orange is not reused for Lab. The static source reserves origin hues; model and color-representation palettes use different categories. Identity survives grayscale through hatch/marker/line redundancy, although dense transparent scatter cannot make every coincident point individually legible. No simulated color-vision-deficiency perceptual study was performed; do not equate redundant coding with tested universal colorblind accessibility.

Tables use fixed decimals including tiny signed endpoints, clear column headers, and no observed 'remain in the released CSV' placeholders. No unlabeled truncated bar baselines or causal chart titles were found. Purposeful centroid arrows and contours inherently cross the clouds they describe; this is not a legend-occlusion defect.

## Module 2: exact continuity/manual findings

The actual M4 manual lists fifteen front-matter/body/reference/optional-appendix components. The current twelve-page paper contains them in the prescribed reading order: title/authors, Abstract, keywords, Introduction, Related Work, Proposed Methodology, Experimental Setup, Results, Comparison, Ablation, Discussion, Conclusion, Declarations, References, Appendix. The abstract is one paragraph of 180 whitespace-delimited LaTeX-source words, within the 150-250 word band, and contains actual cohort, AUROC, F1, contrast-count and perturbation metrics. Six keyword phrases and five contribution bullets appear.

Section VI has all five requested comparison components with explicit subsection headings: summary table, quantitative side-by-side table, methodological differences, absolute/relative differences, fairness/limitations. Table IX lists all ten designated base studies and author/year/problem/method/dataset/metric/result/limitation columns. Table X stars source-reported numbers. Both absolute and relative losses against ResNet-50 and DINOv2 are stated. Different AP/F1/localization tasks are not falsely subtracted from AUROC. No external base method was reimplemented, so the strict ideal of same-setting base-paper reproduction remains unmet; the manuscript is honest about this and should receive partial rather than perfect experimental-comparison credit.

Actual M2 evidence prevents three false accusations: M2 PDF p.7 Step 3 explicitly specifies four nonoverlapping 128-square quadrants; p.8 Step 4 calls 0.05 a starting saturation cutoff and requires development calibration; p.8 Step 5 explicitly makes Human-LD the native primary comparison and resized SD descriptive. Therefore quadrant tiling, calibrated 0.01 and SD side-analysis are consistent with the actual plan. These are not violations to invent from an imagined prior plan.

Actual M1's temporal/art-intention/semantic-independence wording was narrowed by actual M2 before implementation. M4 p.1 explains the temporal refinement; p.9 disclaims chronology, aesthetic intention, semantic/material labels and faithful/useful explanations. M3 already described the same core 185,015/45,000/30,000 cohorts, 104 predictors, 0.9824 AUROC, 542 exploratory passes and JPEG50 0.6819. M4 p.4 labels additional intervals, grouped repartitions and metadata summaries as later summaries from the same caches. This is continuity with disclosed additions, not fabrication.

Separate artist/style/generator holdouts, GAN comparison, broad generator error gallery and subject matching were not completed. M4 pp.3-4 and p.9 explicitly disclose this. Omission of promised experiments remains a scope limitation even when honestly acknowledged. T15 main-paper disclosure remains the corrective item above. Names/department/supervisor follow current author confirmation; older M1 'Azka Atif' spelling is not grounds to override confirmed 'Azka Atiq'. No standalone roll-number line appears in the title block; institution-issued email addresses remain present as required contact information.

## Module 4: scientific honesty and inferential boundaries

No critical causal overclaim was found. P.2 explicitly says prior JPEG-bias results do not prove the present pixel probes exploit JPEG associations. Figure 2 caption and p.9 distinguish metadata discrimination from pixel-model reliance. P.9 states that zero confirmations means zero eligible cells, not accepted nulls, zero true effects or complete JPEG mediation. The ordinal/JPEG mechanism is labeled an untested hypothesis. Equal recompression is expressly said not to establish original common support or restore subject correspondence.

G1 is limited to implemented inspectability/fidelity, with explanation faithfulness and human usefulness untested. G2 is descriptive, not temporal. G3 remains unestablished under verified controls and is presented as a negative validity audit consistent with encoding leakage. Whole-group permutations do not establish exchangeability; bootstrap intervals condition on frozen fits, silhouette uncertainty on cached geometry, and seed sensitivities are not full replications. These qualifications are substantive and consistent with the evidence limits.

Residual scientific limitations are real: no verified subject matching, no encoding overlap, uncertain AI group semantics, conditional rather than full-pipeline uncertainty, low PCA2 neighborhood trustworthiness, no generalization holdouts and no user study. They limit the strength of the research outcome, but truthful limitations should not be converted into allegations of fabricated inference.

## Scope of independent conclusion

No critical defect was found in the assigned modules. Two moderate corrections are required before claiming all requested checks pass. This report records the pre-correction state; final verification must inspect the patched PDF and updated DOCX/package separately.

## First correction review

Independently inspected `final_audit_work/renders/patched_page05.png` at 300 DPI. Splitting Figure 3C into aligned silhouette/ARI strips removes the crossing leaders. However, the first replacement remains **moderately defective**: C1's ten y-axis style-key labels overlap vertically, and C2's x-axis tick labels `0.000` and `0.002` run together. Do not claim zero label overlap for this version. The top row needs more physical height or smaller key text, and C2 needs fewer/shorter ticks.

The new Section VII-B source sentence states, 'No equal-encoding retraining was run; stress tests retain the original fitted probe.' This resolves the requested unrun-retraining disclosure; the literal internal code T15 is unnecessary when the omitted experiment is plainly named. Continuity score is therefore revised to **18.5/20**. DAV remains **27/30** until replacement C labels are legible without occlusion; scientific rigor stays **14/15**.

## Second correction review and final assigned-module scores

Independently inspected the updated `final_round/figures/fig07_baseline_probes_and_ari.png` asset. C1 retains all ten style rows while displaying alternate row keys 2/4/6/8/10; C2 retains the matching row order and shows short separated ticks `0` and `.0034`. Both strips are free of leader lines and observed label/data occlusion. The full ten-style identity is retained through row order, provided the final caption explicitly says that all ten rows run top-to-bottom in B1 order. The previous moderate graphical defect is resolved in this asset; re-embedding and final PDF/package propagation remain the parent audit's responsibility.

**Final scores for the assigned modules: DAV 28/30; manual/cross-milestone continuity 18.5/20; scientific rigor 14/15 (subtotal 60.5/65).** No unresolved critical or moderate defect remains in these assigned modules after the checked corrections. The minor typography/contrast observations and substantive experimental limitations above remain; these prevent perfect scores. Repository/package findings are outside this sub-audit and must be integrated independently.
