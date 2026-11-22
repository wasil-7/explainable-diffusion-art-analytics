"""Stage 11 deterministic report authoring from frozen empirical evidence."""
from common import *
import numpy as np,shutil,hashlib,re
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import pymupdf as fitz

DEST=ROOT/'phase3_output'; REPORT=DEST/'report';FIG=DEST/'figures';QA=DEST/'qa'
for folder in [REPORT,FIG,QA,DEST/'report_tables',ROOT/'figures']:folder.mkdir(exist_ok=True,parents=True)
def read(n):return pd.read_csv(OUT/n)
def fmt(v):
    if pd.isna(v):return 'Not defined'
    if isinstance(v,(bool,np.bool_)):return 'Yes' if v else 'No'
    if isinstance(v,(float,np.floating)):return f'{v:.6f}'
    return str(v)

ORDER=['1c5b90c3f4ee','601afa6e41bc','268221a5e3f9','6c04d0eeab5e','7174ac285c4f','db8080fbeb05','013f01af5670','5a21e33267e5','b11a212074da','8c3f3f2351ec','23ae70d55065','5cbf64c5f2f5','7a92da907ad0','c6446b5d4119','b8504307f55a','39084024fc88']
REF={p:i+1 for i,p in enumerate(ORDER)}

def table_specs():
    t={};t['0']=('Brief component to section mapping',read('brief_component_mapping.csv'),['brief_component_mapping.csv']);ch=read('report_methodology_changes.csv');t['1']=('Documented methodology changes',ch,['report_methodology_changes.csv'])
    a=read('audit_counts.csv');t['2']=('Full release audit by origin and native dimensions',a.groupby(['origin','width','height','format','mode'],as_index=False)['count'].sum(),['audit_counts.csv'])
    full=pd.read_parquet(OUT/'split_manifest.parquet');co=pd.read_parquet(OUT/'cohort_manifest.parquet');rr=[]
    for label,d in [('Full release',full),('Balanced tier two',co),('Native256 Human LD',co[co.primary_eligible])]:
        for split,g in d.groupby('split'):rr.append(dict(cohort=label,split=split,artworks=len(g),source_groups=g.group_id.nunique()))
    t['3']=('Grouped development validation and test split counts',pd.DataFrame(rr),['split_manifest.parquet','cohort_manifest.parquet'])
    t['4']=('Synthetic feature unit tests',read('unit_test_results.csv'),['unit_test_results.csv'])
    b=read('baseline_metrics.csv');b=b[b.model.isin(['handcrafted','frequency','metadata_gated','resnet50','dinov2'])]
    t['5']=('Identical test cohort baseline metrics',b[['model','accuracy','balanced_accuracy','precision','recall','f1','roc_auc','ece','n']],['baseline_metrics.csv'])
    t['6']=('Macro style performance and validation selected settings',b[['model','macro_style_auc','macro_style_f1','C','threshold','development_n','validation_n']],['baseline_metrics.csv'])
    p=read('pca_projection_fidelity.csv');p['representation']='Fixed PCA';s=read('projection_fidelity.csv');s=s[['perplexity','seed','k','n','trustworthiness','continuity']];s['representation']='Exploratory tSNE';t['7']=('Projection neighborhood fidelity',pd.concat([p[['representation','dimensions','k','n','trustworthiness','continuity']],s],ignore_index=True).fillna('Not applicable'),['pca_projection_fidelity.csv','projection_fidelity.csv'])
    t['8']=('Style conditioned feature family drift summaries',read('style_family_drift.csv'),['style_family_drift.csv'])
    facts=read('literature_facts.csv').fillna('');rows=[]
    for pid in ORDER:
        for r in facts[facts.paper_id==pid].to_dict('records'):
            rows.append({'Study and venue':f'[{REF[pid]}] '+r['title']+'; '+r['venue'],'Source type and PDF locator':r['pdf_version_type']+'; PDF p. '+str(r['page_number'])+'; '+r['table_figure'],'Dataset and protocol':r['dataset']+'; '+r['split_protocol'],'Task and endpoint':r['task']+'; '+r['metrics'],'Paper reported result':r['headline_numbers'],'Comparability and caveats':'Context only. Different split, training, source coverage or endpoint; not a direct ranking. '+('Joint source/style and attribution differ from binary detection.' if pid==ORDER[0] else 'Available PDF version governs the claim.')})
    for r in b.to_dict('records'):rows.append({'Study and venue':r['model'],'Source type and PDF locator':'OURS; baseline_metrics.csv','Dataset and protocol':'Frozen native256 Human/LD; grouped source families','Task and endpoint':'Binary origin; AUROC and F1','Paper reported result':f"AUROC {r['roc_auc']:.6f}; F1 {r['f1']:.6f}",'Comparability and caveats':'Same test artworks internally; subject and JPEG confounded. No cross-paper superiority claim.'})
    t['9']=('Quantitative and methodological comparison with collected literature',pd.DataFrame(rows),['literature_facts.csv','baseline_metrics.csv'])
    a=read('ablation_results.csv');t['10']=('Paired feature family ablations',a[a.kind=='family'][['label','roc_auc','f1','delta_auc','delta_auc_low','delta_auc_high','delta_silhouette','delta_silhouette_low','delta_silhouette_high']],['ablation_results.csv'])
    t['11']=('Representation and geometry ablations',a[a.kind!='family'][['label','n_features','roc_auc','f1','delta_auc','delta_auc_low','delta_auc_high']],['ablation_results.csv'])
    t['12']=('Frozen probe perturbation robustness',read('perturbation_results.csv')[['view','roc_auc','f1','silhouette_retention','style_w1_rank_rho','delta_auc_low','delta_auc_high']],['perturbation_results.csv'])
    g=read('error_gallery_cases.csv');t['13']=('Actual held out forensic case index',g[['artwork_id','selection_reason','origin','style','prob_ai','H_pooled','C_pooled']],['error_gallery_cases.csv'])
    cw=read('literature_crosswalk.csv');cw['Reference']=cw.paper_id.map(REF);t['A1']=('Citation source crosswalk',cw[['Reference','crosswalk_id','pdf_version_type','pdf']],['literature_crosswalk.csv'])
    ext=read('style_feature_drift.csv');top=read('display_feature_selection.csv').feature;t['B1']=('Extended style tests for development selected display measurements',ext[ext.feature.isin(top)][['style','feature','w1','ks_D','median_shift','shift_ci_low','shift_ci_high','p_adj','null_p95','raw_rule_pass','confirmed_drift']],['style_feature_drift.csv','display_feature_selection.csv'])
    t['B2']=('Sliced Wasserstein distances and fixed projection count',read('sliced_wasserstein.csv'),['sliced_wasserstein.csv'])
    t['B3']=('Origin silhouette and unsupervised clustering agreement',read('origin_silhouette_ari.csv'),['origin_silhouette_ari.csv'])
    t['B4']=('Color representations across development saturation tertiles',read('color_saturation_ablation.csv'),['color_saturation_ablation.csv'])
    t['B5']=('Failure trigger error rates',read('failure_trigger_rates.csv'),['failure_trigger_rates.csv'])
    t['B6']=('Conditional source group confidence intervals for failure associations',read('failure_trigger_associations.csv').drop(columns='interpretation'),['failure_trigger_associations.csv'])
    t['B7']=('Matched and mixed cohort control ablation',read('control_gate_ablation.csv')[['model','scope','roc_auc','balanced_accuracy','f1','n']],['control_gate_ablation.csv'])
    return t

