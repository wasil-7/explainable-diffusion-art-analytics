"""Cached figure tables and page/version-scoped literature comparison, Stages 8–10."""
from common import *
import numpy as np,joblib
from features import load_rgb, quadrants
from PIL import Image

def main():
    start=time.time();f=pd.read_parquet(OUT/'features_matched.parquet');d=f[f.split.eq('test')].copy()
    paper=pd.read_csv(OUT/'literature_facts.csv').fillna('');rows=[]
    for r in paper.to_dict('records'):
        rows.append({'Study & Venue':r['title']+' | '+str(r['venue']),'Source Type (OURS vs. PAPER-REPORTED [PDF Version])':'PAPER-REPORTED ['+r['pdf_version_type']+']','Dataset & Resolution Protocol':r['dataset']+'; '+r['split_protocol'],'Task & Endpoint':r['task']+'; '+r['metrics'],'Key Quantitative Result':r['headline_numbers'],'Comparability Rating & Caveats':'Context only; endpoint, split, source/generator coverage and/or training differ. No direct superiority claim. Version and page scoped; not independently reproduced.','paper_id':r['paper_id'],'crosswalk_id':r['crosswalk_id'],'PDF page':r['page_number'],'Table/Figure':r['table_figure'],'verification_status':r['verification_status']})
    for name in ['handcrafted','frequency','metadata_gated','resnet50','dinov2']:
        r=json.loads((OUT/f'metrics_{name}.json').read_text());rows.append({'Study & Venue':name,'Source Type (OURS vs. PAPER-REPORTED [PDF Version])':'OURS — cached empirical result','Dataset & Resolution Protocol':'AI-ArtBench; grouped 60:20:20; 30000 Human/LD native256; test6000','Task & Endpoint':'Binary origin classification; frozen probe; AUROC/F1','Key Quantitative Result':f"AUROC {r['roc_auc']:.12g}; F1 {r['f1']:.12g}",'Comparability Rating & Caveats':'Within-study comparable on identical test IDs. JPEG quantization origin-aligned; subjects unverified; descriptive only.','paper_id':'OURS','crosswalk_id':'','PDF page':'','Table/Figure':'baseline_metrics.csv','verification_status':'Computed from held-out predictions'})
    pd.DataFrame(rows).to_csv(OUT/'literature_comparison.csv',index=False)
    # Spectrum/color profiles: pooled test, source-group bootstrap of artwork-weighted means.
    cols=[f'fft_{i:02d}_median' for i in range(16)]+['fft_beta_median']+[f'dwt_{v}_median' for v in ['LL2','LH1','HL1','HH1','LH2','HL2','HH2']]
    profiles=[];rng=np.random.default_rng(SEED)
    for origin,g in d.groupby('origin'):
        groups=list(g.groupby('group_id'));sums=np.array([v[cols].sum().to_numpy() for _,v in groups]);counts=np.array([len(v) for _,v in groups]);w=rng.multinomial(len(groups),np.ones(len(groups))/len(groups),size=1000);means=(w@sums)/(w@counts)[:,None]
        for j,c in enumerate(cols):profiles.append(dict(origin=origin,feature=c,mean=g[c].mean(),ci_low=np.percentile(means[:,j],2.5),ci_high=np.percentile(means[:,j],97.5),n=len(g),source_groups=len(groups)))
    pd.DataFrame(profiles).to_csv(OUT/'spectral_wavelet_profiles.csv',index=False)
    primary=d[d.primary_eligible].copy();pred=pd.read_csv(OUT/'predictions_handcrafted.csv',float_precision='round_trip');primary=primary.merge(pred[['artwork_id','y_true','prob_ai','pred_ai']],on='artwork_id',validate='one_to_one')
    primary['case']=np.select([(primary.y_true==0)&primary.pred_ai,(primary.y_true==1)&~primary.pred_ai,(primary.y_true==1)&primary.pred_ai],['FP','FN','TP'],default='TN')
    primary['error_confidence']=np.where(primary.y_true.eq(0),primary.prob_ai,1-primary.prob_ai)
    selected=[];used=set();styles=set()
    for case in ['FP','FN','TP']:
        sub=primary[primary.case.eq(case)].sort_values('error_confidence',ascending=case=='TP')
        for _ in range(2):
            candidates=sub[~sub.artwork_id.isin(used)&~sub['style'].isin(styles)]
            if candidates.empty:candidates=sub[~sub.artwork_id.isin(used)]
            r=candidates.iloc[0].copy();r['selection_reason']=case;selected.append(r);used.add(r.artwork_id);styles.add(r['style'])
    origin_centers=primary.groupby(['style','origin'])[['H_pooled','C_pooled']].transform('mean');primary['hc_outlier_distance']=np.linalg.norm(primary[['H_pooled','C_pooled']]-origin_centers,axis=1)
    pc=pd.read_parquet(OUT/'pca_coordinates.parquet').set_index('artwork_id').loc[primary.artwork_id];primary['pca_outlier_distance']=np.linalg.norm(pc[['PC1','PC2','PC3']],axis=1)
    for col,label in [('hc_outlier_distance','HC outlier'),('pca_outlier_distance','PCA outlier')]:
        r=primary[~primary.artwork_id.isin(used)].sort_values(col,ascending=False).iloc[0].copy();r['selection_reason']=label;selected.append(r);used.add(r.artwork_id)
    gallery=pd.DataFrame(selected).merge(pd.read_parquet(OUT/'cohort_manifest.parquet')[['artwork_id','path']],on='artwork_id',validate='one_to_one')
    gallery.to_csv(OUT/'error_gallery_cases.csv',index=False)
    images=OUT/'gallery';images.mkdir(exist_ok=True)
    for r in gallery.itertuples():
        rgb=load_rgb(DATA/r.path);Image.fromarray(rgb).save(images/f'{r.artwork_id}.png');Image.fromarray(np.concatenate(quadrants(rgb),axis=1)).save(images/f'{r.artwork_id}_crops.png')
    # ECDF/raincloud values retain all test IDs. Feature selection is frozen dev coefficients.
    top=pd.read_csv(OUT/'display_feature_selection.csv').feature.tolist()
    primary[['artwork_id','origin','style']+top].melt(id_vars=['artwork_id','origin','style'],var_name='feature',value_name='value').to_csv(OUT/'feature_distribution_values.csv',index=False)
    save_json('stage9_10_tables.json',dict(seconds=time.time()-start,literature_claim_rows=len(paper),unique_papers=paper.paper_id.nunique(),all_external_numbers_from='literature_facts.csv',gallery_n=len(gallery),gallery_selection='Two confident FP, FN and TP with distinct styles where possible, plus HC/PCA extreme outliers; qualitative selection on test, not model selection.',profiles_ci='1000 source-group bootstraps; pooled styles and conditional on frozen test source composition. SD is separate resized256 sensitivity.'))
    progress('Stage 8 complete','Eight actual held-out FP/FN/TP/outlier cases selected with IDs, predictions, artwork/quadrant PNGs and cached spectral/color measurements; trigger and border sensitivity tables retained.')
    progress('Stage 9 complete',f'{len(paper)} page/version-scoped literature claim records from {paper.paper_id.nunique()} unique papers compared with five empirical probes; task/split/encoding limitations explicit and no cross-paper superiority claim.')
if __name__=='__main__':main()
