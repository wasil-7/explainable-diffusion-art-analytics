import os
os.environ['PIP_CACHE_DIR'] = r'D:\Dev\pip_cache'
os.environ['TEMP'] = r'D:\Dev\tmp'
os.environ['TMP'] = r'D:\Dev\tmp'
os.environ['TORCH_HOME'] = r'D:\Dev\torch_cache'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from pathlib import Path
import json, time
import sys
if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
# Arrow is optional here. A partially permitted Arrow installation can load its
# base module while Windows blocks its compute DLL, which otherwise prevents
# pandas itself from importing. Treat that optional integration as unavailable;
# never change host policy or attempt to load the blocked binary by another path.
try:
    import pyarrow.compute
except (ImportError, OSError):
    for module_name in list(sys.modules):
        if module_name=='pyarrow' or module_name.startswith('pyarrow.'):
            del sys.modules[module_name]
    sys.modules['pyarrow']=None
import pandas as pd
if sys.modules.get('pyarrow','not-loaded') is None:
    # pandas has recorded Arrow as unavailable. Remove the temporary sentinel so
    # other libraries' sys.modules probes do not mistake it for a loaded module.
    del sys.modules['pyarrow']
pd.options.io.parquet.engine = 'fastparquet'
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results'
DATA = ROOT/'data/archive/Real_AI_SD_LD_Dataset'
SEED = 42
OUT.mkdir(exist_ok=True)
def save_json(name, obj):
    (OUT/name).write_text(json.dumps(obj, indent=2, default=str), encoding='utf-8')
def progress(stage, detail):
    p=ROOT/'PROGRESS.md'
    with p.open('a',encoding='utf-8') as f:
        f.write(f'\n## {stage}\n\n{detail}\n')
    print(stage, detail, flush=True)
