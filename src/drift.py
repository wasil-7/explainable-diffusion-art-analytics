"""Stage 6: source-group resampling; all origin comparisons are descriptive."""
from common import *
import numpy as np, joblib
from scipy.stats import ks_2samp, wasserstein_distance
from sklearn.metrics import silhouette_samples, adjusted_rand_score
from statsmodels.stats.multitest import multipletests

def kmeans2(x):
    """NumPy Lloyd k=2, 20 k-means++ starts (sklearn DLL blocked by host policy)."""
    rng=np.random.default_rng(SEED);best=np.inf;winner=None
    for _ in range(20):
        a=x[rng.integers(len(x))];dist=((x-a)**2).sum(axis=1)
        b=x[rng.choice(len(x),p=dist/dist.sum())] if dist.sum()>0 else x[0]
        centers=np.array([a,b]);previous=None
        for iteration in range(300):
            dd=((x[:,None,:]-centers[None,:,:])**2).sum(axis=2);labels=dd.argmin(axis=1)
            if previous is not None and np.array_equal(labels,previous):break
            previous=labels.copy()
            for k in range(2):
                if (labels==k).any():centers[k]=x[labels==k].mean(axis=0)
        loss=((x-centers[labels])**2).sum()
        if loss<best:best=loss;winner=labels.copy()
    return winner

def standardized(df):
    model=joblib.load(OUT/'models/handcrafted.joblib')
    return model['scaler'].transform(model['imputer'].transform(df[model['columns']].to_numpy())),model['columns']

def family(c):
    if c.startswith('fft_'):return 'FFT'
    if c.startswith('dwt_'):return 'Haar'
    if c.startswith(('H_','C_','tie_')):return 'Ordinal'
    return 'Color/edges'

def random_group_labels(groups, n, rng):
    # Shuffle whole source groups, preserving the number of groups in each arm.
    g,inv=np.unique(groups,return_inverse=True); k=len(g)//2
    order=np.argsort(rng.random((n,len(g))),axis=1)
    labels=np.zeros((n,len(g)),dtype=bool)
    labels[np.arange(n)[:,None],order[:,:k]]=True
    return labels[:,inv]

def randomized_w1(x, labels, batch=100):
    """Exact empirical W1 via sorted CDFs; supports unequal permuted artwork counts."""
    n,p=x.shape; order=np.argsort(x,axis=0); dx=np.diff(np.take_along_axis(x,order,axis=0),axis=0)
    out=np.empty((len(labels),p))
    for a in range(0,len(labels),batch):
        lab=labels[a:a+batch]; n1=lab.sum(axis=1); n0=n-n1
        for j in range(p):
            hit=lab[:,order[:,j]].astype(float); ca=np.cumsum(hit,axis=1)[:,:-1]
            delta=ca/n1[:,None]-(np.arange(1,n)[None,:]-ca)/n0[:,None]
            out[a:a+len(lab),j]=(np.abs(delta)*dx[:,j]).sum(axis=1)
    return out

def cluster_indices(groups):
    return [np.flatnonzero(groups==g) for g in np.unique(groups)]

def bootstrap_shift(a,b,ga,gb,rng,n=1000):
    ia,ib=cluster_indices(ga),cluster_indices(gb); out=np.empty((n,a.shape[1]))
    for i in range(n):
        aa=np.concatenate([ia[j] for j in rng.integers(len(ia),size=len(ia))])
        bb=np.concatenate([ib[j] for j in rng.integers(len(ib),size=len(ib))])
        out[i]=np.median(b[bb],axis=0)-np.median(a[aa],axis=0)
    return np.percentile(out,[2.5,97.5],axis=0)

def silhouette_table(df,x,label='full', save_samples=False):
    rows=[]; samples=[]
    for style,ix in df.groupby('style').indices.items():
        ix=np.asarray(ix); y=df.iloc[ix].origin.ne('Human').to_numpy().astype(int); z=x[ix]
        s=silhouette_samples(z,y)
        pred=kmeans2(z)
        rows.append(dict(style=style,space=label,silhouette=s.mean(),ari=adjusted_rand_score(y,pred),n=len(ix)))
        samples.extend(dict(artwork_id=aid,style=style,space=label,silhouette=float(v)) for aid,v in zip(df.iloc[ix].artwork_id,s))
    return pd.DataFrame(rows),pd.DataFrame(samples)

