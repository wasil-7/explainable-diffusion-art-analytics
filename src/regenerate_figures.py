"""Final DAV figures from released CSVs only. No fitting or inferential rerun."""
from pathlib import Path
import sys,json,hashlib,textwrap,warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse,FancyBboxPatch,Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator,LogLocator,NullFormatter
from scipy.stats import gaussian_kde
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import pd
warnings.filterwarnings('ignore',message="The 'float_precision' argument is deprecated.*")
B=Path(__file__).resolve().parents[1];OUT=B/'results';FIG=B/'figures';TEX=(B/'latex/figures' if (B/'latex').exists() else B/'paper/latex_source/figures')
for p in [FIG,TEX,B/'qa']:p.mkdir(exist_ok=True,parents=True)
ORIGIN={'Human':'#2563EB','LD':'#F97316','SD':'#8458B3'}
MODELS=['handcrafted','frequency','metadata_gated','resnet50','dinov2']
NAMES=['Handcrafted (104-D)','FFT-only (36-D)','Metadata-only','ResNet-50 (frozen)','DINOv2 (frozen)']
MC=['#334155','#A21CAF','#78716C','#854D0E','#4D7C0F'];MARK=['o','s','^','D','X'];DASH=['-','--','-.',':',(0,(5,2,1,2))]
READ={};AUDIT=[];CAPTIONS={}
SHORT_CAPTIONS={
1:'Implemented branch structure. Frozen splits and development calibration precede held-out evaluation; descriptive outputs remain available when the common-support gate blocks independent attribution.',
2:'All 185,015 files are audited; annotations show native dimensions. Full-release/native-256 metadata ROC curves coincide and are drawn once. Size matching leaves perfect technical label ranking, without proving use of that association by pixel probes.',
3:'Five probes share 6,000 test IDs; whiskers are frozen-fit group-bootstrap 95% intervals. Insets zoom ROC to FPR 0–0.02/TPR 0.98–1 and PR to [0.98,1]². Numbered style keys follow B1. Low ARI coexists with strong supervised ranking.',
4:'Shared-axis H–C atlas with LD-minus-Human arrows, Gaussian 95% centroid ellipses (500 group resamples) and within-cell KDE contours (15/40/70% of peak). Full movement names reveal heterogeneous descriptive displacements, without establishing attribution.',
5:'Equal-aspect PCA retains all points (A1); A2 zooms PC1 to [−5,10] and PC2 to [−6,6]. Transparent t-SNE uses perplexity 30, seed 42. Fidelity axis 0.905–0.921 magnifies small differences; whiskers are seed ranges, not confidence intervals.',
6:'FFT/Haar means with 1,000-group-bootstrap 95% intervals. Small open Haar markers expose whiskers; LL2 remains in normalization. SD resizing is descriptive. Broadly similar spectra do not eliminate style-specific differences.',
7:'Family-average W₁ and signed median shifts. All families contain exploratory constituents; redundant asterisks are omitted. The W₁ scale ends at 1.05 (including 1.013); signed colors are zero-centered. These shifts remain unconfirmed.',
10:'Paired family losses and color/crop sensitivities; ordinal removal causes the largest conditional AUROC decrease. B retains all intervals on an explicitly zoomed axis; C bars start at zero. Group intervals retain fits; silhouette intervals additionally retain geometry.',
11:'Separate panels and condition groups avoid dual-axis ambiguity. A shows paired AUROC changes and group-bootstrap 95% intervals from Table XII; original is the zero reference. Silhouette/rank points are descriptive. JPEG 50 reduces ranking despite increased silhouette.',
12:'Eight purposive cases, not prevalence estimates; FP/FN/TP refer to release labels. FFT rows share 10⁻⁴–1 and Haar rows 10⁻⁵–10⁻¹, both logarithmic. S = saturation, V = value, E = edge density, R = hue concentration (N/A when undefined).'
}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7,'axes.titlesize':7.5,'axes.labelsize':7,'xtick.labelsize':6.5,'ytick.labelsize':6.5,'legend.fontsize':6.5,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.65,'savefig.facecolor':'white'})
def read(name):
 p=OUT/name;READ[name]=hashlib.sha256(p.read_bytes()).hexdigest();return pd.read_csv(p,float_precision='round_trip')
def title(s):return s.replace('_',' ').replace('ukiyo-e','Ukiyo-e').title().replace('Ukiyo-E','Ukiyo-e')
def legend(fig,handles,labels,ncol=3,anchor=(.5,.005)):
 return fig.legend(handles,labels,loc='lower center',bbox_to_anchor=anchor,ncol=ncol,frameon=False,columnspacing=1,handlelength=1.8,handletextpad=.4)
