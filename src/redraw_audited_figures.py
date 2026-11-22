"""DAV-only regeneration from existing CSVs. No analysis, model fit or source mutation."""
from pathlib import Path
import sys,os,re,json,textwrap
os.environ['PYTHONDONTWRITEBYTECODE']='1'
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B/'src'))
import publication_figures as pf
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.container import BarContainer
from matplotlib.ticker import MaxNLocator,NullFormatter,LogLocator,LogFormatterMathtext
from matplotlib.markers import MarkerStyle
from matplotlib.collections import PathCollection
import numpy as np
COLORS={'Human':'#2563EB','LD':'#EA580C','SD':'#8458B3'}
pf.COLORS=COLORS;pf.MODEL_COLORS=['#2563EB','#EA580C','#009E73','#8458B3','#494D5F']
MAP={1:2,2:4,3:5,4:6,5:7,6:8,7:3,8:10,9:11,10:12};AUDIT=[]
STYLES=['-','--','-.',':',(0,(5,2,1,2))];MARKERS=['o','s','^','D','X'];HATCH=['','///','...','xx','\\\\']
SHORT={'Art Nouveau':'Art Nouv.','Expressionism':'Expression.','Impressionism':'Impression.','Post Impressionism':'Post-impr.','Renaissance':'Renaiss.','Romanticism':'Romantic.','Surrealism':'Surreal.','Normalized permutation entropy H':'Entropy H','Statistical complexity C':'Complexity C','Full-space origin silhouette retention':'Silhouette ratio','Spearman ρ vs. original style ranking':'Style-rank ρ','Audited artworks':'Artworks','Full native metadata':'Full metadata','Native-256 matched metadata':'Native256 metadata','Full dimensions only':'Dimensions only'}
def shorten(t):
 for a,b in SHORT.items():t=t.replace(a,b)
 return t
