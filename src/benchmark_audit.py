from common import *
from audit import inspect_file
from concurrent.futures import ThreadPoolExecutor
def main():
    folder=DATA/'train/AI_SD_art_nouveau'
    paths=[f'train/AI_SD_art_nouveau/{name}' for name in sorted(os.listdir(folder))[:600]]
    rows=[]
    for j,workers in enumerate([12,32,64]):
        sample=paths[j*200:(j+1)*200];tick=time.time()
        with ThreadPoolExecutor(max_workers=workers) as pool:values=list(pool.map(inspect_file,sample))
        row=dict(workers=workers,n=len(values),seconds=time.time()-tick,errors=sum(bool(r['error']) for r in values));rows.append(row);print(row,flush=True)
    save_json('audit_io_benchmark.json',rows)
if __name__=='__main__':main()
