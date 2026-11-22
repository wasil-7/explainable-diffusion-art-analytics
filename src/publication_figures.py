"""Stage 10: ten 300-DPI composites rendered exclusively from cached result tables."""
from common import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.stats import gaussian_kde
from PIL import Image
import textwrap

COLORS={'Human':'#0072B2','LD':'#D55E00','SD':'#009E73'}
MODEL_COLORS=['#0072B2','#E69F00','#CC79A7','#009E73','#D55E00']
NAMES=['handcrafted','frequency','metadata_gated','resnet50','dinov2']
LABELS=['Handcrafted','FFT only','Metadata','ResNet-50','DINOv2']
FIGS=[]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':11,'axes.labelsize':9,'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
GATE='Descriptive comparisons: JPEG encoding is origin-aligned; subjects are unverified. No confirmed origin effect.'

def csv(name):return pd.read_csv(OUT/name)
def metric(name):return csv('baseline_metrics.csv').set_index('model').loc[name].to_dict()
def title(s):return s.replace('_',' ').title()
def finish(fig,name,caption):
    full=caption+' '+GATE
    fig.text(.03,.015,textwrap.fill(full,175 if fig.get_figwidth()>15 else 145),fontsize=8,va='bottom')
    fig.tight_layout(rect=[.01,.075,.99,.96]);path=OUT/name;fig.savefig(path,dpi=300);plt.close(fig)
    FIGS.append(dict(file=name,dpi=300,caption=full));print('Rendered',name,flush=True)

def fig01():
    fig,axes=plt.subplots(1,2,figsize=(15,6));counts=csv('audit_counts.csv').pivot_table(index='style',columns='origin',values='count',aggfunc='sum').fillna(0);bottom=np.zeros(len(counts))
    for origin in COLORS:axes[0].bar(np.arange(len(counts)),counts[origin],bottom=bottom,color=COLORS[origin],label=origin+(' native 768²' if origin=='SD' else ' native 256²'));bottom+=counts[origin].to_numpy()
    axes[0].set(xticks=range(10),xticklabels=[title(x) for x in counts.index],ylabel='Audited artworks',title='A  Full release: 185,015 readable images');axes[0].tick_params(axis='x',rotation=45);axes[0].legend()
    for i,(name,label) in enumerate([('metadata_ungated_full','Full native metadata'),('metadata_gated','Native-256 matched metadata'),('dimensions_ungated_full','Full dimensions only')]):
        r=csv(f'roc_{name}.csv');m=metric(name);axes[1].plot(r.fpr,r.tpr,color=MODEL_COLORS[i],linestyle=['-','--',':'][i],lw=2,label=f"{label}: AUC {m['roc_auc']:.4f}")
    axes[1].plot([0,1],[0,1],'k:',alpha=.4);axes[1].set(xlabel='False positive rate',ylabel='True positive rate',title='B  Native resolution control leaves JPEG leakage');axes[1].legend(loc='lower right')
    finish(fig,'fig01_dataset_audit_and_confound.png','Full-release and primary metadata probes use different source compositions. Both combined metadata probes attain AUROC 1.0000: matching native dimensions alone does not remove quantization-table leakage. Counts include all release files; ROC uses held-out grouped test sets.')

