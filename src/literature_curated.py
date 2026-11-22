"""Curated claims backed by the batch-extracted PDF pages, never milestone numbers."""
from common import *
import pandas as pd

# crosswalk, authors from PDF first page, venue/year of supplied version,
# dataset, task, split, metrics, claim, PDF page, locator, required literal evidence.
RECORDS=[
('Phase1/1','Dimitrios Karageorgiou; Symeon Papadopoulos; Ioannis Kompatsiaris; Efstratios Gavves','CVPR',2025,'13 generators; mixed real-image sources','AI-image detection','Self-supervised spectral learning; cross-generator evaluation','ROC-AUC','5.5 percentage-point absolute AUC improvement across 13 generators',1,'Abstract','5.5%'),
('Phase1/2','Jin Kim; Byunghwee Lee; Taekho You; Jinhyuk Yun','arXiv:2503.13531v1 (earlier than PNAS)',2025,'WikiArt, 72,447 processed paintings','Creation-year prediction from latent context','Year regression; not a human-vs-AI detection split','R-squared','Context C-vector creation-year prediction R2 = 0.869',8,'Fig. 1I discussion','0.869'),
('Phase1/3','Yixuan Li; Xuelin Liu; Xiaoyang Wang; Bu Sung Lee; Shiqi Wang; Anderson Rocha; Weisi Lin','arXiv:2404.13306v2 (TIFS author version)',2024,'FakeBench','Explainable image authenticity assessment','Human evaluation and zero/few-shot LMM testing; not our grouped artwork split','Detection accuracy','Human overall average accuracy 74.51%',4,'Fig. 3(a), human accuracy summary','74.51'),
('Phase1/4','Chenqi Kong; Anwei Luo; Shiqi Wang; Haoliang Li; Anderson Rocha; Alex C. Kot','arXiv:2310.00234v2 (TPAMI author version)',2024,'12 manipulation datasets','Manipulation localization','Cross-dataset and perturbed-image evaluation; exact per-dataset protocols in full text','Pixel localization; benchmark size','Abstract describes 16 representative detection models across 12 datasets',1,'Abstract','16'),
('Phase1/5','Xiaolong Zhang; Zekai Yu; Jianqiao Zhao','PLOS One',2025,'AI-ArtBench','Full-image and local-image AI-art detection','7:1:2 training/validation/test; extra unseen-generator evaluation','ROC-AUC; accuracy','AUC 0.962 full image and 0.801 local image; cross-model mean accuracy 0.81',1,'Abstract (detailed experiments in full PDF)','0.962'),
('Phase1/6','Luo Li; Tianyi Lu; Jiaxin Song; Ke Cheng','Electronics',2026,'SIDset; additional GenImage experiments','Synthetic-image detection','SIDset 8:1:1 train/validation/test; paper-specific external evaluation','Accuracy; inference latency','Abstract reports average accuracy exceeding 95% and inference time 18.2 ms on NVIDIA A100',1,'Abstract','18.2'),
('Phase1/7','Yikun Ji; Yan Hong; Bowen Deng; Jun Lan; Huijia Zhu; Weiqiang Wang; Liqing Zhang; Jianfu Zhang','arXiv:2510.04225v2',2026,'TRACE and external benchmarks','Grounded real-vs-generated verdict and artifact localization','TRACE training split; TRACE test plus out-of-domain datasets','Accuracy; region grounding','TRACE introduced with 20,000 real and synthetic images with region annotations',1,'Abstract','20,000'),
('Phase1/8','Wang Yinghua; Li Linyan; Ma Wenjuan; Zhang Yunzhe','Scientific Reports 16:497',2026,'Balanced real/generated artwork dataset','Self-distilled transformer artwork detection','70:30 training/testing (Table 2); differs from our grouped protocol','Accuracy; precision; recall; F1; AUC','Abstract: accuracy 99.01%, precision 95.29%, recall 94.58%, F1 94.93%, AUC 99%; metrics are paper-reported, not independently reconciled',1,'Abstract','99.01'),
('Phase2/1','Fabrizio Guillaro; Giada Zingarini; Ben Usman; Avneesh Sud; Davide Cozzolino; Luisa Verdoliva','CVPR',2025,'MS-COCO and self-conditioned synthetic images','Bias-controlled general AI-image detection','Aligned COCO-based training; external generator tests; not paintings','Dataset counts; AUC; balanced accuracy','Training construction uses 51,517 real images and 309,102 generated images',5,'Training paradigm / dataset construction','309,102'),
('Phase2/2','Seunghwan Kim; Byunghwee Lee; Wonjae Lee','Scientific Reports 15:22075',2025,'DeviantArt and Behance 2010–2020','Observational style analysis in entropy-complexity space','Temporal observational analysis; no binary classification split','H and C; similarity relationships','149,780 platform artwork images analyzed; not a matched human–diffusion dataset',1,'Abstract','149,780'),
('Phase2/3','Ravidu Suien Rammuni Silva; Ahmad Lotfi; Isibor Kennedy Ihianle; Golnaz Shahtahmassebi; Jordan J. Bird','arXiv:2412.01512v1 (earlier than TMM)',2024,'AI-ArtBench, 185,015 images, 10 styles','Joint source/style classification and generator attribution','Release train/test; test also used as validation in training (PDF training section); differs from our independent validation','F1; attribution accuracy','Joint source/style F1 0.869; generator-attribution accuracy 0.999; 60,000 human and 125,015 generated images',1,'Abstract','0.869'),
('Phase2/4','Zexi Jia; Zhiqiang Yuan; Xiaoyue Duan; Jinchao Zhang; Jie Zhou; Anil K. Jain','arXiv:2605.24306 (TPAMI author version)',2026,'FakeForm, 62 domains','Cross-domain AI-image detection','Photorealistic training; held-out diverse visual domains','Accuracy; AP','FakeForm mean accuracy/AP 77.7%/88.1%; endpoint is AP, not AUROC',11,'Discussion of Table VI (table on PDF p12)','77.7/88.1'),
('Phase2/5','Beilin Chu; Xuan Xu; Xin Wang; Yufei Zhang; Weike You; Linna Zhou','CVPR',2025,'DiffusionForensics and updated-generator benchmark','Diffusion-image detection','ImageNet-subset pretraining then training-source-specific fine tuning and updated generator testing','AUC; accuracy','Table 2 Kandinsky3-trained mean AUC FIRE 78.1% versus FakeInversion 70.5%; source-specific setting',6,'Table 2, Average row, Kandinsky3 configuration','78.1/72.9'),
('Phase2/6','Haifeng Zhang; Qinghui He; Xiuli Bi; Weisheng Li; Bo Liu; Bin Xiao','CVPR',2025,'15 generator columns in Table 1; 17 generators overall','Universal AI-image detection','Diffusion-source training and cross-series generalization; Table 1 endpoint','Average precision','Table 1 mean AP VIB-Net 95.53%; compare NPR row in same table for 89.98%',6,'Table 1, mAP column','95.53'),
('Phase2/9','Ziheng Guo; Tianxiang Wei; Zeyu Li; Lianghao Zhang; Sisi Li; Jiawan Zhang','TVCG author manuscript',2026,'Scatterplot datasets and user study','Density-aware scatterplot abstraction','Visualization user tasks; not a classifier train/test protocol','Friedman p-value for regional density accuracy','E1 across-method p-values 0.0362, 0.0625, 0.1070 for 600-square, 1200-square, 1800-square canvases; only first <0.05',8,'Section 4.2, Fig. 9 discussion','0.0362'),
('Phase2/10','Amit Kumar Das; Klaus Mueller','TVCG author manuscript',2026,'Misleading-visualization benchmark','Detect/explain/correct misleading charts','Chart benchmark and user studies; not image authenticity detection','Issue identification coverage','Abstract reports 96% issue identification and coverage of 74 misinformation types; not artwork projection accuracy',1,'Abstract','96%'),
]

