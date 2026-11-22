"""Build the portrait final submission from the frozen report and authoritative tables."""
from common import *
from build_report import ORDER, REF, table_specs
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import pymupdf as fitz
import re, hashlib, numpy as np

DEST=ROOT/'phase3_output/submission_build';FIG=DEST/'figures';NAME='i242551_i242532_Milestone03_DSB'
DEST.mkdir(parents=True,exist_ok=True)
def read(n):return pd.read_csv(OUT/n)
def f(v):
    if pd.isna(v):return 'N/A'
    if isinstance(v,(bool,np.bool_)):return 'Yes' if v else 'No'
    if isinstance(v,(float,np.floating)):return f'{v:.4f}'
    return prose(str(v))
def style(s):return s.replace('_',' ').title().replace('Post Impressionism','Post-impr.')
def prose(text):
    text=re.sub(r'\b(Step|Table|Figure|Milestone|Phase|Appendix|Python|Torch|CUDA|all|from|to|at|in|per|with|by|versus|above|below|same|across|after|before|on|of|qualities|over|every|approximately|batch|the|The|full|frozen|balanced|primary|available|complete|AUROC|AUC|F1|BH)(?=\d)',r'\1 ',text)
    # Only prose words: never split hashes, DOIs, model names or feature IDs.
    words='All|Full|Native|Balanced|Primary|Its|ArtBrain|Gaussian|Saturation|Sobel|RAM|SUPER|GTX|and|are|bootstrap|compares|contains|contours|crop|disjoint|explains|fixed|flags|half|handcrafted|has|identical|is|its|maximum|minimum|mixed|native|our|outer|overlapping|perplexities|prompt|reaches|recorded|repeating|resize|resized|seed|seeds|share|stage|use|uses|windowed|yield|yields'
    text=re.sub(r'\b('+words+r')(?=\d)',r'\1 ',text)
    text=re.sub(r'(?<=[A-Za-z]),(?=\d)',', ',text)
    text=re.sub(r'(?<=[;:])(?=[^\s/\\])',' ',text)
    return text

STEPS=[
('Define the Research Input','Artwork records; origin, style, generator and technical metadata. Artist/source/subject/year only where supplied.','185,015 records; no verified subject text, year or prompt IDs; no GAN cohort. Descriptive restriction retained.'),
('Data Collection','Full audit; duplicate/source/prompt grouping; grouped 60:20:20; separate artist, style and generator holdouts.','Full audit and known-family/duplicate groups implemented. Artist families split-disjoint; separate holdout experiments not run; AI prefixes are conservative proxies.'),
('Data Preprocessing','Orientation/profile handling; native Human–LD 256²; four disjoint 128² quadrants; full256 sensitivity.','No EXIF/ICC supplied. RGB conversion; native primary, SD resized descriptive; full256 and five-crop checks.'),
('Feature Engineering / Representation','24-pattern H/C, Hann FFT, two-level Haar, circular HSV, Sobel, Lab; development calibration.','169 measurements, 104 primary predictors. Seven synthetic tests; stable ties and tie-exclusion sensitivity.'),
('Control-Variable Gate / Matched Cohort','Style, subject, exact native size and format; ≥50 test artworks/origin/cell; freeze IDs before Steps 6–7.','300 test artworks/origin/style. Technical gate passes; subject and encoding gates do not. Zero confirmatory-eligible cells.'),
('Visual Analytics and Projection','H,C atlas; development RobustScaler and fixed PCA2/3; t-SNE 5 seeds × p=15/30/50; T(15).','Implemented with loadings, variance, linked points, trustworthiness and continuity. t-SNE exploratory; hex-bin abstraction implemented.'),
('Baseline Methods','L2 logistic handcrafted/metadata probes; optional frozen ResNet-50 and DINOv2; freeze tuning and thresholds.','All five implemented on identical 6,000 test artworks. CUDA encoders frozen; development/validation only fitting and tuning.'),
('Evaluation Metrics','Origin silhouette, unlabeled k=2 ARI, W₁, signed centroid shift, dispersion, macro AUC/F1/BA; 128-direction SW₁.','All cached; H,C centroid displacements and IQR ratios reported. ARI disagreement retained; SW₁ stretch completed.'),
('Statistical / Comparative Analysis','KS D, signed median shifts, 95% group-bootstrap CI; exchangeable permutations; BH; W₁ above split-half P95.','10,000 group randomizations; 1,000 bootstraps; 2,000 split-half nulls. 542 raw passes are exploratory; no eligible confirmation.'),
('Ablation and Component Analysis','Remove each family and each alone; development refits; paired ΔAUC/Δsilhouette; JPEG 95/75/50 and resize.','13 ablations and five stress tests completed. Conditional paired uncertainty and fixed-distance style ranking retained.'),
('Error / Failure Analysis','FP/FN/distant points; artwork crops, spectra, wavelets, colors; signatures, borders, backgrounds; exclusions/reversals.','Eight primary held-out cases; four measurable proxies and boundary exclusion. Semantic/material labels unverified; no SD error-gallery arm.'),
('Final Research Output','Linked H,C atlas, fixed PCA, distance heatmap/uncertainty, ablations/gallery; manifests, crop settings/seeds; dashboard.','All core outputs plus optional dashboard, t-SNE and deep probes. Lightweight submission includes summaries; full caches remain locally.')]

