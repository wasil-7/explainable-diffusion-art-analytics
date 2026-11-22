"""Render the cached density view only; never refit or select analysis parameters."""
from common import *
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

def main():
    density=pd.read_csv(OUT/'hc_density_grid.csv')
    coords=pd.read_parquet(OUT/'pca_coordinates.parquet');test=coords[coords.split.eq('test')]
    xlim=(max(0,test.H_pooled.min()-.02),min(1,test.H_pooled.max()+.02))
    ylim=(max(0,test.C_pooled.min()-.01),test.C_pooled.max()+.01)
    maximum=int(density.total.max());area_scale=120/maximum
    gate=json.loads((OUT/'control_gate.json').read_text())
    qnote='JPEG quantization confounded' if gate.get('jpeg_encoding_control_passed') is False else 'JPEG format matched'
    fig,axes=plt.subplots(2,5,figsize=(17,7),constrained_layout=True)
    for ax,style in zip(axes.ravel(),sorted(density['style'].unique())):
        sub=density[density['style'].eq(style)]
        ax.scatter(sub.H_left+sub.H_width/2,sub.C_bottom+sub.C_height/2,c=sub.ai_fraction,cmap='coolwarm',vmin=0,vmax=1,s=area_scale*sub.total,marker='s',linewidths=0)
        ax.set(title=f'{style}\nn={int(sub.total.sum())}',xlabel='H',ylabel='C',xlim=xlim,ylim=ylim)
        ax.tick_params(labelsize=8)
    examples=sorted(set([max(1,maximum//10),max(1,maximum//2),maximum]))
    handles=[axes[0,0].scatter([],[],s=area_scale*n,marker='s',c='gray',linewidths=0,label=f'n={n}') for n in examples]
    axes[0,0].legend(handles=handles,title='Artworks / bin',loc='lower left',fontsize=7,title_fontsize=7)
    bar=fig.colorbar(plt.cm.ScalarMappable(norm=Normalize(0,1),cmap='coolwarm'),ax=axes,shrink=.85,pad=.01,fraction=.02)
    bar.set_label('LD fraction in bin (0 = Human, 1 = LD)',fontsize=9)
    fig.suptitle(f'Density-aware native-256 Human–LD view: {qnote}; subjects unverified\nSquare area is proportional to count; color is class proportion. All contrasts descriptive.',fontsize=12)
    fig.savefig(OUT/'hc_density_atlas.png',dpi=300);plt.close(fig)
    print('Rendered density view from frozen cached bins',flush=True)
if __name__=='__main__':main()
