"""Render frozen H,C coordinates and centroid uncertainty; no refitting."""
from common import *
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
def main():
    coords=pd.read_parquet(OUT/'pca_coordinates.parquet');coords=coords[coords.split.eq('test')]
    bounds=pd.read_csv(OUT/'hc_theoretical_bounds.csv',float_precision='round_trip')
    ellipses=pd.read_csv(OUT/'hc_centroid_ellipses.csv',float_precision='round_trip')
    gate=json.loads((OUT/'control_gate.json').read_text())
    qnote='JPEG quantization confounded' if gate.get('jpeg_encoding_control_passed') is False else 'JPEG format matched'
    xlim=(max(0,coords.H_pooled.min()-.02),min(1,coords.H_pooled.max()+.02))
    ylim=(max(0,coords.C_pooled.min()-.01),coords.C_pooled.max()+.01)
    colors={'Human':'#0072B2','LD':'#D55E00'}
    fig,axes=plt.subplots(2,5,figsize=(17,7),constrained_layout=True)
    for ax,style in zip(axes.ravel(),sorted(coords['style'].unique())):
        sub=coords[coords['style'].eq(style)]
        for curve in ['lower','upper']:
            b=bounds[bounds.curve.eq(curve)].sort_values('H');ax.plot(b.H,b.C,color='gray',alpha=.25,lw=.6)
        centers={}
        for origin,color in colors.items():
            g=sub[sub.origin.eq(origin)];ax.scatter(g.H_pooled,g.C_pooled,s=4,alpha=.2,color=color,label=origin)
            e=ellipses[ellipses['style'].eq(style)&ellipses.origin.eq(origin)].iloc[0]
            centers[origin]=(e.H,e.C);ax.scatter(e.H,e.C,s=24,color=color)
            ax.add_patch(Ellipse((e.H,e.C),e.width,e.height,angle=e.angle,fill=False,color=color))
        ax.annotate('',xy=centers['LD'],xytext=centers['Human'],arrowprops=dict(arrowstyle='->',color='black'))
        ax.set(title=f'{style}\nn=300/origin; descriptive',xlabel='H',ylabel='C',xlim=xlim,ylim=ylim)
        ax.tick_params(labelsize=8)
    axes[0,0].legend(loc='lower left',fontsize=7)
    fig.suptitle(f'Native-256 H–C atlas: {qnote}; subject matching unavailable\nGray: theoretical bounds. Ellipses: grouped-bootstrap centroid 95% regions. All contrasts descriptive.',fontsize=12)
    fig.savefig(OUT/'hc_atlas.png',dpi=300);plt.close(fig)
if __name__=='__main__':main()
