"""Six interactive views for the cached AI-ArtBench dashboard."""
from common import *
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from dashboard_theme import COLORS,PALETTE,CSS,style_figure

VIEWS=['01 Landing & Executive Summary','02 H–C Feature Atlas','03 Manifold & Fidelity (PCA/t-SNE)',
       '04 Spectral & Wavelet Profiles','05 Style Drift & Ablations','06 Forensic Error Gallery']
SHORT=['01 Overview','02 H–C Atlas','03 Manifold & Fidelity','04 Spectral Profiles','05 Drift & Ablations','06 Forensic Gallery']

def chart(fig,**kwargs):return st.plotly_chart(style_figure(fig),width='stretch',theme=None,**kwargs)
def navigate(index):st.session_state['view']=VIEWS[index]
def title(kicker,heading,description):
    st.markdown(f'<div class="eyebrow">{kicker}</div>',unsafe_allow_html=True)
    st.header(heading);st.markdown(description)

def landing(table,show_table,detail,features,cohort):
    st.markdown('''<section class="glass hero" aria-label="Executive summary"><div>
      <div class="eyebrow">A research atlas · AI-ArtBench</div>
      <h1>Explainable Visual Analytics of Human and Diffusion Artwork</h1>
      <p class="text-xl">Look beyond the prediction. Explore the mathematical texture, color and structure of art—and the controls that shape what we can conclude.</p>
      <div class="origin-key"><span><i class="dot" style="background:#2563EB"></i>Human</span><span><i class="dot" style="background:#F97316"></i>Latent Diffusion</span><span><i class="dot" style="background:#8458B3"></i>Stable Diffusion · descriptive sensitivity</span></div></div>
      <aside class="hero-aside"><div class="eyebrow">The central discovery</div><div class="verdict">Strong separation.<br>Unresolved attribution.</div><p class="text-md">JPEG encoding identifies origin, while subject matches remain unverified. The 542 exploratory shifts are not confirmed diffusion-origin effects.</p></aside></section>''',unsafe_allow_html=True)
    metrics=table('baseline_metrics.csv').set_index('model');audit=json.loads((OUT/'audit_summary.json').read_text())
    values=[(f'{audit["files"]:,}','Audited Artworks'),('30,000','Native-256 Cohort'),(f'{metrics.loc["handcrafted","roc_auc"]:.4f}','Handcrafted AUROC'),(f'{metrics.loc["metadata_gated","roc_auc"]:.4f}','Metadata Confound Discovery')]
    for i,(col,(value,label)) in enumerate(zip(st.columns(4),values)):
        col.markdown(f'<div class="metric-card {"accent" if i==3 else ""}" style="animation-delay:{i*.08}s"><div class="number">{value}</div><div class="metric-label">{label}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-head"><h3>From pixels to evidence</h3><span class="eyebrow">01 → 02 → 03</span></div>',unsafe_allow_html=True)
    steps=[('Mathematical Feature Space','Ordinal entropy, complexity, radial spectra and color turn pixels into inspectable measurements.','Explore the atlas →',1),
           ('Control-Variable Gate','Native dimensions match. Subject and JPEG controls block independent origin attribution.','Inspect the evidence →',4),
           ('Interactive Visual Audit','Follow an artwork from its projection to actual quadrants, spectra and forensic context.','Open the gallery →',5)]
    for i,(col,(head,body,button,target)) in enumerate(zip(st.columns(3),steps),1):
        with col:
            st.markdown(f'<div class="method-card"><div class="step-no">STEP 0{i}</div><h3>{head}</h3><p>{body}</p></div>',unsafe_allow_html=True)
            st.button(button,key=f'method_{i}',on_click=navigate,args=(target,),width='stretch')
    st.subheader('Quick Artwork Inspector')
    cases=table('error_gallery_cases.csv');indexed=cases.set_index('artwork_id')
    aid=st.selectbox('Choose a held-out artwork',cases.artwork_id.tolist(),format_func=lambda i:indexed.loc[i,'origin']+' · '+indexed.loc[i,'style'].replace('_',' ')+' · '+indexed.loc[i,'selection_reason'],key='quick_artwork')
    detail(aid,features,cohort,'quick')
    with st.expander('Executive evidence · baseline probes & research sources'):
        baselines(table,show_table)
        comparison=table('literature_comparison.csv');show_table(comparison)
        st.download_button('Download literature comparison',comparison.to_csv(index=False),'literature_comparison.csv','text/csv')