def fig02():
    d=csv('hc_plot_points.csv');ells=csv('hc_centroid_ellipses.csv');bounds=csv('hc_theoretical_bounds.csv');fig,axes=plt.subplots(2,5,figsize=(18,8),sharex=True,sharey=True)
    xlim=(min(.7,d.H_pooled.min()-.01),1.005);ylim=(-.005,max(.25,d.C_pooled.max()+.01))
    for ax,style in zip(axes.flat,sorted(d['style'].unique())):
        for origin in ['Human','LD']:
            g=d[(d['style']==style)&(d.origin==origin)];color=COLORS[origin];ax.scatter(g.H_pooled,g.C_pooled,s=4,c=color,alpha=.12,rasterized=True)
            xx,yy=np.meshgrid(np.linspace(*xlim,100),np.linspace(*ylim,100));kde=gaussian_kde(g[['H_pooled','C_pooled']].to_numpy().T);density=kde(np.vstack([xx.ravel(),yy.ravel()])).reshape(xx.shape)
            ax.contour(xx,yy,density,levels=np.max(density)*np.array([.15,.4,.7]),colors=[color],linewidths=.8)
            e=ells[(ells['style']==style)&(ells.origin==origin)].iloc[0];ax.add_patch(Ellipse((e.H,e.C),e.width,e.height,angle=e.angle,facecolor=color,edgecolor=color,alpha=.25));ax.plot(e.H,e.C,'o',color=color,ms=4)
        ee=ells[ells['style']==style].set_index('origin');a=ee.loc['Human'];b=ee.loc['LD'];ax.annotate('',xy=(b.H,b.C),xytext=(a.H,a.C),arrowprops=dict(arrowstyle='->',color='#333333',lw=1.3));ax.set(title=title(style),xlim=xlim,ylim=ylim)
        ax.text(.04,.93,f'ΔH={b.H-a.H:+.3f}\nΔC={b.C-a.C:+.3f}',transform=ax.transAxes,fontsize=8,va='top')
    for ax in axes[-1]:ax.set_xlabel('Normalized permutation entropy H')
    for ax in axes[:,0]:ax.set_ylabel('Statistical complexity C')
    fig.suptitle('H–C atlas: Human (blue) → latent diffusion (orange), 300 test artworks per origin/style',fontsize=14)
    finish(fig,'fig02_hc_causality_atlas.png','Contour heights are within-cell KDE levels (15%, 40%, 70% of the peak), not between-cell counts. Centroid ellipses use 500 source-group bootstrap resamples and Gaussian 95% contours. Shared axes; arrows are signed descriptive displacements. The historical filename does not establish causality.')

