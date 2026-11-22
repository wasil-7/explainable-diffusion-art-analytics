"""One batch extraction of all project and paper PDFs; retains page provenance."""
from common import *
import fitz, pandas as pd, hashlib, re, importlib.metadata, platform, shutil, psutil

def main():
    dest=OUT/'pdf_text'; dest.mkdir(exist_ok=True)
    sources={}
    for phase in ['Phase1','Phase2']:
        table=pd.read_csv(ROOT/phase/'Sources.csv').fillna('')
        for rec in table.to_dict('records'):
            folder=ROOT/phase/str(rec['number'])
            rec.update(crosswalk_id=f"{phase}/{rec['number']}", pdf_path=str(next(folder.glob('*.pdf'))))
            rec['source_text']=(folder/'Source.txt').read_text(encoding='utf-8-sig')
            sources[rec['pdf_path']]=rec
    allpages=[]; candidates=[]; crosswalk=[]
    for path in sorted(list(ROOT.glob('*.pdf'))+list(ROOT.glob('Phase*/*/*.pdf'))):
        key=str(path); rec=sources.get(key,{})
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        uid=sha[:12]; pdf=fitz.open(path)
        pages=[p.get_text(sort=True) for p in pdf]
        name=path.relative_to(ROOT).as_posix().replace('/','__')
        (dest/(name+'.txt')).write_text('\n'.join(f'\n=== PDF PAGE {i+1} ===\n{t}' for i,t in enumerate(pages)),encoding='utf-8')
        for i,t in enumerate(pages,1):
            allpages.append(dict(pdf=str(path.relative_to(ROOT)),paper_id=uid,page=i,text=t))
            if rec:
                # Verbatim evidence candidates, not automatically interpreted numeric claims.
                blocks=re.split(r'\n\s*\n',t)
                for b in blocks:
                    if re.search(r'\d',b) and re.search(r'(?i)accuracy|auc|f1|precision|recall|dataset|table\s*\d|fig(?:ure)?\.?\s*\d|trustworthiness|participants',b):
                        candidates.append(dict(paper_id=uid,crosswalk_id=rec['crosswalk_id'],title=rec['title'],authors='See first-page PDF text; curated below',venue='',year='',pdf_version_type=rec['version'],dataset='',task='',split_protocol='',metrics='',headline_numbers='',page_number=i,table_figure='; '.join(re.findall(r'(?i)(?:table|fig(?:ure)?\.?)\s*\d+',b)),evidence_text=b,verification_status='verbatim candidate; not a verified headline claim',doi=rec['doi']))
        if rec:
            crosswalk.append(dict(paper_id=uid,crosswalk_id=rec['crosswalk_id'],title=rec['title'],pdf_version_type=rec['version'],sha256=sha,doi=rec['doi'],pages=len(pages),source_text=rec['source_text'],pdf=str(path.relative_to(ROOT))))
    pd.DataFrame(allpages).to_parquet(OUT/'pdf_pages.parquet',index=False)
    pd.DataFrame(candidates).drop_duplicates(['paper_id','page_number','evidence_text']).to_csv(OUT/'literature_numeric_candidates.csv',index=False)
    pd.DataFrame(crosswalk).to_csv(OUT/'literature_crosswalk.csv',index=False)
    from literature_curated import curate
    curate()
    import torch
    env=dict(python=platform.python_version(),executable=os.sys.executable,cpu=platform.processor(),logical_cpus=os.cpu_count(),ram_bytes=psutil.virtual_memory().total,disks={d:shutil.disk_usage(d)._asdict() for d in ['C:/','D:/']},cuda_available=torch.cuda.is_available(),gpu=torch.cuda.get_device_name(0),gpu_bytes=torch.cuda.get_device_properties(0).total_memory,packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()},environment={k:os.environ.get(k) for k in ['PIP_CACHE_DIR','TEMP','TMP','TORCH_HOME']})
    save_json('environment.json',env)
    (OUT/'ENVIRONMENT.md').write_text('# Environment\n\n```json\n'+json.dumps(env,indent=2)+'\n```\n',encoding='utf-8')
    progress('Stage 0 extraction complete',f'Batch extracted {len(crosswalk)} paper entries ({len(set(r["paper_id"] for r in crosswalk))} distinct hashes), plus all three project PDFs. Literature numeric candidates retain PDF pages and must be curated before quotation. CUDA: {env["gpu"]}.')
if __name__=='__main__': main()
