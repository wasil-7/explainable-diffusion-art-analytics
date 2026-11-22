"""Stages 7–8 numerical sensitivities, paired source-group confidence intervals."""
from common import *
from baselines import probe, metrics
from drift import standardized, silhouette_table, cluster_indices, randomized_w1, family
from scipy.stats import spearmanr, rankdata
import numpy as np,joblib

def auc(y,p):
    n=y.sum();return (rankdata(p)[y.astype(bool)].sum()-n*(n+1)/2)/(n*(len(y)-n))

def binary_f1(y,p):
    return 2*np.sum(y&p)/max(1,y.sum()+p.sum())

def resamples(df,n=1000):
    rng=np.random.default_rng(SEED);g=[]
    for origin,ix in df.groupby('origin').indices.items():
        ix=np.asarray(ix);g.append([ix[v] for v in cluster_indices(df.iloc[ix].group_id.to_numpy())])
    for _ in range(n):yield np.concatenate([np.concatenate([arm[j] for j in rng.integers(len(arm),size=len(arm))]) for arm in g])

def paired_ci(df,base,other,base_s,other_s):
    y=df.origin.ne('Human').to_numpy();out=[]
    for ix in resamples(df):
        out.append([auc(y[ix],other.prob_ai.to_numpy()[ix])-auc(y[ix],base.prob_ai.to_numpy()[ix]),binary_f1(y[ix],other.pred_ai.to_numpy()[ix])-binary_f1(y[ix],base.pred_ai.to_numpy()[ix]),np.mean(other_s[ix]-base_s[ix])])
    ci=np.percentile(out,[2.5,97.5],axis=0)
    return {f'delta_{m}_{b}':ci[i,j] for j,m in enumerate(['auc','f1','silhouette']) for i,b in enumerate(['low','high'])}

def aligned_predictions(name,d):return pd.read_csv(OUT/f'predictions_{name}.csv',float_precision='round_trip').set_index('artwork_id').loc[d.artwork_id].reset_index()

def score_vector(d,x):
    a,b=silhouette_table(d,x)
    return a,b.set_index('artwork_id').loc[d.artwork_id].silhouette.to_numpy()