def fig03():
    pc=csv('pca_plot_points.csv');ts=csv('tsne_plot_points.csv');f=csv('projection_fidelity.csv');pf=csv('pca_projection_fidelity.csv');load=csv('pca_loadings.csv').set_index('feature');fig,axes=plt.subplots(1,3,figsize=(18,7))
    markers=['o','s','^','v','D','P','X','<','>','h']
    for style,marker in zip(sorted(ts['style'].unique()),markers):
        for origin in ['Human','LD']:
            g=ts[(ts['style']==style)&ts.origin.eq(origin)];axes[1].scatter(g.TSNE1,g.TSNE2,s=7,c=COLORS[origin],marker=marker,alpha=.45,rasterized=True)
    for origin in ['Human','LD']:
        g=pc[pc.origin.eq(origin)];axes[0].scatter(g.PC1,g.PC2,c=COLORS[origin],s=4,alpha=.25,label=origin,rasterized=True)
    chosen=['H_pooled','C_pooled','fft_beta_median','dwt_HH1_median','edge_density_median'];v=load.loc[chosen,['PC1','PC2']].to_numpy();scale=.38*max(np.ptp(pc.PC1),np.ptp(pc.PC2))/np.max(np.abs(v))
    arrowcolors=['#333333','#CC79A7','#009E73','#E69F00','#56B4E9']
    for j,(c,vec,color) in enumerate(zip(chosen,v*scale,arrowcolors)):
        axes[0].annotate('',xy=vec,xytext=(0,0),arrowprops=dict(arrowstyle='->',color=color,lw=1.4))
        vv=v[j];axes[0].text(.03,.65-.075*j,f'{c.replace("_median","")}: ({vv[0]:+.4f}, {vv[1]:+.4f})',color=color,transform=axes[0].transAxes,fontsize=7,bbox=dict(facecolor='white',alpha=.8,edgecolor='none'))
    axes[0].set(title='A  Fixed development-fitted PCA',xlabel='PC1',ylabel='PC2');axes[0].legend();p2=pf[pf.dimensions.eq(2)].iloc[0] if 'dimensions' in pf else pf.iloc[0]
    axes[0].text(.03,.96,f"T(15)={p2.trustworthiness:.3f}\nC(15)={p2.continuity:.3f}",transform=axes[0].transAxes,va='top',bbox=dict(facecolor='white',alpha=.85,edgecolor='none'))
    selected=f[(f.perplexity==30)&(f.seed==42)].iloc[0];axes[1].set(title=f'B  Exploratory t-SNE: p=30, seed=42\nT={selected.trustworthiness:.3f}; C={selected.continuity:.3f}',xlabel='t-SNE 1',ylabel='t-SNE 2')
    from matplotlib.lines import Line2D
    handles=[Line2D([0],[0],marker=marker,linestyle='',color='#777777',markersize=4,label=title(style)) for style,marker in zip(sorted(ts['style'].unique()),markers)]
    axes[1].legend(handles=handles,ncol=3,fontsize=6,loc='upper center',bbox_to_anchor=(.5,-.17),columnspacing=.7,handletextpad=.3)
    for metric,color in [('trustworthiness','#0072B2'),('continuity','#D55E00')]:
        grouped=f.groupby('perplexity')[metric];mu=grouped.mean();lo=grouped.min();hi=grouped.max();axes[2].errorbar(mu.index,mu,yerr=np.vstack([mu-lo,hi-mu]),fmt='o-',capsize=5,label=metric,color=color)
        for seed,g in f.groupby('seed'):axes[2].plot(g.perplexity,g[metric],color=color,alpha=.15,lw=.5)
    axes[2].set(title='C  Neighborhood fidelity, k=15',xlabel='Perplexity',ylabel='Score',xticks=[15,30,50]);axes[2].legend()
    finish(fig,'fig03_pca_tsne_trustworthiness.png','PCA points: 6,000 held-out artworks; arrows use a common display multiplier on loadings. t-SNE: fixed 3,000-artwork subset, 150 per style/origin; symbols encode styles and colors origins. Lines span five random-initialization seeds; whiskers show seed ranges, not confidence intervals. t-SNE distances are exploratory and are not used for inference.')

def fig04():
    d=csv('spectral_wavelet_profiles.csv');fig,axes=plt.subplots(1,2,figsize=(15,6))
    for origin,color in COLORS.items():
        g=d[d.origin.eq(origin)].set_index('feature');spec=g.loc[[f'fft_{i:02d}_median' for i in range(16)]];x=(np.arange(16)+.5)/32;beta=g.loc['fft_beta_median','mean']
        axes[0].plot(x,spec['mean'],color=color,label=f'{origin}, mean β={beta:.2f}');axes[0].fill_between(x,spec.ci_low,spec.ci_high,color=color,alpha=.18)
        names=['LH1','HL1','HH1','LH2','HL2','HH2'];w=g.loc['dwt_'+pd.Index(names)+'_median'];xx=np.arange(6)+{'Human':-.22,'LD':0,'SD':.22}[origin]
        axes[1].errorbar(xx,w['mean'],yerr=np.vstack([w['mean']-w.ci_low,w.ci_high-w['mean']]),fmt='o',capsize=3,color=color,label=origin)
    axes[0].set(yscale='log',xlabel='Radial frequency (cycles/pixel)',ylabel='Mean normalized annular power share',title='A  Hann-windowed 16-annulus FFT');axes[1].set(yscale='log',xticks=range(6),xticklabels=names,ylabel='Mean raw-luminance energy ratio (log scale)',title='B  Two-level Haar detail energies')
    for ax in axes:ax.legend()
    finish(fig,'fig04_spectral_and_wavelet_profiles.png','Artwork statistics are medians over four 128² quadrants; shaded bands and whiskers are 95% source-group bootstrap intervals (1,000 resamples). Human/LD use native256; SD is a separate resized768→256 sensitivity, not a controlled counterpart. Haar LH denotes row-highpass response (horizontal edges); LL2 is retained in the denominator.')

