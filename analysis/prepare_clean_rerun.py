"""Archive derived state before empirical replication in an ISOLATED workcopy.

Does not run models, extract images, or delete files. Never use on the only
authoritative evidence copy. The supplied publication package is immutable evidence.
"""
from pathlib import Path
import argparse,shutil,datetime,json
def prepare(root):
 root=Path(root).resolve();results=(root/'results').resolve();analysis=(root/'analysis/results').resolve()
 assert (root/'src/common.py').is_file() and (root/'README.md').is_file(),'Not a release working-copy root'
 assert results.is_relative_to(root) and analysis.is_relative_to(root)
 facts=results/'literature_facts.csv';assert facts.is_file(),'Required input results/literature_facts.csv missing'
 content=facts.read_bytes();stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');archive=(root/'reproduction_before'/stamp).resolve()
 assert archive.is_relative_to(root) and not archive.exists();archive.mkdir(parents=True)
 for source,name in [(results,'results'),(analysis,'analysis_results')]:
  if source.exists():
   target=(archive/name).resolve();assert source.is_relative_to(root) and target.is_relative_to(root);shutil.move(str(source),str(target))
 results.mkdir();(results/'literature_facts.csv').write_bytes(content);analysis.mkdir(parents=True,exist_ok=True)
 receipt=dict(root=str(root),preserved_archive=str(archive),new_results_input='literature_facts.csv',status='Prepared empty derived-state folders; no experiment executed',warning='Run ordered archive-dependent commands next and compare the frozen cohort IDs/hash before accepting results.')
 (archive/'preparation.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');return receipt
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--confirm-working-copy',action='store_true',required=True,help='Acknowledge this is an isolated reproduction copy, not the authoritative delivered evidence');a=p.parse_args()
 print(json.dumps(prepare(Path(__file__).resolve().parent.parent),indent=2))