EXTRA_CLAIMS=[
    ('Phase2/1','AUC; balanced accuracy','Table 3 DINOv2+registers end-to-end AUC 99.0% and balanced accuracy 95.2%, versus linear probing 80.8% and 68.5%',6,'Table 3, DINOv2+reg LP and e2e rows','80.8'),
    ('Phase1/1','ROC-AUC','Table 1 mean AUC SPAI 91.0% versus RINE 85.5% across 13 generators; SPAI SD3 75.9% and SD1.3 99.6%',6,'Table 1, average and generator columns','91.0'),
]

def curate():
    pages=pd.read_parquet(OUT/'pdf_pages.parquet');cross=pd.read_csv(OUT/'literature_crosswalk.csv')
    rows=[]
    expanded=list(RECORDS)
    for crossid,metrics,claim,page,locator,literal in EXTRA_CLAIMS:
        base=list(next(r for r in RECORDS if r[0]==crossid))
        base[7:]=[metrics,claim,page,locator,literal]
        expanded.append(tuple(base))
    for crossid,authors,venue,year,dataset,task,split,metrics,claim,page,locator,literal in expanded:
        rec=cross[cross.crosswalk_id.eq(crossid)].iloc[0]
        evidence=pages[(pages.paper_id==rec.paper_id)&(pages.page==page)].iloc[0].text
        assert literal in evidence,(crossid,literal)
        ids=cross[cross.paper_id.eq(rec.paper_id)].crosswalk_id.tolist()
        row=dict(paper_id=rec.paper_id,crosswalk_id='; '.join(ids),title=rec.title,authors=authors,venue=venue,year=year,pdf_version_type=rec.pdf_version_type,dataset=dataset,task=task,split_protocol=split,metrics=metrics,headline_numbers=claim,page_number=page,table_figure=locator,verification_status='claim checked against batch-extracted PDF page; version scoped',doi=rec.doi,evidence_text=evidence)
        if crossid=='Phase1/2':row['title']='Context-aware Multimodal AI Reveals Hidden Pathways in Five Centuries of Art Evolution'
        rows.append(row)
    pd.DataFrame(rows).to_csv(OUT/'literature_facts.csv',index=False)
    print('Curated literature:',len(rows),'claim records covering',len(RECORDS),'distinct papers',flush=True)
if __name__=='__main__':curate()