def fig05():
    d=csv('style_family_drift.csv');fig,axes=plt.subplots(1,2,figsize=(14,7));styles=sorted(d['style'].unique());fams=['Ordinal','FFT','Haar','Color/edges']
    for ax,col,cmap,head in zip(axes,['w1','median_shift'],['viridis','RdBu_r'],['A  Mean standardized W₁','B  Mean signed median shift (LD − Human)']):
        values=d.pivot(index='style',columns='family',values=col).loc[styles,fams].to_numpy();lim=np.max(np.abs(values));im=ax.imshow(values,cmap=cmap,aspect='auto',vmin=-lim if col=='median_shift' else 0,vmax=lim)
        for i,s in enumerate(styles):
            for j,fam in enumerate(fams):
                r=d[(d['style']==s)&d.family.eq(fam)].iloc[0];mark='*' if r.raw_rule_count>0 else '';ax.text(j,i,f'{values[i,j]:.3f}{mark if col=="w1" else ""}',ha='center',va='center',fontsize=9,color='white' if abs(values[i,j])/max(lim,1e-12)>.55 else 'black')
        ax.set(xticks=range(4),xticklabels=fams,yticks=range(10),yticklabels=[title(s) for s in styles],title=head);fig.colorbar(im,ax=ax,shrink=.8)
    finish(fig,'fig05_style_drift_heatmap.png','Each family cell averages its prespecified measurements after frozen development RobustScaler normalization. * means at least one constituent feature passes the exploratory BH-adjusted group-randomization + split-half-null rule; it is not a family-level test or confirmed drift. Feature-level values, pass counts and signed-shift CIs are in style_feature_drift.csv. Zero confirmatory cells.')

def fig06():
    d=csv('feature_distribution_values.csv');top=csv('display_feature_selection.csv').feature.tolist();stats=csv('style_feature_drift.csv');fig,axes=plt.subplots(3,4,figsize=(18,12));styles=['renaissance','impressionism','ukiyo-e']; rng=np.random.default_rng(SEED)
    # Six selected features: paired violin+ECDF panels; rotate three prespecified real styles.
    for j,c in enumerate(top):
        style=styles[j%3];ax=axes.flat[2*j];ec=axes.flat[2*j+1];g=d[(d.feature==c)&d['style'].eq(style)]
        for k,origin in enumerate(['Human','LD']):
            vals=g[g.origin.eq(origin)].value.dropna().to_numpy();violin=ax.violinplot(vals,positions=[k],showmedians=True,widths=.65)
            for body in violin['bodies']:body.set_facecolor(COLORS[origin]);body.set_alpha(.4)
            ax.scatter(k+rng.uniform(-.15,.15,len(vals)),vals,s=2,c=COLORS[origin],alpha=.2,rasterized=True);ss=np.sort(vals);ec.plot(ss,np.arange(1,len(ss)+1)/len(ss),color=COLORS[origin],label=origin)
        stat=stats[(stats.feature==c)&stats['style'].eq(style)].iloc[0];ax.set(xticks=[0,1],xticklabels=['Human','LD'],title=f'{c}\n{title(style)}');ec.set(title=f'ECDF; KS D={stat.ks_D:.3f}',xlabel='Raw measurement',ylabel='Cumulative fraction');ec.legend()
    finish(fig,'fig06_feature_ecdfs_and_rainclouds.png','The six measurements were selected by absolute coefficients of the frozen development-trained handcrafted probe, without test ranking. Each violin, jitter cloud and ECDF shows one supported historical style (300 artworks per origin); Cubism is absent from this release. KS D is descriptive. Values use raw measurement units; statistical-table distances use development scaling.')

