from common import *
import pandas as pd, numpy as np, hashlib, re
from collections import defaultdict

def main():
    start=time.time(); df=pd.read_parquet(OUT/'audit_manifest.parquet')
    assert len(df)==185015, f'Unexpected release size: {len(df)}'
    assert df.error.eq('').all()
    df.groupby('origin').agg(files=('artwork_id','size'),exif_present=('exif','sum'),icc_present=('icc','sum')).reset_index().to_csv(OUT/'header_presence_counts.csv',index=False)
    n=len(df); parent=np.arange(n); size=np.ones(n,dtype=int)
    def find(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]]; a=parent[a]
        return a
    def union(a,b):
        a,b=find(a),find(b)
        if a==b:return
        if size[a]<size[b]:a,b=b,a
        parent[b]=a;size[a]+=size[b]
    edges=[]
    def link(keys,reason):
        seen={}
        for i,k in enumerate(keys):
            if not k:continue
            if k in seen:union(i,seen[k]);edges.append((i,seen[k],reason))
            else:seen[k]=i
    link(df.sha256,'sha256')
    ph=[int(x,16) for x in df.phash];dh=[int(x,16) for x in df.dhash]
    # Any 64-bit pair <=4 bits differs in at most four of these five blocks.
    # Thus at least one block matches, making this exhaustive for threshold 4.
    buckets=[defaultdict(list) for _ in range(5)]
    boundaries=[(0,13),(13,13),(26,13),(39,13),(52,12)]
    for i,h in enumerate(ph):
        candidates=set()
        for b,(shift,bits) in enumerate(boundaries):candidates.update(buckets[b][(h>>shift)&((1<<bits)-1)])
        for j in candidates:
            if (h^ph[j]).bit_count()<=4 and (dh[i]^dh[j]).bit_count()<=4:
                union(i,j);edges.append((i,j,'phash<=4 AND dhash<=4'))
        for b,(shift,bits) in enumerate(boundaries):buckets[b][(h>>shift)&((1<<bits)-1)].append(i)
        if i%30000==0:print('grouping',i,'seconds',round(time.time()-start),flush=True)
    families=[]; family_kind=[]
    for row in df.itertuples():
        stem=Path(row.path).stem
        if row.origin=='Human' and '_' in stem:
            family='artist:'+stem.split('_')[0].lower(); kind='filename artist prefix'
        elif row.origin!='Human' and re.fullmatch(r'\d+-\d+-\d+',stem):
            family='generated-prefix:'+stem.rsplit('-',1)[0];kind='conservative repeated filename prefix; semantics unverified'
        else:family='';kind='unavailable'
        families.append(family);family_kind.append(kind)
    link(families,'filename family')
    df['family']=families;df['family_kind']=family_kind
    pd.DataFrame([
        dict(field='style',availability='all files',source='parent directory; ukiyo_e normalized to ukiyo-e',interpretation='Provided style labels, not verified artwork dates'),
        dict(field='origin/generator',availability='all files',source='AI_LD_, AI_SD_, or human directory',interpretation='Release generator family only; exact versions unknown'),
        dict(field='artist',availability=f'{sum(k=="filename artist prefix" for k in family_kind)} files',source='Human filename text before first underscore, when present',interpretation='Conservative string family; unparsed names remain unavailable'),
        dict(field='generated family',availability=f'{sum(k.startswith("conservative") for k in family_kind)} files',source='First two of three hyphen-separated numeric filename fields',interpretation='Conservative grouping key; not verified prompt/source-work identity'),
        dict(field='subject/prompt text',availability='no verified matching metadata',source='No supplied sidecar metadata; numeric names lack subject text; 60 directory-stratified JPEG headers had no text fields, see jpeg_metadata_header_sample.json',interpretation='Header-text check is sampled, not exhaustive COM-tag absence proof. No subject matching claimed; all subject-uncertain cells descriptive'),
        dict(field='source-work link',availability='unverified',source='Duplicate hashes and filename prefixes only',interpretation='No complete derivative linkage can be guaranteed'),
        dict(field='creation year',availability='partial ambiguous filename strings',source='Not parsed into a verified field',interpretation='Style is not interpreted as a chronological label'),
        dict(field='technical metadata',availability='all successfully decoded files',source='PIL headers, raw bytes, JPEG tables',interpretation='Dimensions, format, color, bytes, subsampling, progressive, quantization, ICC, EXIF')
    ]).to_csv(OUT/'metadata_field_audit.csv',index=False)
    roots=[find(i) for i in range(n)]
    labels={r:df.iloc[r].artwork_id for r in set(roots)}
    df['group_id']=[labels[r] for r in roots]
    edge_df=pd.DataFrame(edges,columns=['row_a','row_b','reason'])
    edge_df.to_parquet(OUT/'group_edges.parquet',index=False)
    save_json('duplicate_group_summary.json',dict(edge_counts=edge_df.reason.value_counts().to_dict(),thresholds='pHash<=4 AND dHash<=4; prespecified before split; no labels used',exact_duplicate_files=int(df.sha256.duplicated(keep=False).sum()),near_edges=int(edge_df.reason.eq('phash<=4 AND dhash<=4').sum()),source_links='only detected image-equivalence and conservative filename families; verified source links unavailable'))
    # Random-order group allocation minimizes relative squared cell-count error.
    cells=sorted(set(zip(df['style'],df.origin)));cellidx={c:i for i,c in enumerate(cells)}
    ci=np.array([cellidx[x] for x in zip(df['style'],df.origin)])
    groups=df.groupby('group_id',sort=True).indices
    totals=np.bincount(ci,minlength=len(cells));target=np.array([.6,.2,.2])[:,None]*totals
    current=np.zeros_like(target); rng=np.random.default_rng(SEED)
    keys=list(groups);rng.shuffle(keys);keys.sort(key=lambda k:-len(groups[k]))
    assignments={}
    for k in keys:
        counts=np.bincount(ci[groups[k]],minlength=len(cells))
        costs=[np.sum(((current[s]+counts-target[s])**2-(current[s]-target[s])**2)/np.maximum(target[s],1)) for s in range(3)]
        s=int(np.argmin(costs));assignments[k]=['development','validation','test'][s];current[s]+=counts
    df['split']=df.group_id.map(assignments)
    df.to_parquet(OUT/'split_manifest.parquet',index=False)
    df.groupby(['style','origin','split']).size().rename('n').reset_index().to_csv(OUT/'full_split_counts.csv',index=False)
    df.groupby(['style','origin','split']).agg(artworks=('artwork_id','size'),source_groups=('group_id','nunique')).reset_index().to_csv(OUT/'full_split_group_counts.csv',index=False)
    selected=[]
    for (style,origin,split),sub in df.groupby(['style','origin','split'],sort=True):
        quota=900 if split=='development' else 300
        # Distinct exact images; related groups already assigned exclusively.
        sub=sub.sort_values('artwork_id').drop_duplicates('sha256')
        assert len(sub)>=quota,(style,origin,split,len(sub))
        selected.append(sub.sample(n=quota,random_state=SEED))
    cohort=pd.concat(selected).sort_values('artwork_id')
    cohort['primary_eligible']=cohort.origin.isin(['Human','LD']) & cohort.width.eq(256)&cohort.height.eq(256)&cohort['format'].eq('JPEG')
    cohort['analysis_role']=np.where(cohort.primary_eligible,'primary native-256 Human vs LD','descriptive SD resolution-confounded')
    cohort.to_csv(OUT/'cohort_manifest.csv',index=False)
    cohort.to_parquet(OUT/'cohort_manifest.parquet',index=False)
    cohort.groupby(['style','origin','split','primary_eligible']).size().rename('n').reset_index().to_csv(OUT/'cohort_counts.csv',index=False)
    cohort.groupby(['style','origin','split','primary_eligible']).agg(artworks=('artwork_id','size'),distinct_exact_images=('sha256','nunique'),source_groups=('group_id','nunique')).reset_index().to_csv(OUT/'cohort_group_counts.csv',index=False)
    assert df.groupby('group_id').split.nunique().max()==1
    assert df.groupby('sha256').split.nunique().max()==1
    primary=cohort[cohort.primary_eligible]
    testcounts=primary[primary.split.eq('test')].groupby(['style','origin']).size()
    assert len(testcounts)==20 and testcounts.min()>=200
    gate=dict(passed=True,seed=SEED,cohort_n=len(cohort),primary_n=len(primary),minimum_primary_test_cell=int(testcounts.min()),split='grouped 60:20:20',near_duplicate_rule='64-bit pHash <=4 AND dHash <=4; exhaustive multi-index search; transitive closure with SHA256 and filename families',family_semantics='Human artist prefix where underscore exists; AI first two numeric fields grouped conservatively across generators and styles; unverified as actual prompt IDs',subject_match='No verified subject/prompt text supplied. Subject matching cannot be claimed. Primary is file/style-controlled only; subject-control component of G3 unresolved.',sd='separate descriptive sensitivity, bilinear resized for standardized feature extraction',group_count=len(groups),max_group_size=int(df.groupby('group_id').size().max()),edges=len(edges),manifest_sha256=hashlib.sha256((OUT/'cohort_manifest.csv').read_bytes()).hexdigest(),seconds=time.time()-start)
    save_json('control_gate.json',gate)
    gate['confirmatory_subject_gate_passed']=False
    gate['interpretation']='All cells descriptive under Milestone2 Step5 because subject matches are uncertain; passed refers to file/style/support gate only.'
    save_json('control_gate.json',gate)
    progress('Stage 2 complete: Step 5 file-control gate frozen',f'{len(cohort):,} balanced artworks, {len(primary):,} primary; minimum {testcounts.min()} test images/origin/style. Group closure includes duplicates and filename families. Subject metadata unavailable; no subject matching claimed. Manifest SHA256: {gate["manifest_sha256"]}.')
if __name__=='__main__':main()