def projections(space,styles,origins,features,cohort,table,hex_figure,detail):
    source=table({'H–C':'hc_plot_points.csv','PCA':'pca_plot_points.csv','t-SNE':'tsne_plot_points.csv'}[space])
    x,y={'H–C':('H_pooled','C_pooled'),'PCA':('PC1','PC2'),'t-SNE':('TSNE1','TSNE2')}[space]
    filtered=source[source['style'].isin(styles)&source.origin.isin(origins)]
    extent=(float(source[x].min()),float(source[x].max()),float(source[y].min()),float(source[y].max()))
    if space=='t-SNE':
        fid=table('projection_fidelity.csv');r=fid[(fid.perplexity==30)&(fid.seed==42)].iloc[0]
        st.info(f'Trustworthiness {r.trustworthiness:.4f} · Continuity {r.continuity:.4f} · k=15 · Perplexity 30 · Seed 42. Random initialization; distances and clusters are exploratory.')
    elif space=='PCA':
        r=table('pca_projection_fidelity.csv').iloc[0]
        st.info(f'Development-fitted PCA · Trustworthiness {r.trustworthiness:.4f} · Continuity {r.continuity:.4f} · Fixed audit subset, k=15.')
    else:st.info('24 ordinal states · Four disjoint 128² quadrants · Stable ties. H–C is a measurement plane; it does not establish causality.')
    st.caption(f'{len(filtered):,} shown artworks · '+('fixed 3,000-artwork exploratory subset' if space=='t-SNE' else 'fixed 6,000-artwork primary test set')+' · royal blue Human / orange Latent Diffusion')
    mode=st.radio('Point abstraction',['Raw artworks','Hexagonal density'],horizontal=True,key='abstraction')
    if filtered.empty:st.info('Select at least one movement and origin to display artworks.');return
    selected=None
    if mode=='Raw artworks':
        fig=px.scatter(filtered,x=x,y=y,color='origin',symbol='origin',symbol_map={'Human':'circle','LD':'square'},labels={'H_pooled':'H','C_pooled':'C','origin':'Origin'},color_discrete_map=COLORS,custom_data=['artwork_id','style'],hover_data=['artwork_id','style'],opacity=.65)
        fig.update_traces(marker_size=6);fig.update_xaxes(range=extent[:2]);fig.update_yaxes(range=extent[2:])
        fig.update_layout(height=520,legend=dict(orientation='h',y=-.20,font_size=14))
        event=chart(fig,on_select='rerun',selection_mode='points',key='projection_selection_'+space)
        if event.selection.points:selected=event.selection.points[0]['customdata'][0]
    else:
        chart(hex_figure(filtered,x,y,extent),key='hex_'+space)
        st.caption('Color counts artworks under the active filters. Axes and hexagon boundaries stay fixed; the count colorbar rescales to the displayed subset. Filter one origin to inspect its density.')
    ids=filtered.artwork_id.tolist()
    if selected in ids and selected!=st.session_state.get('last_clicked_artwork'):
        st.session_state['inspect_artwork']=selected;st.session_state['last_clicked_artwork']=selected
    if st.session_state.get('inspect_artwork') not in ids:st.session_state['inspect_artwork']=next((i for i in features.artwork_id if i in set(ids)),ids[0])
    aid=st.selectbox('Inspect artwork (or select a raw point)',ids,key='inspect_artwork');detail(aid,features,cohort,'explorer')