def main():
    pd.DataFrame([['Implementation','3','1','0'],['Dataset and preprocessing','4–5','2–4','1'],['Baseline evaluation','6','5–6','7'],['Graphical visual analytics','7','7–8','2–6'],['Literature comparison','8','9','Not applicable'],['Ablations and robustness','9','10–12','8–9'],['Results analysis and discussion','10','13','10']],columns=['Brief component','Report section','Tables','Figures']).to_csv(OUT/'brief_component_mapping.csv',index=False)
    ch=read('methodology_changes.csv');ch.insert(3,'Justification',['Missing subject and JPEG overlap','Preserve source dependence','Preserve group-level variation','Native clustering DLL blocked','Evaluate both recorded color representations','Separate global from local context','Keep fixed geometry computation tractable','Retain frozen intensive pixel cohort','Preserve paired supported IDs','Semantic annotations unavailable','Release originals already compressed','Avoid test-selected display ranking','Only release styles supported','Optional Arrow DLL blocked']);ch.to_csv(OUT/'report_methodology_changes.csv',index=False)
    specs=table_specs();doc=Document();normal=doc.styles['Normal'];normal.font.name='Times New Roman';normal.font.size=Pt(12);normal.paragraph_format.line_spacing=1.15;normal.paragraph_format.space_after=Pt(7)
    for name in ['Title','Heading 1','Heading 2','Heading 3']:
        st=doc.styles[name];st.font.name='Times New Roman';st.font.color.rgb=RGBColor(0,0,0);st.font.bold=True
    doc.styles['Heading 1'].font.size=Pt(17);doc.styles['Heading 2'].font.size=Pt(13)
    pending_body=False
    def layout(w=8.27,h=11.69,new=True):
        nonlocal pending_body
        pending_body=False
        sec=doc.add_section(WD_SECTION_START.NEW_PAGE) if new else doc.sections[0];sec.page_width=Inches(w);sec.page_height=Inches(h)
        sec.top_margin=sec.bottom_margin=Inches(.7);sec.left_margin=sec.right_margin=Inches(.75);sec.header_distance=sec.footer_distance=Inches(.3)
        return sec
    layout(new=False)
    foot=doc.sections[0].footer.paragraphs[0];foot.alignment=2;foot.add_run('DAV Phase 3  |  ');field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');foot._p.append(field)
    for run in foot.runs:run.font.size=Pt(9)
    def para(text,style=None):
        if pending_body:layout()
        p=doc.add_paragraph(text,style);p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY if style is None else WD_ALIGN_PARAGRAPH.LEFT;p.paragraph_format.keep_together=True;return p
    def chapter(n,heading):layout();doc.add_heading(f'{n} {heading}',1)
    def sub(heading,text):
        if pending_body:layout()
        doc.add_heading(heading,2);para(text)
    used=[]
    def tab(key,wide=True):
        title,df,sources=specs[key];layout(16.54,11.69) if key=='9' else layout(11.69,8.27) if wide else layout()
        p=para('Table '+key+'  '+title);p.runs[0].bold=True;p.paragraph_format.keep_with_next=True
        table=doc.add_table(rows=1,cols=len(df.columns));table.style='Table Grid';table.autofit=False
        available=doc.sections[-1].page_width-doc.sections[-1].left_margin-doc.sections[-1].right_margin
        widths=[available/len(df.columns)]*len(df.columns)
        if key=='9':widths=[available*v for v in [.17,.13,.19,.13,.20,.18]]
        if key=='1':widths=[available*v for v in [.12,.18,.28,.17,.25]]
        for i,(c,w) in enumerate(zip(df.columns,widths)):
            table.columns[i].width=int(w);table.rows[0].cells[i].width=int(w);table.rows[0].cells[i].text=str(c).replace('_',' ')
        repeat=OxmlElement('w:tblHeader');table.rows[0]._tr.get_or_add_trPr().append(repeat)
        for row in df.itertuples(index=False,name=None):
            cells=table.add_row().cells
            for cell,value,w in zip(cells,row,widths):cell.text=fmt(value);cell.width=int(w)
        for ri,row in enumerate(table.rows):
            no=OxmlElement('w:cantSplit');row._tr.get_or_add_trPr().append(no)
            for cell in row.cells:
                if ri==0:
                    shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E9EDF1');cell._tc.get_or_add_tcPr().append(shade)
                for p in cell.paragraphs:
                    p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(3);p.paragraph_format.line_spacing=1
                    for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(9);r.bold=ri==0
        para('Source: '+', '.join('results/'+x for x in sources)+'. Numerical values are rounded only for display; native precision remains in the source artifacts. Undefined values are not interpreted as zero.').runs[0].font.size=Pt(9)
        used.append(key);df.to_csv(DEST/'report_tables'/f'Table_{key}.csv',index=False)
    manifest=read('figure_manifest.csv');captions=dict(zip(manifest.file,manifest.caption));embedded=[]
    def figure(n):
        nonlocal pending_body
        name='fig00_implemented_architecture.png' if n==0 else manifest.iloc[n-1].file
        source=OUT/name;shutil.copy2(source,FIG/name);shutil.copy2(source,ROOT/'figures'/name)
        # Large scientific figure spreads preserve the original composite typography.
        layout(23.39,33.11) if n==10 else layout(23.39,16.54)
        para(f'Figure {n}  '+('Implemented architecture' if n==0 else name[6:-4].replace('_',' '))).runs[0].bold=True
        from PIL import Image
        im=Image.open(source);w,h=im.size;maxw=21.3;maxh=28 if n==10 else 12.6;width=min(maxw,maxh*w/h)
        doc.add_picture(str(source),width=Inches(width));p=para(captions.get(name,'The frozen cohort branches into descriptive feature analytics and frozen probe evaluation. A failed subject or encoding gate blocks confirmatory attribution; figures and report consume cached measurements.'))
        p.runs[0].font.size=Pt(10);embedded.append(name);pending_body=True
    # Cover reproduces the supplied institutional identity without fabricating a logo.
    ref=fitz.open(ROOT/'i242551_i242532_Milestone02_DSB.pdf');image=ref.extract_image(ref[0].get_images()[0][0]);logo=QA/'university_logo.png';logo.write_bytes(image['image']);p=doc.add_paragraph();p.add_run().add_picture(str(logo),width=Inches(.75));p.add_run('  National University of Computer and Emerging Sciences').bold=True
    para('');p=doc.add_paragraph('Data Analysis and Visualization','Title');p.alignment=1
    p=doc.add_paragraph('Milestone 3','Title');p.alignment=1
    p=para('Explainable Visual Analytics of Human and Diffusion Artwork');p.alignment=1;p.runs[0].bold=True
    p=para('Research Implementation and Experimental Evaluation');p.alignment=1
    for text in ['Wasil Kayani (24i-2551)','Umar Asghar (24i-2532)','BS Data Science  |  Section B','Submitted to Ma’am Azka Atif','15 November 2026']:p=para(text);p.alignment=1
    para('This report evaluates reproducible within-style artwork measurements and detector probes. Strong release-origin prediction is observed, but subject uncertainty and origin-aligned JPEG encoding prevent confirmation of an independent diffusion-origin effect.')
    chapter(1,'Abstract')
    para('This study implements explainable visual analytics for human and diffusion artwork in AI-ArtBench. The audit covers 185,015 readable images, and grouped development, validation and test splits preserve known source families and duplicate links. A balanced cohort contains 45,000 artworks; the primary native-resolution comparison uses 30,000 Human and Latent Diffusion artworks, including 6,000 held-out test images. Four disjoint quadrants yield ordinal, spectral, Haar wavelet and color measurements. Fixed principal components, an entropy–complexity atlas and audited exploratory projections support inspection. The handcrafted logistic probe achieves AUROC 0.982415, compared with 0.999945 for frozen ResNet-50, 0.999688 for frozen DINOv2 and 1.000000 for metadata. Among 1,040 feature-by-style comparisons, 542 pass an exploratory adjusted-probability and split-half rule. However, JPEG quantization identifies origin and subject matching is unverifiable; consequently no comparison is eligible for confirmatory attribution. Removing ordinal features reduces AUROC to 0.907994, and JPEG quality 50 reduces it to 0.681893. The contribution is a reproducible, inspectable descriptive atlas and a diagnosis of unresolved controls, rather than confirmation of diffusion-specific aesthetic change.')
    sub('Brief component mapping','Component 1: Section 3 and Figure 0. Component 2: Sections 4–5 and Tables 2–4. Component 3: Section 6 and Tables 5–6. Component 4: Section 7 and Figures 1–7. Component 5: Section 8 and Table 9. Component 6: Section 9 and Tables 10–12. Component 7: Section 10, Table 13 and Figure 10. Conclusion and references are Sections 11–12. Appendices A–C provide provenance, extended results and verification. Numbering retains every master-prompt topic while placing discussion in Section 10 as requested.')
    tab('0',False)
    chapter(2,'Introduction and Research Objectives')
    para('The central question is whether human and diffusion artworks within the same historical movement differ in named ordinal, spatial-frequency and color features after subject, native dimension and file controls. Drift denotes a within-style distribution contrast; it is not temporal evolution or an aesthetic quality judgment. ArtBrain supplies the art benchmark and learned attribution setting [1], while the complexity–entropy study of contemporary platform art motivates interpretable measurement axes [2].')
    para('B-Free motivates content alignment and nuisance controls [3]. SCADET motivates comparisons of local and global artwork context [4]. SPAI, FIRE and VIB-Net motivate frequency and representation checks [5], [6], [7], and CoDA motivates saturation-conditioned color analysis [8]. These approaches differ in training, datasets and endpoints and are not direct performance competitors under the present protocol.')
    para('PixelatedScatter motivates count-aware abstraction [9], and MisVisFix motivates visible diagnostics and inspectable views [10]. These designs do not themselves establish neighborhood fidelity on artworks. Art-evolution regression [11], human perception benchmarks [12], pixel inconsistency detection [13], SIDWA [14], TRACE region analysis [15] and artwork DINO classification [16] provide additional context; their numerical results remain explicitly paper-reported and version-scoped in Table 9.')
    sub('Gaps and prespecified hypotheses','G1 concerns inspectability and projection fidelity. G2 concerns signed style-conditional human–diffusion differences. G3 asks whether separation survives subject and file controls. The empirical alternative for each feature/style cell is a nonzero distribution difference, with direction summarized by the AI-minus-Human median shift. The planned confirmation rule requires adjusted p below 0.05 and W1 above its within-origin split-half 95th percentile. That rule is necessary within the statistical protocol but cannot supersede the control-variable gate. Failed controls restrict all such findings to description.')
    chapter(3,'Implementation and Documented Methodology Changes')
    para('The implementation separates immutable data selection, development-only calibration, frozen representation fitting, test evaluation and reporting. Audit and split modules operate on the full release. Feature extraction, projections and baselines consume frozen artwork IDs. Later robustness views preserve those IDs and reuse fitted scalers and thresholds. The reporting layer reads results instead of retraining models. Figure 0 shows this dependency structure.')
    sub('Module organization and operational controls','The src directory contains orientation, audit, splits, features, projections, deep encoders, logistic probes, drift, ablations, sensitivity pixels and dashboard modules. Independent verification reproduces cached predictions and statistical calculations. CPU image extraction uses twelve processes; CUDA inference uses frozen evaluation-mode encoders and half precision. Batch caches support resumption but are invalid after changes to data, split or feature definitions. Run scripts synchronously and wait for their exit codes.')
    para('The Phase 2 feedback required measurable comparisons, a narrower within-style question, explicit controls, transparent features and projection diagnostics. These are implemented, but the missing subject support and encoding overlap are treated as failed validity conditions. Table 1 records adjustments and their costs; these are not retrospective changes designed to create a positive finding.')
    tab('1');figure(0)
    chapter(4,'Dataset Audit Preprocessing and Experimental Setup')
    para('Every release file was decoded and audited before sampling. The release contains 60,000 Human, 62,092 Latent Diffusion and 62,923 Stable Diffusion artworks. Human and LD images are native 256 by 256; SD images are native 768 by 768. All are JPEG RGB. No decode failures, embedded ICC profiles or EXIF records were found. Known exact duplicate pairs and conservative perceptual duplicate candidates were linked before grouping. Folder style labels were normalized without claiming verified artwork dates or subject semantics.')
    tab('2');tab('3');figure(1)
    sub('Preprocessing and grouping','EXIF orientation and ICC-to-sRGB conversion are implemented even though the audited release has no such metadata. The primary images retain native dimensions and are divided into four nonoverlapping 128 by 128 quadrants. Human artist filename prefixes and conservative AI filename-prefix families are grouped globally, together with duplicate links. AI prefix semantics are unverified and must not be called known prompt IDs. A grouped split prevents known linked files from crossing partitions; it cannot prove independence of unknown derivatives or subjects.')
    sub('Control variable gate','Native dimensions, JPEG format and balanced movement support are technically matched for Human versus LD. The complete gate nevertheless fails. The Human JPEG quantization profile has no common support with the generated profiles, and the metadata-only primary probe reaches AUROC 1.0. No sidecar prompt or subject annotations establish semantic matching. The balanced 45,000-image tier supports computationally intensive features and embeddings; SD remains a separate resized sensitivity, not an eligible primary control.')
    chapter(5,'Mathematical Features Calibration and Reproducibility')
    cal=json.loads((OUT/'feature_calibration.json').read_text());env=json.loads((OUT/'environment.json').read_text())
    sub('Ordinal structure','Luminance is computed from sRGB values. Overlapping row-major 2 by 2 neighborhoods produce 4! = 24 possible order patterns. Stable sorting provides deterministic lexicographic tie handling. Pattern counts are pooled over quadrants before calculating normalized entropy H = −sum(p log p)/log(24). Statistical complexity is H multiplied by Jensen–Shannon divergence from uniform, normalized by the divergence of a point mass from uniform. Tie-excluded variants are cached separately. An empty valid-pattern set is undefined rather than assigned a favorable value.')
    sub('Frequency and wavelet energy','The FFT uses mean-centered luminance and a separable Hann window. Nonzero radial frequencies through 0.5 cycles/pixel are divided into sixteen annuli. Annular shares normalize retained power, high-frequency share uses frequencies above 0.25, and beta is the log mean-power versus log-frequency slope. Two-level periodized Haar decomposition retains LL2 and six detail energies, normalized by total raw luminance energy. LH denotes row-highpass response to horizontal edges, HL column-highpass response, and HH diagonal response. Mean removal is not applied to the Haar energy denominator.')
    sub('Color edges and artwork aggregation',f"Hue is represented by sine, cosine and resultant magnitude rather than a wrapped scalar predictor. The development-only saturation cutoff is {cal['saturation_cutoff']}; the frozen Sobel threshold is {cal['sobel_threshold']:.12f}. Saturation and value medians/IQRs, circular correlations, Lab summaries and edge density are retained. Crop measurements are aggregated using median and IQR; pooled ordinal statistics are separate. Undefined correlations remain flagged and are imputed only through development-fitted preprocessors. There are 169 cached measurements and 104 primary probe predictors; full-canvas, tie-excluded, undefined-count and wrapped hue-angle fields are excluded from the primary vector.")
    tab('4')
    sub('Hardware and frozen training protocol',f"The recorded environment is Python {env['python']}, {env['gpu']} with approximately four GB device memory and twelve logical CPUs. All random seeds use 42. Robust scaling and median imputation are fitted on development only; deep embeddings use StandardScaler. Logistic regularization is selected from the fixed candidate grid using the single validation partition, followed by a development-only final fit. The AI threshold maximizes validation F1. Test predictions are evaluated with those frozen choices. Encoder inference uses batches of thirty-two quadrant crops, four loader workers and float16 CUDA computation; artwork embeddings average four crops.")
    sub('Recorded timing scope','Runtime artifacts distinguish completed extraction from cold native-library loading. Per-invocation analysis times can include resumed cache loading and cannot reconstruct the total time spent in earlier failed invocations. Encoder timings exclude startup. Appendix A records the exact saved timing values with these qualifications; no total experiment runtime is estimated.')
    chapter(6,'Baseline Evaluation')
    para('The five primary probes share the same held-out Human/LD artwork IDs and the same source-group partition. Handcrafted measurements expose named features; FFT-only isolates the radial spectrum family. Frozen ResNet-50 ImageNet V2 and DINOv2 ViT-S/14 provide learned representations with logistic probes. Metadata provides the shortcut diagnostic rather than an artwork-content model. Accuracy, balanced accuracy, positive-class precision/recall/F1, AUROC and fifteen-bin expected calibration error are shown in Table 5; Table 6 reports movement macro averages and validation-selected settings.')
    tab('5');tab('6');figure(7)
    para('The handcrafted AUROC of 0.982415 establishes strong release-origin discrimination on this split. It does not identify why the distributions differ. Both deep encoders approach perfect ranking, while metadata is perfect; the correct interpretation is that this benchmark exposes easy source-associated cues under the observed release composition. AUC near one neither proves aesthetic fidelity nor establishes generator-general content recognition. Calibration error and F1 describe different aspects of the same frozen predictions and should not be substituted for one another.')
    chapter(7,'Graphical Results and Interactive Visual Analytics')
    sub('Entropy complexity atlas','Figure 2 displays every supported movement with common axes, within-cell density contours, source-group centroid uncertainty and signed displacement arrows. These arrows summarize observed distributions. The inherited filename contains the word causality, but the atlas does not identify a causal effect. Human artist groups are fewer than AI filename groups in some movements, so balanced artwork counts do not imply equal effective sample sizes or a universal standard-error bound.')
    figure(2);figure(3);tab('7')
    sub('Projection fidelity and spectral interpretation','PCA is fitted on development only; its fixed coordinates are used on held-out artworks. The large explained-variance fraction does not guarantee neighborhood preservation, as the lower PCA trustworthiness demonstrates. Exploratory t-SNE uses a frozen balanced subset, five random initializations and three perplexities. Seed ranges are stability diagnostics, not confidence intervals. No hypothesis test or cluster discovery claim uses t-SNE distances. Figure 4 contrasts normalized FFT and raw-energy wavelet summaries; SD is explicitly labeled as a resized sensitivity.')
    figure(4);figure(5);figure(6);tab('8')
    sub('Distance tests and decision eligibility','W1 and KS D are calculated for each prespecified standardized feature within style. Median shifts and source-group bootstrap intervals retain direction. Sliced W1 uses 128 fixed unit projections; source dispersion uses AI/Human IQR ratios, with zero-denominator cases marked undefined. Whole-group label randomization preserves the number of AI groups but can alter artwork totals. Because exchangeability under unverified subjects and encoding is unsupported, the resulting adjusted probabilities are exploratory diagnostics. BH correction covers the complete 1,040-test grid; it does not repair invalid controls.')
    sub('Dashboard architecture and walkthrough','The Streamlit and Plotly dashboard reads cached CSV/Parquet outputs. Users filter movements and origins, switch among H–C, fixed PCA and exploratory t-SNE, and choose raw artworks or fixed-bin hexagonal counts. Fidelity badges and the failed-gate banner remain visible. Selecting an artwork reveals its actual quadrants, FFT curve, Haar energies and color/edge summary. Other tabs expose baseline ROC, confidence intervals, drift, ablations, errors, figures and literature. Axis limits and bin boundaries remain fixed within a projection; the density colorbar rescales to active counts and states this explicitly. HTML tables avoid the host-blocked Arrow DLL. This is a count-aware abstraction inspired by PixelatedScatter, not a reproduction of its complete optimization algorithm [9]. The dashboard implements diagnostics rather than MisVisFix’s language-model chart repair [10].')
    chapter(8,'Comparison with Existing Research')
    para('Table 9 separates empirical results from externally reported claims. Every external numerical statement in the table comes verbatim from literature_facts.csv, with exact available PDF version, page and table/figure locator. These are evidence-scoped quotations of reported endpoints, not independent reproductions. Training, sampling, native resolution, generator coverage and endpoint differences prevent a valid cross-paper leaderboard. In particular, ArtBrain joint source/style F1 and generator attribution are not this binary task; AP is not AUROC; context regression is not classification; visualization issue detection is not projection fidelity.')
    tab('9')
    para('The same-dataset SCADET comparison is methodologically informative because crop context and source resolutions matter, but its split and learned system differ from the present frozen probe. B-Free concerns aligned photographic training and uses a different DINO configuration; the present DINOv2 probe does not reproduce it. The Kim study motivates ordinal descriptors without supplying a matched human/diffusion experiment. Reported color and frequency results motivate hypotheses, while the present failed control gate prevents those hypotheses from being confirmed on this release.')
    chapter(9,'Ablation and Perturbation Robustness Studies')
    sub('Feature family contribution','Table 10 compares leave-one-family-out and single-family probes using the same development, validation and test IDs. The fourth family includes HSV, Lab and edges; isolated HSV/Lab/combined alternatives are reported separately. Intervals use identical source-group bootstrap draws for baseline and variant, conditional on frozen models and thresholds. Delta F1 and silhouette accompany delta AUROC in the cached tables. Silhouette intervals resample fixed per-artwork silhouette scores and omit uncertainty from recomputing pairwise geometry.')
    tab('10');tab('11');figure(8)
    sub('Representation and control sensitivities','Removing ordinal features yields the largest family omission loss, but this does not identify ordinal structure as a causal generator signature. Tie exclusion changes the observable because repeated pixels can be associated with JPEG encoding, monochrome regions or art materials. The full-canvas vector has fewer predictors because it has no across-crop IQR, so the geometry comparison also changes dimension. Five crops add overlapping center coverage. Saturation tertiles are frozen development quantiles, not test-optimized bins. The unmatched pixel sensitivity uses the frozen balanced 45,000-image tier; full-release 185,015-image comparisons are metadata diagnostics. Different source composition means their score contrast is not an isolated estimate of resolution leakage.')
    tab('12');figure(9)
    sub('Stress tests and interpretive limits','JPEG recompression and bilinear down/upscaling are applied identically to both held-out origins without refitting the primary probe. Original JPEG files serve as the plotting reference, not pristine Q100 images. Style ranks summarize mean W1 over all prespecified predictors, avoiding test-selected feature rankings. Severe JPEG recompression reduces AUROC and style-rank stability even when silhouette increases. This divergence illustrates why visible separation and unsupervised geometry cannot stand in for robust source classification. Equal recompression is a sensitivity experiment, not a proof that the original encoding confound has been removed: prior compression information and unobserved subjects remain.')
    chapter(10,'Results Analysis and Discussion')
    sub('Why prediction and confirmation differ','The high baseline AUC and zero confirmed effects answer different questions. AUROC 0.982415 measures ranking of release-origin labels in the observed held-out distribution. The drift pipeline asks whether feature distributions differ within movement under a controlled comparison. A detector can exploit subject composition, artist/source selection, JPEG footprints and other correlates of release origin. Known-group separation protects against specific duplicate/family leakage, but does not remove these distributional shortcuts. Thus strong prediction remains a reproducible descriptive result while independent origin attribution is unsupported.')
    sub('Why the controls invalidate confirmatory use of all 542 passes','All 542 exploratory passes fail the prerequisite for confirmatory interpretation. Human and generated JPEG quantization tables have no common support, and the matched metadata probe predicts origin perfectly. Matching JPEG file extension and 256-square dimensions therefore does not match encoding. Decoded-pixel ordinal ties, gradients and spectra can retain compression-associated structure. Separately, no verified subject or prompt identifiers establish semantic overlap. Within-movement comparisons may therefore compare different subject mixtures or materials. In a causal description, origin is associated with encoding, encoding affects measured pixels, and selection into origin groups can share causes with subject content. Conditioning only on movement and dimensions does not block these paths.')
    para('The numerical W1 values, signed shifts and observed label-prediction scores are not erased by this failure. What is invalidated is their use as statistically confirmed diffusion-specific or content-independent effects. BH adjustment controls multiplicity only when the underlying probability model is appropriate. It cannot create exchangeability of source-group labels when encoding and subjects differ. Group bootstrap intervals represent sampling variation conditional on observed groups and cannot remove systematic bias. The conjunction of an adjusted probability and a split-half threshold is therefore insufficient once the control gate fails. The correct eligible confirmation count is zero, not 542; zero eligibility is not evidence that the true human/diffusion effect is zero.')
    sub('What the evidence does and does not identify','Metadata AUROC 1.0 proves that the release contains a perfect technical discriminator under this protocol. It does not establish the fraction of handcrafted or deep-model AUROC caused by compression. No controlled re-encoding experiment with common original sources, subject matching or validated overlap identifies that decomposition. The JPEG stress test shows sensitivity, not causal mediation. Results must not be generalized to unseen generators, unknown encodings, subject-matched paintings or out-of-distribution artwork without a new evaluation. The successful group partition also does not substitute for explicit leave-style-out or leave-generator-out experiments; these were not performed and remain an external-validity limitation.')
    sub('Gap G1 inspectability and projection fidelity','G1 is substantially addressed at the implementation and diagnostic level: named ordinal/spectral/color features are linked to artworks; fixed PCA loadings are visible; t-SNE seed and perplexity fidelity are measured; counts, source-group uncertainty and supported cells are exposed. This does not establish a user-study benefit or a faithful causal embedding. Low PCA neighborhood fidelity and weak origin agreement with unsupervised clusters are useful negative findings rather than defects to conceal.')
    sub('Gap G2 style conditional differences','G2 is partly addressed descriptively. The complete style-by-feature grid, signed shifts, W1, KS D, dispersion, sliced W1 and source-group uncertainty describe which distributions differ in the observed release. The 542 exploratory passes organize candidate contrasts. They cannot establish diffusion-specific stylistic displacement under subject and encoding control. A future preregistered analysis must rebuild eligible matched support and freeze its protocol before using a fresh test set.')
    sub('Gap G3 separation after subject and file controls','G3 remains unresolved as a positive claim and is answered negatively as a control audit: the present technical matching fails to establish the necessary subject and encoding support. The work demonstrates why the requested control gate is essential, locates a perfect JPEG shortcut, and prevents overinterpretation of the atlas. It does not demonstrate that visible separation survives all required controls. This limitation narrows the research conclusion without negating the reproducible measurement, dashboard or failure-diagnosis contributions.')
    sub('Forensic evidence and boundary sensitivity','The gallery samples confident false positives, false negatives, true positives and extreme H–C/PCA cases from actual test artwork. It is deliberately selected for inspection, not an estimate of error prevalence. Low saturation, low edge density and high-frequency thresholds were set using development quantiles; a fixed outer-strip heuristic flags likely boundary-dominated crops. These proxies are not verified subject, paint-medium or frame annotations, and their overlaps prevent causal trigger interpretation. Error-rate gaps and conditional group intervals are reported in Appendix B.')
    border=json.loads((OUT/'border_sensitivity_summary.json').read_text());para(f"The boundary heuristic flags {border['flagged_artworks']} test artworks; {border['all_crops_excluded']} have no retained quadrant. Both sensitivity arms use the identical {border['paired_supported_n']} supported artwork IDs. Excluding flagged quadrants reverses {border['direction_reversals']} signed feature/style directions and {border['exploratory_rule_reversals']} exploratory rule outcomes. Both arms still have zero eligible confirmatory effects. These reversals show local sensitivity; they do not repair missing subject metadata or JPEG common support.")
    tab('13');figure(10)
    sub('Strengths limitations and reference integrity','Strengths are the full-file audit, frozen grouping, development-only fitting, five shared-test probes, complete null caches, explicit uncertainty and reproducible reports. Limitations include uncertain AI family semantics, unknown derivatives, fewer effective human source groups, unverified subjects, deterministic encoding differences, resized SD, representation-dependent distances, conditional bootstrap assumptions and closed-release testing. Paper versions and task endpoints add comparison uncertainty. Two duplicate bibliography entries reduce eighteen source entries to sixteen unique papers; corrected author metadata and version discrepancies are retained in the crosswalk. Unverified earlier headline claims are not imported into this report.')
    chapter(11,'Conclusion and Future Work')
    para('The project delivers a reproducible implementation, explanatory measurements, held-out baselines, a visual atlas and an interactive dashboard. High AUC describes separation in this release, while the failed control gate prevents confirmation of an independent diffusion-origin effect. G1 is substantially implemented, G2 is characterized descriptively, and G3 remains unsupported under the available controls. The principal scientific result is the distinction between measurable association and valid attribution.')
    para('Future work should obtain verified subject/source links, preserve original encodings, establish common support and apply controlled processing before cohort freezing. Re-encoding alone cannot restore lost originals or semantic equivalence. A fresh held-out evaluation should include leave-artist, leave-style and unseen-generator protocols where support permits. It should report negative and unsupported cells, source-group uncertainty and projection fidelity using the same decision rules. Human evaluation of the dashboard and medium-specific analysis require independently labeled data rather than interpreting filename or visual proxies as ground truth.')
    chapter(12,'References')
    facts=read('literature_facts.csv').drop_duplicates('paper_id').set_index('paper_id')
    for pid in ORDER:
        r=facts.loc[pid];p=para(f"[{REF[pid]}] {r.authors.replace(';', ',')}. {r.title}. {r.venue}, {r.year}. Available source: {r.pdf_version_type}. {r.doi}");p.runs[0].font.size=Pt(10)
    chapter('Appendix A','Reproducibility Manifest and Citation Crosswalk');para('The Phase 3 citation order is defined by first appearance in Section 2 and deduplicates source entries. The crosswalk retains both Phase 1 and Phase 2 locations. Source indexes and PDF hashes are independently verified. The frozen cohort SHA256 is '+json.loads((OUT/'control_gate.json').read_text())['manifest_sha256']+'.');tab('A1')
    layout();doc.add_heading('Recorded invocation timings',2)
    for name in ['feature_summary.json','resnet50_embedding_state.json','dinov2_embedding_state.json','sensitivity_pixel_protocol.json','stage6_protocol.json','stage7_8_protocol.json','border_sensitivity_summary.json']:
        obj=json.loads((OUT/name).read_text());para(name+': '+str(obj.get('seconds','Not recorded'))+' seconds. '+obj.get('runtime_scope','Extraction/invocation timing as stored; not a reconstructed total experiment time.'))
    para('Reproduction: set PIP_CACHE_DIR=D:\\Dev\\pip_cache and TEMP=D:\\Dev\\tmp. Use D:\\Dev\\envs\\dav_phase3\\python.exe. Run src/verify_stage10.py for cached empirical verification, src/build_report.py for deterministic document construction and src/verify_report.py for final report checks. Launch the dashboard with python -m streamlit run src/dashboard.py. Source paths, cell provenance and report artifact hashes are retained in phase3_output/.')
    chapter('Appendix B','Extended Statistical and Sensitivity Tables');para('Complete native-precision feature/style results remain in results/style_feature_drift.csv. Table B1 includes all movements for the six display measurements selected exclusively from frozen development coefficients. It is not a new test subset or a second FDR family. All confirmation flags remain false. Tables B2–B7 expose projection, color, trigger and cohort sensitivities.');
    for key in ['B1','B2','B3','B4','B5','B6','B7']:tab(key)
    chapter('Appendix C','Synthetic Tests and Verification Record');para('Table 4 contains the seven original synthetic feature tests. Three additional numerical tests validate empirical CDF W1 against SciPy for unequal sample sizes, exact separated-cluster recovery by NumPy Lloyd k-means, and whole-source-group randomization. The fresh-process cached checkpoint verification passed 179 checks before report construction; the final report-specific checklist records the seven quality gates, exact table/page locations, citation evidence, layout review and artifact hashes. Undefined monochrome hue is explicitly labeled rather than displayed as a measured zero.')
    para('Standard tests cover constant and monochrome images, ramps, white noise, sinusoidal frequency behavior, quadrant coverage and normalized entropy/complexity bounds. Validation proves implementation properties on controlled inputs; it does not validate the subject gate or make the empirical group-label exchangeability assumption true.')
    doc.core_properties.title='Explainable Visual Analytics of Human and Diffusion Artwork';doc.core_properties.author='Wasil Kayani; Umar Asghar';doc.core_properties.subject='DAV Phase 3 implementation and experimental evaluation'
    doc.save(REPORT/'Milestone3_Final.docx')
    save={'tables':[dict(key=k,title=specs[k][0],sources=specs[k][2]) for k in used],'embedded_figures':embedded,'reference_order':ORDER,'format':'Times New Roman 12pt body, 1.15 spacing; 9pt wide tables; large figure spreads preserve source typography','numbering':'Twelve numbered sections; Section10 discussion per user instruction; appendices unnumbered.'}
    (DEST/'report_manifest.json').write_text(json.dumps(save,indent=2),encoding='utf-8');shutil.copy2(OUT/'literature_facts.csv',DEST/'literature_facts.csv')
    print('Report DOCX built; tables',len(used),'figures',len(embedded),flush=True)