def main():
    start=time.time();allf=pd.read_parquet(OUT/'features_matched.parquet').sort_values('artwork_id').reset_index(drop=True);df=allf[allf.primary_eligible].reset_index(drop=True)
    x,cols=standardized(df);mask=df.split.eq('test').to_numpy();d=df[mask].reset_index(drop=True);base=aligned_predictions('handcrafted',d)
    base_s=pd.read_parquet(OUT/'silhouette_samples.parquet');base_s=base_s[base_s.space.eq('full')].set_index('artwork_id').loc[d.artwork_id].silhouette.to_numpy()
    variants=[]
    for fam in ['Ordinal','FFT','Haar','Color/edges']:
        for mode in ['without','only']:
            use=[c for c in cols if (family(c)==fam)==(mode=='only')];variants.append((f'ab_{mode}_{fam.split("/")[0]}',df[use].to_numpy(),use,'family',f'{mode} {fam}'))
    hsv=[c for c in cols if not c.startswith('lab_')]
    lab=[c for c in cols if family(c)!='Color/edges' or c.startswith(('lab_','edge_'))]
    variants.extend([('ab_HSV',df[hsv].to_numpy(),hsv,'color','HSV'),('ab_Lab',df[lab].to_numpy(),lab,'color','Lab')])
    full=[c for c in df if c.startswith('full_') and 'no_ties' not in c and 'undefined' not in c and 'hue_mean' not in c]
    variants.append(('ab_full_canvas',df[full].to_numpy(),full,'geometry','full 256'))
    five=pd.read_parquet(OUT/'features_geometry.parquet').set_index('artwork_id').loc[df.artwork_id]
    variants.append(('ab_five_crop',five[cols].to_numpy(),cols,'geometry','five 128 crops'))
    ties=[c.replace('H_','H_no_ties_',1) if c.startswith('H_') else c.replace('C_','C_no_ties_',1) if c.startswith('C_') else c for c in cols]
    variants.append(('ab_tie_excluded',df[ties].to_numpy(),ties,'ties','ties excluded'))
    rows=[]
    calrows=[]; dev=df.split.eq('development');cuts=np.quantile(df.loc[dev,'s_median_median'],[1/3,2/3])
    terciles=np.digitize(d.s_median_median,cuts);save_json('saturation_tertiles.json',dict(development_cutpoints=cuts.tolist(),feature='s_median_median',rule='Development-only pooled Human/LD tertiles; fixed for every model'))
    for name,values,features,kind,label in variants:
        path=OUT/f'metrics_{name}.json'
        result=json.loads(path.read_text()) if path.exists() else probe(name,df,values,features)
        other=aligned_predictions(name,d);m=joblib.load(OUT/f'models/{name}.joblib');z=m['scaler'].transform(m['imputer'].transform(values[mask]))
        ss=OUT/f'silhouette_{name}.parquet'
        if ss.exists():other_s=pd.read_parquet(ss).set_index('artwork_id').loc[d.artwork_id].silhouette.to_numpy()
        else:
            _,other_s=score_vector(d,z);pd.DataFrame(dict(artwork_id=d.artwork_id,silhouette=other_s)).to_parquet(ss,index=False)
        br=json.loads((OUT/'metrics_handcrafted.json').read_text())
        rows.append(dict(model=name,kind=kind,label=label,n_features=len(features),roc_auc=result['roc_auc'],f1=result['f1'],silhouette=np.mean(other_s),delta_auc=result['roc_auc']-br['roc_auc'],delta_f1=result['f1']-br['f1'],delta_silhouette=np.mean(other_s-base_s),**paired_ci(d,base,other,base_s,other_s)))
        if kind=='color':
            for k in range(3):
                ix=terciles==k;sub=d[ix].reset_index(drop=True);pr=other[ix].reset_index(drop=True);y=sub.origin.ne('Human').to_numpy()
                boots=[auc(y[v],pr.prob_ai.to_numpy()[v]) for v in resamples(sub)]
                calrows.append(dict(model=label,tertile=['low','medium','high'][k],n=int(ix.sum()),roc_auc=auc(y,pr.prob_ai.to_numpy()),auc_low=np.percentile(boots,2.5),auc_high=np.percentile(boots,97.5),f1=binary_f1(y,pr.pred_ai.to_numpy())))
        print('Ablation complete',name,flush=True)
    # Combined is the original primary probe, not a newly selected fit.
    for k in range(3):
        ix=terciles==k;sub=d[ix].reset_index(drop=True);pr=base[ix].reset_index(drop=True);y=sub.origin.ne('Human').to_numpy();boots=[auc(y[v],pr.prob_ai.to_numpy()[v]) for v in resamples(sub)]
        calrows.append(dict(model='HSV+Lab',tertile=['low','medium','high'][k],n=int(ix.sum()),roc_auc=auc(y,pr.prob_ai.to_numpy()),auc_low=np.percentile(boots,2.5),auc_high=np.percentile(boots,97.5),f1=binary_f1(y,pr.pred_ai.to_numpy())))
    pd.DataFrame(rows).to_csv(OUT/'ablation_results.csv',index=False);pd.DataFrame(calrows).to_csv(OUT/'color_saturation_ablation.csv',index=False)
    if not (OUT/'metrics_ab_unmatched_mixed.json').exists():probe('ab_unmatched_mixed',allf,allf[cols].to_numpy(),cols)
    controls=[]
    for n,scope in [('ab_unmatched_mixed','45000 balanced pixel cohort; Human vs LD+SD, SD native768 resized256'),('handcrafted','30000 primary pixel cohort; Human vs LD native256'),('metadata_ungated_full','185015 full-release native metadata'),('metadata_gated','30000 primary native metadata'),('dimensions_ungated_full','185015 dimensions only')]:
        r=json.loads((OUT/f'metrics_{n}.json').read_text());controls.append(dict(scope=scope,**r))
    pd.DataFrame(controls).to_csv(OUT/'control_gate_ablation.csv',index=False)
    bm=joblib.load(OUT/'models/handcrafted.joblib');baseline_w=pd.read_csv(OUT/'style_feature_drift.csv').groupby('style').w1.mean();stress=[];stylew=[]
    for view in ['jpeg95','jpeg75','jpeg50','resize0.5','resize0.75']:
        vf=pd.read_parquet(OUT/f'features_{view}.parquet').set_index('artwork_id').loc[d.artwork_id];z=bm['scaler'].transform(bm['imputer'].transform(vf[cols].to_numpy()));p=bm['model'].predict_proba(z)[:,1]
        pr=base.copy();pr['prob_ai']=p;pr['pred_ai']=p>=bm['threshold'];pr.to_csv(OUT/f'predictions_{view}.csv',index=False)
        scores,sv=score_vector(d,z);scores.to_csv(OUT/f'style_scores_{view}.csv',index=False)
        w=[]
        for style,ix in d.groupby('style').indices.items():
            y=d.iloc[ix].origin.ne('Human').to_numpy();v=randomized_w1(z[ix],y[None,:])[0].mean();w.append((style,v));stylew.append(dict(view=view,style=style,w1_mean=v))
        w=pd.Series(dict(w));rho=spearmanr(baseline_w.loc[w.index],w).statistic
        r=metrics(d.origin.ne('Human').to_numpy(),p,bm['threshold']);stress.append(dict(view=view,**r,silhouette=sv.mean(),silhouette_retention=sv.mean()/base_s.mean(),style_w1_rank_rho=rho,**paired_ci(d,base,pr,base_s,sv)))
    pd.DataFrame(stress).to_csv(OUT/'perturbation_results.csv',index=False);pd.DataFrame(stylew).to_csv(OUT/'perturbed_style_w1.csv',index=False)
    # Every primary baseline: source-group CI per style, conditional on frozen fits.
    cirows=[]
    for name in ['handcrafted','frequency','metadata_gated','resnet50','dinov2']:
        pr=aligned_predictions(name,d)
        for style,ix in d.groupby('style').indices.items():
            sub=d.iloc[ix].reset_index(drop=True);pp=pr.iloc[ix];y=sub.origin.ne('Human').to_numpy();p=pp.prob_ai.to_numpy();pred=pp.pred_ai.to_numpy()
            boots=np.array([[auc(y[v],p[v]),binary_f1(y[v],pred[v])] for v in resamples(sub)])
            cirows.append(dict(model=name,style=style,roc_auc=auc(y,p),f1=binary_f1(y,pred),auc_low=np.percentile(boots[:,0],2.5),auc_high=np.percentile(boots[:,0],97.5),f1_low=np.percentile(boots[:,1],2.5),f1_high=np.percentile(boots[:,1],97.5)))
    pd.DataFrame(cirows).to_csv(OUT/'baseline_per_style_ci.csv',index=False)
    # Border exclusion: retain each artwork and drop flagged quadrants, not entire source groups.
    border=pd.read_parquet(OUT/'features_border.parquet').set_index('artwork_id').loc[d.artwork_id];supported=border.retained_crops.gt(0).to_numpy();zz=bm['scaler'].transform(bm['imputer'].transform(border[cols].to_numpy()));borderrows=[]
    for style,ix in d.groupby('style').indices.items():
        ix=np.asarray(ix);ix=ix[supported[ix]];y=d.iloc[ix].origin.ne('Human').to_numpy();w=randomized_w1(zz[ix],y[None,:])[0]
        shifts=np.median(zz[ix][y],axis=0)-np.median(zz[ix][~y],axis=0)
        for j,c in enumerate(cols):borderrows.append(dict(style=style,feature=c,border_excluded_w1=w[j],border_excluded_shift=shifts[j],supported_artworks=len(ix)))
    borderstats=pd.DataFrame(borderrows).merge(pd.read_csv(OUT/'style_feature_drift.csv')[['style','feature','median_shift','w1','raw_rule_pass','confirmed_drift']],on=['style','feature'])
    borderstats['direction_reversed']=borderstats.median_shift*borderstats.border_excluded_shift<0;borderstats['confirmatory_conclusion_reversed']=False
    borderstats.to_csv(OUT/'border_exclusion_drift.csv',index=False)
    triggers={'low_saturation':('s_median_median',.10,'low'),'flat_color':('edge_density_median',.10,'low'),'high_frequency':('fft_high_median',.90,'high')};triggerrows=[];flagframe=pd.DataFrame({'artwork_id':d.artwork_id,'border_crops':border.border_crops.to_numpy()})
    for label,(col,q,direction) in triggers.items():
        cut=df.loc[dev,col].quantile(q);flag=d[col].le(cut).to_numpy() if direction=='low' else d[col].ge(cut).to_numpy();flagframe[label]=flag
        for v in [False,True]:
            ix=flag==v;errors=base.pred_ai.to_numpy()!=base.y_true.to_numpy();triggerrows.append(dict(trigger=label,flag=v,n=ix.sum(),errors=errors[ix].sum(),error_rate=errors[ix].mean(),threshold=cut,threshold_source='development pooled quantile'))
    flagframe['heavy_border']=border.border_crops.to_numpy()>0
    for v in [False,True]:
        ix=flagframe.heavy_border.to_numpy()==v;errors=base.pred_ai.to_numpy()!=base.y_true.to_numpy();triggerrows.append(dict(trigger='heavy_border',flag=v,n=ix.sum(),errors=errors[ix].sum(),error_rate=errors[ix].mean() if ix.any() else np.nan,threshold='SD<0.025 and adjacent strip jump>0.08',threshold_source='fixed geometry heuristic'))
    flagframe.to_csv(OUT/'failure_trigger_flags.csv',index=False);pd.DataFrame(triggerrows).to_csv(OUT/'failure_trigger_rates.csv',index=False)
    # Select six featured measurements exclusively by the frozen dev-trained coefficients.
    coefs=np.abs(bm['model'].coef_[0]);pd.DataFrame(dict(feature=cols,abs_development_coefficient=coefs)).sort_values('abs_development_coefficient',ascending=False).head(6).to_csv(OUT/'display_feature_selection.csv',index=False)
    save_json('stage7_8_protocol.json',dict(seconds=time.time()-start,bootstrap_resamples=1000,paired_bootstrap='Whole source groups resampled within origin, identical draws for baseline/variant; fits/thresholds fixed. Silhouette CI resamples cached per-artwork scores conditional on fixed geometry, without recomputing pairwise distances.',control_ablation='Full185015 native metadata contrasts retained. Pixel mixed-origin experiment uses pre-frozen balanced45000 tier2 cohort, not all185015; SD resized256 and source composition differs, so differences cannot isolate resolution alone.',full_canvas='Single full256 feature vector (no across-crop IQR duplicates), versus four/five crop aggregation; dimension differs and is reported.',border='No refit or new hypothesis decisions after inspection; directional sensitivity only, zero confirmatory conclusions in either condition.',kmeans='NumPy Lloyd k2, 20 seeded k-means++ starts, max300 iterations; sklearn native KMeans DLL blocked by Windows Application Control.',border_flagged_artworks=int(flagframe.heavy_border.sum()),border_all_excluded=int((~supported).sum())))
    progress('Stage 7 complete','Family/color/tie/crop/control ablations, source-group paired uncertainty, saturation strata, five held-out perturbations and style-rank stability cached. Mixed pixel ablation uses frozen balanced45000 cohort; full185015 metadata diagnostic retained; no isolated causal resolution claim.')
    progress('Stage 8 numerical analysis complete',f'Development-defined failure triggers and boundary-crop exclusion checked; {flagframe.heavy_border.sum()} border-flagged test artworks. Actual held-out gallery selection and profiles will be rendered in Stage10.')
if __name__=='__main__':main()