def baselines(table,show_table):
    models=['handcrafted','frequency','metadata_gated','resnet50','dinov2']
    metrics=table('baseline_metrics.csv');show_table(metrics[metrics.model.isin(models)][['model','roc_auc','f1','accuracy','ece','n']])
    roc=go.Figure()
    for i,name in enumerate(models):
        r=table(f'roc_{name}.csv');roc.add_trace(go.Scatter(x=r.fpr,y=r.tpr,name=name,line_color=['#334155','#A21CAF','#78716C','#854D0E','#4D7C0F'][i]))
    roc.update_layout(title='Held-out ROC · five frozen probes',xaxis_title='False positive rate',yaxis_title='True positive rate',height=380);chart(roc,key='baseline_roc')
    st.caption('Identical 6,000 test IDs. Frozen encoders; development/validation tuning. Metadata exposes residual JPEG leakage.');show_table(table('baseline_per_style_ci.csv'))

def spectral(table):
    title('04 / frequency & scale','Spectral & Wavelet Profiles','Compare cached spectra and wavelet energies. Human and LD are native 256; SD is a separate resized, descriptive sensitivity.')
    selected=st.multiselect('Profile origins',['Human','LD','SD'],default=['Human','LD','SD'],key='profile_origins');data=table('spectral_wavelet_profiles.csv')
    for family in ['FFT','Haar']:
        names=[f'fft_{i:02d}_median' for i in range(16)] if family=='FFT' else [f'dwt_{n}_median' for n in ['LH1','HL1','HH1','LH2','HL2','HH2']]
        x=(np.arange(16)+.5)/32 if family=='FFT' else ['LH1','HL1','HH1','LH2','HL2','HH2'];fig=go.Figure()
        for origin in selected:
            rows=data[data.origin.eq(origin)].set_index('feature').loc[names]
            fig.add_trace(go.Scatter(x=x,y=rows['mean'],mode='lines+markers',name=origin,line_color=COLORS[origin],error_y=dict(type='data',array=rows.ci_high-rows['mean'],arrayminus=rows['mean']-rows.ci_low,symmetric=False,thickness=1)))
        fig.update_layout(title='Hann-windowed 16-annulus FFT' if family=='FFT' else 'Two-level Haar detail energies',height=370,yaxis_type='log',xaxis_title='Radial frequency (cycles/pixel)' if family=='FFT' else 'Detail band',yaxis_title='Normalized power share' if family=='FFT' else 'Raw-luminance energy ratio')
        if selected:chart(fig,key='profile_'+family)
    if not selected:st.info('Select an origin to compare its profile.')
    st.caption('1,000 source-group bootstrap intervals. Haar normalization retains LL2. These profiles do not restore subject matching or JPEG common support.')

def drift(styles,table,show_table):
    title('05 / shifts & sensitivity','Style Drift & Ablations','A measurable difference begins an investigation. The control gate determines which conclusions are supported.')
    family=table('style_family_drift.csv');family=family[family['style'].isin(styles)]
    if len(family):
        fig=px.density_heatmap(family,x='family',y='style',z='w1',histfunc='avg',color_continuous_scale='Greys');fig.update_layout(title='Style-conditional feature drift · mean standardized W₁',height=460);chart(fig,key='style_heatmap')
    else:st.info('Select a movement to display its drift summaries.')
    st.caption('542 exploratory passes · Zero confirmatory-eligible comparisons. Subject/encoding exchangeability is unsupported; multiplicity correction cannot fix those controls.')
    data=table('style_feature_drift.csv');feature=st.selectbox('Inspect measured feature',sorted(data.feature.unique()),key='drift_feature')
    show_table(data[data.feature.eq(feature)&data['style'].isin(styles)][['style','w1','median_shift','shift_ci_low','shift_ci_high','p_adj','null_p95','raw_rule_pass','confirmed_drift']])
    st.subheader('Ablation & perturbation evidence');show_table(table('ablation_results.csv')[['label','roc_auc','delta_auc','delta_auc_low','delta_auc_high','delta_silhouette']]);show_table(table('perturbation_results.csv')[['view','roc_auc','f1','silhouette_retention','style_w1_rank_rho']])
    st.caption('Paired intervals resample source groups. Silhouette uncertainty conditions on fixed per-artwork geometry. No test-set refitting.')
    with st.expander('Publication figures & source tables'):
        manifest=table('figure_manifest.csv');chosen=st.selectbox('Publication figure',manifest.file.tolist(),key='publication_figure');path=ROOT/'figures'/chosen
        if not path.exists():path=OUT/chosen
        st.image(str(path));st.caption(manifest.set_index('file').loc[chosen,'caption'])