def origins():return [Line2D([],[],color=ORIGIN[o],marker=m,ls=ls,ms=3) for o,m,ls in [('Human','o','-'),('LD','s','--'),('SD','^',':')]]
def finish(fig,n,name,caption,extra=None):
 fig.canvas.draw();ren=fig.canvas.get_renderer();overlap=[]
 for leg in fig.legends:
  overlap += [i for i,a in enumerate(fig.axes) if leg.get_window_extent(ren).overlaps(a.get_window_extent(ren))]
 assert not overlap,(name,overlap)
 fig.savefig(FIG/name,dpi=450,bbox_inches='tight',pad_inches=.035);fig.savefig(TEX/f'figure_{n:02}.png',dpi=450,bbox_inches='tight',pad_inches=.035)
 CAPTIONS[str(n)]=SHORT_CAPTIONS.get(n,caption);AUDIT.append(dict(figure=n,file=name,legend_axes_overlaps=overlap,source_csvs=dict(READ),details=extra or {},full_explanation=caption));plt.close(fig);print('Rendered',n,name,flush=True)
def architecture():
 fig,ax=plt.subplots(figsize=(3.45,1.6));ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
 def box(x,y,w,h,txt,edge='#475569',fill='#FFFFFF'):
  ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=.012',facecolor=fill,edgecolor=edge,lw=.8));ax.text(x,y,txt,ha='center',va='center',fontsize=6.8)
 def arrow(a,b,ls='-'):ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',color='#334155',lw=.8,linestyle=ls))
 box(.5,.91,.77,.13,'Audit images, sources and duplicates');box(.5,.68,.77,.13,'Freeze grouped IDs; calibrate on development');box(.5,.45,.77,.13,'Cache measurements and frozen representations');arrow((.5,.84),(.5,.76));arrow((.5,.61),(.5,.53))
 box(.23,.15,.40,.21,'Descriptive outputs:\nheld-out probes and atlas');box(.77,.18,.40,.25,'Common-support gate\nSubjects / JPEG fail\nNo eligible attribution',edge='#991B1B',fill='#FEF2F2');arrow((.38,.37),(.23,.27));arrow((.62,.37),(.77,.32))
 fig.subplots_adjust(0,0,1,1)
 finish(fig,1,'fig00_implemented_architecture.png','Implemented branch structure. Frozen source-group splits and development calibration precede held-out evaluation. Descriptive outputs remain available when the common-support gate blocks independent attribution.')
def dataset():
 fig,ax=plt.subplots(1,2,figsize=(7.16,1.65),gridspec_kw={'width_ratios':[1,1.2]});d=read('audit_counts.csv');tot=d.groupby('origin')['count'].sum()
 for i,o in enumerate(['Human','LD','SD']):
  ax[0].bar(i,tot[o],width=.6,color=ORIGIN[o],edgecolor='#334155',linewidth=.4,hatch=['','///','..'][i]);ax[0].text(i,tot[o]+2000,f'{tot[o]:,}\n'+('256²' if o!='SD' else '768²'),ha='center',fontsize=6.5)
 ax[0].set(xticks=range(3),xticklabels=['Human','LD','SD'],ylim=(0,80000),ylabel='Audited artworks',title='A  Counts and native dimensions');ax[0].yaxis.set_major_locator(MaxNLocator(4))
 d=read('roc_metadata_gated.csv');ax[1].plot(d.fpr,d.tpr,color='#334155',lw=1,marker='o',ms=2,label='Full / native-256 metadata: 1.0000')
 q=read('roc_metadata_ungated_full.csv');assert all(((v.fpr==0)|(v.tpr==1)).all() for v in [d,q])
 d=read('roc_dimensions_ungated_full.csv');ax[1].plot(d.fpr,d.tpr,color='#78716C',ls='--',lw=1,marker='s',ms=2,label='Full dimensions only: 0.7516');ax[1].plot([0,1],[0,1],':',color='#A8A29E',lw=.6)
 ax[1].set(xlabel='False positive rate',ylabel='True positive rate',title='B  Metadata ranking remains perfect',xlim=(-.02,1.02),ylim=(-.02,1.05));h,l=ax[1].get_legend_handles_labels();fig.tight_layout(rect=[0,.26,1,1],pad=.35,w_pad=1.2);legend(fig,h,l,2)
 finish(fig,2,'fig01_dataset_audit_and_confound.png','All 185,015 files are audited. Counts are summed over ten movements; annotations give native dimensions. The full-release and native-256 metadata ROC curves coincide and are shown once, despite different test populations. Matching native size therefore leaves a technical source association; it does not identify use of that association by pixel probes.')
