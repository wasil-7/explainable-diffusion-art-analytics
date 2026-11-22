# Explainable visual analytics of diffusion artwork

This project measures Human and diffusion artwork in AI-ArtBench using named ordinal, frequency, wavelet and color descriptors, grouped prediction probes and linked visual diagnostics. The exhaustive audit covers 185,015 images; the primary native-256 Human/Latent Diffusion cohort contains 30,000 artworks with 6,000 held-out test cases.

Strong release-origin prediction does not establish independent origin attribution. JPEG encoding is origin-aligned and verified subject matches are unavailable. All 542 exploratory passes among 1,040 feature/style comparisons therefore remain unconfirmed.

Official repository: https://github.com/wasil-7/explainable-diffusion-art-analytics

## Results

| Probe | Test AUROC | Test F1 |
|---|---:|---:|
| Handcrafted, 104 predictors | 0.9824 | 0.9420 |
| FFT-only | 0.6839 | 0.6830 |
| Metadata diagnostic | 1.0000 | 0.9997 |
| Frozen ResNet-50 | 0.9999 | 0.9972 |
| Frozen DINOv2 | 0.9997 | 0.9955 |

The encoders outperform the handcrafted probe. Intervals condition on frozen fits and recorded source groups. Five supplementary repartitions reuse the selected cohort, original extraction calibration and cached vectors; they are not five full independent replications.

![Held-out probe evaluation](figures/fig07_baseline_probes_and_ari.png)

![Descriptive style-feature shifts](figures/fig05_style_drift_heatmap.png)

## Dashboard

Six linked views connect the overview, H–C atlas, projections, spectra, drift and gallery. The compact package contains all plotted summaries and eight pixel-inspectable cases; arbitrary-artwork inspection requires local images and caches. The interface has not undergone a user study or explanation-faithfulness evaluation.

![Dashboard overview](figures/dashboard_landing.png)

![Artwork atlas](figures/dashboard_atlas.png)

Using the recorded Python environment:

```sh
python -m streamlit run src/dashboard.py
```

## Paper and editable source

`paper/paper.pdf` is the twelve-page IEEE manuscript. `paper/paper.docx` is a native editable Word counterpart with separate pagination. `paper/supplementary.pdf` contains S1. The complete editable LaTeX source is in `paper/latex_source/`.

From that source folder, the same command works in Windows PowerShell, macOS Terminal or a Linux shell when Tectonic is installed:

```sh
tectonic -X compile --keep-logs main.tex
```

The first build may download TeX packages. Building the paper requires no image archive, GPU or trained model. See [BUILD.md](BUILD.md) for the tested toolchain.

## Reproduction

[REPRODUCIBILITY.md](REPRODUCIBILITY.md) maps commands, cache prerequisites and output files. `requirements.txt` and `environment.yml` record the original environment. The experiments used a local CUDA-enabled GTX 1650 SUPER, not a hosted notebook. A fresh-machine full experimental replication is not claimed.

Frozen split IDs and their hashes are in `splits/`; measurements, predictions and summaries are in `results/` and `analysis/results/`. Raw AI-ArtBench images, encoder weights and large caches are excluded. Obtain the dataset from https://www.kaggle.com/datasets/ravidussilva/real-ai-art ; its Human source is ArtBench-10, https://github.com/liaopeiyuan/artbench .

Before a complete empirical rerun, use a separate working copy and follow the clean-state preparation instructions. Retaining completion flags without the excluded arrays/models can skip required work. Existing mathematical tests and CSV-only figure rendering can be run with:

```sh
python -m pytest tests/ -q -p no:cacheprovider
python src/regenerate_figures.py
```

On the original Windows host, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` avoids an unrelated blocked optional plugin. See the reproduction guide for the exact original-host environment settings. Tests verify mathematical invariants, not causal attribution.

## Repository layout

- `src/`, `tests/`: implementation and mathematical tests.
- `results/`, `analysis/`, `splits/`: lightweight experimental evidence and frozen IDs.
- `figures/`, `paper/`: presentation assets, manuscript and editable source.
- `milestones/`: earlier submitted research documents, retained as historical versions.
- `audit/`: verification receipts and review history; these are excluded from the instructor-facing GCR package.

The current print-readability assessment is [audit/PRINT_READABILITY_AUDIT.md](audit/PRINT_READABILITY_AUDIT.md). It is a bounded review, not an institutional originality certificate or a guaranteed course grade. Cite this work using `CITATION.cff`; underlying datasets and methods retain their own citations and terms.
