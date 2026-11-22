"""Synchronous, fail-fast Stage6–10 resume; never starts a background runner."""
from common import *
import subprocess

def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true',help='Regenerate figures, verify current caches/dashboard, then write the checkpoint');args=parser.parse_args()
    for name in ['resnet50','dinov2']:
        state=json.loads((OUT/f'{name}_embedding_state.json').read_text());assert state['completed']==45000
    analyses=[] if args.verify_only else ['src/drift.py','src/sensitivity_pixels.py','src/ablations.py','src/border_analysis.py','src/uncertainty_tables.py','src/visual_tables.py']
    for relative in analyses+['src/publication_figures.py','tests/test_drift.py','src/verify_dashboard.py','src/verify_stage10.py','src/finalize_stage10.py']:
        print('Running synchronously:',relative,flush=True)
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/relative)],cwd=ROOT,check=True,env=os.environ.copy())
if __name__=='__main__':main()
