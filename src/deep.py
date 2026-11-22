"""Frozen ImageNet ResNet50 and DINOv2 ViT-S/14, CUDA FP16, 32 crops/batch."""
import faulthandler
faulthandler.enable()
faulthandler.dump_traceback_later(90,repeat=True)
from common import *
print('deep startup: common/pandas ready',flush=True)
import torch
print('deep startup: torch ready',flush=True)
import torchvision,numpy as np,pandas as pd
print('deep startup: torchvision ready',flush=True)
from torch.utils.data import Dataset,DataLoader
from features import load_rgb,quadrants
print('deep startup: image libraries ready',flush=True)
faulthandler.cancel_dump_traceback_later()

def model_for(name):
    torch.manual_seed(SEED)
    if name=='resnet50':
        model=torchvision.models.resnet50(weights=torchvision.models.ResNet50_Weights.IMAGENET1K_V2)
        model.fc=torch.nn.Identity();dim=2048
    else:
        model=torch.hub.load('facebookresearch/dinov2','dinov2_vits14',trust_repo=True);dim=384
    for p in model.parameters():p.requires_grad_(False)
    return model.eval().to('cuda:0'),dim

class Crops(Dataset):
    def __init__(self,df):self.records=list(df[['artwork_id','path']].itertuples(index=False,name=None))
    def __len__(self):return len(self.records)
    def __getitem__(self,i):
        aid,path=self.records[i];rgb=load_rgb(DATA/path)
        x=torch.from_numpy(np.stack(quadrants(rgb))).permute(0,3,1,2).float()/255
        x=torch.nn.functional.interpolate(x,size=(224,224),mode='bilinear',align_corners=False,antialias=True)
        x=(x-torch.tensor([.485,.456,.406])[None,:,None,None])/torch.tensor([.229,.224,.225])[None,:,None,None]
        return i,x

def main(prefetch=False):
    assert torch.cuda.is_available(),'CUDA required'
    torch.set_num_threads(1);torch.backends.cudnn.benchmark=False
    torch.backends.cudnn.deterministic=True
    if prefetch:
        for name in ['resnet50','dinov2']:
            model,dim=model_for(name);print(name,dim,'weights ready',flush=True);del model;torch.cuda.empty_cache()
        return
    df=pd.read_parquet(OUT/'cohort_manifest.parquet').sort_values('path').reset_index(drop=True)
    df[['artwork_id']].to_csv(OUT/'embedding_ids.csv',index=False)
    summaries=[]
    import hashlib
    weight_hashes={}
    for weight in (Path(os.environ['TORCH_HOME'])/'hub/checkpoints').glob('*.pth'):
        sha=hashlib.sha256()
        with weight.open('rb') as stream:
            for block in iter(lambda:stream.read(1024*1024),b''):sha.update(block)
        weight_hashes[weight.name]=sha.hexdigest()
    save_json('pretrained_weight_provenance.json',dict(weights_sha256=weight_hashes,resnet='torchvision ResNet50_Weights.IMAGENET1K_V2',dinov2='facebookresearch/dinov2 dinov2_vits14 pretrained official hub',crop_transform='EXIF/ICC to sRGB; native256 quadrants 128; each resized224 bilinear antialias; ImageNet mean/std; mean across4; SD separately resized256 first',frozen=True))
    for name in ['resnet50','dinov2']:
        start=time.time();model,dim=model_for(name)
        path=OUT/f'{name}_embeddings.npy';state=OUT/f'{name}_embedding_state.json'
        done=json.loads(state.read_text())['completed'] if state.exists() else 0
        matrix=np.lib.format.open_memmap(path,mode='r+' if path.exists() else 'w+',dtype=np.float32,shape=(len(df),dim))
        dataset=Crops(df.iloc[done:]);loader=DataLoader(dataset,batch_size=8,num_workers=4,pin_memory=True,persistent_workers=True,prefetch_factor=2)
        torch.cuda.reset_peak_memory_stats()
        with torch.inference_mode():
            for idx,x in loader:
                x=x.flatten(0,1).to('cuda:0',non_blocking=True)
                with torch.cuda.amp.autocast(dtype=torch.float16):z=model(x)
                values=z.float().reshape(-1,4,dim).mean(1).cpu().numpy()
                inds=idx.numpy()+done;matrix[inds]=values
                completed=int(inds[-1]+1)
                if completed%1000==0 or completed==len(df):
                    matrix.flush();save_json(f'{name}_embedding_state.json',dict(completed=completed,total=len(df),dimension=dim,seconds=time.time()-start,device='cuda:0',fp16=True,crop_batch_size=32,num_workers=4,peak_gpu_bytes=torch.cuda.max_memory_allocated()))
                    print(name,completed,'/',len(df),'seconds',round(time.time()-start),'peakVRAM',torch.cuda.max_memory_allocated(),flush=True)
        matrix.flush();summaries.append(json.loads(state.read_text()));del model,matrix,loader;torch.cuda.empty_cache()
    save_json('deep_extraction_summary.json',summaries)
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--prefetch',action='store_true');args=p.parse_args();main(args.prefetch)