def specs():
    old={'2':('',read('audit_counts.csv').groupby(['origin','width','height','format','mode'],as_index=False)['count'].sum(),['results/audit_counts.csv']),
         '3':('',pd.read_csv(ROOT/'phase3_output/report_tables/Table_3.csv'),['phase3_output/report_tables/Table_3.csv','results/cohort_manifest.csv','results/full_split_counts.csv'])};t={}
    t[1]=('Implementation of the twelve methodology steps.',pd.DataFrame([[str(i)+'. '+n,p,a] for i,(n,p,a) in enumerate(STEPS,1)],columns=['Milestone 2 step','Promise (M2 pp. 7–10)','Implementation and status']),[.23,.34,.43],['i242551_i242532_Milestone02_DSB.pdf','results/control_gate.json','results/stage6_protocol.json','results/stage7_8_protocol.json'])
    changes=[
    ['M1 → M2 scope','Temporal Data Drift & Distribution Shifts in Art History; five centuries; Cubism examples.','M2 defines within-style human–diffusion contrast, not time. Only ten release styles used; no year/medium labels.'],
    ['Step 2 holdouts','Separate artist, style and generator holdout experiments.','Known artist families grouped; no separate leave-artist/style/generator runs. Cross-style and unseen-generator generalization untested.'],
    ['Step 5 matching','Subject, exact dimensions and file format; uncertain subjects descriptive.','Subjects unavailable; JPEG tables origin-aligned with zero common support. Technical matching alone cannot support independent origin attribution.'],
    ['Step 4 hue cutoff','0.05 starting point; select lowest stable development cutoff.','Selected 0.01; Sobel 0.0483168. Calibration is planned adaptation, not test-driven selection.'],
    ['Step 9 inference','Group-bootstrap uncertainty and valid exchangeable permutations/pair swaps.','Whole-group randomizations preserve group counts, not artwork totals. Exchangeability unsupported; probabilities remain exploratory.'],
    ['Step 9 null','Within-origin split-half P95; BH across feature/style tests.','1,000 disjoint group halves per origin; 2,000 pooled nulls, 1,040-test BH. Statistical thresholds do not supersede Step 5.'],
    ['Clustering/runtime','Unlabeled k-means and readable cached tables.','NumPy Lloyd k=2, 20 starts replaces host-blocked sklearn DLL; fastparquet/HTML avoids blocked Arrow. No security-policy change.'],
    ['Color family','HSV/edges plus repeat color analysis in Lab.','Combined color family includes both; HSV-only, Lab-only, combined and saturation-stratified ablations expose this choice.'],
    ['Crop sensitivity','Full256 versus four non-overlapping128 quadrants.','Full256 has no across-crop IQRs, so dimension also changes. Five overlapping crops add a center-context sensitivity.'],
    ['Paired silhouette CI','Paired held-out changes and group uncertainty.','Bootstrap cached per-artwork silhouette scores in fixed geometry; pairwise geometry is not recomputed each draw.'],
    ['Unmatched sensitivity','Full-release controls and matched/native comparisons.','Full185,015 metadata probes; pixel sensitivity on frozen45,000 with SD resized256. Composition changes prevent isolating resolution alone.'],
    ['Failure analysis','Signatures, borders, flat/monochrome backgrounds and exclusion sensitivity.','Quantile proxies and fixed border heuristic; no semantic annotation claims. Two arms share 5,924 supported images; 76 unsupported.'],
    ['Stress-test reference','JPEG qualities95/75/50; separate resizing.','Original is already JPEG, not pristine Q100. Identical recompression is a stress test, not recovery of original common support.'],
    ['Visual feature selection','Explain discriminative named features.','Six largest absolute development-fit coefficients; no test-effect ranking. Density abstraction is inspired by, not a reimplementation of, PixelatedScatter.'],
    ['Literature provenance','M1/M2 metadata, venue and headline claims.','16 unique sources from18 entries; exact available PDF version/page governs. Unsupported earlier numbers and author/venue claims are corrected, not carried forward.']]
    t[2]=('Changes from the planned methodology and their effect.',pd.DataFrame(changes,columns=['Item','Earlier promise / context','Implementation and validity impact']),[.18,.33,.49],['results/report_methodology_changes.csv','results/feature_calibration.json','results/literature_facts.csv'])
    a=old['2'][1];t[3]=('Full release audit by origin and native dimensions.',a[['origin','width','height','format','mode','count']].rename(columns={'origin':'Origin','width':'Width','height':'Height','format':'Format','mode':'Mode','count':'Images'}),[.2,.14,.14,.17,.15,.2],old['2'][2])
    a=old['3'][1].copy();a.cohort=a.cohort.replace({'Balanced tier two':'Balanced45k','Native256 Human LD':'Primary30k'});a.columns=['Cohort','Split','Artworks','Source groups'];t[4]=('Grouped development, validation and test split counts.',a,[.3,.2,.25,.25],old['3'][2])
    a=read('unit_test_results.csv');testrows=[[r.test.split('.')[-1].replace('test_','').replace('_',' '),'Pass' if r.passed else 'Fail',f(r.seconds)+' s'] for r in a.itertuples()]
    setup=[['Environment','Python3.12.16; Torch2.6 / CUDA12.4','GTX1650 SUPER4GB; RAM16GB'],['Encoders','ResNet-50:2048; DINOv2 ViT-S/14:384','Frozen; FP16 batch32 crops; four loaders'],['Calibration','Saturation0.01; Sobel0.0483168','Development only; seed42']]
    t[5]=('Experimental setup and synthetic feature unit tests.',pd.DataFrame(setup+testrows,columns=['Setup / test','Setting / outcome','Detail / recorded time']),[.32,.38,.30],['results/environment.json','results/feature_calibration.json','results/unit_test_results.csv'])
    b=read('baseline_metrics.csv');b=b[b.model.isin(['handcrafted','frequency','resnet50','dinov2','metadata_gated'])].copy();b['Model']=b.model.map({'handcrafted':'Handcrafted','frequency':'FFT only','resnet50':'ResNet-50','dinov2':'DINOv2','metadata_gated':'Metadata'})
    a=b[['Model','roc_auc','f1','balanced_accuracy','precision','recall','ece','macro_style_auc','macro_style_f1']].copy();a.columns=['Probe','AUC','F1','Acc./BA','Prec.','Recall','ECE','Macro AUC','Macro F1'];t[6]=('Held-out baseline evaluation and macro-style performance.',a,[.16]+[.105]*8,['results/baseline_metrics.csv'])
    rows=[]
    for r in read('pca_projection_fidelity.csv').itertuples():rows.append([f'PCA {r.dimensions}D','Fixed',r.trustworthiness,r.continuity])
    for r in read('projection_fidelity.csv').itertuples():rows.append([f't-SNE p={r.perplexity}',str(r.seed),r.trustworthiness,r.continuity])
    t[7]=('Projection neighborhood fidelity (trustworthiness and continuity).',pd.DataFrame(rows,columns=['Representation','Seed','T(15)','Continuity(15)']),[.35,.15,.25,.25],['results/pca_projection_fidelity.csv','results/projection_fidelity.csv'])
    a=read('style_family_drift.csv');rows=[]
    for s,g in a.groupby('style'):
        g=g.set_index('family');rows.append([style(s)]+[f'{g.loc[c,"w1"]:.3f} / {g.loc[c,"median_shift"]:+.3f}' for c in ['Ordinal','FFT','Haar','Color/edges']]+[str(int(g.raw_rule_count.sum()))])
    t[8]=('Style-conditioned feature-family drift summaries.',pd.DataFrame(rows,columns=['Style','Ordinal','FFT','Haar','Color / edges','Raw passes']),[.24,.17,.17,.17,.17,.08],['results/style_family_drift.csv'])
    facts=read('literature_facts.csv').fillna('');short=['ArtBrain','Complexity–entropy','B-Free','SCADET','SPAI','FIRE','VIB-Net','CoDA','PixelatedScatter','MisVisFix','Art evolution','FakeBench','Pixel inconsistency','SIDWA','Locate–then–examine','Self-distilled artwork']
    rows=[]
    for pid,label in zip(ORDER,short):
        g=facts[facts.paper_id.eq(pid)];r=g.iloc[0];rows.append([f'[{REF[pid]}] {label}\n{r.crosswalk_id}',r.dataset+'\n'+r.task+'\n'+r.split_protocol,'; '.join(g.headline_numbers.unique()),r.pdf_version_type+'; PDF p. '+', '.join(str(x) for x in g.page_number.unique()),'Different protocol / endpoint; '+('same release, different split and learned model.' if label=='SCADET' else 'not a matched comparison with our AUROC.')])
    t[9]=('Quantitative and methodological comparison with collected literature [1]–[16].',pd.DataFrame(rows,columns=['Study / continuity','Dataset / task / protocol','Paper-reported result','Available evidence','Fair-comparison limit']),[.17,.23,.27,.17,.16],['results/literature_facts.csv','results/literature_crosswalk.csv'])
    a=read('ablation_results.csv');rows=[]
    for r in a.itertuples():rows.append([r.label,r.n_features,f(r.roc_auc),f(r.f1),f'{r.delta_auc:+.4f}\n[{r.delta_auc_low:+.4f}, {r.delta_auc_high:+.4f}]',f'{r.delta_silhouette:+.4f}'])
    t[10]=('Paired feature-family, representation and geometry ablations.',pd.DataFrame(rows,columns=['Variant','Dims','AUC','F1','ΔAUC [95% CI]','Δsilh.']),[.28,.08,.12,.12,.28,.12],['results/ablation_results.csv'])
    a=read('perturbation_results.csv');rows=[]
    for r in a.itertuples():rows.append([r.view,r.roc_auc,r.f1,f'{r.delta_auc_low:+.4f}, {r.delta_auc_high:+.4f}',r.silhouette_retention,r.style_w1_rank_rho])
    t[11]=('Frozen-probe perturbation robustness under JPEG recompression and resizing.',pd.DataFrame(rows,columns=['View','AUC','F1','ΔAUC 95% CI','Silh. ratio','Rank ρ']),[.19,.13,.13,.28,.14,.13],['results/perturbation_results.csv'])
    rows=[['G1 / RQ1','M1: Explainable Data Visualization vs. Opaque Learned Features. M2: Inspectability and projection fidelity.','Named H,C and pixel features, artwork links, fixed PCA loadings/variance, T(15)/continuity and dashboard.','Implemented diagnostics; no user study or proof of semantic explanation.'],['G2 / RQ2–RQ3','M1: Temporal Data Drift & Distribution Shifts in Art History. M2: Style-conditional human–diffusion differences.','Within-style W₁, KS D, signed shifts, group intervals; 542/1,040 exploratory raw-rule passes.','Descriptive support only; not temporal drift, historical fidelity or confirmed diffusion effect.'],['G3 / Step5','M1: Data Aggregation Bias and Semantic Over-Reliance. M2: Whether separation survives subject and file controls.','Native256 comparison; metadata AUC1.0000; no JPEG common support; unverified subjects.','Not established. Forensic discovery identifies why the attribution requirement cannot be met.'],['Decision rule','M2 Step9: adjusted p<0.05 AND W₁>within-origin split-half P95, within eligible cells.','10,000 randomizations; BH1,040; 2,000 nulls; zero eligible and zero confirmed.','Cannot reject or confirm an independent origin effect. Zero eligible is not evidence of zero true effects.']]
    t[12]=('Hypotheses and research gaps from Milestone 2 and what the experiments show.',pd.DataFrame(rows,columns=['Gap / rule','Milestone continuity','Experimental evidence','Verdict']),[.13,.32,.30,.25],['Milestone_1_Revamped_24i-2551_24i-2532.docx.pdf','i242551_i242532_Milestone02_DSB.pdf','results/stage6_protocol.json','results/control_gate.json'])
    a=read('error_gallery_cases.csv');a=a[['artwork_id','selection_reason','origin','style','prob_ai','H_pooled','C_pooled']].copy();a['artwork_id']=a.artwork_id.str[:10];a['style']=a['style'].map(style);a.columns=['ID prefix','Reason','Origin','Style','p(AI)','H','C'];t[13]=('Held-out forensic error gallery case index.',a,[.19,.18,.10,.22,.11,.10,.10],['results/error_gallery_cases.csv'])
    return t