def fig07():
    fig=plt.figure(figsize=(19,11));gs=fig.add_gridspec(2,6);roc=fig.add_subplot(gs[0,:2]);pr=fig.add_subplot(gs[0,2:4]);scatter=fig.add_subplot(gs[0,4:]);aa=fig.add_subplot(gs[1,:3]);ff=fig.add_subplot(gs[1,3:]);ci=csv('baseline_per_style_ci.csv');styles=sorted(ci['style'].unique())
    for j,(name,label,color) in enumerate(zip(NAMES,LABELS,MODEL_COLORS)):
        r=csv(f'roc_{name}.csv');p=csv(f'pr_{name}.csv');m=metric(name);roc.plot(r.fpr,r.tpr,color=color,label=f"{label} {m['roc_auc']:.4f}");pr.plot(p.recall,p.precision,color=color,label=label)
        g=ci[ci.model.eq(name)].set_index('style').loc[styles];xx=np.arange(10)+(j-2)*.15
        for ax,measure,lo,hi in [(aa,'roc_auc','auc_low','auc_high'),(ff,'f1','f1_low','f1_high')]:
            low=np.maximum(0,g[measure]-g[lo]);high=np.maximum(0,g[hi]-g[measure]);ax.bar(xx,g[measure],width=.14,color=color,label=label,yerr=np.vstack([low,high]),error_kw=dict(elinewidth=.6,capsize=1))
    roc.plot([0,1],[0,1],'k:',alpha=.4);roc.set(title='A1  Held-out ROC',xlabel='False positive rate',ylabel='True positive rate');pr.set(title='A2  Held-out precision–recall',xlabel='Recall',ylabel='Precision');roc.legend(fontsize=7);pr.legend(fontsize=7)
    s=csv('origin_silhouette_ari.csv');s=s[s.space.eq('full')];scatter.scatter(s.silhouette,s.ari,c='#0072B2',s=35)
    offsets={'baroque':(8,13),'renaissance':(-48,12),'surrealism':(-35,18),'post_impressionism':(-20,-16),'impressionism':(5,4)}
    for r in s.itertuples():scatter.annotate(title(r.style),xy=(r.silhouette,r.ari),xytext=offsets.get(r.style,(3,3)),textcoords='offset points',fontsize=7,arrowprops=dict(arrowstyle='-',lw=.4,color='gray') if r.style in offsets else None)
    scatter.axhline(0,color='gray',ls=':',lw=.6);scatter.axvline(0,color='gray',ls=':',lw=.6);scatter.set(title='C  Full-space origin labels vs. k-means',xlabel='Origin silhouette',ylabel='Unsupervised k=2 ARI')
    for ax,head in [(aa,'B1  Per-style AUROC'),(ff,'B2  Per-style F1')]:ax.set(xticks=range(10),xticklabels=[title(s) for s in styles],ylim=(.45,1.025),title=head);ax.tick_params(axis='x',rotation=40)
    aa.legend(ncol=5,fontsize=7,loc='upper center',bbox_to_anchor=(.5,-.28))
    finish(fig,'fig07_baseline_probes_and_ari.png','All five probes share the same 6,000 Human/LD test IDs; regularization and thresholds were fixed on development/validation. Whiskers: 1,000 within-origin source-group bootstrap 95% intervals conditional on frozen fits. ARI uses unlabeled NumPy Lloyd k-means (20 seeded starts); clustering is fitted separately within each style and compared with labels afterward.')

