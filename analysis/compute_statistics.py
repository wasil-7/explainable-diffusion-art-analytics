"""Supplementary analysis; read original caches, write only m4_final/results."""
from pathlib import Path
import os,sys,time,json,hashlib
os.environ['PYTHONDONTWRITEBYTECODE']='1'
B=Path(__file__).resolve().parent; ROOT=B.parent
sys.path.insert(0,str(ROOT/'src'))
from common import pd
import numpy as np
from baselines import feature_columns,metrics
from ablations import resamples,auc,binary_f1
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler,StandardScaler
from sklearn.linear_model import LogisticRegression,LogisticRegressionCV
from sklearn.model_selection import PredefinedSplit
from sklearn.metrics import precision_recall_curve
from threadpoolctl import threadpool_limits
O=B/'results';O.mkdir(exist_ok=True)
def bootstrap():
 start=time.time();names=['handcrafted','frequency','metadata_gated','resnet50','dinov2']
 preds={n:pd.read_csv(ROOT/'results'/f'predictions_{n}.csv',float_precision='round_trip').sort_values('artwork_id').reset_index(drop=True) for n in names}
 d=preds[names[0]];y=d.y_true.to_numpy().astype(bool)
 for p in preds.values():assert p.artwork_id.equals(d.artwork_id) and p.y_true.equals(d.y_true)
 point={n:[auc(y,p.prob_ai.to_numpy()),binary_f1(y,p.pred_ai.to_numpy().astype(bool))] for n,p in preds.items()}
 boot=np.empty((1000,5,2))
 for b,ix in enumerate(resamples(d)):
  for j,n in enumerate(names):
   p=preds[n];boot[b,j]=[auc(y[ix],p.prob_ai.to_numpy()[ix]),binary_f1(y[ix],p.pred_ai.to_numpy().astype(bool)[ix])]
 rows=[]
 original=pd.read_csv(ROOT/'results/baseline_metrics.csv').set_index('model')
 for j,n in enumerate(names):
  assert abs(point[n][0]-original.loc[n,'roc_auc'])<1e-12
  assert abs(point[n][1]-original.loc[n,'f1'])<1e-12
  ci=np.percentile(boot[:,j,:],[2.5,97.5],axis=0)
  rows.append(dict(model=n,roc_auc=point[n][0],auc_low=ci[0,0],auc_high=ci[1,0],f1=point[n][1],f1_low=ci[0,1],f1_high=ci[1,1],resamples=1000,groups=d.group_id.nunique()))
 pd.DataFrame(rows).to_csv(O/'baseline_group_ci.csv',index=False)
 rows=[]
 for n in ['frequency','resnet50','dinov2']:
  j=names.index(n);delta=boot[:,0,0]-boot[:,j,0];lo,hi=np.percentile(delta,[2.5,97.5])
  rows.append(dict(comparison='handcrafted minus '+n,delta_auc=point['handcrafted'][0]-point[n][0],ci_low=lo,ci_high=hi,resamples=1000,zero_excluded=bool(lo>0 or hi<0)))
 pd.DataFrame(rows).to_csv(O/'paired_probe_differences.csv',index=False);np.savez_compressed(O/'baseline_bootstrap_draws.npz',values=boot,models=names)
 print('Frozen-split point estimates unchanged; 1000 paired source-group draws completed.',flush=True)
