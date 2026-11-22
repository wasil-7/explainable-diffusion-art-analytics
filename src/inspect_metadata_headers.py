"""Header-only sample from every release-split/style/origin directory; no pixel decoding."""
from pathlib import Path
from PIL import Image,ExifTags
import json,os
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results';DATA=ROOT/'data/archive/Real_AI_SD_LD_Dataset'
def main():
    paths=(OUT/'audit_paths.txt').read_text(encoding='utf-8').splitlines()
    sample={}
    for rel in paths:sample.setdefault(rel.rsplit('/',1)[0],rel)
    rows=[]
    for folder,rel in sample.items():
        with Image.open(DATA/rel) as im:
            exif=im.getexif();tags=dict(exif)
            if 34665 in exif:
                try:tags.update(exif.get_ifd(34665))
                except Exception as e:tags['ifd_error']=str(e)
            texttags={str(ExifTags.TAGS.get(k,k)):repr(v)[:1000] for k,v in tags.items() if k in [270,315,36867,37510,40091,40092,40093,40094,40095]}
            info={k:repr(v)[:1000] for k,v in im.info.items() if k.lower() in ['comment','parameters','description','prompt']}
            rows.append(dict(path=rel,info_keys=list(im.info),exif_tags=[str(ExifTags.TAGS.get(k,k)) for k in tags],text_tags=texttags,text_info=info))
    (OUT/'jpeg_metadata_header_sample.json').write_text(json.dumps(dict(n=len(rows),scope='One header per each release split/style/origin directory; not an exhaustive comment-tag absence claim',records=rows),indent=2),encoding='utf-8')
    print('Headers sampled',len(rows),'with EXIF text',sum(bool(r['text_tags']) for r in rows),'with text info',sum(bool(r['text_info']) for r in rows),flush=True)
if __name__=='__main__':main()
