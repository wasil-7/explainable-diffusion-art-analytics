"""Fresh-process audit of the portrait report, source numbers, PDF geometry and package."""
from common import *
from build_submission import DEST,NAME,specs,f,ORDER,STEPS
from docx import Document
from docx.oxml.ns import qn
import pymupdf as fitz
from PIL import Image,ImageDraw
import numpy as np,re,zipfile,hashlib

def main():
    package=ROOT/'GCR_Submission'/NAME
    base=package if (package/(NAME+'.pdf')).exists() else DEST
    pdf=fitz.open(base/(NAME+'.pdf'));doc=Document(base/(NAME+'.docx'));qa=DEST/'qa';qa.mkdir(exist_ok=True)
    checks=[]
    def check(name,passed,detail=''):
        checks.append({'check':name,'passed':bool(passed),'detail':str(detail)})
    manifest=json.loads((DEST/'submission_report_manifest.json').read_text());definitions=specs()
    check('exactly13 native tables',len(doc.tables)==13)
    cells=0
    for n,tb in enumerate(doc.tables,1):
        df=definitions[n][1];expected=[list(df.columns)]+[[f(v) for v in row] for row in df.itertuples(index=False,name=None)]
        actual=[[c.text for c in row.cells] for row in tb.rows];cells+=sum(map(len,actual));check(f'Table{n}: every cell matches fresh authoritative-source transformation',actual==expected)
        check(f'Table{n}: repeat header / no split rows',bool(tb.rows[0]._tr.xpath('./w:trPr/w:tblHeader')) and all(row._tr.xpath('./w:trPr/w:cantSplit') for row in tb.rows))
        borders=tb._tbl.xpath('./w:tblPr/w:tblBorders/*');check(f'Table{n}: black half-point six-edge grid',len(borders)==6 and all(x.get(qn('w:sz'))=='4' and x.get(qn('w:color'))=='000000' for x in borders))
        check(f'Table{n}: Calibri9 cells',all(r.font.name=='Calibri' and abs(r.font.size.pt-9)<.01 for row in tb.rows for c in row.cells for p in c.paragraphs for r in p.runs))
        width=sum(c.width.inches for c in tb.rows[0].cells);check(f'Table{n}: portrait width',abs(width-6.67)<.03,width)
    paragraphs=[p.text for p in doc.paragraphs];headings=[p.text for p in doc.paragraphs if p.style.name=='Heading 1']
    check('eight numbered sections in chronological order',[int(re.match(r'^(\d+)\.',x)[1]) for x in headings if re.match(r'^\d+\.',x)]==list(range(1,9)),headings)
    check('Tables1–13 caption order',[int(re.match(r'^Table (\d+)\.',x)[1]) for x in paragraphs if re.match(r'^Table \d+\.',x)]==list(range(1,14)))
    check('Figures1–12 caption order, no zero-indexing',[int(re.match(r'^Figure (\d+)\.',x)[1]) for x in paragraphs if re.match(r'^Figure \d+\.',x)]==list(range(1,13)))
    check('DOCX100percent portrait and0.8-inch margins',all(s.page_width<s.page_height and all(abs(v.inches-.8)<.005 for v in [s.top_margin,s.bottom_margin,s.left_margin,s.right_margin]) for s in doc.sections))
    check('body Times New Roman11',doc.styles['Normal'].font.name=='Times New Roman' and doc.styles['Normal'].font.size.pt==11)
    check('headings13 and11.5 TNR',all(doc.styles[s].font.name=='Times New Roman' and doc.styles[s].font.size.pt==size for s,size in [('Heading 1',13),('Heading 2',11.5)]))
    check('no forced paragraph page breaks',not any(p._p.xpath('.//w:br[@w:type="page"]') for p in doc.paragraphs))
    forced=[p.text for p in doc.paragraphs if p.paragraph_format.page_break_before]
    check('only references and appendices force a new page',forced==['References','Appendix A: Reproducibility Manifest, Citation Crosswalk & Timings','Appendix B: Extended Statistical & Sensitivity Tables'])
    for heading in forced:
        found=[(i,p) for i,p in enumerate(pdf) if any(heading==' '.join(b[4].split()) for b in p.get_text('blocks'))]
        check(heading+' starts at page top',len(found)==1 and any(heading in ' '.join(b[4].split()) and b[1]<85 for b in found[0][1].get_text('blocks')))
    full='\n'.join(p.get_text() for p in pdf)
    gate=json.loads((OUT/'control_gate.json').read_text());protocol=json.loads((OUT/'stage6_protocol.json').read_text())
    check('frozenmanifest exact SHA survives typesetting',gate['manifest_sha256'] in full)
    check('discussion preserves ineligibility / no causal assertion',all(x in full for x in ['zero eligible','exchangeability','Benjamini','not proof','unseen-generator']) or all(x in full for x in ['zero eligible','exchangeability','Benjamini','neither evidence','unseen-generator']))
    check('current control gate and542 raw passes',not gate['confirmatory_gate_passed'] and protocol['raw_rule_passes']==542 and protocol['confirmed_drift_cells']==0)
    check('pagecount30–35',30<=len(pdf)<=35,len(pdf))
    check('cover exact metadata and M2 instructor spelling',all(x in pdf[0].get_text() for x in ['National University','Milestone 3','15 – 11 – 26','Wasil Kayani','Umar Asghar','Ma’am Azka Atiq','DSB (Section B)']))
    m2=fitz.open(ROOT/'i242551_i242532_Milestone02_DSB.pdf');m2text=' '.join(p.get_text() for p in m2);norm=lambda x:re.sub(r'\s+',' ',x).strip()
    for i,(name,_,_) in enumerate(STEPS,1):check(f'M2 Step{i} exact promised heading traced',f'Step {i} — {name}.' in norm(m2text))
    facts=pd.read_csv(OUT/'literature_facts.csv').fillna('');table9=' '.join(c.text for row in doc.tables[8].rows for c in row.cells)
    for pid in ORDER:
        subset=facts[facts.paper_id.eq(pid)]
        check(f'literature{pid}: all curated headline claims in Table9',all(norm(s) in norm(table9) for s in subset.headline_numbers))
    references=[x for x in paragraphs if re.match(r'^\[\d+\]',x)];check('exactly16 unique reference entries',[int(re.match(r'^\[(\d+)\]',x)[1]) for x in references]==list(range(1,17)))
    for pid,entry in zip(ORDER,references):
        source=facts[facts.paper_id.eq(pid)].iloc[0]
        check(f'reference{pid}: exact title and DOI',source.title in entry and source.doi in entry)
    intro=' '.join(paragraphs[:paragraphs.index('2. Implementation of the Proposed Methodology')]);check('all16 cited before methods',all(f'[{i}]' in intro for i in range(1,17)))
    # Recompute primary metrics from per-artwork predictions, independent of the report builder.
    from sklearn.metrics import roc_auc_score,f1_score,balanced_accuracy_score,accuracy_score
    metrics=pd.read_csv(OUT/'baseline_metrics.csv').set_index('model');ids=[]
    for model in ['handcrafted','frequency','metadata_gated','resnet50','dinov2']:
        d=pd.read_csv(OUT/f'predictions_{model}.csv');ids.append(set(d.artwork_id));r=metrics.loc[model]
        for name,score in [('roc_auc',roc_auc_score(d.y_true,d.prob_ai)),('f1',f1_score(d.y_true,d.pred_ai)),('balanced_accuracy',balanced_accuracy_score(d.y_true,d.pred_ai)),('accuracy',accuracy_score(d.y_true,d.pred_ai))]:check(f'{model} {name}: reproduced from frozen predictions',abs(score-r[name])<1e-9)
    check('five identical6000 test IDs',all(len(x)==6000 and x==ids[0] for x in ids))
    # Balance/group counts can be independently checked from the retained CSV without a Parquet DLL.
    cohort=pd.read_csv(OUT/'cohort_manifest.csv');t4=definitions[4][1]
    for name,d in [('Balanced45k',cohort),('Primary30k',cohort[cohort.primary_eligible])]:
        for split,g in d.groupby('split'):
            r=t4[(t4.Cohort==name)&(t4.Split==split)].iloc[0];check(f'{name}/{split}: rows and source groups',r.Artworks==len(g) and r['Source groups']==g.group_id.nunique())
    check('known source groups split-disjoint',cohort.groupby('group_id').split.nunique().max()==1)
    z=zipfile.ZipFile(base/(NAME+'.docx'));embedded={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
    for r in manifest['figures']:
        path=DEST/'figures'/r['file'];im=Image.open(path)
        check(f'native figure{r["number"]}/{path.name}: pixels and300DPI',hashlib.sha256(path.read_bytes()).hexdigest() in embedded and abs(im.info.get('dpi',(0,0))[0]-300)<1)
    provenance=json.loads((DEST/'heatmap_pixel_provenance.json').read_text());original=Image.open(ROOT/'figures/fig05_style_drift_heatmap.png').convert('RGB')
    for i,box in enumerate(provenance['crop_boxes'],1):check(f'Figure7 panel{i}: actual original fig05 pixels',np.array_equal(np.asarray(original.crop(tuple(box))),np.asarray(Image.open(DEST/f'figures/fig05_style_drift_heatmap_{i}.png'))))
    pages=[]
    for i,p in enumerate(pdf):
        check(f'PDFpage{i+1}: portrait',p.rect.width<p.rect.height)
        spans=[s for b in p.get_text('dict')['blocks'] if b['type']==0 for line in b['lines'] for s in line['spans'] if s['text'].strip()]
        outside=[s['text'] for s in spans if s['bbox'][0]<20 or s['bbox'][2]>p.rect.width-20 or s['bbox'][1]<15 or s['bbox'][3]>p.rect.height-15]
        check(f'PDFpage{i+1}: text inside page bounds',not outside,outside)
        pictures=p.get_image_info();bad=[x['bbox'] for x in pictures if x['bbox'][0]<50 or x['bbox'][1]<45 or x['bbox'][2]>p.rect.width-50 or x['bbox'][3]>p.rect.height-45]
        check(f'PDFpage{i+1}: images inside portrait content bounds',not bad,bad)
        check(f'PDFpage{i+1}: substantive text or figure',len(p.get_text().strip())>20 or bool(pictures))
        pages.append({'page':i+1,'text_characters':len(p.get_text()),'images':len(pictures),'outside':outside,'image_outside':bad})
        p.get_pixmap(matrix=fitz.Matrix(1.8,1.8)).save(qa/f'page-{i+1:02}.png')
    for start in range(0,len(pdf),8):
        canvas=Image.new('RGB',(1500,1080),'#cccccc');dr=ImageDraw.Draw(canvas)
        for j,i in enumerate(range(start,min(start+8,len(pdf)))):
            im=Image.open(qa/f'page-{i+1:02}.png');im.thumbnail((370,510));x=(j%4)*375;y=(j//4)*540;canvas.paste(im,(x,y+20));dr.text((x+8,y+2),str(i+1),fill='black')
        canvas.save(qa/f'contact-{start//8+1}.png')
    check('no placeholder markers',not re.search(r'\b(TODO|TBD|Lorem ipsum|INSERT HERE)\b',full,re.I))
    if base==package:
        allowed={'src','tests','figures','results','.streamlit','README.md','requirements.txt',NAME+'.docx',NAME+'.pdf'}
        check('package top-level allowlist',set(x.name for x in package.iterdir())==allowed)
        files=[p for p in package.rglob('*') if p.is_file()];forbidden=[str(p) for p in files if p.suffix in ['.parquet','.npy','.npz','.txt'] and p.name!='requirements.txt' or '__pycache__' in p.parts or any(v in p.parts for v in ['data','Phase1','Phase2','pdf_text','models'])]
        check('no prohibited heavy inputs / agent logs',not forbidden and not any(p.name in ['PROGRESS.md','CHECKLIST.md','REVIEW_NOTES.md','FINAL_SUMMARY.md','DEMO_GUIDE_FOR_WASIL.md'] for p in files),forbidden)
        check('all original Python scripts copied',{p.name for p in (ROOT/'src').glob('*.py')}=={p.name for p in (package/'src').glob('*.py')})
        size=sum(p.stat().st_size for p in files);check('uncompressed package under30MB',size<30_000_000,size)
        archive=package.parent/(NAME+'.zip');check('ZIP under30MB',archive.stat().st_size<30_000_000,archive.stat().st_size)
        with zipfile.ZipFile(archive) as zz:
            check('ZIP integrity and exact file set',zz.testzip() is None and set(zz.namelist())=={str(p.relative_to(package.parent)).replace('\\','/') for p in files})
            check('ZIP every file matches directory',all(hashlib.sha256(zz.read(str(p.relative_to(package.parent)).replace('\\','/'))).digest()==hashlib.sha256(p.read_bytes()).digest() for p in files))
        for ext in ['.pdf','.docx']:check('root copy matches package'+ext,(ROOT/(NAME+ext)).read_bytes()==(package/(NAME+ext)).read_bytes())
    pd.DataFrame(checks).to_csv(DEST/'submission_checks.csv',index=False)
    (DEST/'page_geometry.json').write_text(json.dumps(pages,indent=2))
    (DEST/'submission_verification.json').write_text(json.dumps({'passed':all(x['passed'] for x in checks),'checks':len(checks),'table_cells_verified':cells,'pages':len(pdf),'scientific_confirmatory_gate_passed':False,'base':str(base),'visual_review':'Separate rendered-page review required; not inferred from automated geometry'},indent=2))
    failures=[x for x in checks if not x['passed']];print(json.dumps({'checks':len(checks),'table_cells':cells,'pages':len(pdf),'failures':failures},indent=2),flush=True)
    if failures:raise SystemExit(1)
if __name__=='__main__':main()
