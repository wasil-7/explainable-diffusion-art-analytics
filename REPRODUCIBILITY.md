# Reproduction command and output map

The supplied CSVs, manifests and figure/gallery assets suffice to rebuild the document and plots. The original archive, extracted feature arrays, encoder vectors and fitted model caches are excluded. They must be recreated or supplied before cache-dependent empirical stages. The commands below are documented entry points, not a claim of a fresh end-to-end rerun in this editorial round. Use an isolated working copy: several original stages overwrite results and update PROGRESS.md.

The fixed original cohort hash is `e27a00766ad8825201aac6d4167a5a98b319d5b18b136ffb20d5765073472936`. `splits/` contains original grouped IDs; the consistency replay in `audit/final_round/final_checks.json` checks source-group disjointness, cohort membership and published split counts without retuning a model. Do not substitute a new split for a failed frozen-manifest check.

## Environment

On the original workstation:

```powershell
$env:PIP_CACHE_DIR='D:\Dev\pip_cache'
$env:TEMP='D:\Dev\tmp'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
$py='D:\Dev\envs\dav_phase3\python.exe'
```

On another workstation, install the pinned requirements in a Python 3.12 environment and set `$py` to that interpreter. The recorded native-library host restrictions and unrecorded original cuDNN version prevent claiming a fully specified fresh-machine replication. No blocked native binary is bypassed.

## Prepare an isolated empirical-rerun copy

Start by copying the release into a separate reproduction working directory. Preserve the delivered package untouched. The release intentionally supplies metrics/completion JSONs but excludes large embedding arrays and fitted model files. Existing baselines skip on metrics JSON, and encoder extraction trusts completion state: **do not pair retained completion flags with missing caches**. Archive existing derived results and create clean output folders before any empirical command:

```powershell
& $py analysis/prepare_clean_rerun.py --confirm-working-copy
```

Run this only inside that isolated copy. The helper checks the repository root, moves `results/` and `analysis/results/` under a timestamped `reproduction_before/` folder, restores only the required `results/literature_facts.csv`, and leaves the raw archive and supplied frozen `splits/` untouched. It deletes nothing and executes no experiment. It was tested on synthetic filesystem fixtures; no actual empirical evidence was moved by that test. Use existing complete matching caches only if all arrays/models and their state correspond; otherwise this clean preparation is necessary.

## Archive and cache dependent stages, in order

Acquire AI-ArtBench from its cited provider and preserve bytes/relative paths under `data/archive/Real_AI_SD_LD_Dataset/`. `src/common.py` resolves paths from the repository root. The original environment sets its separate Torch cache at `D:\Dev\torch_cache`; ensure the chosen cache exists and encoder weights can be obtained. GPU extraction uses CUDA, not a Kaggle runtime.

| Ordered command from repository root | Required input / principal outputs | Publication evidence |
|---|---|---|
| `& $py src/audit.py` | Original archive; writes batch audit caches, `audit_manifest.parquet`, `audit_counts.csv`, `audit_encoding_counts.csv`, `audit_summary.json` | Table II; Fig. 2 counts |
| `& $py src/inspect_metadata_headers.py` | Original archive; sampled header/text-tag audit, `jpeg_metadata_header_sample.json` | Header-audit scope; not exhaustive absence of comments |
| `& $py src/splits.py` | Audit manifest; duplicate/source-family closure, frozen `cohort_manifest.csv`, split/group counts, `control_gate.json` | Table III, cohort hash and gate limits; compare supplied split IDs |
| `& $py src/extract_features.py` | Frozen manifest plus archive; development calibration, four-quadrant/full/tie feature caches, `features_matched.parquet`, unit-test/calibration summaries | 104 primary versus 169 cached measurements; mathematical features |
| `& $py src/projections.py` | Feature cache; development-fitted PCA and held-out H/C, t-SNE points, fidelity sweeps, loadings/centroid intervals | Table VII; Figs. 4–5 |
| `& $py src/deep.py --prefetch` then `& $py src/deep.py` | Original archive, frozen manifest, CUDA and model weights; embedding IDs, completed states, ResNet/DINOv2 vector caches | Frozen encoder representations, not finetuning |
| `& $py src/baselines.py` | Feature and embedding caches; selected C/threshold, predictions/ROC/PR, full and per-style metrics, metadata controls | Table IV points, Fig. 2 metadata ROC, Fig. 3 curves |
| `& $py src/drift.py` | Frozen features and source groups; 1,040 feature/style comparisons, 10,000 group-label randomizations, group intervals/nulls, style-family summaries, inter-style distances | Table VIII; Figs. 4/7; 542 exploratory and zero eligible confirmations |
| `& $py src/sensitivity_pixels.py` | Archive, frozen primary predictions/features; transformed pixel feature caches | Equal JPEG/resize stress inputs; does not retrain equal-encoding origins |
| `& $py src/ablations.py` | Baseline/feature/perturbation caches; family/color/crop/tie refits, paired sensitivity summaries, mixed-cohort control | Tables XI–XII, Table X mixed F1, baseline per-style intervals; Figs. 3/9–10 |
| `& $py src/border_analysis.py` | Archive/features; border flags, paired supported IDs/drift changes | 369 flags, 76 unsupported, paired 5,924 and 12/23 reversals |
| `& $py src/uncertainty_tables.py` | Existing prediction/sensitivity outputs; group intervals and overlapping failure-trigger association CSVs | `failure_trigger_associations.csv`; descriptive uncertainty |
| `& $py src/visual_tables.py` | Frozen cached features/predictions plus `literature_facts.csv`; distributions, profiles, selected held-out gallery PNGs and comparison CSV | Table XIII; Figs. 6/11/S1; literature claims |
| `& $py src/publication_figures.py` | Cached PCA/tSNE/features; exports current `pca_plot_points.csv`, `hc_plot_points.csv`, `tsne_plot_points.csv` and historical chart layouts | Refreshes final rendering inputs; run `src/regenerate_figures.py` afterward to restore the final audited layouts |
| `& $py analysis/compute_statistics.py` | Frozen feature/embedding caches and predictions; writes `analysis/results/` bootstrap intervals/draws/paired differences and five regrouped probes | Tables IV–VI aggregate/paired intervals and five conditional repartitions; per-style intervals come from ablations.py |