def repartitions():
 start=time.time()
 import duckdb
 df=duckdb.sql('SELECT * FROM read_parquet(?)',params=[str(ROOT/'results/features_matched.parquet')]).df()
 df=df[df.primary_eligible].sort_values('artwork_id').reset_index(drop=True)
 cols=feature_columns(df);meta=['width','height','bytes','aspect','subsampling','progressive','qt_mean']
 metadata=pd.read_csv(ROOT/'results/cohort_manifest.csv').set_index('artwork_id').loc[df.artwork_id]
 matrices={'handcrafted':df[cols].to_numpy(float),'frequency':df[[c for c in cols if c.startswith('fft_')]].to_numpy(float),'metadata_gated':metadata[meta].to_numpy(float)}
 ids=pd.read_csv(ROOT/'results/embedding_ids.csv');indices=pd.Index(ids.artwork_id).get_indexer(df.artwork_id);assert indices.min()>=0
 for name in ['resnet50','dinov2']:matrices[name]=np.load(ROOT/'results'/f'{name}_embeddings.npy',mmap_mode='r')[indices]
 cells=sorted(set(zip(df['style'],df.origin)));ci=np.array([cells.index(c) for c in zip(df['style'],df.origin)]);groups=df.groupby('group_id',sort=True).indices
 target=np.array([.6,.2,.2])[:,None]*np.bincount(ci,minlength=len(cells));allrows=pd.read_csv(O/'multiseed_metrics.csv').to_dict('records') if (O/'multiseed_metrics.csv').exists() else [];splitrows=[]
 for seed in [43,44,45,46,47]:
  rng=np.random.default_rng(seed);keys=list(groups);rng.shuffle(keys);keys.sort(key=lambda k:-len(groups[k]));current=np.zeros_like(target);assign={}
  for key in keys:
   counts=np.bincount(ci[groups[key]],minlength=len(cells));cost=[np.sum(((current[s]+counts-target[s])**2-(current[s]-target[s])**2)/np.maximum(target[s],1)) for s in range(3)];s=int(np.argmin(cost));assign[key]=s;current[s]+=counts
  split=df.group_id.map(assign).to_numpy();train,val,test=[split==i for i in range(3)]
  manifest=df[['artwork_id','origin','style','group_id']].copy();manifest['split']=np.array(['development','validation','test'])[split];manifest.to_csv(O/f'split_seed_{seed}.csv',index=False)
  assert manifest.groupby('group_id').split.nunique().max()==1
  for i,label in enumerate(['development','validation','test']):splitrows.append(dict(seed=seed,split=label,n=int((split==i).sum()),groups=df.loc[split==i,'group_id'].nunique()))
  yy=df.origin.ne('Human').to_numpy().astype(int)
  for name,x in matrices.items():
   if any(r['seed']==seed and r['model']==name for r in allrows):continue
   tick=time.time();imp=SimpleImputer(strategy='median',keep_empty_features=True);scaler=StandardScaler() if name in ['resnet50','dinov2'] else RobustScaler();xt=scaler.fit_transform(imp.fit_transform(x[train]));xv=scaler.transform(imp.transform(x[val]));xe=scaler.transform(imp.transform(x[test]))
   fold=PredefinedSplit(np.r_[np.full(train.sum(),-1),np.zeros(val.sum(),dtype=int)])
   tune=LogisticRegressionCV(Cs=[.001,.01,.1,1,10,100],cv=fold,scoring='roc_auc',max_iter=2000,solver='lbfgs',refit=False,n_jobs=1,random_state=seed).fit(np.concatenate([xt,xv]),np.r_[yy[train],yy[val]])
   c=float(tune.C_[0]);model=LogisticRegression(C=c,max_iter=2000,random_state=seed).fit(xt,yy[train]);pv=model.predict_proba(xv)[:,1];p,r,ts=precision_recall_curve(yy[val],pv);f=2*p[:-1]*r[:-1]/np.maximum(p[:-1]+r[:-1],1e-12);threshold=float(ts[np.argmax(f)])
   prob=model.predict_proba(xe)[:,1];result=metrics(yy[test],prob,threshold);result.update(seed=seed,model=name,C=c,seconds=time.time()-tick,development_n=int(train.sum()),validation_n=int(val.sum()));allrows.append(result)
   pred=manifest.loc[test].copy();pred['y_true']=yy[test];pred['prob_ai']=prob;pred['pred_ai']=prob>=threshold;pred.to_csv(O/f'predictions_seed{seed}_{name}.csv',index=False)
   pd.DataFrame(allrows).to_csv(O/'multiseed_metrics.csv',index=False)
   print(seed,name,result['roc_auc'],result['f1'],flush=True)
 pd.DataFrame(allrows).to_csv(O/'multiseed_metrics.csv',index=False);pd.DataFrame(splitrows).to_csv(O/'multiseed_split_counts.csv',index=False)
 summary=pd.DataFrame(allrows).groupby('model').agg(auc_mean=('roc_auc','mean'),auc_sd=('roc_auc','std'),f1_mean=('f1','mean'),f1_sd=('f1','std'),runs=('seed','nunique')).reset_index();summary.to_csv(O/'multiseed_summary.csv',index=False)
 protocol=dict(bootstrap_seed=42,bootstrap_draws=1000,bootstrap='Origin-stratified source-group resampling, same indices for every probe; percentile intervals; frozen fits and thresholds.',split_seeds=[43,44,45,46,47],scope='Regroup the same frozen 30000-artwork primary cohort; transitive group identities preserved; greedy style/origin-balanced 60:20:20 allocation; all five probes retune C and threshold within each development/validation split. Cached frozen encoder embeddings reused; no new embedding extraction.',limitations='Conditional on the original selected cohort and cached features. These are five grouped repartitions, not five independent data collections. Original seed42 point estimates remain authoritative.',seconds_this_resume=time.time()-start,initial_three_probe_run_seconds=35.907137870788574)
 protocol['feature_calibration']='Original seed42 development-calibrated feature thresholds fixed across repartitions; only imputer/scaler/C/F1 threshold refitted. Conditional split sensitivity, not full pipeline replication.'
 (O/'supplementary_statistics_protocol.json').write_text(json.dumps(protocol,indent=2),encoding='utf8');print(summary.to_string(index=False),flush=True)
if __name__=='__main__':
 with threadpool_limits(limits=1):
  if not (O/'baseline_group_ci.csv').exists():bootstrap()
  repartitions()
