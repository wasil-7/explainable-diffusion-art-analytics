"""Additional real-image views for Stages 7–8; resumable fixed-size parts."""
from common import *
from features import *
from concurrent.futures import ProcessPoolExecutor
import warnings
warnings.filterwarnings('ignore',category=RuntimeWarning)

def aggregate(outputs,aid):
    out={'artwork_id':aid}
    for key in outputs[0][0]:
        vals=np.array([o[0][key] for o in outputs]);vals=vals[np.isfinite(vals)]
        out[key+'_median']=np.median(vals) if len(vals) else np.nan
        out[key+'_iqr']=np.subtract(*np.percentile(vals,[75,25])) if len(vals) else np.nan
    out['H_pooled'],out['C_pooled']=hc(sum(o[1] for o in outputs))
    out['H_no_ties_pooled'],out['C_no_ties_pooled']=hc(sum(o[2] for o in outputs))
    return out

def border_flag(rgb):
    y=luminance(rgb)
    # Prespecified geometry-only heuristic, independent of predictions and origin.
    strips=[(y[:8],y[8:16]),(y[-8:],y[-16:-8]),(y[:,:8],y[:,8:16]),(y[:,-8:],y[:,-16:-8])]
    return any(a.std()<.025 and abs(a.mean()-b.mean())>.08 for a,b in strips)

def work(job):
    aid,path,threshold,saturation,view,is_test=job;rgb=load_rgb(DATA/path)
    if view.startswith('jpeg'):
        buffer=io.BytesIO();Image.fromarray(rgb).save(buffer,format='JPEG',quality=int(view[4:]),subsampling=2);buffer.seek(0)
        with Image.open(buffer) as im:rgb=np.array(im.convert('RGB'))
    elif view.startswith('resize'):
        size=int(256*float(view[6:]));rgb=np.array(Image.fromarray(rgb).resize((size,size),Image.Resampling.BILINEAR).resize((256,256),Image.Resampling.BILINEAR))
    crops=quadrants(rgb);outputs=[crop_features(c,threshold,saturation) for c in crops]
    if view=='geometry':
        five=aggregate(outputs+[crop_features(rgb[64:192,64:192],threshold,saturation)],aid)
        flags=[border_flag(c) for c in crops];kept=[o for o,flag in zip(outputs,flags) if not flag]
        border=aggregate(kept,aid) if kept else {'artwork_id':aid}
        border.update(border_crops=sum(flags),retained_crops=len(kept),border_exclusion_supported=bool(kept))
        return five,border if is_test else None
    return aggregate(outputs,aid),None

def main():
    start=time.time();df=pd.read_parquet(OUT/'cohort_manifest.parquet');df=df[df.primary_eligible].sort_values('path')
    cal=json.loads((OUT/'feature_calibration.json').read_text());cache=OUT/'sensitivity_parts';cache.mkdir(exist_ok=True)
    views=['geometry','jpeg95','jpeg75','jpeg50','resize0.5','resize0.75']
    with ProcessPoolExecutor(max_workers=12) as pool:
        for view in views:
            sub=df if view=='geometry' else df[df.split.eq('test')]
            for part,a in enumerate(range(0,len(sub),500)):
                dest=cache/f'{view}_{part:04d}.parquet'
                if dest.exists():continue
                jobs=[(r.artwork_id,r.path,cal['sobel_threshold'],cal['saturation_cutoff'],view,r.split=='test') for r in sub.iloc[a:a+500].itertuples()]
                results=list(pool.map(work,jobs,chunksize=8))
                if view=='geometry':
                    borders=[b for _,b in results if b is not None]
                    if borders:pd.DataFrame(borders).to_parquet(cache/f'border_{part:04d}.parquet',index=False)
                pd.DataFrame([f for f,_ in results]).to_parquet(dest,index=False)
                print(view,min(a+500,len(sub)),'/',len(sub),flush=True)
    for view in views+['border']:
        pd.concat([pd.read_parquet(p) for p in sorted(cache.glob(f'{view}_*.parquet'))],ignore_index=True).to_parquet(OUT/f'features_{view}.parquet',index=False)
    save_json('sensitivity_pixel_protocol.json',dict(seconds=time.time()-start,five_crop_n=len(df),perturbation_n_per_view=6000,views=views,border_rule='Flag a quadrant if any outer 8-pixel strip has luminance SD <0.025 and its mean differs by >0.08 from the adjacent 8-pixel strip. Aggregate unflagged quadrants; flag all-excluded cases unsupported.',jpeg='Pillow JPEG, subsampling 2; baseline is original release JPEG, NOT Q=100 re-encoding.',resize='Pillow bilinear down/up on the standardized RGB256 canvas',five_crop='Four 128x128 quadrants plus central [64:192,64:192], pooled ordinal counts and median/IQR of five crop measurements'))
if __name__=='__main__':main()