if __name__=='__main__':
    if '--dashboard-image-only' in sys.argv:
        import zipfile
        from lxml import etree
        name='i242551_i242532_Milestone03_DSB'
        target=ROOT/'phase3_output/submission_build'/(name+'.docx')
        with zipfile.ZipFile(target) as archive:
            entries={info.filename:(info,archive.read(info.filename)) for info in archive.infolist()}
        ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
        xml=etree.fromstring(entries['word/document.xml'][1]);previous=None;rel=None
        for paragraph in xml.findall('.//w:body/w:p',ns):
            text=''.join(paragraph.itertext())
            if text.startswith('Figure 9.'):
                rel=previous.find('.//a:blip',ns).get('{'+ns['r']+'}embed');break
            if paragraph.find('.//a:blip',ns) is not None:previous=paragraph
        assert rel
        rels=etree.fromstring(entries['word/_rels/document.xml.rels'][1])
        media='word/'+next(x.get('Target') for x in rels if x.get('Id')==rel)
        image=(ROOT/'figures/fig11_dashboard_ui.png').read_bytes()
        temporary=target.with_suffix('.swap.docx')
        with zipfile.ZipFile(temporary,'w') as archive:
            for path,(info,data) in entries.items():archive.writestr(info,image if path==media else data)
        temporary.replace(target)
        print('Replaced Figure 9 image only; all other DOCX entries preserved')
        raise SystemExit(0)
    if '--submission' in sys.argv:
        from build_submission import main as build_portrait_submission
        build_portrait_submission()
        raise SystemExit(0)
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(14,5));ax.axis('off');boxes=[('Audit full release\n185,015 files',.02),('Group and freeze\n60:20:20 split',.22),('Features and frozen\nencoder representations',.44),('Held-out probes\nand descriptive drift',.67)]
    for text,x in boxes:ax.text(x,.62,text,transform=ax.transAxes,bbox=dict(boxstyle='round,pad=.7',fc='#eef3f6',ec='#0072B2'),fontsize=12,va='center');
    for x in [.18,.40,.63]:ax.annotate('',xy=(x+.035,.62),xytext=(x,.62),xycoords='axes fraction',arrowprops=dict(arrowstyle='->'))
    ax.text(.5,.22,'Subject and JPEG gate FAILED → no confirmatory origin attribution\nCached tables → scientific figures → linked dashboard → report and verification',ha='center',va='center',fontsize=13,color='#8b2b1c',transform=ax.transAxes);fig.tight_layout();fig.savefig(OUT/'fig00_implemented_architecture.png',dpi=300);plt.close(fig)
    main()
