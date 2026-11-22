# Fresh scientific review

Review of the revised LaTeX, bibliography, table CSVs, appendix, original metric CSVs, and new statistical outputs against Milestone4_Fix_Prompt.md and the course rubric. This is an independent agent review; it is not a Claude, institutional, or human review. No manuscript or original outputs were edited. Encoder repartition refits were in progress; their interim three-model summary is deliberately not assessed as final. Visual rendering is outside this review.

## Required substantive corrections

1. **High — qualify the ARI claim by representation.** `latex/main.tex`, Held-Out Probe Evaluation, says unlabeled ARI has maximum 0.0034. `results/origin_silhouette_ari.csv` contains H–C ARI 0.5419137143 for realism (and several other substantial H–C ARIs). The 0.0034063381 maximum applies full/PCA spaces. Replace with: “In the full standardized and PCA spaces, unlabeled ARI is at most 0.0034 after rounding.” Preserve the distinction from supervised ranking.

2. **High — replace hardcoded numerical literature references.** Tables 1 and 7 contain literal `[1]` through `[16]`, inherited from the previous ordering. New first use is p1,p3,p2,p11,p16,..., so `[2] Complexity–entropy` incorrectly points to B-Free and many later labels are wrong. Generate table references with `\cite{pN}` and regenerate relevant CSV/crosswalk presentation consistently. Preserve manuscript years explicitly as version years; do not silently substitute publication years for the evidence version.

3. **Medium — state the actual scope of the five repartitions.** `compute_statistics.py` reuses `features_matched.parquet` with seed-42 development-calibrated feature-extraction thresholds. It refits imputation, scaling, C and F1 threshold within each repartition, but does not rerun feature calibration. Add: “Feature-extraction thresholds remain fixed from the original seed-42 development partition; preprocessing and probes are refitted.” This makes the split-sensitivity interpretation accurate without requiring a new extraction pipeline.

4. **Medium — repair references to missing appendix evidence.** Main text says overlapping-trigger error-rate gaps and group intervals are “retained in the appendix,” but the current `appendix_evidence.tex` includes none; it says they are supplied with the release. Point directly to the released `failure_trigger_associations.csv` (or include the actual table). Likewise the “supplementary change table” is not included by the current LaTeX inputs, although `tables/changes.tex` exists. Name its released artifact accurately or include/cite it.

5. **Medium — remove ambiguous reproduction wording in Table 8.** All five executed probes are labeled “Reimplemented frozen evaluation”; nearby text correctly says they reproduce none of SCADET/SPAI/B-Free. Replace that cell with “Implemented logistic probe” to avoid suggesting a faithful baseline-paper reproduction.

## Smaller editorial corrections / completion checks

- **Low:** Table 10 prints JPEG-95 upper delta bound as `-0.0000`, although the source is -0.000035200897. Use scientific notation or more digits so the nonzero negative bound remains clear. Five-crop Table 9 similarly rounds a small positive bound (+0.0000427419014) to +0.0000; preserve it if discussing exclusion of zero.
- **Low:** “Permutation entropy ... uses stable row-major ranking ... yields ...” is grammatically broken; use “Stable row-major ranking ... yields ...” after introducing permutation entropy.
- **Low:** `references.bib` SciPy author list contains `Paul and  and Vijaykumar`; remove the empty author token. `p16` has Crossref family/given names in an unusual order; verify the PDF's author display before reversing any names (this review does not establish a correction).
- Confirm the supervisor spelling and actual AI-tool list with the authors as a pending action; current declarations still assert Ms. Azka Atiq and four named tools. Do not claim those were author-confirmed merely from inherited text.
- Update the final five-model seed table/protocol when encoder refits finish. No finding here treats the interim three-model seed summary as a scientific inconsistency.

## Checks that passed

- Primary AUROC/F1, ECE and tuning settings in Table 4 agree with `results/baseline_metrics.csv`; new AUROC/F1 bounds match `m4_final/results/baseline_group_ci.csv` to displayed precision.
- All three paired AUROC differences and intervals agree with `paired_probe_differences.csv`: +0.2985 [0.2812,0.3176], -0.0175 [-0.0216,-0.0140], -0.0173 [-0.0213,-0.0138].
- Quoted ablation, JPEG/resize and projection metrics match their original CSVs. Relative differences use correct denominators and are expressly cross-protocol rather than verified improvements.
- Negative inference is preserved in abstract, discussion and conclusion: metadata AUROC 1.0000, zero eligible confirmations, missing subject/common-encoding support, and stronger ResNet-50/DINOv2 ranking. No claim that metadata causally explains all pixel-model performance was found.
- Conditional bootstrap limitations, unverified randomization exchangeability, descriptive H–C shifts, lack of independent replication and user-study limitations are explicit.
- Regex citation audit across main/table/appendix text found no missing or uncited bibliography entries, including the bibliography-control entry. This does not detect the literal-number error above. Abstract has 181 whitespace-delimited words, within 150–250.
- No milestone-number wording or claim of external/human review remains in the inspected manuscript body. Process language is substantially cleaner; promised-but-unrun protocols remain honestly disclosed.
