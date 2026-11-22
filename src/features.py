"""Deterministic, identical feature definitions for all image origins."""
from common import *
import numpy as np, scipy.fft as fft, pywt, cv2, itertools, io
from PIL import Image, ImageOps, ImageCms
from functools import lru_cache
cv2.setNumThreads(1)
PERMS=list(itertools.permutations(range(4)))
LOOKUP=np.zeros(256,dtype=np.int64)
for i,p in enumerate(PERMS): LOOKUP[sum(p[j]*4**j for j in range(4))]=i

def load_rgb(path, resize_sd=True):
    with Image.open(path) as src:
        im=ImageOps.exif_transpose(src)
        profile=im.info.get('icc_profile')
        if profile:
            im=ImageCms.profileToProfile(im,ImageCms.ImageCmsProfile(io.BytesIO(profile)),ImageCms.createProfile('sRGB'),outputMode='RGB')
        else:im=im.convert('RGB')
        if im.size!=(256,256):
            if not resize_sd:raise ValueError(im.size)
            im=im.resize((256,256),Image.Resampling.BILINEAR)
        return np.asarray(im,dtype=np.uint8)

def quadrants(rgb):return [rgb[:128,:128],rgb[:128,128:],rgb[128:,:128],rgb[128:,128:]]
def luminance(rgb):return cv2.cvtColor(rgb.astype(np.float32)/255,cv2.COLOR_RGB2GRAY).astype(np.float64)
def ordinal_counts(y):
    a=np.stack([y[:-1,:-1],y[:-1,1:],y[1:,:-1],y[1:,1:]],axis=-1).reshape(-1,4)
    order=np.argsort(a,axis=1,kind='stable')
    code=LOOKUP[order@np.array([1,4,16,64])]
    tied=(np.diff(np.sort(a,axis=1),axis=1)==0).any(axis=1)
    return np.bincount(code,minlength=24),np.bincount(code[~tied],minlength=24),float(tied.mean())
def hc(counts):
    if counts.sum()==0:return np.nan,np.nan
    p=counts/counts.sum();u=np.ones(24)/24
    def ent(v):
        v=v[v>0];return -np.sum(v*np.log(v))
    h=ent(p)/np.log(24);j=ent((p+u)/2)-(ent(p)+ent(u))/2
    delta=np.zeros(24);delta[0]=1
    jmax=ent((delta+u)/2)-ent(u)/2
    return h,h*j/jmax
@lru_cache(None)
def fft_geometry(shape):
    fy=fft.fftfreq(shape[0]);fx=fft.fftfreq(shape[1]);r=np.hypot(fy[:,None],fx[None,:])
    valid=(r>0)&(r<=.5);bins=np.minimum((r[valid]*32).astype(int),15)
    return r,valid,bins,np.outer(np.hanning(shape[0]),np.hanning(shape[1]))
def correlation(a,b):
    if len(a)<2 or np.std(a)<1e-10 or np.std(b)<1e-10:return np.nan
    return float(np.corrcoef(a,b)[0,1])
def crop_features(rgb,threshold=.15,saturation=.05):
    y=luminance(rgb);counts,excluded,ties=ordinal_counts(y)
    h,c=hc(counts);he,ce=hc(excluded)
    d=dict(H=h,C=c,H_no_ties=he,C_no_ties=ce,tie_fraction=ties)
    r,valid,bins,window=fft_geometry(y.shape)
    power=np.abs(fft.fft2((y-y.mean())*window))**2
    band=np.bincount(bins,weights=power[valid],minlength=16);total=band.sum()
    shares=band/total if total>1e-24 else np.zeros(16)
    for i,v in enumerate(shares):d[f'fft_{i:02d}']=v
    d['fft_high']=float(power[(r>.25)&(r<=.5)].sum()/total) if total>1e-24 else 0.
    sizes=np.bincount(bins,minlength=16);meanpower=band/np.maximum(sizes,1);freq=(np.arange(16)+.5)/32
    good=meanpower>1e-24
    d['fft_beta']=float(np.polyfit(np.log(freq[good]),np.log(meanpower[good]),1)[0]) if good.sum()>1 else np.nan
    coeff=pywt.wavedec2(y,'haar',level=2,mode='periodization')
    # PyWavelets cH responds to row variation (horizontal edges), cV to column variation.
    energies=[np.sum(coeff[0]**2)]+[np.sum(a**2) for level in [coeff[2],coeff[1]] for a in level]
    denom=sum(energies)
    for name,e in zip(['LL2','LH1','HL1','HH1','LH2','HL2','HH2'],energies):d['dwt_'+name]=e/denom if denom else 0.
    hsv=cv2.cvtColor(rgb.astype(np.float32)/255,cv2.COLOR_RGB2HSV);angle=hsv[...,0].ravel()*np.pi/180
    s=hsv[...,1].ravel();v=hsv[...,2].ravel();mask=s>saturation
    cos=np.cos(angle[mask]);sin=np.sin(angle[mask])
    d['hue_valid']=float(mask.mean());d['hue_cos']=float(cos.mean()) if mask.any() else np.nan;d['hue_sin']=float(sin.mean()) if mask.any() else np.nan
    d['hue_resultant']=float(np.hypot(d['hue_cos'],d['hue_sin']));d['hue_mean']=float(np.arctan2(d['hue_sin'],d['hue_cos']))
    for name,vals in [('s',s),('v',v)]:d[name+'_median']=float(np.median(vals));d[name+'_iqr']=float(np.subtract(*np.percentile(vals,[75,25])))
    d['r_sv']=correlation(s,v)
    for name,a in [('cos',cos),('sin',sin)]:
        for bn,b in [('s',s[mask]),('v',v[mask])]:d['r_'+name+'_'+bn]=correlation(a,b)
    lab=cv2.cvtColor(rgb.astype(np.float32)/255,cv2.COLOR_RGB2Lab).reshape(-1,3)
    for i,name in enumerate(['L','a','b']):d['lab_'+name+'_median']=float(np.median(lab[:,i]));d['lab_'+name+'_iqr']=float(np.subtract(*np.percentile(lab[:,i],[75,25])))
    for i,j in [(0,1),(0,2),(1,2)]:d[f'lab_r_{i}{j}']=correlation(lab[:,i],lab[:,j])
    gx=cv2.Sobel(y,cv2.CV_64F,1,0,ksize=3)/8;gy=cv2.Sobel(y,cv2.CV_64F,0,1,ksize=3)/8
    d['edge_density']=float((np.hypot(gx,gy)>threshold).mean())
    d['undefined_correlations']=sum(not np.isfinite(value) for key,value in d.items() if key.startswith('r_') or key.startswith('lab_r_'))
    return d,counts,excluded

def artwork_features(job):
    artwork_id,path,threshold,saturation=job
    rgb=load_rgb(DATA/path);crops=quadrants(rgb)
    outputs=[crop_features(c,threshold,saturation) for c in crops]
    out={'artwork_id':artwork_id}
    for key in outputs[0][0]:
        values=np.array([x[0][key] for x in outputs]);values=values[np.isfinite(values)]
        out[key+'_median']=float(np.median(values)) if len(values) else np.nan
        out[key+'_iqr']=float(np.subtract(*np.percentile(values,[75,25]))) if len(values) else np.nan
    out['H_pooled'],out['C_pooled']=hc(sum(x[1] for x in outputs))
    out['H_no_ties_pooled'],out['C_no_ties_pooled']=hc(sum(x[2] for x in outputs))
    full,_,_=crop_features(rgb,threshold,saturation)
    out.update({'full_'+k:v for k,v in full.items()})
    return out