The supplementary-statistics script skips its bootstrap if `analysis/results/baseline_group_ci.csv` already exists and skips seed/model fits already present in `multiseed_metrics.csv`. Re-running a complete supplied release therefore resumes instead of proving new fits. To recompute, preserve the supplied evidence and use a separate working copy with an initially empty `analysis/results/`; this requires all excluded caches above. Original seed-42 feature calibration and cached encoder vectors remain fixed across seeds 43–47. It is conditional split sensitivity, not five full pipeline repetitions.

The published local release mirrors selected manuscript summaries from `analysis/results/` into `results/`. The mixed-cohort F1 is the executed `ab_unmatched_mixed` row of `control_gate_ablation.csv`; JPEG quantization means are recorded in `control_gate.json`/encoding counts. These are cached summaries, not newly collected data. `current_relative_differences.json` divides unrounded baseline point differences by each comparator AUROC.

## Supplied-data rebuilding, without empirical fitting

```powershell
& $py -m pytest tests/ -q -p no:cacheprovider
& $py src/regenerate_figures.py
& $py -m streamlit run src/dashboard.py
```

The first command runs ten data-free mathematical tests. The second draws all eleven static composites from supplied CSVs/gallery assets; it performs no training or inferential analysis. The third opens the six-view dashboard with all plotted summaries and eight inspectable gallery cases. Actual paper screenshot captures are supplied; their linked-pixel subset is not an arbitrary-artwork image archive.

From `paper/latex_source/`:

```powershell
& $py rebuild_tables.py
tectonic -X compile --keep-logs main.tex
```

Every one of the thirteen main tables has a CSV, a layout template and a generated TeX wrapper. Text/literature tables preserve source/version scope; they are not newly computed external-model results. The clean-source and CSV-rebuild compilations are tested against the final PDF text and pixels. `paper/supplementary.pdf` supplies S1, explicitly named in the manuscript. Full environment installation, statistical re-estimation and encoder extraction are not claimed as executed during final polish.

## Publication and institutional checks

The official repository is https://github.com/wasil-7/explainable-diffusion-art-analytics. The authors will push after the local build, then public contents can be verified. No Zenodo DOI is requested or fabricated. Turnitin/iThenticate and any institutional AI-use review must use the final PDF; neither a local overlap screen nor an AI detector supplies a guaranteed plagiarism/AI score. All four author-confirmed tools are declared transparently: Codex, Antigravity, Claude and SciSpace.


## Final forensic audit supersedes earlier publication-status notes

The official public repository is populated at initial release commit `6a6df880abbe8061cd145c41adfccdfe730e045e`. Its live README rendered successfully with all four images loaded. `FINAL_AUDIT.md` is the supplied-request forensic audit, including the independent visual/manual review, numerical checks and packaging findings. This local audited revision fixes Fig.3 label collisions, explicitly discloses unrun equal-encoding retraining, and preserves exact artifact bytes using `.gitattributes`. It must be committed and pushed as an update; it is not falsely described as already online.

Git had normalized research CSV line endings, invalidating byte-level checksum comparisons despite unchanged parsed values. The new `* -text` rule preserves the exact local scientific artifacts. From this prepared Git folder, execute:

```powershell
git add --renormalize .
git add .
git commit -m "Apply final forensic audit fixes and preserve artifact checksums"
git push origin main
```

Do not force-push. A subsequent public-commit check must confirm the audited PDF, source, FINAL_AUDIT.md and checksums. Institutional Turnitin/iThenticate and department-name confirmation remain author actions, not fabricated passes. No new image/model/statistical pipeline was executed for this audit. The current GCR ZIP uses canonical root `paper.pdf`, `paper.docx`, `supplementary.pdf`, `latex_source.zip` and `release/`.
