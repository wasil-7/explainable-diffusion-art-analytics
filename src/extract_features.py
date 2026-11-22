from common import *
from features import *
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
def main():
    start=time.time();df=pd.read_parquet(OUT/'cohort_manifest.parquet')
    assert (OUT/'control_gate.json').exists()
    pilot=df[df.primary_eligible & df.split.eq('development')].groupby(['style','origin'],group_keys=False).sample(10,random_state=SEED)
    grads=[];sat=[];hue_pilot=[]
    for row in pilot.itertuples():
        rgb=load_rgb(DATA/row.path);y=luminance(rgb)
        gx=cv2.Sobel(y,cv2.CV_64F,1,0,ksize=3)/8;gy=cv2.Sobel(y,cv2.CV_64F,0,1,ksize=3)/8
        grads.append(np.hypot(gx,gy)[::8,::8].ravel());sat.append(cv2.cvtColor(rgb.astype(np.float32)/255,cv2.COLOR_RGB2HSV)[::8,::8,1].ravel())
        for crop in quadrants(rgb):
            hsv=cv2.cvtColor(crop.astype(np.float32)/255,cv2.COLOR_RGB2HSV)[::4,::4]
            hue_pilot.append((hsv[...,0].ravel()*np.pi/180,hsv[...,1].ravel()))
    threshold=float(np.percentile(np.concatenate(grads),75))
    # Stability is change of the circular resultant vector upon a +0.025 cutoff perturbation.
    # Use development only; no origin labels or classifier scores used by the criterion.
    candidates=[]
    for cutoff in [.01,.025,.05,.075,.10,.15]:
        changes=[];coverage=[]
        for angles,s in hue_pilot:
            mask=s>cutoff;strict=s>(cutoff+.025);coverage.append(mask.mean())
            if mask.any() and strict.any():changes.append(abs(np.exp(1j*angles[mask]).mean()-np.exp(1j*angles[strict]).mean()))
        candidates.append(dict(cutoff=cutoff,median_vector_change=float(np.median(changes)),p90_vector_change=float(np.percentile(changes,90)),median_valid_fraction=float(np.median(coverage))))
    stable=[c['cutoff'] for c in candidates if c['p90_vector_change']<=.05 and c['median_valid_fraction']>=.5]
    saturation=min(stable) if stable else .05
    pd.DataFrame(candidates).to_csv(OUT/'saturation_pilot.csv',index=False)
    save_json('saturation_selection.json',dict(selected=saturation,rule='Lowest candidate whose development-crop 90th percentile resultant-vector change under cutoff+0.025 is <=0.05, with median valid coverage >=0.5; fallback 0.05',candidates=candidates,fallback=not bool(stable)))
    save_json('feature_calibration.json',dict(seed=SEED,pilot_artwork_ids=pilot.artwork_id.tolist(),split='development only',n=len(pilot),sobel_threshold=threshold,saturation_cutoff=saturation,saturation_valid_fraction=float((np.concatenate(sat)>saturation).mean()),rule='Sobel /8 luminance gradient 75th percentile over fixed systematic development-pilot pixels; hue cutoff chosen by development circular-vector stability and coverage, see saturation_selection.json; no label performance optimization',icc='Embedded ICC converted to sRGB; absent profiles assumed sRGB; EXIF orientation applied',ordinal='4! =24 patterns, correcting 24! typo in master prompt; stable lexicographic ties; exact ties also excluded separately',dwt='pywt cH=LH row-highpass, cV=HL column-highpass; constant/black zero-energy shares defined as zero'))
    cache=OUT/'feature_parts';cache.mkdir(exist_ok=True)
    df=df.sort_values('path')
    with ProcessPoolExecutor(max_workers=12) as pool:
        for part,offset in enumerate(range(0,len(df),500)):
            dest=cache/f'{part:04d}.parquet'
            if dest.exists():continue
            jobs=[(r.artwork_id,r.path,threshold,saturation) for r in df.iloc[offset:offset+500].itertuples()]
            pd.DataFrame(pool.map(artwork_features,jobs,chunksize=8)).to_parquet(dest,index=False)
            print('features',min(offset+500,len(df)),'/',len(df),'seconds',round(time.time()-start),flush=True)
    features=pd.concat([pd.read_parquet(p) for p in sorted(cache.glob('*.parquet'))],ignore_index=True)
    merged=df[['artwork_id','origin','style','split','primary_eligible','group_id']].merge(features,on='artwork_id',validate='one_to_one')
    merged.to_parquet(OUT/'features_matched.parquet',index=False)
    gate=json.loads((OUT/'control_gate.json').read_text())
    gate['feature_unit_gate_passed']=bool(pd.read_csv(OUT/'unit_test_results.csv').passed.all())
    gate['feature_cache_n']=len(merged)
    gate['feature_readiness_passed']=bool(merged[['H_pooled','C_pooled']].notna().all().all())
    assert gate['feature_unit_gate_passed'] and gate['feature_readiness_passed']
    gate['step5_finalization']='Frozen file/style/support IDs rechecked after Step4 features and before Step6 projections; subject gate unmet, all cells descriptive'
    save_json('control_gate.json',gate)
    save_json('feature_summary.json',dict(n=len(merged),columns=len(features.columns)-1,seconds=time.time()-start))
    progress('Stage 3 complete',f'Unit-tested mathematical features cached for {len(merged):,} artworks: four non-overlapping quadrants, pooled ordinal counts, median/IQR aggregation, and separate full-canvas features. SD features are descriptive resized sensitivity only.')
if __name__=='__main__':main()
