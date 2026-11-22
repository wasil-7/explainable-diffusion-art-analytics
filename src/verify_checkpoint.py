"""Read-only integrity checks for the Stage 5 checkpoint, not later research stages."""
from common import *
import pandas as pd,numpy as np,hashlib,joblib
from sklearn.metrics import roc_auc_score,f1_score

def main():
    checks=[]
    def check(name,passed,detail=''):
        checks.append(dict(check=name,passed=bool(passed),detail=detail));assert passed,(name,detail)
    audit=pd.read_parquet(OUT/'audit_manifest.parquet');full=pd.read_parquet(OUT/'split_manifest.parquet');cohort=pd.read_parquet(OUT/'cohort_manifest.parquet');features=pd.read_parquet(OUT/'features_matched.parquet')
    check('Full file audit',len(audit)==185015 and audit.error.eq('').all())
    check('Full split covers every audited file',len(full)==185015 and set(full.artwork_id)==set(audit.artwork_id))
    check('Group split disjoint',full.groupby('group_id').split.nunique().max()==1)
    check('Exact hash split disjoint',full.groupby('sha256').split.nunique().max()==1)
    check('Known families split disjoint',full[full.family.ne('')].groupby('family').split.nunique().max()==1)
    edges=pd.read_parquet(OUT/'group_edges.parquet')
    check('All duplicate/family edges contained',np.array_equal(full.iloc[edges.row_a.to_numpy()].split.to_numpy(),full.iloc[edges.row_b.to_numpy()].split.to_numpy()))
    counts=cohort.groupby(['style','origin','split']).size()
    check('Balanced 45k cohort',len(cohort)==45000 and len(counts)==90 and set(counts)=={300,900})
    primary=cohort[cohort.primary_eligible]
    check('Only native256 Human LD in technical primary',len(primary)==30000 and set(primary.origin)=={'Human','LD'} and primary.width.eq(256).all() and primary.height.eq(256).all() and primary['format'].eq('JPEG').all())
    gate=json.loads((OUT/'control_gate.json').read_text())
    check('Frozen manifest unchanged',gate['manifest_sha256']==hashlib.sha256((OUT/'cohort_manifest.csv').read_bytes()).hexdigest())
    check('Subject uncertainty explicit',gate['confirmatory_subject_gate_passed'] is False)
    check('Encoding confound and confirmatory failure explicit',gate['jpeg_encoding_control_passed'] is False and gate['confirmatory_gate_passed'] is False)
    check('Feature IDs one-to-one',features.artwork_id.is_unique and set(features.artwork_id)==set(cohort.artwork_id))
    check('Synthetic feature unit tests',pd.read_csv(OUT/'unit_test_results.csv').passed.all())
    check('H normalized',features.H_pooled.between(0,1+1e-12).all())
    check('C normalized',features.C_pooled.between(-1e-12,1).all())
    scores=pd.read_csv(OUT/'projection_fidelity.csv')
    check('All tSNE runs with fidelity',len(scores)==15 and set(scores.perplexity)=={15,30,50} and scores[['trustworthiness','continuity']].ge(0).all().all() and scores[['trustworthiness','continuity']].le(1).all().all())
    check('Seed audit uses random initializations',scores.initialization.eq('random').all())
    primary_ids=set(primary[primary.split.eq('test')].artwork_id)
    metrics=pd.read_csv(OUT/'baseline_metrics.csv',float_precision='round_trip')
    for name in ['handcrafted','frequency','metadata_gated','resnet50','dinov2']:
        pred=pd.read_csv(OUT/f'predictions_{name}.csv',float_precision='round_trip')
        check(name+' same test IDs',set(pred.artwork_id)==primary_ids)
        row=metrics[metrics.model.eq(name)].iloc[0]
        check(name+' metric reproduction',abs(roc_auc_score(pred.y_true,pred.prob_ai)-row.roc_auc)<1e-12 and abs(f1_score(pred.y_true,pred.prob_ai>=row.threshold)-row.f1)<1e-12)
    for name in ['metadata_ungated_full','dimensions_ungated_full','filesize_ungated_full','jpeg_ungated_full']:
        row=metrics[metrics.model.eq(name)].iloc[0]
        check(name+' uses full release',row.development_n+row.validation_n+row.n==185015)
    for name in ['resnet50','dinov2']:
        state=json.loads((OUT/f'{name}_embedding_state.json').read_text())
        array=np.load(OUT/f'{name}_embeddings.npy',mmap_mode='r')
        check(name+' complete CUDA cache',state['completed']==45000 and state['fp16'] and state['device']=='cuda:0' and np.isfinite(array).all())
    cross=pd.read_csv(OUT/'literature_crosswalk.csv');lit=pd.read_csv(OUT/'literature_facts.csv')
    check('18 paper entries deduplicated to16',len(cross)==18 and cross.paper_id.nunique()==16 and lit.paper_id.nunique()==16)
    expected_sha={f'{phase}/{r.number}':r.sha256 for phase in ['Phase1','Phase2'] for r in pd.read_csv(ROOT/phase/'Sources.csv').itertuples()}
    check('Paper hashes agree with source indexes',all(r.sha256==expected_sha[r.crosswalk_id] for r in cross.itertuples()))
    pd.DataFrame(checks).to_csv(OUT/'checkpoint_integrity_checks.csv',index=False)
    # Reproduce held-out probabilities from frozen model/preprocessing in this fresh process.
    d=features[features.primary_eligible & features.split.eq('test')].sort_values('artwork_id')
    frozen=joblib.load(OUT/'models/handcrafted.joblib')
    x=frozen['scaler'].transform(frozen['imputer'].transform(d[frozen['columns']].to_numpy(dtype=float)))
    p=frozen['model'].predict_proba(x)[:,1];cached=pd.read_csv(OUT/'predictions_handcrafted.csv',float_precision='round_trip').set_index('artwork_id').loc[d.artwork_id]
    check('Fresh-process handcrafted probabilities',np.max(np.abs(p-cached.prob_ai.to_numpy()))<1e-12)
    pd.DataFrame(checks).to_csv(OUT/'checkpoint_integrity_checks.csv',index=False)
    save_json('checkpoint_verification.json',dict(passed=True,checks=len(checks),stages_completed=[0,1,2,3,4,5],stages_not_run=list(range(6,13))))
    pca=json.loads((OUT/'pca_summary.json').read_text())
    lines=['# Stage 5 checkpoint','', 'Completed Stages 0–5 only. Stages 6–12 were not executed.','',
           f'Audit: {len(audit):,} files. Balanced cohort: {len(cohort):,} artworks. Native-256 Human–LD technical cohort: {len(primary):,}; held-out primary test: {len(primary_ids):,}.',
           '', '**Interpretation:** Native dimensions, style and JPEG format are matched. Subjects are unverified and JPEG quantization is aligned with origin; the full confirmatory gate fails. Gated metadata AUROC is '+str(gate['gated_metadata_roc_auc'])+'. All comparisons are descriptive and do not establish content differences independent of encoding. SD remains a separate resolution-confounded sensitivity cache. See CONTROL_GATE_LIMITATIONS.md.','',
           '| Primary probe | Accuracy | Balanced accuracy | F1 (AI) | AUROC | ECE |','|---|---:|---:|---:|---:|---:|']
    for r in metrics.iloc[:5].itertuples():
        lines.append(f'| {r.model} | {r.accuracy} | {r.balanced_accuracy} | {r.f1} | {r.roc_auc} | {r.ece} |')
    lines+=['','Values above use the saved CSV precision. Per-style macro AUROC/F1, thresholds, regularization, confusion matrices, ROC/PR coordinates and validation tuning scores are in results/.','',
            '## Separate full-release metadata audit','', '| Probe | Test n | AUROC | Balanced accuracy |','|---|---:|---:|---:|']
    for r in metrics.iloc[5:].itertuples():lines.append(f'| {r.model} | {r.n} | {r.roc_auc} | {r.balanced_accuracy} |')
    lines+=['','Full-release probes compare Human with LD+SD; gated probes compare Human with LD. Their source compositions differ, so score changes are not a causal estimate of resolution effects.','',
            f'PCA explained variance ratios (development-fitted, three fixed axes): {pca["explained_variance_ratio"]}.',
            f't-SNE: {len(scores)} runs, five seeds × perplexities 15/30/50; fixed balanced subset n=3,000. Trustworthiness range: {scores.trustworthiness.min()}–{scores.trustworthiness.max()}; continuity range: {scores.continuity.min()}–{scores.continuity.max()} (k=15).',
            f'Integrity checks passed: {len(checks)}. Synthetic feature tests passed: {len(pd.read_csv(OUT/"unit_test_results.csv"))}.',
            '', '## Artifacts','',
            '- Data: audit_manifest.parquet; split_manifest.parquet; cohort_manifest.csv; features_matched.parquet; resnet50_embeddings.npy; dinov2_embeddings.npy; embedding_ids.csv.',
            '- Gate/evidence: control_gate.json; metadata_field_audit.csv; literature_facts.csv; literature_crosswalk.csv; REVIEW_NOTES.md; environment.json.',
            '- Projections: pca_coordinates.parquet; pca_loadings.csv; pca_summary.json; pca_projection_fidelity.csv; projection_fidelity.csv; tsne/.',
            '- Figures: hc_atlas.png; hc_density_atlas.png; pca_3d.png; pca_tsne_audit.png; baseline_roc_pr.png; dataset_audit_metadata.png.',
            '- Verification: checkpoint_integrity_checks.csv; checkpoint_verification.json; unit_test_results.csv.',
            '', 'Reproduction commands are in the root README.md. Root PROGRESS.md records completed stages. No final report or dashboard was created at this checkpoint.','']
    (OUT/'CHECKPOINT_SUMMARY.md').write_text('\n'.join(lines),encoding='utf-8')
    progress('Stage 5 checkpoint verified','Fresh-process integrity checks passed, including full-release audit, grouped-family leakage checks, frozen manifest checksum, same held-out IDs for all primary baselines, cached metric reproduction and frozen-model probability reproduction. Stopped before Stage 6.')
if __name__=='__main__':main()
