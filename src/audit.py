"""Full-release audit, cached in resumable batches; no pixel sampling."""
from common import *
import pandas as pd, numpy as np, hashlib, io
from PIL import Image, JpegImagePlugin
import imagehash
from concurrent.futures import ThreadPoolExecutor

def inspect_file(rel):
    try:
        path=DATA/rel; raw=path.read_bytes()
        with Image.open(io.BytesIO(raw)) as im:
            w,h=im.size
            ph=str(imagehash.phash(im)); dh=str(imagehash.dhash(im))
            sampling=JpegImagePlugin.get_sampling(im) if im.format=='JPEG' else -1
            q=im.quantization if hasattr(im,'quantization') else {}
            cell=path.parent.name
            origin='LD' if cell.startswith('AI_LD_') else 'SD' if cell.startswith('AI_SD_') else 'Human'
            style=cell.removeprefix('AI_LD_').removeprefix('AI_SD_').removeprefix('Real_').removeprefix('real_').replace('ukiyo_e','ukiyo-e')
            return dict(artwork_id=hashlib.sha256(rel.encode()).hexdigest()[:20],path=rel,release_split=Path(rel).parts[0],cell=cell,origin=origin,style=style,width=w,height=h,format=im.format,mode=im.mode,bytes=len(raw),aspect=w/h,subsampling=sampling,progressive=int(bool(im.info.get('progressive') or im.info.get('progression'))),qt_mean=float(np.mean([x for t in q.values() for x in t])) if q else np.nan,qt_hash=hashlib.sha256(str(q).encode()).hexdigest()[:16],icc=int(bool(im.info.get('icc_profile'))),exif=int(bool(im.getexif())),sha256=hashlib.sha256(raw).hexdigest(),phash=ph,dhash=dh,error='')
    except Exception as e: return dict(path=rel,error=repr(e))

def main():
    start=time.time(); cache=OUT/'audit_parts'; cache.mkdir(exist_ok=True)
    catalog=OUT/'audit_paths.txt'
    if catalog.exists():
        paths=catalog.read_text(encoding='utf-8').splitlines()
        assert len(paths)==185015 and len(set(paths))==185015,'Invalid cached release path list'
    else:
        paths=sorted((Path(base)/name).relative_to(DATA).as_posix() for base,dirs,files in os.walk(DATA) for name in files)
        catalog.write_text('\n'.join(paths)+'\n',encoding='utf-8')
    save_json('dataset_inventory.json',dict(files=len(paths),extensions=pd.Series([Path(p).suffix.lower() for p in paths]).value_counts().to_dict()))
    cached_at_start=0
    with ThreadPoolExecutor(max_workers=32) as pool:
        for part,offset in enumerate(range(0,len(paths),3000)):
            dest=cache/f'{part:04d}.parquet'
            if dest.exists():
                old=pd.read_parquet(dest)
                assert len(old)==len(paths[offset:offset+3000]),f'Incomplete cache: {dest}'
                cached_at_start+=len(old)
                continue
            rows=list(pool.map(inspect_file,paths[offset:offset+3000],chunksize=32))
            temp=dest.with_suffix('.parquet.tmp')
            pd.DataFrame(rows).to_parquet(temp,index=False)
            os.replace(temp,dest)
            print(f'audit {min(offset+3000,len(paths))}/{len(paths)} elapsed {time.time()-start:.1f}s',flush=True)
    df=pd.concat([pd.read_parquet(p) for p in sorted(cache.glob('*.parquet'))],ignore_index=True)
    df.to_parquet(OUT/'audit_manifest.parquet',index=False)
    df.groupby(['style','origin','width','height','format','mode'],dropna=False).size().rename('count').reset_index().to_csv(OUT/'audit_counts.csv',index=False)
    df.groupby(['style','origin','subsampling','progressive','qt_hash','qt_mean'],dropna=False).size().rename('count').reset_index().to_csv(OUT/'audit_encoding_counts.csv',index=False)
    save_json('audit_summary.json',dict(files=len(df),errors=int(df.error.ne('').sum()),exact_duplicate_files=int(df.sha256.duplicated(keep=False).sum()),seconds_this_invocation=time.time()-start,cached_files_at_start=cached_at_start,workers=32,executor='threads for I/O-limited full audit',timing_note='Earlier invocations retained in audit_run*.log; this invocation resumes valid batch caches'))
    progress('Stage 1 audit complete',f'Audited {len(df):,} files; {df.error.ne("").sum()} read failures. Full metadata probe follows frozen grouped splits. See results/audit_counts.csv.')
if __name__=='__main__': main()