def main():
    tables=specs();doc=Document();normal=doc.styles['Normal'];normal.font.name='Times New Roman';normal.font.size=Pt(11);normal.paragraph_format.line_spacing=1.15;normal.paragraph_format.space_after=Pt(6)
    for name,size in [('Title',22),('Heading 1',13),('Heading 2',11.5)]:
        st=doc.styles[name];st.font.name='Times New Roman';st.font.size=Pt(size);st.font.bold=True;st.font.color.rgb=RGBColor(0,0,0)
        st.paragraph_format.space_before=Pt(10);st.paragraph_format.space_after=Pt(6)
        for el in st.element.xpath('.//w:pBdr'):el.getparent().remove(el)
        rf=st.element.get_or_add_rPr().find(qn('w:rFonts'))
        if rf is not None:
            for k in list(rf.attrib):
                if 'Theme' in k:del rf.attrib[k]
    for sec in doc.sections:
        sec.page_width=Inches(8.27);sec.page_height=Inches(11.69);sec.left_margin=sec.right_margin=sec.top_margin=sec.bottom_margin=Inches(.8);sec.footer_distance=Inches(.35)
    def para(text,align=None):
        text=prose(text)
        p=doc.add_paragraph(text);p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY if align is None else align;return p
    def heading(text,level=1):
        p=doc.add_heading(text,level)
        if text=='References' or text.startswith('Appendix '):p.paragraph_format.page_break_before=True
    def caption(kind,n,text):
        p=doc.add_paragraph();p.add_run(f'{kind} {n}. ').bold=True;p.add_run(prose(text))
        for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(10.5)
        p.paragraph_format.line_spacing=1;p.paragraph_format.space_after=Pt(6);return p
    used=[];figure_records=[]
    def table(n):
        title,df,widths,sources=tables[n];p=caption('Table',n,title);p.paragraph_format.keep_with_next=True
        tb=doc.add_table(rows=1,cols=len(df.columns));tb.autofit=False
        pr=tb._tbl.tblPr;wid=pr.find(qn('w:tblW'));wid.set(qn('w:w'),'5000');wid.set(qn('w:type'),'pct')
        borders=OxmlElement('w:tblBorders')
        for edge in ['top','left','bottom','right','insideH','insideV']:
            e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'000000');borders.append(e)
        pr.append(borders);marg=OxmlElement('w:tblCellMar')
        for edge,v in [('top',60),('bottom',60),('left',100),('right',100)]:
            e=OxmlElement('w:'+edge);e.set(qn('w:w'),str(v));e.set(qn('w:type'),'dxa');marg.append(e)
        pr.append(marg)
        for row in [list(df.columns)]+[[f(v) for v in r] for r in df.itertuples(index=False,name=None)]:
            cells=tb.rows[0].cells if len(tb.rows)==1 and not tb.cell(0,0).text else tb.add_row().cells
            for i,(cell,value,w) in enumerate(zip(cells,row,widths)):
                cell.text=str(value);cell.width=Inches(6.67*w);tb.columns[i].width=Inches(6.67*w)
        for i,row in enumerate(tb.rows):
            tr=row._tr.get_or_add_trPr();tr.append(OxmlElement('w:cantSplit'))
            if i==0:tr.append(OxmlElement('w:tblHeader'))
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.space_after=Pt(0);p.paragraph_format.space_before=Pt(0);p.paragraph_format.line_spacing=1
                    if i==0:p.paragraph_format.keep_with_next=True
                    for r in p.runs:r.font.name='Calibri';r.font.size=Pt(9);r.bold=i==0
        used.append({'number':n,'title':title,'columns':df.columns.tolist(),'cells':[[f(v) for v in r] for r in df.itertuples(index=False,name=None)],'sources':sources})
        df.to_csv(DEST/f'table_{n:02}.csv',index=False)
    mapping={1:'fig00_implemented_architecture.png',2:'fig01_dataset_audit_and_confound.png',3:'fig07_baseline_probes_and_ari.png',4:'fig02_hc_causality_atlas.png',5:'fig03_pca_tsne_trustworthiness.png',6:'fig04_spectral_and_wavelet_profiles.png',7:'fig05_style_drift_heatmap.png',8:'fig06_feature_ecdfs_and_rainclouds.png',9:'fig11_dashboard_ui.png',10:'fig08_ablation_forest_plot.png',11:'fig09_perturbation_robustness.png',12:'fig10_forensic_error_gallery.png'}
    captions={1:'Implemented architecture. Frozen IDs and development calibration feed descriptive analytics and held-out probes. The control-variable gate determines attribution eligibility.',2:'Dataset audit and metadata confound diagnostic. Full-release and primary probes have different source compositions; both metadata AUROCs are1.0000.',3:'Baseline ROC, precision–recall, per-style AUROC/F1, and unsupervised k-means ARI. Five probes share6,000 test IDs; per-style bars use1,000 source-group bootstrap intervals conditional on frozen fits. Clustering remains label-free until ARI evaluation.',4:'Entropy–Complexity atlas across ten art movements. Human(blue) → LD(orange);300 artworks/origin/style. Shared axes; contours15/40/70% of each KDE peak;500-group-bootstrap Gaussian95% centroid ellipses. Arrows are descriptive.',5:'Fixed PCA, exploratory t-SNE, and neighborhood fidelity curves. PCA:6,000 test artworks; arrows share a display multiplier. t-SNE:3,000 balanced artworks; five random seeds, p=15/30/50. Whiskers show seed ranges, not confidence intervals.',6:'Hann-windowed16-annulus FFT and two-level Haar wavelet energy profiles. Bands/whiskers:1,000-group-bootstrap95% intervals. Human/LD native256; SD resized768→256, descriptive only. LL2 remains in Haar normalization.',7:'Style-conditional feature-family drift heatmap (standardized W₁ and signed median shift). Actual fig05 panels stacked without altering pixels. * marks at least one exploratory constituent pass, not a family test or confirmation. Zero confirmatory cells.',8:'Top discriminative feature ECDFs and raincloud distributions. Six features selected by absolute development-fit coefficients;300 test artworks/origin in each displayed style. Raw measurement units; KS D descriptive.',9:'Interactive Streamlit and Plotly visual analytics dashboard. Actual running application captures: glassmorphic landing overview and interactive H–C atlas with the control-gate warning. The submission edition retains all projection points and eight pixel-inspectable gallery cases.',10:'Paired family ablation forest plot, saturation strata, and crop context sensitivity. Variant minus primary baseline;1,000 paired group-bootstrap intervals. Silhouette uncertainty conditions on cached geometry; saturation boundaries are development-defined.',11:'Perturbation robustness and style-rank stability. Frozen probe and scaler; both origins transformed identically. AUROC intervals use1,000 group bootstraps. Rankρ compares10-style mean standardized W₁. Original means release JPEG, not pristine Q100.',12:'Forensic error gallery across FP, FN, TP, and H–C/PCA outliers. Actual artworks, disjoint quadrants, FFT, Haar and HSV/edge measurements; purposive inspection, not prevalence estimation. Hue R is undefined where no valid hue pixels remain.'}
    def figure(n):
        names=[mapping[n]] if n!=12 else ['fig10_forensic_error_gallery_1.png','fig10_forensic_error_gallery_2.png']
        if n==7:names=['fig05_style_drift_heatmap_1.png','fig05_style_drift_heatmap_2.png']
        for i,name in enumerate(names):
            from PIL import Image
            im=Image.open(FIG/name);width=min(6.25 if n==4 else 6.67,8.6*im.width/im.height)
            p=doc.add_paragraph();p.alignment=1;p.paragraph_format.keep_with_next=True;p.paragraph_format.space_after=Pt(3);p.add_run().add_picture(str(FIG/name),width=Inches(width))
            if i==0:caption('Figure',n,captions[n])
            else:
                p=para(f'Figure {n} (continued). '+('Signed median shifts (LD minus Human), using the same ten styles and four feature families.' if n==7 else 'Remaining four held-out cases, using the same measurements and scales.'));p.runs[0].font.size=Pt(10.5)
            figure_records.append({'number':n,'file':name,'sha256':hashlib.sha256((FIG/name).read_bytes()).hexdigest()})
    # Exact institutional layout from M2, with requested M3 metadata and date.
    sec=doc.sections[0];bdr=OxmlElement('w:pgBorders');bdr.set(qn('w:offsetFrom'),'page')
    for edge in ['top','left','bottom','right']:
        e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'8');e.set(qn('w:space'),'24');e.set(qn('w:color'),'000000');bdr.append(e)
    sec._sectPr.append(bdr)
    ref=fitz.open(ROOT/'i242551_i242532_Milestone02_DSB.pdf');logo=DEST/'university_logo.png';logo.write_bytes(ref.extract_image(ref[0].get_images()[0][0])['image'])
    p=para('',0);p.paragraph_format.left_indent=Inches(.28);p.paragraph_format.space_before=Pt(10);p.add_run().add_picture(str(logo),width=Inches(.8));r=p.add_run('  National University of Computer and Emerging Sciences');r.bold=True;r.font.size=Pt(15)
    position=OxmlElement('w:position');position.set(qn('w:val'),'40');r._r.get_or_add_rPr().append(position)
    p.paragraph_format.space_after=Pt(85)
    p=para('Data Analysis & Visualization',1);p.runs[0].font.size=Pt(27);p.runs[0].font.bold=True;p.runs[0].font.color.rgb=RGBColor.from_string('225C91');p.paragraph_format.space_after=Pt(20)
    border=OxmlElement('w:pBdr');e=OxmlElement('w:bottom');e.set(qn('w:val'),'single');e.set(qn('w:sz'),'12');border.append(e);p._p.get_or_add_pPr().append(border)
    p=para('Milestone 3',1);p.runs[0].bold=True;p.runs[0].font.size=Pt(25)
    p=para('Research Implementation and\nExperimental Evaluation',1);p.runs[0].bold=True;p.runs[0].font.size=Pt(21);p.paragraph_format.space_after=Pt(35);p.paragraph_format.line_spacing=1
    for label,value in [('NAME:','Wasil Kayani, Umar Asghar'),('ROLL NUMBER:','24I - 2551, 24I - 2532'),('DEGREE PROGRAM:','BS DS'),('SECTION:','DSB (Section B)'),('SUBJECT NAME:','Data Analysis and Visualization'),('DATE OF SUBMISSION:','15 – 11 – 26 (15 November 2026)'),('SUBMITTED TO:','Ma’am Azka Atiq')]:
        p=doc.add_paragraph();p.paragraph_format.left_indent=Inches(.75);p.paragraph_format.tab_stops.add_tab_stop(Inches(3.75));p.add_run(label).bold=True;p.add_run('\t'+value);p.paragraph_format.space_after=Pt(7)
        for r in p.runs:r.font.size=Pt(12)
    p=para('Explainable Visual Analytics of Human and Diffusion Artwork: Research Implementation and Experimental Evaluation',1);p.paragraph_format.space_before=Pt(30);p.runs[0].bold=True
    sec=doc.add_section(WD_SECTION_START.NEW_PAGE)
    for el in sec._sectPr.xpath('./w:pgBorders'):el.getparent().remove(el)
    sec.footer.is_linked_to_previous=False;p=sec.footer.paragraphs[0];p.alignment=2;field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');p._p.append(field)
    old=Document(ROOT/'phase3_output/report/Milestone3_Final.docx');blocks={};key=None
    for p in old.paragraphs:
        if p.style.name.startswith('Heading'):key=p.text;blocks[key]=[]
        elif key and p.text and not p.text.startswith(('Table ','Figure ','Source: ')):blocks[key].append(p.text)
    fm={0:1,1:2,2:4,3:5,4:6,5:7,6:8,7:3,8:10,9:11,10:12};tm={0:1,1:2,2:3,3:4,4:5,5:6,6:6,7:7,8:8,9:9,10:10,11:10,12:11,13:13}
    def reuse(key):
        for text in blocks.get(key,[]):
            text=re.sub(r'Figure (\d+)',lambda m:'Figure '+str(fm.get(int(m[1]),int(m[1]))),text)
            text=re.sub(r'Table (\d+)',lambda m:'Table '+str(tm.get(int(m[1]),int(m[1]))),text)
            text=text.replace('Section 10','Section 8').replace('Section 2 and deduplicates','Section 1 and deduplicates')
            para(text)
    heading('Abstract');reuse('1 Abstract')
    heading('1. Introduction');reuse('2 Introduction and Research Objectives')
    para('Milestone1 identified G1: Explainable Data Visualization vs. Opaque Learned Features; G2: Temporal Data Drift & Distribution Shifts in Art History; and G3: Data Aggregation Bias and Semantic Over-Reliance. Milestone2 narrowed these to inspectability/projection fidelity, style-conditional human–diffusion differences, and whether separation survives subject and file controls. We retain those refinements rather than interpreting style labels as timestamps or measurement differences as aesthetic intention.')
    b=read('baseline_metrics.csv').set_index('model');d=read('ablation_results.csv');q=read('perturbation_results.csv').set_index('view')
    para('The five headline findings are the complete 185,015-file audit with an origin-aligned JPEG signature; handcrafted AUROC 0.9824 versus metadata 1.0000; 542 exploratory statistical passes with zero eligible confirmations; an ordinal-removal AUROC loss of 0.0744; and JPEG 50 AUROC 0.6819 with style-rank ρ 0.3697. Together they support a transparent release-discrimination analysis and a critical forensic and methodological discovery, while blocking causal diffusion-origin attribution.')
    para('The reproducibility entry point is README.md in the submission folder, with src/, tests/, figures/ and lightweight results/. No remote repository URL is asserted. The complete working directory retains the dataset, frozen split/feature/encoder caches and source PDFs; the submission explicitly excludes those large or third-party assets.')
    heading('2. Implementation of the Proposed Methodology');heading('2.1 Overview',2)
    reuse('3 Implementation and Documented Methodology Changes')
    para('Table1 mirrors all twelve Milestone2 steps (PDF pp.7–10); Table12 resolves their research-gap implications. Tables are generated from frozen results or a source-anchored promise audit. Displayed main-body floats use three or four decimals; exact values, undefined flags, citations and native-precision statistical tables remain in results/. This provenance and rounding rule applies throughout without repeated table footnotes.')
    table(1);figure(1);heading('2.2 Changes to the Milestone 2 methodology',2);table(2)
    para('The wording of Step5 already made uncertain subject cells descriptive. Continuing the frozen analyses therefore preserves that planned restriction. The mismatch is a limit of the available benchmark, not permission to relabel exploratory passes as confirmations. Table2 also distinguishes planned sensitivity analyses from additional implementation choices and genuinely unperformed work.')
    heading('3. Dataset, Preprocessing and Experimental Setup');heading('3.1 Datasets and full-release audit',2);reuse('4 Dataset Audit Preprocessing and Experimental Setup');table(3);figure(2)
    heading('3.2 Preprocessing, grouping and the Control-Variable Gate',2)
    para('The full grouped partition contains110,999 development,37,016 validation and37,000 test files. A frozen balanced45,000-image tier contains1,500 artworks per style/origin (900/300/300); the primary30,000 Human–LD tier preserves native256 dimensions. Each primary test cell has300 distinct artworks per origin, exceeding the planned minimum50. Five exact duplicate pairs and conservative source families remain split-disjoint. Human artist prefixes are interpretable group identifiers; AI two-field numeric prefixes are conservative proxies, not verified prompt identities. Unknown derivative links cannot be ruled out.')
    table(4)
    para('All inputs decode as RGB JPEG; no EXIF orientation or ICC profile was supplied. RGB conversion and four disjoint128×128 quadrants cover the native256 canvas once. SD remains a separate resized sensitivity. Frozen IDs pass dimension/style/support checks, but subject matching cannot be verified and Human–LD quantization-table overlap is zero. The legacy control_gate.json field passed refers to the technical gate; confirmatory_gate_passed=false is the scientific eligibility verdict.')
    heading('3.3 Mathematical features, calibration and hardware setup',2)
    reuse('Ordinal structure');para('Using Milestone2 notation, S(p)=−Σⱼpⱼln(pⱼ), H=S(p)/ln(24), and C=H×J(p,u)/J(δ,u), where J is Jensen–Shannon divergence, u is uniform and δ a point mass. Four ranked pixels yield4!=24 states; the later master-prompt24! notation is a typo, not a different feature space.')
    reuse('Frequency and wavelet energy');reuse('Color edges and artwork aggregation');table(5);reuse('Hardware and frozen training protocol')
    para('The logistic grid is C∈{0.001,0.01,0.1,1,10,100}, chosen by validation AUROC; thresholds maximize validation F1. Final fits use development only. Four quadrant crops are bilinearly resized to224 and ImageNet-normalized for both frozen encoders; four float32 embeddings are averaged after CUDA FP16 inference. All primary classifiers retain identical test IDs. Batch caches enable resumption, not reuse after changing features or splits.')
    heading('4. Baseline Evaluation')
    para('Table6 evaluates handcrafted104-dimensional, FFT-only, frozen ResNet-50, frozen DINOv2 and metadata logistic probes on the same6,000 Human/LD test artworks. Accuracy equals balanced accuracy on this balanced cohort. Precision, recall and F1 use the AI-positive label; ECE uses15 bins. Macro scores average the10 style cells. Frozen encoder performance is not fine-tuned end-to-end performance.')
    table(6);figure(3)
    para('The handcrafted AUROC0.9824 is a strong held-out release-discrimination result. ResNet-50 reaches0.9999 and DINOv2 reaches0.9997, while metadata reaches1.0000. These scores do not isolate the origin-specific pixel contribution, establish aesthetic fidelity or demonstrate unseen-generator recognition. A perfect metadata diagnostic exposes an available shortcut; it does not quantify how much each pixel model uses that shortcut. Near-zero full-space k-means ARI (maximum0.0034) shows that strong supervised prediction need not yield two natural unlabeled clusters.')
    heading('5. Graphical Results');heading('5.1 RQ1: Entropy–Complexity (H–C) Atlas',2)
    para('The atlas links the named entropy and complexity measurements to actual held-out artworks. Shared axes, source-group centroid intervals and LD-minus-Human arrows expose within-style displacement without implying causality. Balanced artwork counts do not guarantee equal effective source-group sizes. The historical fig02 filename contains “causality”; the figure and conclusions remain descriptive.')
    figure(4)
    heading('5.2 RQ2: Dimensionality reduction and neighborhood fidelity',2);table(7);figure(5)
    para('All fidelity values use k=15 on the fixed3,000-artwork audit subset. PCA2 explains approximately93.57% of development variance but T(15)=0.6928 and continuity=0.7571; PCA3 reaches95.12% variance, T=0.7800 and continuity=0.8869. Explained variance therefore cannot substitute for local fidelity. t-SNE uses1,000 iterations, five random-initialization seeds42–46 and perplexities15/30/50; p30/seed42 is the fixed display, not the best test-selected run. Inferential distances remain in standardized feature space or fixed PCA.')
    heading('5.3 RQ3: Spectral, wavelet, and style-conditional feature drift',2);figure(6);figure(7);figure(8)
    para('Table8 cells report mean standardized W₁ / mean signed median shift for each prespecified family. Raw passes count constituent features satisfying both numerical thresholds, not independent family discoveries. Averaging signed shifts can cancel opposite constituent directions; the complete1040-row table and confidence bounds are retained digitally.')
    table(8);reuse('Distance tests and decision eligibility')
    para('W₁=∫|FHuman(x)−FLD(x)|dx; KS D=supₓ|FHuman(x)−FLD(x)|. The signed median difference is LD−Human. Silhouette is(b−a)/max(a,b), using known origin labels; k-means labels are fitted without origin. Prespecified raw rule: BH-adjusted p<0.05 AND W₁>null P95. The rule is meaningful for confirmation only when Step5 establishes the necessary control and exchangeability conditions.')
    heading('5.4 Interactive visual analytics dashboard',2);reuse('Dashboard architecture and walkthrough');figure(9)
    para('Run python -m streamlit run src/dashboard.py. The compact submission automatically uses CSV projection points and gallery pixels when Parquet caches are absent. All6,000 primary projection points and3,000 t-SNE points remain filterable; pixel/feature drill-down is limited to the eight supplied forensic cases. Restoring the complete workspace caches and dataset enables arbitrary-artwork inspection. This packaging limit is visible in the interface.')
    heading('6. Comparison with Existing Research')
    para('Table9 covers all16 unique papers across18 Phase1/Phase2 source entries, preserving the original crosswalk IDs. Two duplicate studies (SPAI and SCADET) are counted once. Results are checked against literature_facts.csv and the collected PDF pages. Exact task, endpoint and available version govern the claim; no direct cross-paper leaderboard is justified. AP, AUROC, joint origin/style F1, generator attribution, year regression and chart-issue identification are distinct endpoints.')
    table(9)
    para('The nearest contextual comparator is SCADET on AI-ArtBench, but its learned architecture and split differ. Its0.962 full-image versus0.801 local AUROC motivates the same-artwork context test, not a superiority claim for our0.9824. B-Free trains an aligned photographic detector; its99.0% AUROC and95.2% balanced accuracy do not describe our frozen DINO probe. ArtBrain0.869 joint F1 and0.999 attribution accuracy are not binary Human–LD AUROC. PixelatedScatter user-study p-values and MisVisFix issue-identification rates do not establish our projection fidelity.')
    para('Source integrity also corrects earlier milestones: the collected pixel-inconsistency PDF credits Kong et al., and SIDWA credits Luo Li, Tianyi Lu, Jiaxin Song and Ke Cheng; the complete names appear in References as recorded in the source crosswalk. ArtBrain is represented by its available 2024 arXiv version rather than silently claiming access to the later journal manuscript. Locate–then–examine remains the collected arXiv version; conference acceptance is not inferred. Unsupported earlier headline precision or accuracy claims are replaced by page-verified evidence.')
    para('Milestone 1 also grouped SCADET with wavelet evidence; its collected method is spectral/FFT, whereas SIDWA motivates the DWT comparison. The earlier broad language about frequency robustness, aesthetic intention and semantic independence is treated as motivation requiring tests, not as a demonstrated property of this implementation. The signed within-style question and explicit control gate in Milestone 2 provide the operative scope.')
    heading('7. Ablation and Perturbation Robustness Studies');heading('7.1 Feature-family, color-space and crop-geometry ablations',2);table(10);figure(10)
    para('Removing ordinal measurements lowers AUROC from0.9824 to0.9080 (Δ−0.0744); ordinal-only reaches0.8888. FFT-only reaches0.6839. These are conditional predictive contributions among correlated features, not causal allocations of image origin. HSV and Lab alternatives, saturation strata, tie exclusion and full/five-crop variants retain the same test IDs. Full256 reaches0.9790 and five-crop0.9810; full256 also changes vector dimensionality, so the difference is not pure context size. Paired intervals resample whole source groups with fits and thresholds frozen.')
    heading('7.2 JPEG recompression and resize stress tests',2);table(11);figure(11)
    para('JPEG95 largely preserves AUROC (0.9822), whereas JPEG75 falls to0.8354 and JPEG50 to0.6819. Half-size reduction followed by standardization reaches0.7744. Style-rankρ under JPEG50 is0.3697. A perturbation may reduce predictive discrimination while increasing origin silhouette, so the two metrics do not validate one another. These interventions demonstrate nuisance sensitivity; equal recompression cannot undo previously lost information or verify subject alignment.')
    heading('8. Results Analysis and Discussion');heading('8.1 Answers to the research questions and hypotheses verdict',2);table(12)
    para('The RQ1–RQ3 labels organize the graphical analyses: named ordinal structure, projection reliability and spectral/style-conditional distributions. Milestone2 posed one overarching question and three gap commitments rather than three separately preregistered hypotheses. Table12 therefore preserves the exact gap wording and the Step9 rule without inventing directional preregistration. G1 is implemented as an auditable diagnostic system; G2 is characterized descriptively; G3 is not established under the supplied controls.')
    heading('8.2 Addressing the research gaps: The Control-Variable Gate as a Forensic Discovery',2)
    para('The central result is a critical forensic and methodological discovery: the mandatory Step5 gate exposes origin-aligned JPEG quantization and unverifiable subjects in a benchmark that otherwise supports very high baseline AUROC. Human and LD native dimensions agree, yet their quantization-table hashes have zero common support. Metadata alone obtains AUROC1.0000. File extension equality is therefore insufficient evidence of equivalent encoding. The audit identifies a concrete mechanism by which apparent source separation can arise without establishing an independent diffusion-origin effect.')
    para('The542 exploratory passes are numerically reproducible associations, but their use as confirmed diffusion-origin effects is invalid. Whole-group permutation preserves recorded families, not the unobserved subject balance or encoding distribution required for exchangeability. Benjamini–Hochberg controls multiplicity only under an appropriate testing model; it does not remove systematic bias. Bootstrap intervals describe uncertainty conditional on the observed groups and cannot recover absent common support. Consequently all1040 comparisons are ineligible for confirmatory attribution, even when adjusted p<0.05 and W₁ exceeds the split-half95th percentile.')
    para('High AUROC and zero confirmed effects answer different questions. AUROC measures ranking of observed release labels on a frozen split; the gate asks whether those differences can be attributed independently to diffusion origin. The former succeeds, while the latter cannot be established. Zero eligible confirmations is neither evidence that all true effects are zero nor proof that JPEG explains100% of the pixel models’ performance. Neither the subject contribution nor the encoding contribution is separately identified by these data.')
    para('This discovery advances G1 through visible diagnostics and traceable features, advances G2 through signed within-style measurements with uncertainty, and makes the unresolved condition in G3 experimentally explicit. It does not close G3 or validate the original M1 claim of semantic independence. A successful control gate may reject a proposed inference: that is useful methodological output when its consequences are reported plainly rather than hidden behind detector accuracy.')
    heading('8.3 Forensic error analysis and boundary sensitivity',2);table(13)
    para('The gallery contains two false positives, two false negatives, two true positives and two distant H–C/PCA cases, selected for inspection within the primary Human–LD test set. It is not a random prevalence sample or a separate SD-generator error analysis. Actual quadrant pixels, spectra, wavelets and color summaries reveal what the measured representation sees. Qualitative observations include an isolated object on a white field, typographic cards and ornate frames; these are inspection notes, not verified subject or medium annotations.')
    para('Development-quantile low saturation, low edge density and high-frequency proxies complement a fixed border heuristic: outer8-pixel luminance SD<0.025 and adjacent-strip mean jump>0.08. The border screen flags369 artworks;76 have no supported quadrant. Comparing both arms on the identical5,924 supported artworks yields12 sign reversals and23 exploratory rule reversals, with zero confirmed reversals. This exposes sensitivity to crop support without restoring subject matching or JPEG overlap. Trigger associations and group confidence intervals remain available in the extended digital tables.')
    figure(12)
    heading('8.4 Strengths and limitations',2)
    para('Strengths include an exhaustive readable-file audit, frozen grouped IDs, development-only calibration and fitting, five shared-test probes, complete statistical null caches, paired perturbations and artwork-linked visual evidence. Limitations include uncertain AI filename-family semantics, unknown derivatives, fewer effective Human source groups, unavailable verified subjects and medium/year labels, deterministic encoding differences, resized SD sensitivities and conditional bootstrap assumptions. The full185,015-file audit is not a full185,015-image pixel-feature experiment: intensive features and encoders use the frozen45,000 cohort.')
    para('Separate leave-artist, leave-style and unseen-generator experiments were promised but not run. The grouped split protects known artist families but is not a substitute for those protocols. No semantic matching, material recognition, dashboard user study or independent causal effect estimate was performed. Encoder weights were frozen; no new detector was trained end-to-end. The dashboard uses hexagonal aggregation inspired by earlier visualization work, not the complete PixelatedScatter algorithm or an LLM-powered MisVisFix reproduction. All such distinctions are part of the continuity audit.')
    heading('8.5 Conclusion and future work',2);reuse('11 Conclusion and Future Work')
    heading('References')
    facts=read('literature_facts.csv').drop_duplicates('paper_id').set_index('paper_id')
    for pid in ORDER:
        r=facts.loc[pid];authors=[]
        for author in r.authors.split(';'):
            parts=author.strip().split();authors.append(' '.join(x[0]+'.' for x in parts[:-1])+' '+parts[-1] if len(parts)>1 else author.strip())
        p=para(f'[{REF[pid]}] {", ".join(authors)}, “{r.title},” {r.venue}, {r.year}. Available source: {r.pdf_version_type}. {r.doi}');p.paragraph_format.line_spacing=1;p.paragraph_format.space_after=Pt(5)
    heading('Appendix A: Reproducibility Manifest, Citation Crosswalk & Timings')
    para('Frozen cohort SHA256: '+json.loads((OUT/'control_gate.json').read_text())['manifest_sha256']+'. The complete manifests, crop coordinates, calibration, encoder row IDs and model fits remain in the original workspace. The compact package preserves native-precision summary CSV/JSON, gallery pixels and source code; its inventory records SHA256 for every included file. README.md distinguishes immediate summary-dashboard use from full experimental reproduction requiring the original data and caches.')
    cw=read('literature_crosswalk.csv');cross=[]
    for pid in ORDER:cross.append(f'[{REF[pid]}] '+ '; '.join(cw[cw.paper_id.eq(pid)].crosswalk_id.astype(str)))
    para('Citation crosswalk (Phase1/Phase2 source positions): '+ ' | '.join(cross)+'. Table9 preserves version-specific numerical claims; results/literature_facts.csv retains extracted supporting page text.')
    timing=[]
    for name in ['feature_summary.json','resnet50_embedding_state.json','dinov2_embedding_state.json','sensitivity_pixel_protocol.json','stage6_protocol.json','stage7_8_protocol.json','border_sensitivity_summary.json']:
        ob=json.loads((OUT/name).read_text());timing.append(name.replace('.json','')+': '+f(ob.get('seconds',float('nan')))+' s')
    para('Recorded invocation times: '+'; '.join(timing)+'. These may include resumed cache loading; encoder times exclude cold native-library startup. They are not a reconstructed total project runtime.')
    para('The completed empirical verification recorded179 checks, including frozen-prediction reproduction from cached splits and numerical statistical checks. The previous report-specific verification is historical; the submission has its own current structural, numerical, citation, visual and package checks. Ten synthetic/numerical unit tests cover features, W₁, group randomization and k-means. No test result is treated as evidence that subject or encoding controls passed.')
    bm=read('baseline_metrics.csv').set_index('model')
    para('Frozen probe settings (regularization C; AI-positive probability threshold): '+'; '.join(f'{model}: C={bm.loc[model,"C"]:g}, threshold={bm.loc[model,"threshold"]:.6f}' for model in ['handcrafted','frequency','resnet50','dinov2','metadata_gated'])+'. C was chosen by validation AUROC and the threshold by validation F1. Each final fit uses 18,000 development artworks; validation and test contain 6,000 artworks each. These settings are held fixed during the perturbation tests.')
    heading('Appendix B: Extended Statistical & Sensitivity Tables')
    para('The extended tables are supplied as machine-readable CSVs rather than repeating1040 rows in print: style_feature_drift.csv (all features/styles, W₁, KS D, signed shift, CI, p/BH, null P95, eligibility); sliced_wasserstein.csv (128 fixed directions); origin_silhouette_ari.csv (H–C, PCA2/3 and full space); color_saturation_ablation.csv (development tertiles); failure_trigger_rates.csv and failure_trigger_associations.csv; border_paired_statistical_tests.csv; control_gate_ablation.csv. These files retain full precision and unsupported flags. The following compact extracts summarize the extended sensitivity evidence.')
    a=read('sliced_wasserstein.csv');para('Sliced-Wasserstein distances: '+'; '.join(style(r.iloc[0])+': '+f(r.iloc[1]) for _,r in a.iterrows())+'. All directions and scaling were frozen; these are descriptive distances.')
    a=read('color_saturation_ablation.csv');para('Color-by-saturation AUROC extracts: '+'; '.join(f'{r.model}/{r.tertile}: {r.roc_auc:.4f}' for r in a.itertuples())+'. Tertiles use development boundaries; varying performance does not identify a causal color effect.')
    a=read('control_gate_ablation.csv');para('Control-ablation AUROCs: '+'; '.join(f'{r.model}: {r.roc_auc:.4f}' for r in a.itertuples())+'. Full-release metadata and mixed45,000-pixel comparisons have different source composition and must not be interpreted as a paired causal resolution intervention.')
    para('Selected feature-level entries underlying Figure 8 are reproduced below as compact readouts of the extended statistical table. The feature list comes from development coefficients; displayed styles rotate Renaissance, Impressionism and Ukiyo-e as fixed by the figure renderer. These are not the strongest test effects, and no new multiple-testing family is created. All distances and intervals below use development-fitted standardization; Figure 8 itself displays raw units.')
    drift=read('style_feature_drift.csv');selected=read('display_feature_selection.csv').feature.tolist()
    for j,feature in enumerate(selected):
        movement=['renaissance','impressionism','ukiyo-e'][j%3];r=drift[(drift.feature==feature)&(drift['style']==movement)].iloc[0]
        para(f'{style(movement)} — {feature}: W₁={r.w1:.4f}; KS D={r.ks_D:.4f}; signed median shift={r.median_shift:+.4f}, 95% group-bootstrap CI [{r.shift_ci_low:+.4f}, {r.shift_ci_high:+.4f}]; BH-adjusted p={r.p_adj:.6f}; split-half null P95={r.null_p95:.4f}. Raw numerical rule: {"pass" if r.raw_rule_pass else "does not pass"}; confirmatory eligibility: no.')
    doc.core_properties.title='Explainable Visual Analytics of Human and Diffusion Artwork';doc.core_properties.author='Wasil Kayani; Umar Asghar';doc.core_properties.subject='Milestone 3 Research Implementation and Experimental Evaluation'
    doc.save(DEST/(NAME+'.docx'))
    (DEST/'submission_report_manifest.json').write_text(json.dumps({'tables':used,'figures':figure_records,'references':ORDER},indent=2),encoding='utf-8')
    print('Built portrait report;13 tables,12 figure numbers',flush=True)
if __name__=='__main__':main()
