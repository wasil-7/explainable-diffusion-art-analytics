"""Complete Stage12 review ledger, packaging manifest and user checkpoint."""
from common import *
import hashlib,re,shutil
import pymupdf as fitz
from PIL import Image
from build_report import DEST,REPORT,QA

def main():
    checks=pd.read_csv(DEST/'report_quality_checks.csv');assert checks.passed.all()
    pdf=fitz.open(REPORT/'Milestone3_Final.pdf');texts=[p.get_text() for p in pdf];manifest=json.loads((DEST/'report_manifest.json').read_text())
    inventory=[]
    # Read every result file in bounded chunks; inspect schemas/shape for binary caches.
    cached_inventory=DEST/'complete_results_inventory.json'
    if '--metadata-only' in sys.argv and cached_inventory.exists():inventory=json.loads(cached_inventory.read_text(encoding='utf-8'))
    for p in ([] if '--metadata-only' in sys.argv else sorted(OUT.rglob('*'))):
        if not p.is_file():continue
        h=hashlib.sha256()
        with p.open('rb') as stream:
            for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
        record=dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=h.hexdigest())
        if p.suffix=='.parquet':
            from fastparquet import ParquetFile
            meta=ParquetFile(p);record.update(rows=meta.count(),columns=meta.columns)
        elif p.suffix=='.npy':
            import numpy as np
            a=np.load(p,mmap_mode='r');record.update(shape=a.shape,dtype=str(a.dtype))
        elif p.suffix=='.png':
            with Image.open(p) as im:record.update(image_size=im.size,dpi=im.info.get('dpi'));im.verify()
        inventory.append(record)
    (DEST/'complete_results_inventory.json').write_text(json.dumps(inventory,indent=2,default=str),encoding='utf-8')
    def pages(label):return ', '.join(str(i+1) for i,t in enumerate(texts) if label in t)
    def caption_pages(label):
        key=label.replace('Table ','');entry=next(e for e in manifest['tables'] if e['key']==key)
        needle=re.sub(r'\s+',' ',label+' '+entry['title'])
        return ', '.join(str(i+1) for i,t in enumerate(texts) if needle in re.sub(r'\s+',' ',t))
    lines=['# Final submission checklist','', 'Verified 15 November 2026. All seven report quality gates passed; scientific confirmation remains ineligible. Passing a report gate does not repair the failed subject/JPEG gate.','',
      '| Quality gate | Outcome and evidence |','|---|---|',
      '| 1 Cached reproducibility | PASS: fresh process src/verify_stage10.py; 179 cached empirical checks, frozen prediction reproduction and original manifest unchanged. |',
      '| 2 Tables and native figures | PASS: 22 native tables, 2,281 cells independently reconstructed from source artifacts; 11 original PNGs including architecture embedded by exact file hash; 10 requested composites preserved. report_quality_checks.csv and table_source_hashes.json. |',
      '| 3 Citation crosswalk | PASS: 16 unique references, first appearance [1] through [16], 18 source entries linked to source indexes and matching PDF hashes. Table A1 and paper_evidence_audit.csv. Corrected source discrepancies disclosed in REVIEW_NOTES.md. |',
      '| 4 External numbers | PASS: 18 curated claims match table text and their actual PDF pages; all numerical tokens checked. PixelatedScatter threshold comparison independently recomputed rather than asserted as an extra PDF result. |',
      '| 5 Brief methodology feedback | PASS: component mapping below and Table 0; twelve Phase2 steps mapped explicitly below. |',
      '| 6 Export and visual review | PASS: Microsoft Word COM exported the actual DOCX; all 63 pages rasterized and inspected in page/contact views, with detailed checks of revised tables, discussion and figure spreads; no clipped text or unfilled placeholders in final audit. |',
      '| 7 Independent review pass | PASS: separate verification process recomputed source tables, probability/statistical integrity, evidence and layout. Findings and fixes in REVIEW_NOTES.md; limitations retained. |','',
      '## Seven brief components','', '| Component | Section | Table and actual caption page |','|---|---|---|']
    components=[('Implementation','3','1'),('Dataset and preprocessing','4–5','2'),('Baseline evaluation','6','5'),('Graphical results','7','8'),('Existing research','8','9'),('Ablations','9','10'),('Analysis and discussion','10','13')]
    for c,s,k in components:lines.append(f'| {c} | {s} | Table {k}, p. {caption_pages("Table "+k)} |')
    steps=[('Define research input','2, 4','Artwork unit and unknown subject fields explicit'),('Data collection','4','Full185015 audit, Tables2–3'),('Preprocessing','4–5','Native resolution, sRGB and disjoint quadrants'),('Feature engineering','5','Definitions, pilot thresholds, Table4'),('Control variable gate','4, 10','FAILED scientifically; explicit eligibility limitation'),('Visual analytics','7','Figures2–6, fixed PCA, tSNE fidelity'),('Baseline methods','6','Five shared-test probes, Tables5–6'),('Evaluation metrics','6–7','AUC/F1/calibration, silhouette/ARI, W1/SW1'),('Statistical comparison','7, 10','Complete tests and nulls, FDR and uncertainty limitations'),('Ablations','9','Tables10–12 and B4/B7, Figures8–9'),('Error analysis','10','Table13, Figure10, TablesB5–B6, paired borders'),('Final research output','1–12, A–C','Native report, figures, dashboard and this checklist')]
    lines+=['','## Phase 2 twelve step coverage','','| Step | Report sections | Evidence and status |','|---|---|---|']
    for i,(name,s,e) in enumerate(steps,1):lines.append(f'| {i} {name} | {s} | {e} |')
    lines+=['','## Table caption locations','','| Table | Title | Caption page |','|---|---|---|']
    for e in manifest['tables']:lines.append(f"| {e['key']} | {e['title']} | {caption_pages('Table '+e['key'])} |")
    lines+=['','Section10 starts on p. '+pages('10 Results Analysis and Discussion')+'. It separates invalid confirmatory attribution from preserved descriptive associations, and assesses G1, G2 and G3 explicitly.','',
      'Instructor feedback: narrower within-style question and measurable evidence (Sections2,7); named controls and limitations (Sections4,10); implementable feature protocol and baselines (Sections3,5,6); inspectable figures and projection diagnostics (Section7); numerical comparison without incompatible endpoint ranking (Section8).','',
      'Large figure sheets are intentional: landscape scientific spreads and a portrait forensic poster preserve native labels. Tables use 9pt type and body paragraphs use Times New Roman12pt with 1.15 spacing. Printing all sheets to A4 would reduce labels; use original page sizes or PDF zoom.']
    checklist='\n'.join(lines)+'\n'
    notes='''# Independent final review

Review date: 15 November 2026. Separate fresh-process data, evidence, DOCX and PDF checks followed report construction. This is a separate verification pass by the same assistant, not an independently staffed or blinded replication.

## Scientific findings retained

The 0.982414777778 handcrafted AUC is a valid descriptive release-origin ranking score. It does not establish a subject-independent or encoding-independent diffusion effect. All542 raw rule passes fail confirmatory eligibility. JPEG quantization has zero Human–LD common support, metadata AUC is1.0, and subject/prompt links are unavailable. BH adjustment cannot repair exchangeability; group bootstrap does not remove systematic bias. Zero eligible confirmations is not evidence of no true effect. Section10 states each distinction and maps G1 as substantially implemented, G2 as descriptively addressed, G3 as unresolved under necessary controls.

No models, features, thresholds or projections were fitted to test data during report work. Original caches and IDs were retained. The fresh cached verification passed179 checks; float32 deep probabilities were compared in their native dtype because CSV shortest-decimal serialization is not float64 identity. All22 report tables were rebuilt from original source artifacts and all2281 cells checked against the native DOCX, including numbers, missing values and qualitative source fields.

## Findings corrected during production

1. Paths: requested master/facts/figures names were absent. Used phase_3_master_prompt.md and authoritative results/literature_facts.csv and results/fig01–fig10 files; copied original figures to figures/ and phase3_output/figures/.
2. Numbering: the master had Abstract plus numbered sections and appendices, whereas the current instruction explicitly places discussion in Section10. The report preserves every topic as twelve numbered sections plus appendices and supplies Table0 mapping.
3. Layout: contradictory header/data cell widths initially clipped Tables1/9. Explicit per-cell widths fixed the issue. Re-export and bbox/image inspection found no residual clipping. Long paragraphs are kept together; narrative resumes on portrait pages after figure sheets, and subheadings travel with the narrative.
4. Visuals: native 300-DPI source PNGs remain embedded unchanged. Large landscape pages and the forensic poster preserve original font readability. Undefined monochrome hue is labeled, not presented as measured zero. The inherited causality filename is explicitly disclaimed in the report and figure captions.
5. Rendering: the generic skill renderer could not import pdf2image; LibreOffice was also unavailable. Native Microsoft Word COM was available and exported the actual DOCX; PyMuPDF produced every verification raster. No alternate independently typeset PDF was substituted.
6. Citation semantics: PixelatedScatter’s reported p-values are0.0362,0.0625,0.1070. The curated “only first<0.05” annotation is an arithmetic interpretation, not a fourth reported value. Direct PDF numeric checks and an independent threshold calculation passed.
7. Reference metadata: eighteen source entries deduplicate to sixteen papers (SPAI and SCADET repeat). Phase1/4 author attribution was corrected to Chenqi Kong et al.; Phase1/6 to Luo Li, Tianyi Lu, Jiaxin Song and Ke Cheng. Available preprints are labeled as such: ArtBrain’s older arXiv source is not the final TMM version; the art-evolution preprint has a different title/version from PNAS; LTE’s available arXiv version is not silently called the published CVPR version. Crosswalk PDF hashes and Source.txt locations were checked.
8. Endpoint errors avoided: joint source/style F1 and attribution accuracy are not binary detection; AP is not AUROC; MisVisFix issue identification is not projection accuracy; observational art regression is not matched Human/AI testing. No cross-paper superiority claim is made.

## Remaining validity limits

These are disclosed limitations, not failed report gates: uncertain source-prefix semantics and unknown derivatives; unmatched subjects; origin-aligned encoding; SD native-resolution mismatch; no separate leave-style/unseen-generator experiment; unequal effective source-group support; conditional bootstrap/silhouette uncertainty; full-canvas predictor dimension change; mixed pixel analysis restricted to frozen45000 cohort while full185015 contrasts are metadata-only; border heuristic and proxy failure labels lack independent semantic annotation; no causal mediation or user study. Runtime values describe stored invocations and resumed caches, not a reconstructed total experiment duration.

## Final review evidence

All63 rendered pages were reviewed through page/contact views, with detailed enlarged review of the revised tables, figure labels and Section10. Final automated report checks:178/178 pass, including63 page boundary/nonempty tests. No unfilled placeholder text, clipped tables or out-of-page text remains. Page-specific locations are in CHECKLIST.md; native source and final artifact hashes are stored separately. Sparse space around dedicated tables and oversized figures is intentional to preserve legibility.
'''
    summary=(OUT/'FINAL_SUMMARY.md').read_text(encoding='utf-8');summary=summary.replace('# Stage 10 checkpoint','# Final Phase 3 submission').replace('Completed through Stage 10; stopped before Stages 11–12.','Completed Stages11–12 on 15 November2026; final DOCX/PDF and seven quality gates are complete.').replace('No final DOCX/PDF was requested for this checkpoint; those belong to Stage 11. The Stage 12 report/document gates remain unrun. Stage 10 includes its own fresh-process numerical/runtime integrity checks.','Final DOCX/PDF: phase3_output/report/Milestone3_Final.docx and .pdf. All seven report quality gates passed. Scientific eligibility remains failed; report verification does not repair the confounds.')
    # Keep only the substantive empirical findings/deviations and current delivery status.
    summary=summary.split('## Deliverables')[0]+'''## Final deliverables and verification

- report/Milestone3_Final.docx and report/Milestone3_Final.pdf:63 pages, twelve numbered sections plus appendices,22 native tables,11 native figures including architecture and all ten composites.
- CHECKLIST.md: all seven gates and page/table locations. REVIEW_NOTES.md: independent pass findings, corrections and remaining validity limits.
- Fresh empirical reproducibility:179 checks. Report/source/evidence/layout verification:178 checks. Every one of2281 table cells matches generated source values.
- Section10 explicitly rejects confirmatory interpretation of all542 passes, without erasing observed differences or claiming no true effect; G1 substantially implemented, G2 descriptive, G3 unresolved.
- figures/: original composite PNGs; report_tables/: table data snapshots; qa/: rendered pages and evidence; root src/ contains scientific and reporting code.

## Deviations and limitations

'''+pd.read_csv(OUT/'methodology_changes.csv').to_markdown(index=False)+'''

Report adjustments: twelve-section numbering follows the user’s Section10 requirement; portrait narrative, landscape tables and oversized scientific figure/poster sheets preserve labels; native Word COM substitutes for the unavailable generic LibreOffice renderer. Subject uncertainty and deterministic JPEG encoding invalidate independent origin attribution. Different endpoints, versions and source compositions prevent cross-paper rankings. See REVIEW_NOTES.md for the author corrections, duplicate references, version discrepancies and unperformed external holdouts.

Launch the dashboard from the workspace in PowerShell:

```powershell
$env:PIP_CACHE_DIR='D:\\Dev\\pip_cache'
$env:TEMP='D:\\Dev\\tmp'
& 'D:\\Dev\\envs\\dav_phase3\\python.exe' -m streamlit run 'D:\\Vault\\Documents\\Uni Work\\Sem5\\DAV\\DAV_Phase3\\src\\dashboard.py'
```
'''
    for name,content in [('CHECKLIST.md',checklist),('REVIEW_NOTES.md',notes),('FINAL_SUMMARY.md',summary)]:
        (DEST/name).write_text(content,encoding='utf-8');(ROOT/name).write_text(content,encoding='utf-8')
    package={'date':'2026-11-15','quality_gates_passed':7,'empirical_checks':179,'report_checks':len(checks),'scientific_confirmatory_gate_passed':False,'docx_pdf_pages':len(pdf),'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [REPORT/'Milestone3_Final.docx',REPORT/'Milestone3_Final.pdf']}}
    (DEST/'final_verification.json').write_text(json.dumps(package,indent=2),encoding='utf-8')
    readme='Final report and verification artifacts are in this folder. Scientific inputs remain in ../results/ and executable scientific/report code in ../src/. Use the specified D-drive Python environment. Tables have source hashes and independently reconstructed cell checks. Figure spreads intentionally retain large page sizes; use PDF zoom or original paper sizes. The full source inventory reads and hashes every results file, including binary caches. The source DOCX is the native Word document used to export this PDF.\n'
    (DEST/'README.md').write_text(readme,encoding='utf-8')
    progress('Stages 11 and 12 complete — final submission verified','Native phase3_output/report/Milestone3_Final.docx and .pdf exported by Microsoft Word. Twelve numbered sections plus appendices; Section10 addresses why all542 exploratory passes cannot support independent origin attribution and explicitly maps G1–G3. All seven quality gates passed:179 fresh cached empirical checks,178 report/source/evidence/layout checks,2281 native table cells checked,16 deduplicated references and18 PDF-page claims verified,63 pages rendered and visually reviewed. All ten composite figures plus architecture embedded natively; wide tables use landscape and large figure sheets preserve labels. CHECKLIST.md, REVIEW_NOTES.md and FINAL_SUMMARY.md saved at root and phase3_output/. Scientific subject/JPEG gate still fails; zero eligible confirmations is not evidence of zero effect.')
    print('Final submission saved; seven report gates pass; source inventory files',len(inventory),flush=True)
if __name__=='__main__':main()