def fig08():
    d=csv('ablation_results.csv');fam=d[d.kind.eq('family')];fig=plt.figure(figsize=(18,10));gs=fig.add_gridspec(2,3);a=fig.add_subplot(gs[:,0]);s=fig.add_subplot(gs[:,1]);c=fig.add_subplot(gs[0,2]);g=fig.add_subplot(gs[1,2]);yy=np.arange(len(fam))
    for ax,col,label in [(a,'auc','Δ AUROC'),(s,'silhouette','Δ origin silhouette')]:
        vals=fam['delta_'+col].to_numpy();lo=fam['delta_'+col+'_low'].to_numpy();hi=fam['delta_'+col+'_high'].to_numpy();ax.hlines(yy,lo,hi,color='#0072B2',lw=2);ax.plot(vals,yy,'o',color='#D55E00');ax.axvline(0,color='gray',ls='--');ax.set(yticks=yy,yticklabels=fam.label if col=='auc' else ['']*len(fam),xlabel=label,title='A  Paired family ablations' if col=='auc' else 'Same held-out artwork pairs');ax.invert_yaxis()
    col=csv('color_saturation_ablation.csv')
    for model,color in zip(['HSV','Lab','HSV+Lab'],MODEL_COLORS):
        v=col[col.model.eq(model)].set_index('tertile').loc[['low','medium','high']];c.plot(range(3),v.roc_auc,'o-',color=color,label=model);c.vlines(range(3),v.auc_low,v.auc_high,color=color)
    c.set(xticks=range(3),xticklabels=['Low','Medium','High'],ylabel='AUROC',title='B  Development-defined saturation strata');c.legend()
    geom=d[d.kind.eq('geometry')];base=metric('handcrafted');g.bar(['4 quadrants']+geom.label.tolist(),[base['roc_auc']]+geom.roc_auc.tolist(),color=['#0072B2','#E69F00','#009E73']);g.set(ylim=(.95,1),ylabel='AUROC',title='C  Crop context sensitivity');g.tick_params(axis='x',rotation=12)
    for i,val in enumerate([base['roc_auc']]+geom.roc_auc.tolist()):g.text(i,val+.001,f'{val:.4f}',ha='center',fontsize=9)
    finish(fig,'fig08_ablation_forest_plot.png','Changes are variant minus all-family four-quadrant baseline. Horizontal intervals: 1,000 paired source-group bootstrap draws; silhouette intervals condition on cached per-artwork scores in each fixed geometry. Saturation boundaries use development data only. Full-canvas vectors have no across-crop IQR features; five-crop includes center overlap. See ablation_results.csv for F1, ties and complete paired intervals.')

def fig09():
    d=csv('perturbation_results.csv').set_index('view');base=metric('handcrafted');sil=csv('origin_silhouette_ari.csv');baseline_sil=sil[sil.space.eq('full')].silhouette.mean();fig,axes=plt.subplots(1,2,figsize=(15,6));views=['original','jpeg95','jpeg75','jpeg50','resize0.75','resize0.5'];labels=['Original','JPEG 95','JPEG 75','JPEG 50','Resize .75','Resize .50'];auc=[base['roc_auc']]+d.loc[views[1:],'roc_auc'].tolist();sv=[baseline_sil]+d.loc[views[1:],'silhouette'].tolist()
    intervals=csv('perturbation_auc_intervals.csv').set_index('view').loc[views]
    axes[0].plot(range(6),auc,'o-',color='#0072B2',label='Frozen probe AUROC');axes[0].vlines(range(6),intervals.auc_ci_low,intervals.auc_ci_high,color='#0072B2');axes[0].set(ylabel='AUROC',ylim=(.5,1.03),title='A  Frozen-model robustness');twin=axes[0].twinx();twin.plot(range(6),np.array(sv)/baseline_sil,'s--',color='#D55E00',label='Silhouette / original');twin.set_ylabel('Full-space origin silhouette retention',color='#D55E00');axes[0].legend(loc='lower left');twin.legend(loc='upper right')
    axes[1].bar(range(6),[1]+d.loc[views[1:],'style_w1_rank_rho'].tolist(),color=['#999999']+['#009E73']*5);axes[1].set(ylim=(-.05,1.1),ylabel='Spearman ρ vs. original style ranking',title='B  Stability of mean-feature W₁ ranks')
    for ax in axes:ax.set_xticks(range(6),labels,rotation=25)
    finish(fig,'fig09_perturbation_robustness.png','Both origins undergo identical held-out transformations; original JPEG is the Q=100 reference, not a Q100 re-encode. AUROC whiskers: 1,000 source-group bootstrap 95% intervals, fixed probe and thresholds. Silhouette uses transformed features and frozen scaling. W₁ ranking averages all 104 prespecified standardized measurements within style; ρ spans ten styles. Resize/JPEG are separate interventions, not a continuous severity scale.')

