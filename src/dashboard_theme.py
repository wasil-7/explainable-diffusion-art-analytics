"""White, royal blue and vibrant orange presentation shared by all dashboard views."""
COLORS={'Human':'#2563EB','LD':'#F97316','SD':'#8458B3'}
PALETTE=['#1E40AF','#F97316','#8458B3','#EA580C','#494D5F','#FDBA74']
CSS="""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Titan+One&display=swap');
:root { --forest:#1E40AF; --sage:#8458B3; --ink:#494D5F; --cream:#FFFFFF;
 --blush:#EFF6FF; --border:#E5EAF5; --orange:#F97316; --rust:#EA580C;
 --peach:#FDBA74; --grey:#E5EAF5; --midgrey:#E5EAF5; --muted:#494D5F; }
.stApp { background:radial-gradient(ellipse at 95% 0%,#E5EAF5 0,#F8FAFC 24%,transparent 48%),#FFFFFF; color:var(--ink); }
html,body,[data-testid="stApp"],button,input,textarea,select,p,label,li,
[data-baseweb="select"], [data-testid="stMarkdownContainer"] { font-family:'Quicksand',sans-serif; font-size:14px; }
.stMainBlockContainer { max-width:1500px; padding:2.2rem 3rem 2rem; }
[data-testid="stHeader"] { background:rgba(255,255,255,.92); }
[data-testid="stSidebar"] { background:var(--blush); border-right:1px solid var(--border); }
h1,h2,.display-lg,.display-md { font-family:'Cubano','Titan One','Arial Black',sans-serif!important;
 color:var(--forest)!important; text-transform:uppercase; font-weight:700!important; letter-spacing:.01em; }
h1,.display-lg { font-size:36px!important; line-height:1.17!important; }
h2,.display-md { font-size:30px!important; line-height:1.25!important; }
h3 { font-family:'Quicksand',sans-serif!important; font-weight:700; color:var(--forest); font-size:18px!important; }
.text-xl { font-size:18px; line-height:1.65; } .text-md { font-size:14px; line-height:1.7; }
.eyebrow { font-size:11px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:var(--sage); }
.brand { display:flex; align-items:center; justify-content:space-between; gap:16px; margin:8px 0 12px; }
.brand-name { font-weight:700; font-size:16px; letter-spacing:.07em; color:var(--forest); }
.brand-mark { display:inline-block; width:12px; height:12px; background:var(--orange); border-radius:50%; margin-right:9px; box-shadow:7px -5px 0 var(--forest); }
.brand-note { font-size:11px; letter-spacing:.12em; color:var(--sage); }
.glass,.metric-card,[data-testid="stPlotlyChart"],.method-card {
 background:rgba(255,255,255,.92); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
 border:1px solid #E5EAF5; border-radius:20px; box-shadow:0 10px 28px rgba(73,77,95,.07);
 transition:all .3s cubic-bezier(.22,1,.36,1); animation:fadeInUp .65s both; }
.metric-card:hover,[data-testid="stPlotlyChart"]:hover,.method-card:hover {
 transform:translateY(-4px); box-shadow:0 16px 36px rgba(37,99,235,.12); border-color:#8458B3; }
.hero { padding:32px 36px; display:grid; grid-template-columns:1.9fr 1fr; gap:32px; overflow:hidden; }
.hero h1 { margin:12px 0 16px; max-width:800px; }
.hero p { max-width:720px; margin:0; }
.hero-aside { padding:22px; border-left:1px solid var(--border); display:flex; flex-direction:column; justify-content:center; }
.hero-aside .verdict { font-size:18px; font-weight:700; color:var(--rust); margin:12px 0; }
.origin-key { display:flex; gap:16px; flex-wrap:wrap; margin-top:18px; font-size:12px; font-weight:700; }
.dot { display:inline-block; border-radius:50%; width:8px; height:8px; margin-right:5px; }
.metric-card { padding:19px 20px; min-height:122px; margin:8px 0; }
.metric-card .number { font-family:'Quicksand',sans-serif; font-weight:700; font-size:30px; color:var(--forest); line-height:1.3; }
.metric-card .metric-label { font-size:14px; font-weight:600; margin-top:8px; }
.metric-card.accent .number { color:var(--rust); }
.metric-card:nth-child(2) { animation-delay:.08s; }
.section-head { display:flex; justify-content:space-between; align-items:baseline; margin:18px 0 4px; }
.method-card { padding:19px 22px; min-height:168px; }
.step-no { color:var(--rust); font-size:12px; font-weight:700; letter-spacing:.13em; margin-bottom:8px; }
.method-card h3 { margin:4px 0 9px; }
.method-card p { margin:0; line-height:1.6; }
[data-testid="stButton"] button { border:1px solid var(--border); border-radius:50px; background:rgba(255,255,255,.92); color:var(--forest); font-weight:700; transition:all .3s cubic-bezier(.22,1,.36,1); }
[data-testid="stButton"] button:hover { background:var(--forest); color:var(--cream); border-color:var(--forest); transform:translateY(-2px); }
.st-key-view [role="radiogroup"] { display:flex; flex-wrap:wrap; gap:8px; padding:5px 0 16px; }
.st-key-view [role="radiogroup"] label { border:1px solid var(--border); border-radius:50px; padding:9px 15px; margin:0!important; background:rgba(255,255,255,.92); transition:all .3s cubic-bezier(.22,1,.36,1); }
.st-key-view [role="radiogroup"] label:has(input:checked) { background:var(--forest); color:var(--cream); border-color:var(--forest); }
.st-key-view [role="radiogroup"] label:has(input:checked) p { color:var(--cream); }
.st-key-view [role="radiogroup"] label > div:first-child { display:none; }
.st-key-view [role="radiogroup"] label:hover { border-color:var(--sage); transform:translateY(-2px); }
[data-testid="stAlert"] { border-radius:14px; border:1px solid var(--border); background:#EFF6FF; color:var(--ink); }
[data-testid="stAlert"] > div { background:#EFF6FF!important; color:var(--ink)!important; }
[data-testid="stAlert"] p { color:var(--ink)!important; }
[data-baseweb="tag"] { background:var(--forest)!important; color:var(--cream)!important; }
[data-testid="stPlotlyChart"] { padding:10px; overflow:hidden; }
.table-scroll { overflow-x:auto; border:1px solid var(--border); border-radius:16px; margin:12px 0; background:rgba(255,255,255,.92); }
.table-scroll table { width:100%; border-collapse:collapse; font-size:12px; }
.table-scroll th { background:var(--blush); color:var(--forest); text-align:left; }
.table-scroll td,.table-scroll th { padding:9px 12px; border-bottom:1px solid var(--grey); }
.table-scroll tr:last-child td { border-bottom:none; }
.footer { text-align:center; padding:20px; margin-top:32px; font-weight:600; color:var(--forest); font-size:14px; }
@keyframes fadeInUp { from {opacity:0;transform:translateY(14px);} to {opacity:1;transform:translateY(0);} }
@media(prefers-reduced-motion:reduce) { *,*::before,*::after {animation:none!important;transition:none!important;scroll-behavior:auto!important;} }
@media(max-width:800px) { .stMainBlockContainer {padding:4rem 1rem 1.5rem;} .hero {grid-template-columns:1fr;padding:24px;gap:10px;} .hero-aside {border-left:0;border-top:1px solid var(--border);padding:16px 0 0;} .brand-note {display:none;} h1,.display-lg {font-size:30px!important;} .st-key-view [role="radiogroup"] label {padding:8px 10px;} }
</style>
"""

