"""Portrait 300-DPI submission figures from unchanged cached measurements."""
from common import *
import publication_figures as pf
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image
import numpy as np, hashlib

DEST=ROOT/'phase3_output/submission_build';FIG=DEST/'figures'
FIG.mkdir(parents=True,exist_ok=True)
def finish(fig,name,caption):
    num=int(name[3:5]);axes=fig.axes
    shapes={1:(2,1,6.5),2:(5,2,7.6),3:(2,2,5),4:(2,1,6),6:(6,2,10),7:(4,2,9.5),8:(2,2,6.5),9:(2,1,6)}
    rows,cols,height=shapes[num];fig.set_size_inches(7.2,height)
    if fig._suptitle:fig._suptitle.remove()
    gs=GridSpec(rows,cols,figure=fig,left=.13,right=.96,bottom=.09,top=.96,hspace=.75 if num==6 else .65,wspace=.5)
    if num==3:slots=[gs[0,0],gs[0,1],gs[1,:]]
    elif num==7:slots=[gs[0,0],gs[0,1],gs[3,:],gs[1,:],gs[2,:]]
    elif num==9:slots=[gs[0,0],gs[1,0],gs[0,0]]
    else:slots=[gs[i//cols,i%cols] for i in range(len(axes))]
    for ax,slot in zip(axes,slots):
        ax.set_position(slot.get_position(fig));ax.tick_params(labelsize=8)
        ax.title.set_fontsize(9);ax.xaxis.label.set_size(8);ax.yaxis.label.set_size(8)
        for txt in ax.texts:txt.set_fontsize(min(txt.get_fontsize(),8))
        legend=ax.get_legend()
        if legend:
            for txt in legend.get_texts():txt.set_fontsize(7)
        if num==2:
            ax.set_xlabel('Entropy H');ax.set_ylabel('Complexity C');ax.tick_params(labelbottom=True,labelleft=True)
        if num==6:
            ax.set_title(ax.get_title().replace('_median','').replace('_',' '),fontsize=8)
    if num==3:
        axes[1].get_legend().remove()
        axes[1].text(.99,.02,'Style symbols: see dashboard',ha='right',transform=axes[1].transAxes,fontsize=7)
        axes[0].set_title('A  Fixed PCA',fontsize=9);axes[1].set_title('B  t-SNE p30, seed42',fontsize=9)
        for txt in axes[0].texts:
            if ': (' in txt.get_text():txt.set_text(txt.get_text().split(':')[0]);txt.set_fontsize(6)
    if num==7:
        axes[3].get_legend().remove()
        for ax in axes[3:]:ax.set_xticklabels([x.get_text().replace('Post Impressionism','Post-impr.').replace('Impressionism','Impr.').replace('Expressionism','Expr.').replace('Renaissance','Renaiss.') for x in ax.get_xticklabels()],rotation=25,ha='right')
        # Labels in the original scatter are too crowded at portrait width; keyed ranks preserve every value.
        for text in list(axes[2].texts):text.remove()
        axes[2].set_title('C  Within-style silhouette versus unlabeled k-means ARI',fontsize=9)
    if num==8:
        from matplotlib.ticker import MaxNLocator
        axes[0].set_yticklabels([x.get_text().replace('without','Drop').replace('only','Only').replace('Color/edges','Color') for x in axes[0].get_yticklabels()],fontsize=7)
        for ax in axes[:2]:ax.xaxis.set_major_locator(MaxNLocator(4))
        axes[0].set_title('A  Paired family AUROC changes',fontsize=9)
        axes[1].set_title('B  Paired silhouette changes',fontsize=9)
        axes[2].set_title('C  Saturation strata',fontsize=9)
        axes[3].set_title('D  Crop context',fontsize=9)
    fig.savefig(FIG/name,dpi=300,bbox_inches='tight',pad_inches=.08);plt.close(fig)
    return caption

def architecture():
    fig,ax=plt.subplots(figsize=(7.2,4.6));ax.axis('off')
    entries=[('Full-release audit: 185,015 artworks',.91),('Source groups + duplicate links → frozen 60:20:20 IDs',.73),('Features + Step 5 gate\nSubjects/JPEG unmet → descriptive analysis',.55),('Descriptive atlas / drift  |  Frozen encoders + logistic probes',.31),('Paired ablations → linked dashboard → traceable report',.10)]
    for label,y in entries:ax.text(.5,y,label,ha='center',va='center',fontsize=10,bbox=dict(boxstyle='square,pad=.65',fc='#eef3f6',ec='#0072B2'),transform=ax.transAxes)
    for y in [.83,.65,.45,.21]:ax.annotate('',xy=(.5,y-.05),xytext=(.5,y+.025),arrowprops=dict(arrowstyle='->'),xycoords='axes fraction')
    fig.savefig(FIG/'fig00_implemented_architecture.png',dpi=300,bbox_inches='tight');plt.close(fig)

def heatmap():
    # Preserve the actual fig05 pixels. Remove its paragraph footer and stack the two original panels.
    src=ROOT/'figures/fig05_style_drift_heatmap.png';im=Image.open(src).convert('RGB');w,h=im.size
    panels=[im.crop((0,60,2100,1898)),im.crop((2050,60,w,1898))]
    canvas=Image.new('RGB',(2150,panels[0].height*2),'white')
    for i,p in enumerate(panels):
        canvas.paste(p,(0,i*p.height));p.save(FIG/f'fig05_style_drift_heatmap_{i+1}.png',dpi=(300,300),optimize=True)
    canvas.save(FIG/src.name,dpi=(300,300),optimize=True)
    (DEST/'heatmap_pixel_provenance.json').write_text(json.dumps({'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'crop_boxes':[[0,60,2100,1898],[2050,60,4200,1898]],'operation':'Original pixels; remove footer and stack original panels. Report embeds the two original-pixel panels consecutively under Figure7; no data changes.'},indent=2))

def gallery():
    d=pf.csv('error_gallery_cases.csv')
    for part in range(2):
        from matplotlib.ticker import LogLocator, NullFormatter
        fig=plt.figure(figsize=(7.2,9.3));outer=fig.add_gridspec(4,1,left=.12,right=.97,top=.94,bottom=.06,hspace=.7)
        for j,r in enumerate(d.iloc[part*4:part*4+4].itertuples()):
            gs=outer[j].subgridspec(2,3,height_ratios=[1.1,.8],hspace=.6,wspace=.65)
            im=fig.add_subplot(gs[0,0]);im.imshow(Image.open(OUT/'gallery'/f'{r.artwork_id}.png'));im.axhline(127.5,color='white',lw=.6);im.axvline(127.5,color='white',lw=.6);im.axis('off')
            crop=fig.add_subplot(gs[0,1:]);crop.imshow(Image.open(OUT/'gallery'/f'{r.artwork_id}_crops.png'));crop.axis('off');crop.set_title(f'{r.selection_reason} · {r.origin} · {r.style.replace("_"," ")}\np(AI)={r.prob_ai:.3f}; ID {r.artwork_id[:10]} · TL/TR/BL/BR',fontsize=7)
            a=fig.add_subplot(gs[1,0]);a.plot((np.arange(16)+.5)/32,[getattr(r,f'fft_{i:02d}_median') for i in range(16)],color=pf.COLORS[r.origin]);a.set(yscale='log',title=f'FFT β={r.fft_beta_median:.2f}',xlabel='cycles / pixel')
            b=fig.add_subplot(gs[1,1]);names=['LH1','HL1','HH1','LH2','HL2','HH2'];b.bar(range(6),[getattr(r,f'dwt_{n}_median') for n in names],color=pf.COLORS[r.origin]);b.set(yscale='log',xticks=range(6),xticklabels=names,title='Haar detail energy');b.tick_params(axis='x',rotation=30)
            for ax in [a,b]:ax.yaxis.set_major_locator(LogLocator(base=10,numticks=3));ax.yaxis.set_minor_formatter(NullFormatter())
            c=fig.add_subplot(gs[1,2]);vals=[r.s_median_median,r.v_median_median,r.edge_density_median,r.hue_resultant_median];c.bar(range(4),vals,color=pf.COLORS[r.origin]);c.set(ylim=(0,1),xlim=(-.5,3.5),xticks=range(4),xticklabels=['S','V','Edge','Hue R'],title=f'H={r.H_pooled:.3f}; C={r.C_pooled:.3f}')
            for k,v in enumerate(vals):
                if not np.isfinite(v):c.text(k,.1,'N/A',ha='center',fontsize=7)
            for ax in [a,b,c]:ax.tick_params(labelsize=7);ax.title.set_fontsize(8);ax.xaxis.label.set_fontsize(7)
        fig.savefig(FIG/f'fig10_forensic_error_gallery_{part+1}.png',dpi=300,bbox_inches='tight',pad_inches=.1);plt.close(fig)
    ims=[Image.open(FIG/f'fig10_forensic_error_gallery_{i}.png') for i in [1,2]];canvas=Image.new('RGB',(ims[0].width,ims[0].height*2),'white')
    for j,im in enumerate(ims):canvas.paste(im,(0,j*im.height))
    canvas.save(FIG/'fig10_forensic_error_gallery.png',dpi=(300,300),optimize=True)

def main():
    pf.finish=finish
    architecture()
    for draw in [pf.fig01,pf.fig02,pf.fig03,pf.fig04,pf.fig06,pf.fig07,pf.fig08,pf.fig09]:draw();print(draw.__name__,flush=True)
    heatmap();gallery()
    import shutil
    shutil.copy2(ROOT/'figures/fig11_dashboard_ui.png',FIG/'fig11_dashboard_ui.png')
    print('Portrait assets complete',flush=True)
if __name__=='__main__':main()
