"""Run independent Stage 5 CPU probes; the final pass reuses their frozen caches."""
from common import *
from baselines import metadata_only,probe,feature_columns
import pandas as pd
def main():
    metadata_only()
    df=pd.read_parquet(OUT/'features_matched.parquet')
    df=df[df.primary_eligible].sort_values('artwork_id').reset_index(drop=True)
    cols=feature_columns(df)
    for name,features in [('handcrafted',cols),('frequency',[c for c in cols if c.startswith('fft_')])]:
        if not (OUT/f'metrics_{name}.json').exists():probe(name,df,df[features].to_numpy(dtype=float),features)
    print('Independent Stage 5 tabular probes complete; caches frozen',flush=True)
if __name__=='__main__':main()
