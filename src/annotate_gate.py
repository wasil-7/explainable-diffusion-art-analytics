"""Document measured residual confounding without changing frozen IDs or preprocessing."""
from common import *
import pandas as pd
def main():
    enc=pd.read_csv(OUT/'audit_encoding_counts.csv')
    keys=['origin','subsampling','progressive','qt_hash','qt_mean']
    profiles=enc.groupby(keys,dropna=False)['count'].sum().reset_index()
    profiles.to_csv(OUT/'jpeg_origin_profiles.csv',index=False)
    human=set(profiles.loc[profiles.origin.eq('Human'),'qt_hash'])
    ld=set(profiles.loc[profiles.origin.eq('LD'),'qt_hash'])
    primary=profiles[profiles.origin.isin(['Human','LD'])]
    identical=primary[['subsampling','progressive','qt_hash','qt_mean']].drop_duplicates().shape[0]==1
    gate=json.loads((OUT/'control_gate.json').read_text())
    gate['jpeg_quantization_common_support_human_ld']=len(human & ld)
    gate['jpeg_encoding_control_passed']=bool(identical)
    gate['jpeg_origin_profiles']=profiles.to_dict('records')
    gate['gated_metadata_roc_auc']=json.loads((OUT/'metrics_metadata_gated.json').read_text())['roc_auc']
    gate['full_jpeg_header_roc_auc']=json.loads((OUT/'metrics_jpeg_ungated_full.json').read_text())['roc_auc']
    gate['confirmatory_gate_passed']=bool(gate['passed'] and gate['confirmatory_subject_gate_passed'] and identical)
    gate['interpretation']='Native dimensions/style/JPEG-format gate passes. Full confirmatory gate fails: subjects unverified and JPEG quantization aligned with origin. All comparisons descriptive; no attribution independent of encoding is established.'
    save_json('control_gate.json',gate)
    text='# Control-gate limitations\n\nThe frozen native-dimension, style and JPEG-format cohort is unchanged. It is descriptive: verified subject matching is unavailable and JPEG quantization has no common support between Human and LD in this release.\n\n'
    text+=f'Gated metadata AUROC: {gate["gated_metadata_roc_auc"]}. Full-release JPEG-header-only AUROC: {gate["full_jpeg_header_roc_auc"]}. Classification performance cannot establish content differences independent of encoding.\n\n'
    text+='| Origin | Files | Mean quantization-table value | Table hash |\n|---|---:|---:|---|\n'
    for r in profiles.itertuples():text+=f'| {r.origin} | {r.count} | {r.qt_mean} | {r.qt_hash} |\n'
    text+='\nThese are observed table values, not inferred JPEG quality settings. No cohort IDs, scaling rules, model parameters or thresholds were changed in response to the test results.\n'
    (OUT/'CONTROL_GATE_LIMITATIONS.md').write_text(text,encoding='utf-8')
    print('Gate annotated: subject and JPEG-quantization controls unresolved; frozen cohort unchanged',flush=True)
if __name__=='__main__':main()