def baselines():
 fig=plt.figure(figsize=(7.16,2.8));gs=fig.add_gridspec(2,6,height_ratios=[.85,1.6]);roc=fig.add_subplot(gs[0,:2]);pr=fig.add_subplot(gs[0,2:4]);ari=fig.add_subplot(gs[0,4:]);auc=fig.add_subplot(gs[1,:3]);f1=fig.add_subplot(gs[1,3:]);ci=read('baseline_per_style_ci.csv');styles=sorted(ci['style'].unique())
 ir=roc.inset_axes([.48,.12,.47,.40]);ip=pr.inset_axes([.48,.06,.47,.40])
 for j,m in enumerate(MODELS):
  r=read('roc_'+m+'.csv');p=read('pr_'+m+'.csv')
  for a,x,y in [(roc,r.fpr,r.tpr),(ir,r.fpr,r.tpr),(pr,p.recall,p.precision),(ip,p.recall,p.precision)]:a.plot(x,y,color=MC[j],ls=DASH[j],lw=.8)
  g=ci[ci.model.eq(m)].set_index('style').loc[styles];yy=np.arange(10)+(j-2)*.18
  for a,key,lo,hi in [(auc,'roc_auc','auc_low','auc_high'),(f1,'f1','f1_low','f1_high')]:
   a.errorbar(g[key],yy,xerr=np.vstack([np.maximum(0,g[key]-g[lo]),np.maximum(0,g[hi]-g[key])]),fmt=MARK[j],color=MC[j],ms=1.6,markerfacecolor='white',capsize=.8,elinewidth=.65,lw=.6)
 roc.set(xlabel='False positive rate',ylabel='TPR',title='A1  ROC',xlim=(0,1),ylim=(0,1.03));pr.set(xlabel='Recall',ylabel='Precision',title='A2  Precision–recall',xlim=(0,1),ylim=(0,1.03))
 ir.set(xlim=(0,.02),ylim=(.98,1.001),xticks=[],yticks=[]);ip.set(xlim=(.98,1),ylim=(.98,1.001),xticks=[],yticks=[]);
 for a in [ir,ip]:a.tick_params(labelsize=4.5,pad=.5,length=1);a.set_facecolor('#F8FAFC');a.text(.98,.05,'zoom',transform=a.transAxes,ha='right',fontsize=4.5)
 d=read('origin_silhouette_ari.csv');d=d[d.space.eq('full')]
 for i,r in enumerate(d.sort_values('silhouette').itertuples()):
  ari.plot(r.silhouette,r.ari,'o',color='#334155',ms=2);ari.annotate(str(styles.index(r.style)+1),(r.silhouette,r.ari),xytext=(.028+(i//2)*.017,.0048 if i%2==0 else .0039),textcoords='data',fontsize=5.5,ha='center',arrowprops=dict(arrowstyle='-',lw=.3,color='#64748B'))
 ari.set(xlabel='Origin silhouette',ylabel='k=2 ARI',title='C  Full-space clusters',ylim=(-.0005,.0056));ari.xaxis.set_major_locator(MaxNLocator(3));ari.yaxis.set_major_locator(MaxNLocator(3))
 for a,head,key in [(auc,'B1  Per-style AUROC','AUROC'),(f1,'B2  Per-style F1','F1')]:a.set(yticks=range(10),yticklabels=[title(s) if a==auc else str(i+1) for i,s in enumerate(styles)],xlabel=key,title=head);a.invert_yaxis();a.set_xlim(.38 if a==f1 else .45,1.015);a.xaxis.set_major_locator(MaxNLocator(4));a.tick_params(axis='y',labelsize=6)
 fig.tight_layout(rect=[0,.15,1,1],pad=.35,h_pad=.9,w_pad=1.3);legend(fig,[Line2D([],[],color=c,marker=m,ls=ls,ms=3) for c,m,ls in zip(MC,MARK,DASH)],NAMES,3)
 finish(fig,3,'fig07_baseline_probes_and_ari.png','Five probes use identical 6,000 test IDs. Insets magnify FPR 0–0.02/TPR 0.98–1 and recall/precision 0.98–1; full curves remain visible. Per-style dots show 1,000-group-bootstrap 95% intervals conditional on frozen fits. Style keys 1–10 follow the full names in B1 (alphabetical order). C labels every style and includes the maximum ARI point; near-zero clustering agreement does not validate attribution.')
def atlas():
 d=read('hc_plot_points.csv');ell=read('hc_centroid_ellipses.csv');fig,axes=plt.subplots(2,5,figsize=(7.16,2.05),sharex=True,sharey=True);xl=(min(.7,d.H_pooled.min()-.01),1.005);yl=(-.005,max(.25,d.C_pooled.max()+.01))
 for ax,style in zip(axes.flat,sorted(d['style'].unique())):
  for o,m,ls in [('Human','o','-'),('LD','s','--')]:
   g=d[d['style'].eq(style)&d.origin.eq(o)];ax.scatter(g.H_pooled,g.C_pooled,s=1.6,c=ORIGIN[o],marker=m,alpha=.18,rasterized=True)
   xx,yy=np.meshgrid(np.linspace(*xl,70),np.linspace(*yl,70));z=gaussian_kde(g[['H_pooled','C_pooled']].to_numpy().T)(np.vstack([xx.ravel(),yy.ravel()])).reshape(xx.shape);ax.contour(xx,yy,z,levels=z.max()*np.array([.15,.4,.7]),colors=[ORIGIN[o]],linestyles=ls,linewidths=.65)
   e=ell[ell['style'].eq(style)&ell.origin.eq(o)].iloc[0];ax.add_patch(Ellipse((e.H,e.C),e.width,e.height,angle=e.angle,facecolor='none',edgecolor=ORIGIN[o],linestyle=ls,lw=.9,zorder=5));ax.plot(e.H,e.C,m,color=ORIGIN[o],ms=2.4)
  es=ell[ell['style'].eq(style)].set_index('origin');h,l=es.loc['Human'],es.loc['LD'];ax.annotate('',xy=(l.H,l.C),xytext=(h.H,h.C),arrowprops=dict(arrowstyle='->',color='#111827',lw=.9,mutation_scale=5),zorder=7);ax.set(title=title(style),xlim=xl,ylim=yl)
  ax.tick_params(labelsize=6,length=2,pad=1)
 for a in axes[-1]:a.set_xlabel('H',labelpad=1)
 for a in axes[:,0]:a.set_ylabel('C',labelpad=1)
 fig.tight_layout(rect=[0,.18,1,1],pad=.3,h_pad=.7,w_pad=.5)
 handles=origins()[:2]+[Line2D([],[],color='#111827',marker='>',ls='-',ms=3),Patch(facecolor='none',edgecolor='#475569'),Line2D([],[],color='#475569',ls='--')];legend(fig,handles,['Human','LD','LD − Human centroid','95% centroid ellipse','Within-cell KDE contours'],3)
 finish(fig,4,'fig02_hc_causality_atlas.png','Ten full movement names share H/C axes. Dark arrows show descriptive LD-minus-Human centroid displacement; outlined ellipses are Gaussian 95% contours of 500 source-group bootstrap centroids. KDE contours denote 15/40/70% of each cell peak. Neither formal coordinates nor displacement establish aesthetic merit or independent origin effects.')
def projections():
 pc=read('pca_plot_points.csv');ts=read('tsne_plot_points.csv');f=read('projection_fidelity.csv');fig=plt.figure(figsize=(7.16,1.9));gs=fig.add_gridspec(1,4,width_ratios=[1,1,1.7,1.55]);a,z,t,c=[fig.add_subplot(gs[0,i]) for i in range(4)]
 for o,m in [('Human','o'),('LD','s')]:
  g=pc[pc.origin.eq(o)]
  for ax in [a,z]:ax.scatter(g.PC1,g.PC2,color=ORIGIN[o],marker=m,s=1.2,alpha=.2,rasterized=True)
  g=ts[ts.origin.eq(o)];t.scatter(g.TSNE1,g.TSNE2,edgecolors=ORIGIN[o],facecolors='none',linewidths=.25,marker=m,s=2.1,alpha=.25,rasterized=True)
 a.set(title='A1  PCA full',xlabel='PC1',ylabel='PC2');a.set_aspect('equal',adjustable='box');z.set(title='A2  PCA zoom',xlabel='PC1',ylabel='PC2',xlim=(-5,10),ylim=(-6,6));z.set_aspect('equal',adjustable='box');t.set(title='B  t-SNE, p=30, seed=42',xlabel='t-SNE 1',ylabel='t-SNE 2')
 for j,key in enumerate(['trustworthiness','continuity']):
  q=f.groupby('perplexity')[key];mu=q.mean();lo=q.min();hi=q.max();c.errorbar(mu.index,mu,yerr=np.vstack([mu-lo,hi-mu]),color=['#334155','#78716C'][j],fmt=['o-','s--'][j],ms=2.5,capsize=2,lw=.8,label=['T(15)','C(15)'][j])
 c.set(title='C  Fidelity (zoom)',xlabel='Perplexity',ylabel='T(15), C(15)',ylim=(.905,.921),yticks=[.905,.910,.915,.920],xticks=[15,30,50]);
 for ax in [a,z,t]:ax.xaxis.set_major_locator(MaxNLocator(3));ax.yaxis.set_major_locator(MaxNLocator(3))
 fig.tight_layout(rect=[0,.22,1,1],pad=.3,w_pad=.8);legend(fig,origins()[:2]+[Line2D([],[],color='#334155',marker='o',ms=3),Line2D([],[],color='#78716C',marker='s',ls='--',ms=3)],['Human','LD','Trustworthiness T(15)','Continuity C(15)'],4)
 finish(fig,5,'fig03_pca_tsne_trustworthiness.png','Fixed PCA uses equal coordinate scaling: A1 retains all points; A2 explicitly zooms PC1 to [−5,10] and PC2 to [−6,6] without changing analysis. Hollow, transparent t-SNE markers expose both origins. Fidelity panel C zooms 0.905–0.921; whiskers are seed ranges, not confidence intervals. PCA2 T(15)=0.6928 and C(15)=0.7571; explained variance alone does not guarantee neighborhood preservation.')
def spectral():
 d=read('spectral_wavelet_profiles.csv');fig,axes=plt.subplots(1,2,figsize=(7.16,1.95));bands=['LH1','HL1','HH1','LH2','HL2','HH2'];x=(np.arange(16)+.5)/32
 for j,o in enumerate(ORIGIN):
  g=d[d.origin.eq(o)].set_index('feature');s=g.loc[[f'fft_{i:02d}_median' for i in range(16)]];axes[0].plot(x,s['mean'],color=ORIGIN[o],ls=DASH[j],marker=MARK[j],ms=1.5,lw=.8);axes[0].fill_between(x,s.ci_low,s.ci_high,color=ORIGIN[o],alpha=.18)
  w=g.loc[['dwt_'+v+'_median' for v in bands]];xx=np.arange(6)+(j-1)*.18;axes[1].plot(xx,w['mean'],linestyle='none',marker=MARK[j],color=ORIGIN[o],markerfacecolor='white',ms=2,zorder=2);axes[1].errorbar(xx,w['mean'],yerr=np.vstack([w['mean']-w.ci_low,w.ci_high-w['mean']]),fmt='none',color=ORIGIN[o],elinewidth=1,capsize=2,capthick=.8,zorder=5)
 axes[0].set(title='A  Hann-windowed FFT',xlabel='Radial frequency (cycles/pixel)',ylabel='Power share (log scale)',yscale='log');axes[1].set(title='B  Two-level Haar',xticks=range(6),xticklabels=bands,ylabel='Energy ratio (log scale)',yscale='log')
 fig.tight_layout(rect=[0,.20,1,1],pad=.3,w_pad=1);legend(fig,origins(),['Human','LD','SD (resized sensitivity)'],3)
 finish(fig,6,'fig04_spectral_and_wavelet_profiles.png','Mean FFT shares and Haar energies with 1,000-source-group-bootstrap 95% intervals. Small open Haar markers leave whiskers visible. Human/LD use native 256²; SD is resized and descriptive. LL2 remains in Haar normalization. Similar pooled spectra do not rule out style-specific contrasts.')
def heatmap():
 d=read('style_family_drift.csv');styles=sorted(d['style'].unique());families=['Ordinal','FFT','Haar','Color/edges'];fig,axes=plt.subplots(1,2,figsize=(7.16,2.05))
 for ax,key,cmap,head in zip(axes,['w1','median_shift'],['Greys','RdGy_r'],['A  Mean standardized W₁','B  Mean signed shift (LD − Human)']):
  vals=d.pivot(index='style',columns='family',values=key).loc[styles,families].to_numpy();lim=1.05 if key=='w1' else float(np.max(np.abs(vals)));im=ax.imshow(vals,cmap=cmap,vmin=0 if key=='w1' else -lim,vmax=lim,aspect='auto')
  for i in range(10):
   for j in range(4):
    rgb=im.cmap(im.norm(vals[i,j]));lum=sum(x*w for x,w in zip(rgb,[.2126,.7152,.0722]));ax.text(j,i,f'{vals[i,j]:.3f}',ha='center',va='center',fontsize=6,color='white' if lum<.5 else 'black')
  ax.set(xticks=range(4),xticklabels=families,yticks=range(10),yticklabels=[title(s) for s in styles],title=head);ax.tick_params(labelsize=6.2,length=0,pad=2);cb=fig.colorbar(im,ax=ax,fraction=.035,pad=.02);cb.ax.tick_params(labelsize=6,length=2)
 fig.tight_layout(pad=.3,w_pad=1)
 finish(fig,7,'fig05_style_drift_heatmap.png','Family-average standardized Wasserstein distance and signed median shift. Every family has at least one exploratory constituent pass, so redundant asterisks are omitted. The distance scale extends to 1.05 and includes the Ukiyo-e Haar value 1.013; signed colors are symmetric around zero. Averages are descriptive, not family-level tests or confirmed effects.',dict(distance_color_max=1.05,signed_center=0))

def distributions():
 d=read('feature_distribution_values.csv');top=read('display_feature_selection.csv').feature.tolist();stats=read('style_feature_drift.csv');styles=['renaissance','impressionism','ukiyo-e'];fig,axes=plt.subplots(3,4,figsize=(7.16,2.8));rng=np.random.default_rng(42)
 for j,feature in enumerate(top):
  style=styles[j%3];a,e=axes.flat[2*j],axes.flat[2*j+1];g=d[d.feature.eq(feature)&d['style'].eq(style)]
  for k,(o,m,ls) in enumerate([('Human','o','-'),('LD','s','--')]):
   values=g[g.origin.eq(o)].value.dropna().to_numpy();v=a.violinplot(values,positions=[k],showmedians=True,widths=.65)
   for body in v['bodies']:body.set_facecolor(ORIGIN[o]);body.set_alpha(.20)
   for key in ['cbars','cmins','cmaxes','cmedians']:v[key].set_color(ORIGIN[o]);v[key].set_linewidth(.6)
   a.scatter(k+rng.uniform(-.13,.13,len(values)),values,s=.5,marker=m,color=ORIGIN[o],alpha=.15,rasterized=True);x=np.sort(values);e.plot(x,np.arange(1,len(x)+1)/len(x),color=ORIGIN[o],ls=ls,lw=.8)
  a.set(xticks=[0,1],xticklabels=['Human','LD'],title=feature.replace('_median','').replace('_pooled','')+' / '+title(style));a.title.set_fontsize(6.5);stat=stats[stats.feature.eq(feature)&stats['style'].eq(style)].iloc[0];e.set(title=f'ECDF; KS D={stat.ks_D:.3f}',xlabel='Raw measurement',ylabel='Fraction');a.yaxis.set_major_locator(MaxNLocator(3));e.xaxis.set_major_locator(MaxNLocator(3));e.set_yticks([0,1])
 fig.tight_layout(rect=[0,.12,1,1],pad=.3,h_pad=.65,w_pad=.7);legend(fig,origins()[:2],['Human','LD'],2)
 finish(fig,8,'fig06_feature_ecdfs_and_rainclouds.png','Supplementary Fig. S1. Six features selected from absolute coefficients of the development-trained handcrafted probe, with prespecified display styles and 300 test artworks per origin/style. Violin/jitter distributions and ECDFs retain raw units; KS D is descriptive. Feature selection does not rank held-out effects. Common-support controls remain failed.')
def ablations():
 d=read('ablation_results.csv');fam=d[d.kind.eq('family')];fig=plt.figure(figsize=(7.16,2.3));gs=fig.add_gridspec(2,3,width_ratios=[1.1,1,1.1]);a=fig.add_subplot(gs[:,0]);s=fig.add_subplot(gs[:,1]);c=fig.add_subplot(gs[0,2]);g=fig.add_subplot(gs[1,2]);yy=np.arange(len(fam))
 for ax,key,label in [(a,'auc','Δ AUROC'),(s,'silhouette','Δ silhouette')]:
  ax.errorbar(fam['delta_'+key],yy,xerr=np.vstack([fam['delta_'+key]-fam['delta_'+key+'_low'],fam['delta_'+key+'_high']-fam['delta_'+key]]),fmt='o',color='#334155',ms=2.4,capsize=1.4,elinewidth=.8);ax.axvline(0,color='#78716C',ls='--',lw=.7);ax.set(yticks=yy,yticklabels=fam.label if key=='auc' else ['']*len(fam),xlabel=label,title='A  Family removal / isolation' if key=='auc' else 'Paired held-out differences');ax.invert_yaxis();ax.tick_params(labelsize=6);ax.xaxis.set_major_locator(MaxNLocator(4))
 color=read('color_saturation_ablation.csv');palette=['#854D0E','#4B5563','#A21CAF']
 for j,model in enumerate(['HSV','Lab','HSV+Lab']):
  v=color[color.model.eq(model)].set_index('tertile').loc[['low','medium','high']];c.errorbar(range(3),v.roc_auc,yerr=np.vstack([v.roc_auc-v.auc_low,v.auc_high-v.roc_auc]),fmt=MARK[j]+DASH[j],ms=2.2,color=palette[j],capsize=1.5,lw=.7,label=model)
 lower=min(.94,float(color.auc_low.min())-.003);upper=max(1,float(color.auc_high.max())+.003);c.set(xticks=range(3),xticklabels=['Low','Medium','High'],ylim=(lower,upper),ylabel='AUROC (zoom)',title='B  Saturation strata');c.yaxis.set_major_locator(MaxNLocator(3));c.tick_params(labelsize=6)
 geom=d[d.kind.eq('geometry')];base=read('baseline_metrics.csv').set_index('model').loc['handcrafted','roc_auc'];values=[base]+geom.roc_auc.tolist();g.bar(range(3),values,color='#64748B',edgecolor='#334155',linewidth=.4);g.set(xticks=range(3),xticklabels=['4 quadrants','Full 256','5 crops'],ylim=(0,1.14),ylabel='AUROC',title='C  Crop context (zero baseline)');g.tick_params(labelsize=6)
 for i,v in enumerate(values):g.text(i,v+.035,f'{v:.4f}',ha='center',va='bottom',fontsize=6)
 fig.tight_layout(rect=[0,.08,1,1],pad=.3,w_pad=.7,h_pad=1.2);legend(fig,[Line2D([],[],color=co,marker=ma,ls=ls,ms=3) for co,ma,ls in zip(palette,MARK,DASH)],['HSV','Lab','HSV+Lab'],3,anchor=(.82,.002))
 finish(fig,10,'fig08_ablation_forest_plot.png',f'Paired family changes, development-defined saturation strata and crop sensitivities. Family intervals resample source groups; silhouette intervals condition on cached geometry. B zooms AUROC to {lower:.3f}–{upper:.3f} and retains all whiskers; C starts at zero and offsets bar labels. Ordinal removal has the largest conditional predictive loss. Brown/gray/magenta encode color representations, never origin.',dict(saturation_ylim=[lower,upper],all_saturation_intervals_in_bounds=bool((color.auc_low>=lower).all() and (color.auc_high<=upper).all())))
def robustness():
 d=read('perturbation_results.csv').set_index('view');iv=read('perturbation_auc_intervals.csv').set_index('view');order=['original','jpeg95','jpeg75','jpeg50','original','resize0.75','resize0.5'];xx=np.array([0,1,2,3,5,6,7]);labs=['Orig.','95','75','50','Orig.','×.75','×.50'];fig,axes=plt.subplots(1,3,figsize=(7.16,1.85))
 base=iv.loc['original','roc_auc'];auc=np.array([0 if k=='original' else d.loc[k,'roc_auc']-base for k in order]);lo=np.array([0 if k=='original' else d.loc[k,'delta_auc_low'] for k in order]);hi=np.array([0 if k=='original' else d.loc[k,'delta_auc_high'] for k in order]);axes[0].errorbar(xx,auc,yerr=np.vstack([auc-lo,hi-auc]),fmt='o',color='#334155',ms=2.2,capsize=2,elinewidth=.8);axes[0].axhline(0,color='#78716C',ls='--',lw=.6)
 for ax,key in [(axes[1],'silhouette_retention'),(axes[2],'style_w1_rank_rho')]:ax.plot(xx,[1 if k=='original' else d.loc[k,key] for k in order],linestyle='none',marker='s' if ax==axes[1] else '^',color='#334155',ms=3)
 for ax,head,label,ylim in zip(axes,['A  Paired frozen-probe change','B  Origin silhouette ratio','C  Style-rank correlation'],['Δ AUROC','Ratio to original','Spearman ρ'],[(-.35,.025),(0,1.5),(0,1.08)]):
  ax.set(xticks=xx,xticklabels=labs,title=head,ylabel=label,ylim=ylim);ax.tick_params(axis='x',rotation=45,labelsize=6);ax.axvline(4,color='#CBD5E1',lw=.65);ax.yaxis.set_major_locator(MaxNLocator(4));ax.set_xlabel('JPEG quality       Resize factor',fontsize=6.3)
 fig.tight_layout(pad=.3,w_pad=1)
 finish(fig,11,'fig09_perturbation_robustness.png','Separate aligned panels compare paired frozen-probe AUROC change, silhouette ratio and style-rank correlation. A uses the exact paired changes and group-bootstrap intervals in Table XII. Original is a zero reference by definition, not an estimated zero-width interval. B/C are descriptive points, without invented intervals. JPEG 50 weakens ranking while silhouette rises; inputs are release JPEGs, not pristine quality 100.')
def gallery():
 d=read('error_gallery_cases.csv');fig,axes=plt.subplots(8,5,figsize=(7.16,4.9));bands=['LH1','HL1','HH1','LH2','HL2','HH2']
 for row,(r,axs) in enumerate(zip(d.itertuples(),axes)):
  bottom=.925-row*.122;pos=[(.025,bottom,.07,.065),(.135,bottom,.20,.065),(.415,bottom,.18,.061),(.665,bottom,.14,.061),(.87,bottom,.12,.061)]
  for k,ax in enumerate(axs):ax.set_position(pos[k]);ax.tick_params(labelsize=4.5,length=1,pad=.5);ax.title.set_fontsize(5)
  axs[0].imshow(Image.open(OUT/'gallery'/f'{r.artwork_id}.png'));axs[0].axis('off');axs[0].set_title(f'{row+1}. {r.selection_reason} / {r.origin}\n{title(r.style)}',fontsize=5,pad=2);axs[1].imshow(Image.open(OUT/'gallery'/f'{r.artwork_id}_crops.png'));axs[1].axis('off');axs[1].set_title('TL · TR · BL · BR',fontsize=5,pad=2)
  vals=np.array([getattr(r,f'fft_{i:02d}_median') for i in range(16)]);axs[2].plot((np.arange(16)+.5)/32,vals,color=ORIGIN[r.origin],lw=.75);axs[2].set(yscale='log',ylim=(1e-4,1),xlim=(0,.5),xticks=[0,.5],yticks=[1e-4,1e-2,1]);axs[2].set_title(f'FFT (log); β={r.fft_beta_median:.2f}',fontsize=5,pad=2);axs[2].set_xlabel('f (cycles/pixel)',fontsize=4.5,labelpad=.5)
  vals=np.array([getattr(r,f'dwt_{v}_median') for v in bands]);axs[3].plot(range(6),vals,linestyle='none',marker='o' if r.origin=='Human' else 's',color=ORIGIN[r.origin],ms=2.2);axs[3].set(yscale='log',ylim=(1e-5,.1),xticks=range(6),xticklabels=bands,yticks=[1e-5,1e-3,.1]);axs[3].set_title('Haar (log scale)',fontsize=5,pad=2);axs[3].tick_params(axis='x',rotation=35,labelsize=4)
  for ax in axs[2:4]:ax.yaxis.set_minor_locator(LogLocator(base=10,subs=[]));ax.yaxis.set_minor_formatter(NullFormatter())
  vals=[r.s_median_median,r.v_median_median,r.edge_density_median,r.hue_resultant_median];axs[4].barh(range(4),vals,color=ORIGIN[r.origin],height=.58);axs[4].set(xlim=(0,1),ylim=(-1.1,3.9),yticks=range(4),yticklabels=['S','V','E','R'],xticks=[0,1]);axs[4].set_title(f'H={r.H_pooled:.3f}; C={r.C_pooled:.3f}',fontsize=5,pad=2);axs[4].tick_params(axis='y',pad=2)
  for i,v in enumerate(vals):
   if not np.isfinite(v):axs[4].text(.05,i,'N/A',fontsize=5,va='center')
 finish(fig,12,'fig10_forensic_error_gallery.png','Eight purposively selected held-out cases: FP/FN/TP are false positive/false negative/true positive against release labels. All FFT rows share 10⁻⁴–1 and all Haar rows 10⁻⁵–10⁻¹, both logarithmic. S = saturation, V = value, E = edge density, R = hue resultant; N/A means undefined hue. Canvas, disjoint quadrants and measurements expose inspectable examples, not estimated error prevalence.',dict(fft_shared_limits=[1e-4,1],haar_shared_limits=[1e-5,.1]))
def main():
 for fn in [architecture,dataset,baselines,atlas,projections,spectral,heatmap,distributions,ablations,robustness,gallery]:fn()
 (B/'qa/figure_audit.json').write_text(json.dumps(AUDIT,indent=2),encoding='utf8');(B/'results/figure_captions.json').write_text(json.dumps(CAPTIONS,indent=2),encoding='utf8');(B/'results/figure_source_hashes.json').write_text(json.dumps(READ,indent=2),encoding='utf8');(B/'results/color_map.json').write_text(json.dumps(dict(origins=ORIGIN,models=dict(zip(MODELS,MC)),color_representations={'HSV':'#854D0E','Lab':'#4B5563','HSV+Lab':'#A21CAF'}),indent=2),encoding='utf8');print('All static composites regenerated from saved data; origin hues are reserved.',flush=True)
if __name__=='__main__':main()
