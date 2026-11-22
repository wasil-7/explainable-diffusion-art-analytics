# Editable source and build record

The authoritative manuscript is plain-text `main.tex`, with editable `references.bib`, thirteen table CSV/template/wrapper sets, relative figure assets, IEEEtran class/style files, and the two appendix/derived-text includes. No page-image PDF imitation is used.

From this folder, with Tectonic 0.17.0 installed, run one command:

```powershell
tectonic -X compile --keep-logs main.tex
```

The first run may download TeX packages. This exact command is tested from a separate clean source directory. Paper compilation needs no archive, GPU, model weights or feature caches. Fonts are embedded. Legacy class/font warnings are permitted; undefined references/citations, errors and overfull boxes are not.

To rebuild table cells from CSV without experiments:

```powershell
python rebuild_tables.py
tectonic -X compile --keep-logs main.tex
```

The original workstation uses `D:\Dev\envs\dav_phase3\python.exe`, `PIP_CACHE_DIR=D:\Dev\pip_cache`, and `TEMP=D:\Dev\tmp`. The clean compile and CSV regeneration are tested; a fresh-environment complete image/encoder rerun is not claimed. `paper.docx` is an optional native editable single-column counterpart with separate pagination; the twelve-page IEEE PDF is the submission-layout authority.
