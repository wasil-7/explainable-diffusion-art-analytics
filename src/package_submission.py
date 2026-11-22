"""Assemble an allowlisted lightweight GCR package without moving original working files."""
from common import *
import shutil,zipfile,hashlib,ast,re,importlib.metadata
from build_submission import NAME,DEST,prose

PACKAGE=ROOT/'GCR_Submission'/NAME
def main():
    PACKAGE.mkdir(parents=True,exist_ok=True)
    for p in [PACKAGE/'src',PACKAGE/'tests',PACKAGE/'results/gallery',PACKAGE/'figures']:p.mkdir(exist_ok=True,parents=True)
    (PACKAGE/'.streamlit').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'.streamlit/config.toml',PACKAGE/'.streamlit/config.toml')
    for suffix in ['.docx','.pdf']:
        shutil.copy2(DEST/(NAME+suffix),PACKAGE/(NAME+suffix));shutil.copy2(DEST/(NAME+suffix),ROOT/(NAME+suffix))
    for folder in ['src','tests']:
        for src in (ROOT/folder).glob('*.py'):shutil.copy2(src,PACKAGE/folder/src.name)
    for src in (DEST/'figures').glob('*.png'):
        if not re.search(r'(gallery|heatmap)_[12]\.png$',src.name):shutil.copy2(src,PACKAGE/'figures'/src.name)
    for src in (ROOT/'figures').glob('dashboard_*.png'):shutil.copy2(src,PACKAGE/'figures'/src.name)
    excluded_prefixes=('predictions_','pr_','roc_','validation_tuning_')
    special={'pca_plot_points.csv','hc_plot_points.csv','tsne_plot_points.csv'}|{f'{kind}_{model}.csv' for kind in ['pr','roc'] for model in ['handcrafted','frequency','metadata_gated','resnet50','dinov2']}
    included=[]
    for src in OUT.iterdir():
        if not src.is_file() or src.suffix not in ['.csv','.json']:continue
        if src.name in special or (src.stat().st_size<500000 and not src.name.startswith(excluded_prefixes) and src.name not in ['embedding_ids.csv','failure_trigger_flags.csv','drift_test_ids.csv','tsne_sample_manifest.csv','stage10_artifact_inventory.csv']):
            shutil.copy2(src,PACKAGE/'results'/src.name);included.append(src.name)
    for src in (OUT/'gallery').glob('*.png'):shutil.copy2(src,PACKAGE/'results/gallery'/src.name)
    for src in DEST.glob('table_*.csv'):shutil.copy2(src,PACKAGE/'results'/('submission_'+src.name))
    for name in ['submission_report_manifest.json','heatmap_pixel_provenance.json']:
        shutil.copy2(DEST/name,PACKAGE/'results'/name)
    runtime=ROOT/'phase3_output/ui_upgrade/compact_runtime_verification.json'
    if runtime.exists():shutil.copy2(runtime,PACKAGE/'results/compact_runtime_verification.json')
    # A compact, supported read-only dashboard works from the included CSVs and eight real gallery images.
    readme='''# Explainable Visual Analytics of Human and Diffusion Artwork

**Milestone 3 — Wasil Kayani (24I-2551), Umar Asghar (24I-2532), DSB.**

The report implements the twelve Milestone2 steps and all seven Phase3 rubric components. It audits185,015 files and evaluates a frozen30,000-image native256 Human–LD cohort, with6,000 held-out artworks. Handcrafted AUROC is0.9824, ResNet-50 is0.9999, DINOv2 is0.9997, and metadata is1.0000. The Step5 gate discovers origin-aligned JPEG encoding and unavailable verified subject matches:542 exploratory passes are **not confirmed diffusion-origin effects**. Zero cells are eligible for confirmation.

## Contents and provenance

The PDF and editable Word report contain13 numbered tables and12 numbered figures. `figures/` contains300-DPI composites, architecture and an actual dashboard capture. `results/` contains native-precision summary tables,18 curated claims across16 unique papers, and eight actual held-out gallery artworks with quadrants. `submission_table_*.csv` reproduces every report table. `submission_inventory.json` records package hashes. `src/` and `tests/` retain the complete Python source set.

## Setup and immediate dashboard use

Python3.12 is the recorded environment. From this directory:

```powershell
$env:PIP_CACHE_DIR='D:\\Dev\\pip_cache'
$env:TEMP='D:\\Dev\\tmp'
& 'D:\\Dev\\envs\\dav_phase3\\python.exe' -m pip install -r requirements.txt
& 'D:\\Dev\\envs\\dav_phase3\\python.exe' -m streamlit run src/dashboard.py
```

On a separate machine, substitute your Python3.12 executable and writable cache/temp directories. The existing Windows environment already has the scientific dependencies. Requirements pin the versions recorded for this experiment; GPU libraries are optional for browsing the supplied results and installed separately below.

Filter movements/origins, switch H–C/PCA/t-SNE, and select raw points or hexagonal counts. All6,000 primary points and3,000 t-SNE points are included. The compact edition explicitly limits pixel/feature drill-down to the eight Forensic cases because the185,015-image dataset and full feature caches are excluded. All baseline, drift, ablation, figure and literature views use included summary data. Original full-workspace behavior is retained when caches and images are available; a blocked Parquet dependency falls back visibly to the compact edition.

## Tests and full experimental reproduction

```powershell
& 'D:\\Dev\\envs\\dav_phase3\\python.exe' tests/test_features.py
& 'D:\\Dev\\envs\\dav_phase3\\python.exe' tests/test_drift.py
& 'D:\\Dev\\envs\\dav_phase3\\python.exe' src/verify_dashboard.py
```

Tests execute synchronously; wait for each exit code. Original verification scripts can write summary artifacts under results/. A full numerical rerun requires the original dataset at `data/archive/Real_AI_SD_LD_Dataset/`, frozen Parquet/NumPy caches and fitted models. Those are intentionally excluded from this lightweight submission and remain in the authors’ original workspace. Restore them without changing IDs or feature definitions, then run `src/verify_stage10.py`. `src/run_checkpoint.py` covers Stages0–5; `src/run_stage10.py` covers6–10. Running from raw data also requires collected Phase1/Phase2 PDFs and their source metadata for literature extraction. Those third-party PDFs are not redistributed here.

For CUDA12.4 reproduction, install the recorded pair separately using the official wheel index:

```powershell
& 'D:\\Dev\\envs\\dav_phase3\\python.exe' -m pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124
```

Both encoders stay frozen; embedding inference uses CUDA FP16 on four224-pixel quadrant views. Exact settings, group-bootstrap scope, randomization restrictions, timings and manifest hash are recorded in JSON artifacts and AppendixA. The historical report builders require the original milestone PDFs and full working tree. The final portrait builder is `src/build_submission.py`; `src/submission_assets.py` creates portrait figures from cached rendering inputs. Native Word PDF export is used in the original Windows workspace. No source claims, data splits or model fits were changed for report formatting.

## Interpretation limits

This is release discrimination and descriptive within-style distribution analysis. It is not a causal diffusion-origin estimate, temporal-art-history experiment, unseen-generator benchmark or human evaluation of dashboard usefulness. Exact encoding controls and verified subject links are absent. Equal JPEG recompression cannot restore them. AP, AUROC, joint F1, attribution accuracy and chart-issue identification in the literature table are kept distinct. See report Tables1,2,9 and12 for cross-milestone promises, changes, comparison limits and verdicts.
'''
    chunks=readme.split('```')
    for i in range(0,len(chunks),2):
        chunks[i]=prose(chunks[i])
        chunks[i]=re.sub(r'\b(audits|contain|contains|four|Tables|Stages)(?=\d)',r'\1 ',chunks[i])
        chunks[i]=chunks[i].replace('AppendixA','Appendix A')
    readme='```'.join(chunks)
    screenshots='''## Dashboard screenshots

### Overview & Landing

An interactive executive summary, live artwork inspector and links into the analysis.

![Overview and landing page](figures/dashboard_landing.png)

### Interactive H–C Atlas

Filter movements and origins, select an artwork, and inspect its measured features. All comparisons remain descriptive because the subject and JPEG controls are unresolved.

![Interactive entropy–complexity atlas](figures/dashboard_atlas.png)

The six navigation views cover the overview, H–C atlas, manifold fidelity, spectral profiles, drift/ablations and forensic gallery. The overview's expandable evidence section retains baseline metrics and literature downloads. The `.streamlit/config.toml` theme travels with the package; launch Streamlit from this directory. Google Fonts supplies Quicksand and Titan One, with local sans-serif fallbacks when offline.

'''
    readme=readme.replace('## Contents and provenance',screenshots+'## Contents and provenance')
    readme=readme.replace('The final portrait builder is `src/build_submission.py`','Run `python src/build_report.py --submission` for the final portrait builder (`src/build_submission.py`)')
    (PACKAGE/'README.md').write_text(readme,encoding='utf-8')
    root_readme=ROOT/'README.md'
    if root_readme.exists():
        current=root_readme.read_text(encoding='utf-8')
        marker='<!-- dashboard-screenshots -->'
        current=re.sub(r'<!-- dashboard-screenshots -->.*?<!-- /dashboard-screenshots -->','',current,flags=re.S).rstrip()
        root_readme.write_text(current+'\n\n'+marker+'\n'+screenshots+'<!-- /dashboard-screenshots -->\n',encoding='utf-8')
    else:root_readme.write_text(readme,encoding='utf-8')
    packages=['numpy','pandas','scipy','scikit-learn','matplotlib','seaborn','pillow','PyWavelets','ImageHash','fastparquet','joblib','streamlit','plotly','python-docx','pymupdf','psutil','tqdm','timm','safetensors','huggingface-hub','playwright']
    lines=['# Recorded Python 3.12 environment; CUDA torch/torchvision installation is documented in README.']
    for name in packages:
        try:lines.append(name+'=='+importlib.metadata.version(name))
        except importlib.metadata.PackageNotFoundError:pass
    (PACKAGE/'requirements.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    guide=['# Private demo guide for Wasil','This file is intentionally excluded from the submission and ignored by Git.','## Launch','Use the fixed Python and PIP_CACHE_DIR/TEMP environment from the submission README. Run `python -m streamlit run src/dashboard.py` in the original workspace; the clean package also supports a compact edition.','## Three-minute demonstration','0:00–0:30: State the within-style question and show Step5: native256 is controlled, but subjects/JPEG are not.','0:30–1:00: Filter a movement in H–C, switch PCA/t-SNE, explain T(15), and show raw versus hexagonal counts.','1:00–1:30: Open Baseline probes:0.9824 handcrafted, near-perfect encoders, metadata1.0000. Explain release discrimination versus attribution.','1:30–2:00: Show drift heatmap:542 exploratory passes, zero eligible confirmations. BH and bootstraps do not fix confounding.','2:00–2:30: Open Forensic cases and point to actual quadrants, FFT/Haar/color evidence. Explain eight selected cases are not prevalence estimates.','2:30–3:00: Show JPEG50 AUC0.6819, ordinal-removalΔ−0.0744; conclude G1 implemented, G2 descriptive, G3 unresolved.','## Viva answers','Why zero confirmed? No verified subject matching or JPEG common support; the prespecified statistical rule cannot override eligibility.','Did JPEG cause all predictive performance? Not identified. Metadata perfection shows an available shortcut, not its causal share in pixel models.','Why not temporal drift? Milestone2 explicitly narrowed Milestone1 to within-style distribution differences; no creation-year control.','Is the dataset fully processed? All185,015 files audited;45,000 features/encoders;30,000 primary;6,000 test.','What was not run? Separate artist/style/generator holdouts, semantic/material annotation, dashboard user study, end-to-end encoder training.','How is the light package reproducible? Summaries, source, gallery and compact dashboard run directly; full numeric reruns require preserved raw data/caches.','## Every source script']
    for p in sorted((ROOT/'src').glob('*.py')):
        tree=ast.parse(p.read_text(encoding='utf-8-sig'));desc=ast.get_docstring(tree) or 'Shared implementation module; see entry points and call sites.'
        artifacts=sorted(set(re.findall(r'[A-Za-z0-9_]+\.(?:csv|json|parquet|npy|npz|png|docx|pdf)',p.read_text(encoding='utf-8-sig'))))
        guide.append(f'- `{p.relative_to(ROOT)}` — {desc.splitlines()[0]} Outputs/inputs: '+', '.join('`'+a+'`' for a in artifacts))
    guide+=['## Every chart and result table','Original figures remain under figures/ and results/. Portrait counterparts live under phase3_output/submission_build/figures/ and the clean package. Report tables1–13 are mapped in submission_report_manifest.json.']
    for p in sorted((ROOT/'figures').glob('*.png')):guide.append('- `'+str(p.relative_to(ROOT))+'`')
    for p in sorted(OUT.glob('*.csv')):guide.append('- `'+str(p.relative_to(ROOT))+'`'+(' — included summary' if p.name in included else ' — full-workspace artifact'))
    (ROOT/'DEMO_GUIDE_FOR_WASIL.md').write_text('\n\n'.join(guide),encoding='utf-8')
    (ROOT/'.gitignore').write_text('/*\n!/GCR_Submission/\n/GCR_Submission/*\n!/GCR_Submission/'+NAME+'/\n!/GCR_Submission/'+NAME+'/**\n**/__pycache__/\n**/*.pyc\n/DEMO_GUIDE_FOR_WASIL.md\n',encoding='utf-8')
    inventory=[]
    for p in sorted(PACKAGE.rglob('*')):
        if p.is_file() and p.name!='submission_inventory.json':inventory.append({'path':p.relative_to(PACKAGE).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (PACKAGE/'results/submission_inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
    total=sum(p.stat().st_size for p in PACKAGE.rglob('*') if p.is_file())
    assert total<30_000_000,('Uncompressed package exceeds30MB',total)
    zip_path=PACKAGE.parent/(NAME+'.zip')
    with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(PACKAGE.rglob('*')):
            if p.is_file():z.write(p,str(p.relative_to(PACKAGE.parent)))
    assert zip_path.stat().st_size<30_000_000
    print('Package bytes',total,'ZIP bytes',zip_path.stat().st_size,'files',len(inventory)+1,flush=True)
if __name__=='__main__':main()
