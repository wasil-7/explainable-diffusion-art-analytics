from common import *
import pandas as pd,numpy as np,joblib
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler,StandardScaler
from sklearn.linear_model import LogisticRegression,LogisticRegressionCV
from sklearn.model_selection import PredefinedSplit
from sklearn.metrics import accuracy_score,balanced_accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix,roc_curve,precision_recall_curve,average_precision_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def feature_columns(df):
    # Full-canvas/tie-excluded measurements cached for later sensitivity, not mixed into primary.
    return [c for c in df if (c.endswith('_median') or c.endswith('_iqr') or c in ['H_pooled','C_pooled']) and not c.startswith('full_') and 'no_ties' not in c and 'undefined' not in c and 'hue_mean' not in c]

def ece(y,p):
    bins=np.minimum((p*15).astype(int),14);return sum(np.mean(bins==i)*abs(y[bins==i].mean()-p[bins==i].mean()) for i in range(15) if (bins==i).any())
def metrics(y,p,threshold):
    pred=p>=threshold
    return dict(accuracy=accuracy_score(y,pred),balanced_accuracy=balanced_accuracy_score(y,pred),precision=precision_score(y,pred,zero_division=0),recall=recall_score(y,pred,zero_division=0),f1=f1_score(y,pred,zero_division=0),f1_macro_binary=f1_score(y,pred,average='macro',zero_division=0),roc_auc=roc_auc_score(y,p),average_precision=average_precision_score(y,p),ece=ece(y,p),n=len(y),threshold=threshold)

def probe(name,df,x,columns):
    start=time.time();y=df.origin.ne('Human').to_numpy().astype(int)
    masks={s:df.split.eq(s).to_numpy() for s in ['development','validation','test']}
    train=masks['development'];val=masks['validation'];test=masks['test']
    imputer=SimpleImputer(strategy='median',keep_empty_features=True);scaler=StandardScaler() if name in ['resnet50','dinov2'] else RobustScaler()
    xt=imputer.fit_transform(x[train]);xt=scaler.fit_transform(xt)
    xv=scaler.transform(imputer.transform(x[val]));xe=scaler.transform(imputer.transform(x[test]))
    # All preprocessing fitted only on development; this single predefined fold tunes on validation.
    tune=LogisticRegressionCV(Cs=[.001,.01,.1,1,10,100],cv=PredefinedSplit(np.r_[np.full(train.sum(),-1),np.zeros(val.sum(),dtype=int)]),scoring='roc_auc',max_iter=2000,solver='lbfgs',refit=False,n_jobs=1,random_state=SEED)
    tune.fit(np.concatenate([xt,xv]),np.r_[y[train],y[val]])
    pd.DataFrame(dict(C=tune.Cs_,validation_roc_auc=tune.scores_[tune.classes_[1]][0])).to_csv(OUT/f'validation_tuning_{name}.csv',index=False)
    c=float(tune.C_[0]);model=LogisticRegression(C=c,max_iter=2000,random_state=SEED).fit(xt,y[train])
    pv=model.predict_proba(xv)[:,1];precision,recall,thresholds=precision_recall_curve(y[val],pv)
    f1=2*precision[:-1]*recall[:-1]/np.maximum(precision[:-1]+recall[:-1],1e-12)
    threshold=float(thresholds[np.argmax(f1)])
    # Test accessed once after C and decision threshold frozen.
    p=model.predict_proba(xe)[:,1];yt=y[test]
    result=metrics(yt,p,threshold);result.update(model=name,C=c,development_n=int(train.sum()),validation_n=int(val.sum()),seconds=time.time()-start)
    pred=df.loc[test,['artwork_id','origin','style','group_id']].copy();pred['y_true']=yt;pred['prob_ai']=p;pred['pred_ai']=p>=threshold
    pred.to_csv(OUT/f'predictions_{name}.csv',index=False)
    rows=[]
    for style,g in pred.groupby('style'):
        if g.y_true.nunique()<2:continue
        rows.append(dict(model=name,style=style,**metrics(g.y_true.to_numpy(),g.prob_ai.to_numpy(),threshold)))
    pd.DataFrame(rows).to_csv(OUT/f'per_style_{name}.csv',index=False)
    result['macro_style_auc']=float(np.mean([r['roc_auc'] for r in rows]));result['macro_style_f1']=float(np.mean([r['f1'] for r in rows]))
    pd.DataFrame(confusion_matrix(yt,p>=threshold),index=['Human','AI'],columns=['pred_Human','pred_AI']).to_csv(OUT/f'confusion_{name}.csv')
    fpr,tpr,rt=roc_curve(yt,p);pd.DataFrame(dict(fpr=fpr,tpr=tpr,threshold=rt)).to_csv(OUT/f'roc_{name}.csv',index=False)
    pr,re,pt=precision_recall_curve(yt,p);pd.DataFrame(dict(precision=pr,recall=re,threshold=np.r_[pt,np.nan])).to_csv(OUT/f'pr_{name}.csv',index=False)
    dest=OUT/'models';dest.mkdir(exist_ok=True)
    joblib.dump(dict(imputer=imputer,scaler=scaler,model=model,threshold=threshold,columns=columns,seed=SEED,cohort_manifest_sha256=json.loads((OUT/'control_gate.json').read_text())['manifest_sha256']),dest/f'{name}.joblib')
    save_json(f'metrics_{name}.json',result);print(result,flush=True)
    return result