def render_app(table,show_table,hex_figure,detail):
    st.markdown(CSS,unsafe_allow_html=True)
    st.markdown('<div class="brand"><div class="brand-name"><i class="brand-mark"></i> AI-ARTBENCH</div><div class="brand-note">ARTWORK · MEASUREMENT · EVIDENCE</div></div>',unsafe_allow_html=True)
    view=st.radio('Explore the research',VIEWS,format_func=lambda v:SHORT[VIEWS.index(v)],horizontal=True,key='view',label_visibility='collapsed')
    compact=not (OUT/'features_matched.parquet').exists()
    try:
        cohort=table('error_gallery_cases.csv') if compact else table('cohort_manifest.parquet');features=table('error_gallery_cases.csv') if compact else table('features_matched.parquet')
    except (ImportError,OSError):compact=True;cohort=features=table('error_gallery_cases.csv')
    hc=table('hc_plot_points.csv');st.sidebar.header('Refine the view')
    styles=st.sidebar.multiselect('Art movement',sorted(hc['style'].unique()),default=sorted(hc['style'].unique()),key='styles');origins=st.sidebar.multiselect('Origin',['Human','LD'],default=['Human','LD'],key='origins')
    st.sidebar.caption('Movement filters apply to atlas, manifold and drift. Origin filters apply to atlas and manifold. Profiles and curated gallery cases have their own controls.')
    if view!=VIEWS[0]:st.warning('Descriptive evidence only. JPEG quantization identifies origin and subjects cannot be matched reliably. No confirmed diffusion-origin drift.')
    if view==VIEWS[0]:landing(table,show_table,detail,features,cohort)
    elif view==VIEWS[1]:
        title('02 / mathematical feature space','H–C Feature Atlas','Entropy and complexity across ten art movements. All comparisons remain descriptive.');projections('H–C',styles,origins,features,cohort,table,hex_figure,detail)
    elif view==VIEWS[2]:
        title('03 / geometry & neighborhoods','Manifold & Fidelity','Follow neighborhoods through fixed PCA and exploratory t-SNE. Visual separation alone is not evidence of origin effects.')
        space=st.radio('Projection',['PCA','t-SNE'],horizontal=True,key='manifold_space');projections(space,styles,origins,features,cohort,table,hex_figure,detail)
        with st.expander('All audited projection runs'):show_table(table('projection_fidelity.csv'));show_table(table('pca_projection_fidelity.csv'))
    elif view==VIEWS[3]:spectral(table)
    elif view==VIEWS[4]:drift(styles,table,show_table)
    else:
        title('06 / inspect the exceptions','Forensic Error Gallery','Eight held-out cases: two FP, two FN, two TP and two projection outliers. This is purposive inspection, not a prevalence estimate.')
        cases=table('error_gallery_cases.csv');indexed=cases.set_index('artwork_id');aid=st.selectbox('Gallery case',cases.artwork_id.tolist(),format_func=lambda i:indexed.loc[i,'selection_reason']+' · '+str(i)[:12],key='gallery_case');detail(aid,features,cohort,'gallery')
        with st.expander('Failure triggers & boundary sensitivity'):show_table(table('failure_trigger_rates.csv'))
        st.caption('Triggers use development quantiles or a fixed border heuristic. Associations are descriptive; all-quadrant exclusions remain unsupported.')
    if compact:st.caption('Compact edition · All cached projection points are available. Pixel and feature inspection covers the eight supplied gallery cases. The complete workspace supports every artwork.')
    st.caption('Cached evidence · Filters do not train models or change the frozen cohort.')
    st.markdown('<footer class="glass footer">Wasil Kayani · Umer Asghar</footer>',unsafe_allow_html=True)
