"""Execute only Stages 0–5. Audit may already be running separately."""
from common import *
import subprocess,sys,importlib
def run(script,*args):
    print('START',script,*args,flush=True)
    if script in ['tests/test_features.py','src/deep.py','src/verify_checkpoint.py']:
        subprocess.run([sys.executable,str(ROOT/script),*args],cwd=ROOT,env=os.environ.copy(),check=True)
    else:
        assert not args
        importlib.import_module(Path(script).stem).main()
    print('DONE',script,flush=True)
def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--wait-for-audit',action='store_true');p.add_argument('--from-stage4',action='store_true');p.add_argument('--from-stage5',action='store_true');a=p.parse_args()
    if a.from_stage5:
        run('src/deep.py');run('src/baselines.py');run('src/verify_checkpoint.py')
        return
    if a.from_stage4:
        run('src/projections.py');run('src/deep.py');run('src/baselines.py');run('src/verify_checkpoint.py')
        return
    if a.wait_for_audit:
        while not (OUT/'audit_summary.json').exists():time.sleep(10)
    else:
        run('src/orientation.py');run('src/audit.py')
    run('src/inspect_metadata_headers.py')
    run('src/splits.py')
    run('tests/test_features.py')
    run('src/extract_features.py')
    run('src/projections.py')
    run('src/deep.py')
    run('src/baselines.py')
    run('src/verify_checkpoint.py')
if __name__=='__main__':main()