def fig10():
    d=csv('error_gallery_cases.csv');fig,axes=plt.subplots(len(d),5,figsize=(20,22),gridspec_kw={'width_ratios':[1.25,1.5,1.3,1.3,1.3]})
    for row,(r,axs) in enumerate(zip(d.itertuples(),axes)):
        im=np.array(Image.open(OUT/'gallery'/f'{r.artwork_id}.png'));axs[0].imshow(im);axs[0].axhline(127.5,color='white',lw=.7);axs[0].axvline(127.5,color='white',lw=.7);axs[0].set_title(f'{r.selection_reason}: {r.origin} | {title(r.style)}\np(AI)={r.prob_ai:.3f}; ID {str(r.artwork_id)[:10]}',fontsize=8);axs[0].axis('off')
        axs[1].imshow(Image.open(OUT/'gallery'/f'{r.artwork_id}_crops.png'));axs[1].axis('off');axs[1].set_title('Actual TL · TR · BL · BR crops',fontsize=8)
        vals=[getattr(r,f'fft_{i:02d}_median') for i in range(16)];axs[2].plot((np.arange(16)+.5)/32,vals,color=COLORS[r.origin]);axs[2].set(yscale='log',xlabel='cycles/pixel',ylabel='FFT power share');axs[2].set_title(f'β={r.fft_beta_median:.2f}',fontsize=8)
        names=['LH1','HL1','HH1','LH2','HL2','HH2'];axs[3].bar(range(6),[getattr(r,f'dwt_{n}_median') for n in names],color=COLORS[r.origin]);axs[3].set(yscale='log',xticks=range(6),xticklabels=names,ylabel='Haar energy share');axs[3].tick_params(axis='x',labelsize=7,rotation=30)
        labels=['Saturation','Value','Edge fraction','Hue resultant'];values=[r.s_median_median,r.v_median_median,r.edge_density_median,r.hue_resultant_median]
        axs[4].barh(range(4),values,color=COLORS[r.origin]);axs[4].set(xlim=(0,1),ylim=(-.6,3.6),yticks=range(4),yticklabels=labels,title=f'H={r.H_pooled:.3f}; C={r.C_pooled:.3f}');axs[4].tick_params(axis='y',labelsize=7)
        for k,value in enumerate(values):
            if not np.isfinite(value):axs[4].text(.04,k,'undefined: no valid hue',fontsize=7,va='center')
    finish(fig,'fig10_forensic_error_gallery.png','Eight actual held-out cases from the handcrafted probe, selected for inspection rather than prevalence estimation. FP/FN/TP denote prediction against release-origin labels; two extreme H–C/PCA cases supplement errors. Each row includes the original with quadrant boundaries, actual quadrant pixels, cached FFT/Haar profiles and color/edge summaries. Full IDs, selection reasons and predictions are in error_gallery_cases.csv.')

def main():
    # CSV rendering inputs allow independent regeneration without re-fitting any transform.
    pc=pd.read_parquet(OUT/'pca_coordinates.parquet');pc[pc.split.eq('test')].to_csv(OUT/'pca_plot_points.csv',index=False)
    pd.read_parquet(OUT/'tsne/p30_s42.parquet').to_csv(OUT/'tsne_plot_points.csv',index=False)
    pc[pc.split.eq('test')][['artwork_id','style','origin','H_pooled','C_pooled']].to_csv(OUT/'hc_plot_points.csv',index=False)
    for draw in [fig01,fig02,fig03,fig04,fig05,fig06,fig07,fig08,fig09,fig10]:draw()
    pd.DataFrame(FIGS).to_csv(OUT/'figure_manifest.csv',index=False)
    (OUT/'FIGURE_CAPTIONS.md').write_text('\n\n'.join(f"**{r['file']}**\n\n{r['caption']}" for r in FIGS),encoding='utf-8')
if __name__=='__main__':main()
