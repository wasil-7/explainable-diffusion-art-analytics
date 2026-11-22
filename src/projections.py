from common import *
from baselines import feature_columns
from features import hc
import pandas as pd,numpy as np,joblib
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from scipy.spatial.distance import cdist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
COLORS={'Human':'#0072B2','LD':'#D55E00'}

def neighbor_ranks(x):
    dist=cdist(x,x);np.fill_diagonal(dist,np.inf)
    order=np.argsort(dist,axis=1).astype(np.int32)
    ranks=np.empty_like(order);ranks[np.arange(len(x))[:,None],order]=np.arange(1,len(x)+1)
    return order,ranks
def fidelity(original_order,original_ranks,z,k=15):
    zo,zr=neighbor_ranks(z);n=len(z);rows=np.arange(n)[:,None]
    intrusion=original_ranks[rows,zo[:,:k]];extrusion=zr[rows,original_order[:,:k]]
    normal=2/(n*k*(2*n-3*k-1))
    return 1-normal*np.maximum(intrusion-k,0).sum(),1-normal*np.maximum(extrusion-k,0).sum()

def main():
    start=time.time();df=pd.read_parquet(OUT/'features_matched.parquet');df=df[df.primary_eligible].sort_values('artwork_id').reset_index(drop=True)
    gate=json.loads((OUT/'control_gate.json').read_text());assert gate['passed']
    cols=feature_columns(df);train=df.split.eq('development');test=df.split.eq('test')
    imputer=SimpleImputer(strategy='median',keep_empty_features=True);scaler=RobustScaler()
    xtrain=scaler.fit_transform(imputer.fit_transform(df.loc[train,cols]));x=scaler.transform(imputer.transform(df[cols]))
    pca=PCA(n_components=3,svd_solver='full',random_state=SEED).fit(xtrain);z=pca.transform(x)
    coords=df[['artwork_id','style','origin','split','group_id','H_pooled','C_pooled']].copy()
    for i in range(3):coords[f'PC{i+1}']=z[:,i]
    coords.to_parquet(OUT/'pca_coordinates.parquet',index=False)
    fig=plt.figure(figsize=(8,6));ax=fig.add_subplot(111,projection='3d')
    for origin in COLORS:
        sub=coords[test & coords.origin.eq(origin)]
        ax.scatter(sub.PC1,sub.PC2,sub.PC3,s=3,alpha=.25,color=COLORS[origin],label=origin)
    ax.set(xlabel=f'PC1 ({pca.explained_variance_ratio_[0]:.1%})',ylabel=f'PC2 ({pca.explained_variance_ratio_[1]:.1%})',zlabel=f'PC3 ({pca.explained_variance_ratio_[2]:.1%})',title='Fixed development-fitted PCA; test n=6,000\nNative-256 file controls; subject-uncertain, descriptive')
    ax.legend();fig.tight_layout();fig.savefig(OUT/'pca_3d.png',dpi=300);plt.close(fig)
    pd.DataFrame(pca.components_.T,index=cols,columns=['PC1','PC2','PC3']).rename_axis('feature').reset_index().to_csv(OUT/'pca_loadings.csv',index=False)
    save_json('pca_summary.json',dict(explained_variance_ratio=pca.explained_variance_ratio_.tolist(),fit_split='development',development_n=int(train.sum()),projected_n=len(df),features=cols))
    (OUT/'models').mkdir(exist_ok=True)
    joblib.dump(dict(imputer=imputer,scaler=scaler,pca=pca,columns=cols),OUT/'models'/'projection.joblib')
    # Theoretical 24-state entropy-complexity envelopes.
    bounds=[]
    for a in np.linspace(1/24,1,500):
        h,c=hc(np.r_[a,np.repeat((1-a)/23,23)]);bounds.append(dict(curve='lower',H=h,C=c))
    for m in range(2,25):
        for a in np.linspace(0,1/m,60):
            p=np.r_[a,np.repeat((1-a)/(m-1),m-1),np.zeros(24-m)]
            h,c=hc(p);bounds.append(dict(curve='upper',H=h,C=c))
    bd=pd.DataFrame(bounds);bd.to_csv(OUT/'hc_theoretical_bounds.csv',index=False)
    centroid_rows=[];ellipse_rows=[];rng=np.random.default_rng(SEED)
    for (style,origin),g in coords[test].groupby(['style','origin']):
        vals=g[['H_pooled','C_pooled']].to_numpy();groups=g.groupby('group_id').indices;keys=list(groups)
        boot=[]
        for _ in range(500):
            idx=np.concatenate([groups[keys[i]] for i in rng.integers(0,len(keys),len(keys))]);boot.append(vals[idx].mean(axis=0))
        cov=np.cov(np.array(boot).T);eig,vec=np.linalg.eigh(cov);eig=np.maximum(eig,0)
        width,height=2*np.sqrt(5.991*eig[::-1]);angle=float(np.degrees(np.arctan2(vec[1,-1],vec[0,-1])))
        center=vals.mean(0);centroid_rows.append(dict(style=style,origin=origin,n=len(g),groups=len(keys),H=center[0],C=center[1]))
        ellipse_rows.append(dict(style=style,origin=origin,H=center[0],C=center[1],width=width,height=height,angle=angle,bootstrap_resamples=500))
    centers=pd.DataFrame(centroid_rows);centers.to_csv(OUT/'hc_centroids.csv',index=False);ellipses=pd.DataFrame(ellipse_rows);ellipses.to_csv(OUT/'hc_centroid_ellipses.csv',index=False)
    human=centers[centers.origin.eq('Human')].set_index('style');ld=centers[centers.origin.eq('LD')].set_index('style')
    pd.DataFrame(dict(delta_H=ld.H-human.H,delta_C=ld.C-human.C)).to_csv(OUT/'hc_descriptive_displacements.csv')
    fig,axes=plt.subplots(2,5,figsize=(17,7));density=[]
    testcoords=coords[test]
    common_xlim=(max(0,testcoords.H_pooled.min()-.02),min(1,testcoords.H_pooled.max()+.02))
    common_ylim=(max(0,testcoords.C_pooled.min()-.01),testcoords.C_pooled.max()+.01)
    for ax,style in zip(axes.ravel(),sorted(coords['style'].unique())):
        g=coords[test & coords['style'].eq(style)]
        ax.plot(bd[bd.curve.eq('lower')].H,bd[bd.curve.eq('lower')].C,'k-',alpha=.15,lw=.5)
        upper=bd[bd.curve.eq('upper')].sort_values('H')
        ax.plot(upper.H,upper.C,'k-',alpha=.15,lw=.5)
        for origin in COLORS:
            sub=g[g.origin.eq(origin)];ax.scatter(sub.H_pooled,sub.C_pooled,s=4,alpha=.2,color=COLORS[origin],label=origin)
            e=ellipses[(ellipses['style']==style)&(ellipses.origin==origin)].iloc[0]
            ax.scatter(e.H,e.C,s=24,color=COLORS[origin]);ax.add_patch(Ellipse((e.H,e.C),e.width,e.height,angle=e.angle,fill=False,color=COLORS[origin]))
        ax.annotate('',xy=(ld.loc[style,'H'],ld.loc[style,'C']),xytext=(human.loc[style,'H'],human.loc[style,'C']),arrowprops=dict(arrowstyle='->',color='black'))
        ax.set(title=f'{style}\nn=300/origin; descriptive',xlabel='H',ylabel='C');ax.set_xlim(*common_xlim);ax.set_ylim(*common_ylim)
        hist_h,xe,ye=np.histogram2d(g[g.origin.eq('Human')].H_pooled,g[g.origin.eq('Human')].C_pooled,bins=25,range=[[0,1],[0,.5]])
        hist_l,_,_=np.histogram2d(g[g.origin.eq('LD')].H_pooled,g[g.origin.eq('LD')].C_pooled,bins=[xe,ye])
        for i,j in zip(*np.nonzero(hist_h+hist_l)):
            density.append(dict(style=style,H_left=xe[i],C_bottom=ye[j],H_width=xe[i+1]-xe[i],C_height=ye[j+1]-ye[j],Human=int(hist_h[i,j]),LD=int(hist_l[i,j]),total=int(hist_h[i,j]+hist_l[i,j]),ai_fraction=float(hist_l[i,j]/(hist_h[i,j]+hist_l[i,j]))))
    axes[0,0].legend(fontsize=7);fig.suptitle('Native-256 file-controlled H–C atlas; subject matching unavailable; ellipses: group-bootstrap centroid 95% regions')
    fig.tight_layout();fig.savefig(OUT/'hc_atlas.png',dpi=300);plt.close(fig)
    density=pd.DataFrame(density);density.to_csv(OUT/'hc_density_grid.csv',index=False)
    from render_density import main as render_density
    from render_hc_atlas import main as render_hc_atlas
    render_hc_atlas()
    render_density()
    # Balanced frozen test subset for feasible exact neighborhood-fidelity calculations.
    sample=df[test].groupby(['style','origin'],group_keys=False).sample(n=150,random_state=SEED).sort_values('artwork_id')
    sx=x[sample.index];sample[['artwork_id','style','origin','split']].to_csv(OUT/'tsne_sample_manifest.csv',index=False)
    oo,orr=neighbor_ranks(sx);scores=[]
    pc_fidelity=[]
    for ndim in [2,3]:
        pt,pc=fidelity(oo,orr,pca.transform(sx)[:,:ndim])
        pc_fidelity.append(dict(dimensions=ndim,k=15,n=len(sample),trustworthiness=pt,continuity=pc,explained_variance_ratio_sum=float(pca.explained_variance_ratio_[:ndim].sum())))
    pd.DataFrame(pc_fidelity).to_csv(OUT/'pca_projection_fidelity.csv',index=False)
    tsdir=OUT/'tsne';tsdir.mkdir(exist_ok=True)
    for perplexity in [15,30,50]:
        for seed in [42,43,44,45,46]:
            dest=tsdir/f'p{perplexity}_s{seed}.parquet';meta=tsdir/f'p{perplexity}_s{seed}.json'
            if meta.exists():scores.append(json.loads(meta.read_text()));continue
            tick=time.time();tz=TSNE(n_components=2,perplexity=perplexity,random_state=seed,init='random',learning_rate='auto',max_iter=1000,n_jobs=1).fit_transform(sx)
            trust,continuity=fidelity(oo,orr,tz)
            row=dict(perplexity=perplexity,seed=seed,initialization='random',k=15,n=len(sample),trustworthiness=trust,continuity=continuity,seconds=time.time()-tick,sampling='150 per style/origin from fixed test, seed42; exploratory transductive subset; no statistical inference')
            projection=sample[['artwork_id','style','origin','split']].copy();projection['TSNE1']=tz[:,0];projection['TSNE2']=tz[:,1];projection.to_parquet(dest,index=False);meta.write_text(json.dumps(row,indent=2));scores.append(row);print(row,flush=True)
    pd.DataFrame(scores).to_csv(OUT/'projection_fidelity.csv',index=False)
    from render_projection_audit import main as render_projection_audit
    render_projection_audit()
    save_json('projection_runtime.json',dict(seconds=time.time()-start))
    progress('Stage 4 complete','Development-fitted fixed 2D/3D PCA; held-out H–C atlas, theoretical bounds, density abstraction and centroid uncertainty; all 15 t-SNE seed/perplexity runs with exact trustworthiness and continuity on a frozen balanced 3,000-test-artwork subset. All views descriptive because subject matches cannot be verified.')
if __name__=='__main__':main()