def finish(fig,name,caption):
 n=int(name[3:5]);height={1:2.15,2:2.4,3:2.25,4:2.05,5:2.4,6:2.8,7:2.8,8:2.7,9:2.15,10:5.7}[n];fig.set_size_inches(7.16,height)
 if fig._suptitle:fig._suptitle.remove()
 handles=[];labels=[]
 for ax in fig.axes:
  hh,ll=ax.get_legend_handles_labels()
  for h,l in zip(hh,ll):
   l=shorten(l)
   if n==7:
    for old,new in zip(pf.LABELS,['Handcrafted','FFT only','Metadata','ResNet-50','DINOv2']):
     if l.startswith(old):l=new;break
   if l not in labels and not l.startswith('_'):handles.append(h);labels.append(l)
  if ax.get_legend():ax.get_legend().remove()
  for key in ['title','xlabel','ylabel']:
   s=shorten(getattr(ax,'get_'+key)())
   if key=='ylabel' and ax.get_yscale()=='log' and 'log scale' not in s:s+=' (log scale)'
   getattr(ax,'set_'+key)(s,fontsize=6.5)
  ax.tick_params(labelsize=6,length=2,pad=1)
  for t in list(ax.texts):
   t.set_fontsize(5.8)
   if n==7 and ax==fig.axes[2]:t.remove()
  if n in [1,7] and any(len(x.get_text())>8 for x in ax.get_xticklabels()):
   ax.tick_params(axis='x',rotation=55)
   for t in ax.get_xticklabels():t.set_ha('right');t.set_fontsize(5.3)
  for j,container in enumerate([c for c in ax.containers if isinstance(c,BarContainer)]):
   for patch in container.patches:patch.set_hatch(HATCH[j%5]);patch.set_linewidth(.25);patch.set_edgecolor('#494D5F')
  if any(isinstance(c,BarContainer) for c in ax.containers) and ax.get_yscale()!='log':ax.set_ylim(bottom=0)
 if n==1:
  for j,line in enumerate(fig.axes[1].lines[:3]):line.set_linestyle(STYLES[j]);line.set_marker(MARKERS[j]);line.set_markevery(max(1,len(line.get_xdata())//9));line.set_markersize(2)
 if n==2:
  for ax in fig.axes:
   for i,c in enumerate([c for c in ax.collections if isinstance(c,PathCollection) and len(c.get_offsets())>10]):
    marker=MarkerStyle(['o','s'][i%2]);c.set_paths([marker.get_path().transformed(marker.get_transform())])
   for i,line in enumerate(ax.lines):line.set_marker(['o','s'][i%2]);line.set_markersize(3)
   delta=''
   for txt in list(ax.texts):
    if txt.get_text().startswith('ΔH='):delta=txt.get_text().replace('\n','; ');txt.remove()
   ax.set_title(shorten(ax.get_title())+'\n'+delta,fontsize=6);ax.set_xlabel('H',fontsize=6);ax.set_ylabel('C',fontsize=6)
  handles=[Line2D([],[],color=COLORS[o],marker=m,linestyle=ls,label=o) for o,m,ls in [('Human','o','-'),('LD','s','--')]];labels=['Human','LD (descriptive)']
 if n==3:
  a,b,c=fig.axes
  # Origin is redundant hue+shape; styles remain in their dedicated atlas facets.
  for ax in [a,b]:
   for col in ax.collections:
    if isinstance(col,PathCollection) and len(col.get_offsets())>1:
     fc=col.get_facecolors();is_human=bool(len(fc) and fc[0,2]>fc[0,0]);m=MarkerStyle('o' if is_human else 's');col.set_paths([m.get_path().transformed(m.get_transform())])
  for txt in list(a.texts):txt.remove()
  a.set_title('A  Fixed PCA\nT(15)=0.693; C(15)=0.757',fontsize=6.5)
  feats=[];colors=[]
  handles=[Line2D([],[],marker='o',color=COLORS['Human'],linestyle=''),Line2D([],[],marker='s',color=COLORS['LD'],linestyle='')]+[Line2D([],[],color=x) for x in colors]+[Line2D([],[],color=x,marker=m,linestyle=ls) for x,m,ls in [('#0072B2','o','-'),('#D55E00','s','--')]]
  labels=['Human','LD']+feats+['Trustworthiness','Continuity']
  for line in c.lines:
   if len(line.get_xdata())==3 and line.get_linestyle() not in ['None','',None]:
    orange=str(line.get_color()).lower()=='#d55e00';line.set_linestyle('--' if orange else '-');line.set_marker('s' if orange else 'o')
 if n==4:
  fig.axes[0].set_ylabel('Power share (log scale)',fontsize=6.5);fig.axes[1].set_ylabel('Detail-energy ratio (log scale)',fontsize=6.5)
  for j,line in enumerate(fig.axes[0].lines):line.set_marker(['o','s','^'][j%3]);line.set_markersize(2);line.set_linestyle(STYLES[j%3])
  handles=[Line2D([],[],marker=m,color=COLORS[o],linestyle=STYLES[i]) for i,(o,m) in enumerate([('Human','o'),('LD','s'),('SD','^')])];labels=['Human','LD','SD (resized sensitivity)']
  for j,container in enumerate(fig.axes[1].containers):
   if hasattr(container,'lines') and container.lines[0] is not None:container.lines[0].set_marker(['o','s','^'][j%3])
 if n==5:
  for ax in fig.axes:
   if not ax.images:continue
   im=ax.images[0]
   for t in ax.texts:
    x,y=t.get_position();rgba=im.cmap(im.norm(im.get_array()[round(y),round(x)]));lum=sum(c*w for c,w in zip(rgba,[.2126,.7152,.0722]));t.set_color('black' if lum>.53 else 'white')
 if n==6:
  for ax in fig.axes[1::2]:ax.set_ylabel('Fraction',fontsize=6.5)
  for ax in fig.axes[1::2]:
   for j,line in enumerate(ax.lines):line.set_linestyle(STYLES[j%2]);line.set_marker(['o','s'][j%2]);line.set_markersize(2);line.set_markevery(max(1,len(line.get_xdata())//5))
  handles=[Line2D([],[],color=COLORS[o],marker=m,linestyle=STYLES[i]) for i,(o,m) in enumerate([('Human','o'),('LD','s')])];labels=['Human','LD']
 if n==7:
  fig.axes[2].set_ylabel('k=2 ARI',fontsize=6.5)
  for ax in fig.axes[:2]:
   for j,line in enumerate(ax.lines[:5]):line.set_linestyle(STYLES[j]);line.set_marker(MARKERS[j]);line.set_markersize(2);line.set_linewidth(.9);line.set_markevery(max(1,len(line.get_xdata())//10))
  for ax in fig.axes[-2:]:ax.set_ylim(0,1.07)
  handles=[Line2D([],[],color=c,marker=m,linestyle=ls) for c,m,ls in zip(pf.MODEL_COLORS,MARKERS,STYLES)];labels=['Handcrafted','FFT only','Metadata','ResNet-50','DINOv2']
 if n==8:
  fig.axes[0].xaxis.set_major_locator(MaxNLocator(4));fig.axes[1].xaxis.set_major_locator(MaxNLocator(4))
  for j,line in enumerate(fig.axes[2].lines):line.set_linestyle(STYLES[j%3]);line.set_marker(MARKERS[j%3])
  fig.axes[2].set_ylabel('AUROC (zoomed axis)',fontsize=6.5);fig.axes[3].set_ylim(0,1.06)
  for p in fig.axes[3].patches:p.set_facecolor('#2563EB')
 if n==9:
  for ax in [fig.axes[0],fig.axes[-1]]:
   for line in ax.lines:
    if line.get_marker() not in ['None','',None]:line.set_linestyle('None')
  fig.axes[0].set_ylabel('AUROC (axis 0.5–1.03)',fontsize=6.5)
 if n==10:
  cases=pf.csv('error_gallery_cases.csv')
  for row,r in enumerate(cases.itertuples()):
   axs=fig.axes[row*5:(row+1)*5];axs[0].set_title(f'{row+1}. {r.selection_reason} / {r.origin}\n{pf.title(r.style)}',fontsize=5.8);axs[1].set_title('TL · TR · BL · BR',fontsize=5.8);axs[2].set_ylabel('');axs[2].set_xlabel('f (cycles/pixel)',fontsize=5.5);axs[2].set_title(f'FFT (log scale)\nβ={r.fft_beta_median:.2f}',fontsize=5.5);axs[3].set_ylabel('');axs[3].set_title('Haar (log scale)',fontsize=5.8);axs[4].set_yticks(range(4),['S','V','Edge','R']);axs[4].tick_params(axis='y',labelsize=5.5);axs[2].xaxis.set_major_locator(MaxNLocator(2));axs[4].xaxis.set_major_locator(MaxNLocator(2));axs[3].yaxis.set_minor_formatter(NullFormatter())
   vals=[patch.get_height() for patch in list(axs[3].patches)]
   for patch in list(axs[3].patches):patch.remove()
   axs[3].plot(range(len(vals)),vals,linestyle='None',marker='o' if r.origin=='Human' else 's',markersize=3,color=COLORS[r.origin])
   for ax in axs:
    for t in ax.texts:
     if 'undefined:' in t.get_text():t.set_text('N/A')
 # All legends occupy a reserved figure band, never data axes.
 band=.30 if n==3 else (.19 if handles else .015)
 if n!=10:fig.tight_layout(rect=[0,band,1,1],pad=.35,h_pad=.7,w_pad=.7)
 else:
  for row in range(8):
   bottom=.925-row*.123
   positions=[(.04,bottom,.065,.064),(.15,bottom,.19,.064),(.425,bottom,.18,.055),(.67,bottom,.13,.055),(.865,bottom,.125,.055)]
   for k,ax in enumerate(fig.axes[row*5:(row+1)*5]):
    ax.set_position(positions[k]);ax.title.set_fontsize(4.5);ax.title.set_position((.5,1.02));ax.tick_params(labelsize=4,length=1,pad=.5);ax.xaxis.label.set_fontsize(4);ax.xaxis.labelpad=1
    if k in [2,3]:ax.yaxis.set_major_locator(LogLocator(base=10,numticks=2));ax.yaxis.set_minor_locator(LogLocator(base=10,subs=[]));ax.yaxis.set_minor_formatter(NullFormatter());ax.yaxis.set_major_formatter(LogFormatterMathtext(base=10,labelOnlyBase=True))
    if k==4:ax.set_yticks(range(4),['S','V','E','R']);ax.tick_params(axis='y',labelsize=4)
 legend=fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.003),ncol=3 if len(labels)>3 else max(1,len(labels)),fontsize=5.8,frameon=False,columnspacing=1.0,handlelength=2) if handles else None
 fig.canvas.draw();renderer=fig.canvas.get_renderer();overlap=[]
 if legend:
  bb=legend.get_window_extent(renderer)
  overlap=[i for i,ax in enumerate(fig.axes) if bb.overlaps(ax.get_window_extent(renderer))]
 assert not overlap,(name,overlap)
 AUDIT.append(dict(file=name,axes=len(fig.axes),legend_count=int(legend is not None),legend_data_axes_overlaps=overlap,bar_axes_zero=[ax.get_ylim()[0]==0 for ax in fig.axes if any(isinstance(c,BarContainer) for c in ax.containers) and ax.get_yscale()!='log'],log_axes_labeled=all('log scale' in ax.get_ylabel() or 'log scale' in ax.get_title() for ax in fig.axes if ax.get_yscale()=='log'),median_shift_zero_centered=all(abs(im.norm.vmin+im.norm.vmax)<1e-10 for ax in fig.axes for im in ax.images if 'signed' in ax.get_title().lower())))
 fig.savefig(B/'figures'/name,dpi=450,bbox_inches='tight',pad_inches=.02);fig.savefig(B/'paper/latex_source/figures'/f'figure_{MAP[n]:02}.png',dpi=450,bbox_inches='tight',pad_inches=.02);plt.close(fig);print('Audited',name,flush=True)
def main():
 pf.finish=finish
 for fn in [pf.fig01,pf.fig02,pf.fig03,pf.fig04,pf.fig05,pf.fig06,pf.fig07,pf.fig08,pf.fig09,pf.fig10]:fn()
 (B/'audit/dav_figure_audit.json').write_text(json.dumps(AUDIT,indent=2,default=lambda x:bool(x) if isinstance(x,np.bool_) else float(x)),encoding='utf8')
 print('All10 composites regenerated from existing CSVs; zero legend/data-axes overlap.',flush=True)
if __name__=='__main__':main()
