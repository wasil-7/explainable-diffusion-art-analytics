"""Additional conditional source-group intervals for stress and failure associations."""
from common import *
from ablations import resamples,auc,aligned_predictions
import numpy as np

def main():
    f=pd.read_parquet(OUT/'features_matched.parquet');d=f[f.primary_eligible&f.split.eq('test')].sort_values('artwork_id').reset_index(drop=True);y=d.origin.ne('Human').to_numpy();draws=list(resamples(d));rows=[]
    for view in ['original','jpeg95','jpeg75','jpeg50','resize0.5','resize0.75']:
        p=aligned_predictions('handcrafted' if view=='original' else view,d).prob_ai.to_numpy();vals=[auc(y[v],p[v]) for v in draws];rows.append(dict(view=view,roc_auc=auc(y,p),auc_ci_low=np.percentile(vals,2.5),auc_ci_high=np.percentile(vals,97.5)))
    pd.DataFrame(rows).to_csv(OUT/'perturbation_auc_intervals.csv',index=False)
    flags=pd.read_csv(OUT/'failure_trigger_flags.csv').set_index('artwork_id').loc[d.artwork_id];pred=aligned_predictions('handcrafted',d);errors=(pred.pred_ai!=pred.y_true).to_numpy();rows=[]
    for trigger in ['low_saturation','flat_color','high_frequency','heavy_border']:
        flag=flags[trigger].to_numpy();gap=errors[flag].mean()-errors[~flag].mean();boots=[]
        for ix in draws:
            v=flag[ix];e=errors[ix];boots.append(e[v].mean()-e[~v].mean())
        rows.append(dict(trigger=trigger,error_rate_gap_flag_minus_unflagged=gap,gap_ci_low=np.percentile(boots,2.5),gap_ci_high=np.percentile(boots,97.5),bootstrap_resamples=1000,interpretation='Descriptive association; overlapping triggers and encoding/source composition uncontrolled.'))
    pd.DataFrame(rows).to_csv(OUT/'failure_trigger_associations.csv',index=False)
if __name__=='__main__':main()
