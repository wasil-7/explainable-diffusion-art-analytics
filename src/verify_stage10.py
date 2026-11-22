"""Fresh-process checks for the Stage 10 scientific checkpoint; no refitting."""
from common import *
import numpy as np,joblib,hashlib
from PIL import Image
from scipy.stats import wasserstein_distance
from statsmodels.stats.multitest import multipletests
from sklearn.metrics import roc_auc_score,f1_score
from drift import standardized

def main():
    checks=[]
    def check(name,ok,detail=''):
        checks.append(dict(check=name,passed=bool(ok),detail=detail));assert ok,(name,detail)
    cohort=pd.read_parquet(OUT/'cohort_manifest.parquet');full=pd.read_parquet(OUT/'split_manifest.parquet');f=pd.read_parquet(OUT/'features_matched.parquet');primary=f[f.primary_eligible].sort_values('artwork_id');d=primary[primary.split.eq('test')].reset_index(drop=True);gate=json.loads((OUT/'control_gate.json').read_text())
    check('Full audit/split coverage',len(full)==185015 and full.artwork_id.is_unique)
    check('Source groups remain split-disjoint',full.groupby('group_id').split.nunique().max()==1)
    check('Frozen cohort manifest unchanged',hashlib.sha256((OUT/'cohort_manifest.csv').read_bytes()).hexdigest()==gate['manifest_sha256']=='e27a00766ad8825201aac6d4167a5a98b319d5b18b136ffb20d5765073472936')
    check('Confirmatory gate still fails explicitly',not gate['confirmatory_gate_passed'] and not gate['jpeg_encoding_control_passed'] and not gate['confirmatory_subject_gate_passed'])
    check('Original feature unit tests passed',pd.read_csv(OUT/'unit_test_results.csv').passed.all())
    check('Drift numerical unit checks passed',pd.read_csv(OUT/'drift_unit_test_results.csv').passed.all())
    ids=set(d.artwork_id);meta=cohort.set_index('artwork_id').loc[d.artwork_id];embedding_ids=pd.read_csv(OUT/'embedding_ids.csv');ei=pd.Index(embedding_ids.artwork_id).get_indexer(d.artwork_id)
    model_names=['handcrafted','frequency','metadata_gated','resnet50','dinov2']+pd.read_csv(OUT/'ablation_results.csv').model.tolist()
    for name in model_names:
        pred=pd.read_csv(OUT/f'predictions_{name}.csv',float_precision='round_trip').set_index('artwork_id').loc[d.artwork_id];r=json.loads((OUT/f'metrics_{name}.json').read_text());m=joblib.load(OUT/f'models/{name}.joblib')
        check(name+' identical held-out IDs',len(pred)==6000 and set(pred.index)==ids)
        check(name+' held-out metric reproduction',abs(roc_auc_score(pred.y_true,pred.prob_ai)-r['roc_auc'])<1e-12 and abs(f1_score(pred.y_true,pred.prob_ai>=r['threshold'])-r['f1'])<1e-12)
        source=pd.read_parquet(OUT/'features_geometry.parquet').set_index('artwork_id').loc[d.artwork_id] if name=='ab_five_crop' else meta if name=='metadata_gated' else d
        values=np.load(OUT/f'{name}_embeddings.npy',mmap_mode='r')[ei] if name in ['resnet50','dinov2'] else source[m['columns']].to_numpy(dtype=float)
        z=m['scaler'].transform(m['imputer'].transform(values));p=m['model'].predict_proba(z)[:,1]
        # Pandas serializes float32 probabilities with their shortest float32-roundtrip
        # decimals. Restore the model output dtype before comparing their native values.
        native_cached=pred.prob_ai.to_numpy().astype(p.dtype)
        check(name+' frozen probability reproduction',np.max(np.abs(p-native_cached))<1e-11,'Compared in native model output dtype '+str(p.dtype)+'; float32 CSV decimals round-trip as float32, not float64.')
        check(name+' uses original frozen manifest',m['cohort_manifest_sha256']==gate['manifest_sha256'])
    x,cols=standardized(d);stats=pd.read_csv(OUT/'style_feature_drift.csv');check('Complete prespecified feature/style grid',len(stats)==1040 and len(cols)==104 and not stats.duplicated(['style','feature']).any())
    check('BH scope and correction reproduce',np.max(np.abs(multipletests(stats.p_group_randomization,method='fdr_bh')[1]-stats.p_adj))<1e-12)
    check('Decision rule agrees with saved components',np.array_equal(stats.raw_rule_pass,(stats.p_adj<.05)&(stats.w1>stats.null_p95)))
    check('No unsupported confirmed drift',not stats.confirmed_drift.any() and not stats.confirmatory_eligible.any())
    for style,ix in d.groupby('style').indices.items():
        y=d.iloc[ix].origin.ne('Human').to_numpy();z=x[ix];expected=np.array([wasserstein_distance(z[~y,j],z[y,j]) for j in range(len(cols))]);actual=stats[stats['style'].eq(style)].set_index('feature').loc[cols].w1.to_numpy();check(style+' W1 reproduces independently',np.max(np.abs(expected-actual))<1e-10)
        null=np.load(OUT/'drift_parts'/f'{style}_nulls.npz');check(style+' actual 10k permutations and 2k split-half nulls',null['permutation_w1'].shape==(10000,104) and null['within_origin_split_half_w1'].shape==(2000,104))
        pvals=(1+(null['permutation_w1']>=expected[None,:]-1e-12).sum(axis=0))/10001;check(style+' cached randomization p reproduces',np.max(np.abs(pvals-stats[stats['style'].eq(style)].set_index('feature').loc[cols].p_group_randomization))<1e-12)
    directions=np.load(OUT/'sw1_fixed_directions.npy');check('128 fixed unit directions',directions.shape==(128,104) and np.allclose(np.linalg.norm(directions,axis=1),1))
    for view,n in [('geometry',30000),('border',6000),('jpeg95',6000),('jpeg75',6000),('jpeg50',6000),('resize0.5',6000),('resize0.75',6000)]:
        viewf=pd.read_parquet(OUT/f'features_{view}.parquet');expected_ids=set(primary.artwork_id) if view=='geometry' else ids;check(view+' complete cached real-image feature IDs',len(viewf)==n and viewf.artwork_id.is_unique and set(viewf.artwork_id)==expected_ids)
        if view not in ['geometry','border']:
            pred=pd.read_csv(OUT/f'predictions_{view}.csv',float_precision='round_trip').set_index('artwork_id').loc[d.artwork_id];m=joblib.load(OUT/'models/handcrafted.joblib');v=viewf.set_index('artwork_id').loc[d.artwork_id,m['columns']].to_numpy();p=m['model'].predict_proba(m['scaler'].transform(m['imputer'].transform(v)))[:,1];check(view+' no-refit prediction reproduction',np.max(np.abs(p-pred.prob_ai.to_numpy()))<1e-11)
    b=pd.read_csv(OUT/'border_paired_statistical_tests.csv');bs=json.loads((OUT/'border_sensitivity_summary.json').read_text());check('Border arms use identical supported n per style',b.groupby(['style','arm']).supported_artworks.first().groupby('style').nunique().eq(1).all() and bs['paired_supported_n']==5924 and len(b)==2080)
    check('No confirmatory reversal implied',not b.confirmed_drift.any() and bs['confirmatory_reversals']==0)
    for arm,g in b.groupby('arm'):check(arm+' BH corrected separately over1040',len(g)==1040 and np.allclose(multipletests(g.p,method='fdr_bh')[1],g.p_adj))
    fig_manifest=pd.read_csv(OUT/'figure_manifest.csv');check('All ten required composite figures',len(fig_manifest)==10 and all(f'fig{i:02d}_' in fig_manifest.iloc[i-1].file for i in range(1,11)))
    for r in fig_manifest.itertuples():
        path=OUT/r.file
        with Image.open(path) as im:check(r.file+' readable 300DPI',path.stat().st_size>20000 and min(im.size)>=1500 and abs(im.info['dpi'][0]-300)<1)
        check(r.file+' caption discloses gate', 'Descriptive comparisons' in r.caption and 'No confirmed origin effect' in r.caption)
    gallery=pd.read_csv(OUT/'error_gallery_cases.csv');check('Gallery uses actual held-out artworks',len(gallery)==8 and gallery.artwork_id.is_unique and set(gallery.artwork_id).issubset(ids) and {'FP','FN','TP','HC outlier','PCA outlier'}.issubset(set(gallery.selection_reason)))
    for r in gallery.itertuples():check('Gallery '+str(r.artwork_id)+' real source and crop files',(DATA/r.path).exists() and (OUT/'gallery'/f'{r.artwork_id}_crops.png').exists())
    # Blank OURS pages otherwise coerce integer PDF pages to float ("6.0").
    lit=pd.read_csv(OUT/'literature_facts.csv',dtype=str,keep_default_na=False);comparison=pd.read_csv(OUT/'literature_comparison.csv',dtype=str,keep_default_na=False);papers=comparison[comparison.paper_id.ne('OURS')]
    check('Literature comparison retains all verified claims',len(papers)==len(lit)==18 and papers.paper_id.nunique()==16)
    for r in papers.to_dict('records'):
        match=lit[(lit.paper_id==r['paper_id'])&(lit.headline_numbers==r['Key Quantitative Result'])];check('Literature exact numeric evidence '+r['paper_id'],len(match)==1 and match.iloc[0].pdf_version_type in r['Source Type (OURS vs. PAPER-REPORTED [PDF Version])'] and str(match.iloc[0].page_number)==str(r['PDF page']))
    dv=json.loads((OUT/'dashboard_verification.json').read_text());check('Dashboard actual runtime interactions passed',dv['passed'])
    pd.DataFrame(checks).to_csv(OUT/'stage10_integrity_checks.csv',index=False)
    source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['src','tests'] for p in (ROOT/folder).glob('*.py')};save_json('stage10_source_hashes.json',source_hashes)
    save_json('stage10_verification.json',dict(passed=True,checks=len(checks),stages_completed=list(range(11)),stages_not_run=[11,12],note='Scoped Stage10 integrity checks performed; final report/document gates in Stages11–12 were not requested. No model training, tuning, feature calibration or projection refit in this verification process.',manifest_sha256=gate['manifest_sha256']))
    print('Stage10 checks passed:',len(checks),flush=True)
if __name__=='__main__':main()