def main():
    start=time.time(); df=pd.read_parquet(OUT/'features_matched.parquet');df=df[df.primary_eligible].sort_values('artwork_id').reset_index(drop=True)
    x,cols=standardized(df); test=df.split.eq('test').to_numpy(); d=df[test].reset_index(drop=True); x=x[test]
    np.save(OUT/'drift_standardized_test.npy',x); pd.DataFrame({'artwork_id':d.artwork_id}).to_csv(OUT/'drift_test_ids.csv',index=False)
    cache=OUT/'drift_parts';cache.mkdir(exist_ok=True)
    for si,(style,ix) in enumerate(d.groupby('style').indices.items()):
        dest=cache/f'{style}.csv'
        if dest.exists():continue
        rng=np.random.default_rng(SEED+si); sub=d.iloc[ix];z=x[ix]; y=sub.origin.ne('Human').to_numpy();groups=sub.group_id.to_numpy()
        # Known source groups must be origin-homogeneous in the primary comparison.
        assert sub.groupby('group_id').origin.nunique().max()==1
        g,gi=np.unique(groups,return_inverse=True); gy=np.array([y[gi==i][0] for i in range(len(g))]); n1=int(gy.sum())
        order=np.argsort(rng.random((10000,len(g))),axis=1); lab=np.zeros((10000,len(g)),dtype=bool);lab[np.arange(10000)[:,None],order[:,:n1]]=True
        perm=randomized_w1(z,lab[:,gi]); observed=randomized_w1(z,y[None,:])[0]
        null=np.concatenate([randomized_w1(z[y==v],random_group_labels(groups[y==v],1000,rng)) for v in [False,True]])
        p95=np.percentile(null,95,axis=0); ci=bootstrap_shift(z[~y],z[y],groups[~y],groups[y],rng)
        human_iqr=np.subtract(*np.percentile(z[~y],[75,25],axis=0));ai_iqr=np.subtract(*np.percentile(z[y],[75,25],axis=0))
        rows=[]
        for j,c in enumerate(cols):
            rows.append(dict(style=style,feature=c,family=family(c),w1=observed[j],ks_D=ks_2samp(z[~y,j],z[y,j]).statistic,median_shift=np.median(z[y,j])-np.median(z[~y,j]),shift_ci_low=ci[0,j],shift_ci_high=ci[1,j],iqr_ratio=ai_iqr[j]/human_iqr[j] if human_iqr[j]>0 else np.nan,human_iqr_zero=human_iqr[j]==0,p_group_randomization=(1+(perm[:,j]>=observed[j]-1e-12).sum())/10001,null_p95=p95[j],human_groups=len(np.unique(groups[~y])),ai_groups=len(np.unique(groups[y]))))
        pd.DataFrame(rows).to_csv(dest,index=False)
        np.savez_compressed(cache/f'{style}_nulls.npz',permutation_w1=perm,within_origin_split_half_w1=null,columns=np.array(cols))
        print('Stage 6 finished',style,flush=True)
    stats=pd.concat([pd.read_csv(p) for p in sorted(cache.glob('*.csv'))],ignore_index=True)
    stats['p_adj']=multipletests(stats.p_group_randomization,method='fdr_bh')[1]
    stats['raw_rule_pass']=(stats.p_adj<.05)&(stats.w1>stats.null_p95)
    stats['confirmatory_eligible']=False;stats['confirmed_drift']=False
    stats['limitation']='JPEG quantization origin-aligned; subjects unverified; group exchangeability unsupported'
    stats.to_csv(OUT/'style_feature_drift.csv',index=False)
    stats.groupby(['style','family']).agg(w1=('w1','mean'),median_shift=('median_shift','mean'),raw_rule_fraction=('raw_rule_pass','mean'),raw_rule_count=('raw_rule_pass','sum'),features=('feature','size')).reset_index().to_csv(OUT/'style_family_drift.csv',index=False)
    pca=joblib.load(OUT/'models/projection.joblib'); print('projection keys',list(pca),flush=True)
    pc=pd.read_parquet(OUT/'pca_coordinates.parquet').set_index('artwork_id').loc[d.artwork_id]
    spaces={'HC':d[['H_pooled','C_pooled']].to_numpy(),'PCA2':pc[['PC1','PC2']].to_numpy(),'PCA3':pc[['PC1','PC2','PC3']].to_numpy(),'full':x}
    scores=[];sample_rows=[];centroids=[]
    for name,z in spaces.items():
        a,b=silhouette_table(d,z,name);scores.append(a);sample_rows.append(b)
        for origin in ['Human','LD']:
            means=np.array([z[(d['style']==s)&(d.origin==origin)].mean(axis=0) for s in sorted(d['style'].unique())])
            from scipy.spatial.distance import cdist
            dist=cdist(means,means)
            centroids.extend(dict(space=name,origin=origin,style_a=sa,style_b=sb,distance=dist[i,j]) for i,sa in enumerate(sorted(d['style'].unique())) for j,sb in enumerate(sorted(d['style'].unique())))
    pd.concat(scores).to_csv(OUT/'origin_silhouette_ari.csv',index=False);pd.concat(sample_rows).to_parquet(OUT/'silhouette_samples.parquet',index=False)
    pd.DataFrame(centroids).to_csv(OUT/'interstyle_centroid_distances.csv',index=False)
    rng=np.random.default_rng(SEED);directions=rng.normal(size=(128,len(cols)));directions/=np.linalg.norm(directions,axis=1)[:,None];np.save(OUT/'sw1_fixed_directions.npy',directions)
    sw=[]
    for style,ix in d.groupby('style').indices.items():
        z=x[ix]@directions.T;y=d.iloc[ix].origin.ne('Human').to_numpy()
        sw.append(dict(style=style,sw1=np.mean([wasserstein_distance(z[~y,j],z[y,j]) for j in range(128)]),projections=128))
    pd.DataFrame(sw).to_csv(OUT/'sliced_wasserstein.csv',index=False)
    save_json('stage6_protocol.json',dict(seconds=time.time()-start,features=cols,bootstrap_resamples=1000,permutations=10000,null_resamples_per_origin=1000,randomization='Whole source-group labels shuffled within style; original number of AI groups preserved, artwork totals can vary. Exploratory only: exchangeability unsupported.',null='Within each origin, split source groups into two disjoint halves; 1000 splits each origin, pooled P95.',bh_scope=len(stats),standardization='Frozen development-only median imputer and RobustScaler from primary probe',raw_rule_passes=int(stats.raw_rule_pass.sum()),confirmed_drift_cells=0,reason='Subject and JPEG-encoding control gates failed; no causal or confirmatory inference.'))
    progress('Stage 6 complete',f'{len(stats)} feature × style comparisons, 10,000 whole-group randomizations and 1,000 group-bootstrap resamples; source-group split-half nulls, FDR, silhouettes/ARI and SW1 cached. {stats.raw_rule_pass.sum()} exploratory decision-rule passes; zero confirmatory claims because subject/encoding gates fail.')
if __name__=='__main__':main()
