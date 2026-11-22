"""Paired boundary sensitivity, excluding unsupported all-flagged artworks in BOTH arms."""
from common import *
from drift import *

def main():
    start=time.time();f=pd.read_parquet(OUT/'features_matched.parquet');d=f[f.primary_eligible&f.split.eq('test')].sort_values('artwork_id').reset_index(drop=True);x,cols=standardized(d)
    b=pd.read_parquet(OUT/'features_border.parquet').set_index('artwork_id').loc[d.artwork_id];keep=b.retained_crops.gt(0).to_numpy();m=joblib.load(OUT/'models/handcrafted.joblib');z=m['scaler'].transform(m['imputer'].transform(b[cols].to_numpy()))
    cache=OUT/'border_stats_parts';cache.mkdir(exist_ok=True);tables=[]
    for arm,values in [('paired_original',x),('border_excluded',z)]:
        for si,(style,ix) in enumerate(d.groupby('style').indices.items()):
            dest=cache/f'{arm}_{style}.csv'
            if not dest.exists():
                ix=np.asarray(ix);ix=ix[keep[ix]];sub=d.iloc[ix];v=values[ix];y=sub.origin.ne('Human').to_numpy();groups=sub.group_id.to_numpy();rng=np.random.default_rng(SEED+si)
                g,gi=np.unique(groups,return_inverse=True);gy=np.array([y[gi==j][0] for j in range(len(g))]);order=np.argsort(rng.random((10000,len(g))),axis=1);lab=np.zeros((10000,len(g)),dtype=bool);lab[np.arange(10000)[:,None],order[:,:int(gy.sum())]]=True
                perm=randomized_w1(v,lab[:,gi]);w=randomized_w1(v,y[None,:])[0];null=np.concatenate([randomized_w1(v[y==k],random_group_labels(groups[y==k],1000,rng)) for k in [False,True]]);p95=np.percentile(null,95,axis=0);ci=bootstrap_shift(v[~y],v[y],groups[~y],groups[y],rng)
                pd.DataFrame(dict(style=style,feature=cols,w1=w,median_shift=np.median(v[y],axis=0)-np.median(v[~y],axis=0),shift_ci_low=ci[0],shift_ci_high=ci[1],p=(1+(perm>=w[None,:]-1e-12).sum(axis=0))/10001,null_p95=p95,supported_artworks=len(ix),arm=arm)).to_csv(dest,index=False)
                np.savez_compressed(cache/f'{arm}_{style}_nulls.npz',permutation_w1=perm,within_origin_split_half_w1=null)
            tables.append(pd.read_csv(dest))
    both=pd.concat(tables,ignore_index=True);both['p_adj']=both.groupby('arm').p.transform(lambda v:multipletests(v,method='fdr_bh')[1]);both['raw_rule_pass']=(both.p_adj<.05)&(both.w1>both.null_p95);both['confirmed_drift']=False;both.to_csv(OUT/'border_paired_statistical_tests.csv',index=False)
    a=both[both.arm.eq('paired_original')].drop(columns='arm');c=both[both.arm.eq('border_excluded')].drop(columns='arm');merged=a.merge(c,on=['style','feature'],suffixes=('_paired_original','_border_excluded'),validate='one_to_one');merged['direction_reversed']=merged.median_shift_paired_original*merged.median_shift_border_excluded<0;merged['raw_rule_reversed']=merged.raw_rule_pass_paired_original!=merged.raw_rule_pass_border_excluded;merged['confirmatory_conclusion_reversed']=False;merged.to_csv(OUT/'border_exclusion_drift.csv',index=False)
    save_json('border_sensitivity_summary.json',dict(seconds=time.time()-start,flagged_artworks=int(b.border_crops.gt(0).sum()),all_crops_excluded=int((~keep).sum()),paired_supported_n=int(keep.sum()),direction_reversals=int(merged.direction_reversed.sum()),exploratory_rule_reversals=int(merged.raw_rule_reversed.sum()),confirmatory_reversals=0,protocol='Both arms restricted to exactly the same supported artwork IDs. Rerun 10000 whole-group randomizations, 1000 source-group bootstraps and 2000 within-origin split-half nulls; BH across1040 tests separately per arm. Same random group draws in both arms. Encoding/subject limitations apply.'))
    print('Paired border analysis complete',flush=True)
if __name__=='__main__':main()
