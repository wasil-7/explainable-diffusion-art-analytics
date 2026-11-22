"""Cached AI-ArtBench visual analysis. Launch with python -m streamlit run src/dashboard.py."""
from common import *
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from features import load_rgb, quadrants

st.set_page_config(page_title='AI-ArtBench · Visual Evidence',layout='wide',initial_sidebar_state='collapsed')
from dashboard_theme import COLORS,style_figure


@st.cache_data
def table(name):
    path=OUT/name
    return pd.read_parquet(path) if path.suffix=='.parquet' else pd.read_csv(path)

def show_table(df):
    # HTML keeps this read-only dashboard independent of the host-blocked Arrow DLL.
    st.markdown('<div class="table-scroll">'+df.to_html(index=False,escape=True,float_format=lambda x:f'{x:.5g}')+'</div>',unsafe_allow_html=True)

def hex_figure(df,x,y,extent):
    """Hexagonal bin aggregation using Matplotlib's stable binning; Plotly rendering."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    f,ax=plt.subplots();h=ax.hexbin(df[x],df[y],gridsize=35,mincnt=1,extent=extent);xy=h.get_offsets();counts=h.get_array();plt.close(f)
    fig=go.Figure(go.Scatter(x=xy[:,0],y=xy[:,1],mode='markers',marker=dict(symbol='hexagon',size=14,color=counts,colorscale=['#EFF6FF','#8458B3','#1E40AF'],showscale=True,colorbar=dict(title='Artworks')),customdata=counts,hovertemplate='x=%{x:.4g}<br>y=%{y:.4g}<br>artworks=%{customdata}<extra></extra>'))
    fig.update_layout(xaxis_title=x,yaxis_title=y,height=520);fig.update_xaxes(range=extent[:2]);fig.update_yaxes(range=extent[2:]);return fig

def app():
    from dashboard_views import render_app
    render_app(table,show_table,hex_figure,artwork_detail)


def artwork_detail(aid,features,cohort,context):
    if aid not in set(features.artwork_id):
        st.info('This artwork has cached projection coordinates. Its pixels are excluded from the lightweight submission; select a Forensic cases entry for the included pixel and feature drill-down.')
        return
    r=features.set_index('artwork_id').loc[aid];meta=cohort.set_index('artwork_id').loc[aid]
    source=DATA/meta.path
    if not source.exists():source=OUT/'gallery'/f'{aid}.png'
    rgb=load_rgb(source)
    a,b=st.columns([1,2]);a.image(rgb,caption=f'{meta.origin} · {meta["style"].replace("_"," ")} · {aid}',width=256)
    with b:
        cols=st.columns(4)
        for col,img,label in zip(cols,quadrants(rgb),['Top left','Top right','Bottom left','Bottom right']):col.image(img,caption=label,width=128)
        st.write(f'Entropy H={r.H_pooled:.5f} · complexity C={r.C_pooled:.5f} · saturation={r.s_median_median:.3f} · edge fraction={r.edge_density_median:.3f}')
    left,right=st.columns(2)
    spec=go.Figure(go.Scatter(x=(np.arange(16)+.5)/32,y=[r[f'fft_{i:02d}_median'] for i in range(16)],mode='lines+markers',line_color=COLORS[meta.origin]));spec.update_layout(title=f'Radial FFT; β={r.fft_beta_median:.2f}',yaxis_type='log',xaxis_title='cycles/pixel',yaxis_title='Normalized power share',height=280);left.plotly_chart(style_figure(spec),width='stretch',theme=None,key=context+'_fft')
    names=['LH1','HL1','HH1','LH2','HL2','HH2'];wave=go.Figure(go.Scatter(mode='markers',x=names,y=[r[f'dwt_{n}_median'] for n in names],marker_color=COLORS[meta.origin]));wave.update_layout(title='Haar detail energy ratios (log scale)',yaxis_type='log',height=280);right.plotly_chart(style_figure(wave),width='stretch',theme=None,key=context+'_haar')

if __name__=='__main__':app()