def metadata_only():
    full=pd.read_parquet(OUT/'split_manifest.parquet');cohort=pd.read_parquet(OUT/'cohort_manifest.parquet')
    cols=['width','height','bytes','aspect','subsampling','progressive','qt_mean']
    output=[]
    for name,df in [('metadata_ungated_full',full),('metadata_gated',cohort[cohort.primary_eligible]),('dimensions_ungated_full',full),('filesize_ungated_full',full),('jpeg_ungated_full',full)]:
        use=['width','height','aspect'] if name.startswith('dimensions') else ['bytes'] if name.startswith('filesize') else ['subsampling','progressive','qt_mean'] if name.startswith('jpeg') else cols
        output.append(json.loads((OUT/f'metrics_{name}.json').read_text()) if (OUT/f'metrics_{name}.json').exists() else probe(name,df,df[use].to_numpy(dtype=float),use))
    save_json('metadata_probe_summary.json',output)
    from annotate_gate import main as annotate_gate
    annotate_gate()

def main():
    metadata_only()
    df=pd.read_parquet(OUT/'features_matched.parquet');df=df[df.primary_eligible].sort_values('artwork_id').reset_index(drop=True)
    cols=feature_columns(df)
    for name,features in [('handcrafted',cols),('frequency',[c for c in cols if c.startswith('fft_')])]:
        if not (OUT/f'metrics_{name}.json').exists():probe(name,df,df[features].to_numpy(dtype=float),features)
    ids=pd.read_csv(OUT/'embedding_ids.csv');indices=pd.Index(ids.artwork_id).get_indexer(df.artwork_id);assert min(indices)>=0
    for name in ['resnet50','dinov2']:
        state=json.loads((OUT/f'{name}_embedding_state.json').read_text());assert state['completed']==state['total']
        if not (OUT/f'metrics_{name}.json').exists():
            x=np.load(OUT/f'{name}_embeddings.npy',mmap_mode='r')[indices]
            probe(name,df,x,[f'{name}_{i}' for i in range(x.shape[1])])
    names=['handcrafted','frequency','metadata_gated','resnet50','dinov2','metadata_ungated_full','dimensions_ungated_full','filesize_ungated_full','jpeg_ungated_full']
    results=[json.loads((OUT/f'metrics_{name}.json').read_text()) for name in names]
    pd.DataFrame(results).to_csv(OUT/'baseline_metrics.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for name in names[:5]:
        roc=pd.read_csv(OUT/f'roc_{name}.csv');pr=pd.read_csv(OUT/f'pr_{name}.csv')
        axes[0].plot(roc.fpr,roc.tpr,label=name);axes[1].plot(pr.recall,pr.precision,label=name)
    axes[0].plot([0,1],[0,1],'k--',alpha=.3);axes[0].set(xlabel='False positive rate',ylabel='True positive rate',title='Matched test ROC (n=6,000)');axes[1].set(xlabel='Recall',ylabel='Precision',title='Matched test precision–recall')
    for ax in axes:ax.legend(fontsize=8)
    fig.suptitle('Native-256 JPEG-format matched test; encoding confounded and subjects unverified; descriptive',fontsize=10)
    fig.tight_layout();fig.savefig(OUT/'baseline_roc_pr.png',dpi=300);plt.close(fig)
    counts=pd.read_csv(OUT/'audit_counts.csv').pivot_table(index='style',columns='origin',values='count',aggfunc='sum').fillna(0)
    fig,axes=plt.subplots(1,2,figsize=(13,5));bottom=np.zeros(len(counts))
    for origin,color in [('Human','#0072B2'),('LD','#D55E00'),('SD','#009E73')]:
        axes[0].bar(counts.index,counts[origin],bottom=bottom,label=origin,color=color);bottom+=counts[origin].to_numpy()
    axes[0].tick_params(axis='x',rotation=45,labelsize=7);axes[0].set(title=f'Full release audit: n={int(counts.to_numpy().sum()):,}',ylabel='Artworks');axes[0].legend(fontsize=8)
    for name,label in [('metadata_ungated_full','Full: Human vs LD+SD'),('metadata_gated','Native256: Human vs LD'),('dimensions_ungated_full','Dimensions only, full')]:
        roc=pd.read_csv(OUT/f'roc_{name}.csv');score=json.loads((OUT/f'metrics_{name}.json').read_text())['roc_auc']
        axes[1].plot(roc.fpr,roc.tpr,label=f'{label}; AUC={score:.4f}')
    axes[1].plot([0,1],[0,1],'k--',alpha=.3);axes[1].set(xlabel='False positive rate',ylabel='True positive rate',title='Metadata probes; held-out source composition differs');axes[1].legend(fontsize=7)
    fig.suptitle('Resolution/encoding audit: SD native768 kept separate; JPEG quantization is origin-aligned',fontsize=11)
    fig.tight_layout();fig.savefig(OUT/'dataset_audit_metadata.png',dpi=300);plt.close(fig)
    from render_hc_atlas import main as render_hc_atlas
    from render_density import main as render_density
    from render_projection_audit import main as render_projection_audit
    render_hc_atlas();render_density();render_projection_audit()
    progress('Stage 5 complete', 'All five primary baselines evaluated on the frozen matched test split; full-release ungated metadata and dimensions-only probes evaluated separately. Metrics, per-style summaries, model caches, confusion matrices, ROC/PR coordinates and figures saved under results/. Stages 6+ intentionally not executed.')
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--metadata-only',action='store_true');args=parser.parse_args()
    if args.metadata_only:metadata_only()
    else:main()