def style_figure(fig):
    legend_items=sum(t.showlegend is not False and bool(t.name) for t in fig.data)
    legend_bottom=155 if legend_items>6 else (95 if legend_items>1 else 85)
    fig.update_layout(font=dict(family='Quicksand, sans-serif',size=14,color='#494D5F'),
        title_font=dict(family='Quicksand, sans-serif',size=18,color='#1E40AF'),
        colorway=PALETTE,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='#F8FAFC',
        hoverlabel=dict(bgcolor='#FFFFFF',bordercolor='#E5EAF5',font=dict(family='Quicksand, sans-serif',size=14,color='#1E40AF')),
        margin=dict(l=65,r=25,t=65,b=legend_bottom),legend=dict(orientation='h',y=-.20,x=0,bgcolor='rgba(0,0,0,0)'))
    for i,trace in enumerate(fig.data):
        if trace.type=='scatter':
            if trace.name and ',' in trace.name and trace.name.startswith('LD'):
                symbol=trace.marker.symbol or 'circle'
                trace.marker.symbol=(symbol+'-open') if isinstance(symbol,str) and not symbol.endswith('-open') else symbol
            elif trace.mode and 'lines' in trace.mode:
                trace.line.dash=['solid','dash','dot','dashdot'][i%4]
                trace.marker.symbol=['circle','square','triangle-up','diamond'][i%4]
        if hasattr(trace,'yaxis') and fig.layout.yaxis.type=='log' and fig.layout.yaxis.title.text and 'log scale' not in fig.layout.yaxis.title.text:
            fig.layout.yaxis.title.text+=' (log scale)'
    fig.update_xaxes(automargin=True,title_standoff=5,gridcolor='#E5EAF5',linecolor='#E5EAF5',zerolinecolor='#494D5F')
    if fig.layout.yaxis.title.text:
        fig.layout.yaxis.title.text=fig.layout.yaxis.title.text.replace('Normalized power share','Power share').replace('Raw-luminance energy ratio','Energy ratio')
    fig.update_yaxes(gridcolor='#E5EAF5',linecolor='#E5EAF5',zerolinecolor='#494D5F',nticks=5)
    return fig
