"""Read-only import diagnostics: log which installed DLL is being loaded."""
import os,sys,faulthandler
os.environ.update(PIP_CACHE_DIR=r'D:\Dev\pip_cache',TEMP=r'D:\Dev\tmp',TMP=r'D:\Dev\tmp',TORCH_HOME=r'D:\Dev\torch_cache',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
faulthandler.enable();faulthandler.dump_traceback_later(60,repeat=True)
last=None
def trace(frame,event,arg):
    global last
    if frame.f_code.co_name!='_load_dll_libraries':return None
    dll=frame.f_locals.get('dll')
    if dll and dll!=last:
        print('Loading installed DLL:',dll,flush=True);last=dll
    return trace
sys.settrace(trace)
import torch
sys.settrace(None);faulthandler.cancel_dump_traceback_later()
print('Torch import complete:',torch.__version__,'CUDA:',torch.cuda.is_available(),flush=True)
