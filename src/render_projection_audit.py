"""Render cached projection coordinates and audit scores, without refitting."""
from common import *
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def main():
    coords=pd.read_parquet(OUT/'pca_coordinates.parquet');coords=coords[coords.split.eq('test')]
    chosen=pd.read_parquet(OUT/'tsne/p30_s42.parquet')
    scores=pd.read_csv(OUT/'projection_fidelity.csv');pc=pd.read_csv(OUT/'pca_projection_fidelity.csv').query('dimensions==2').iloc[0]
    ts=scores[(scores.perplexity==30)&(scores.seed==42)].iloc[0]
    summary=json.loads((OUT/'pca_summary.json').read_text());ev=summary['explained_variance_ratio']
    gate=json.loads((OUT/'control_gate.json').read_text())
    qnote='JPEG quantization confounded' if gate.get('jpeg_encoding_control_passed') is False else 'JPEG format matched'
    fig,axes=plt.subplots(1,3,figsize=(15,4.7),constrained_layout=True)
    colors={'Human':'#0072B2','LD':'#D55E00'}
    for origin,color in colors.items():
        sub=coords[coords.origin.eq(origin)];axes[0].scatter(sub.PC1,sub.PC2,s=3,alpha=.25,color=color,label=origin)
        sub=chosen[chosen.origin.eq(origin)];axes[1].scatter(sub.TSNE1,sub.TSNE2,s=3,alpha=.3,color=color,label=origin)
    axes[0].set(title=f'Fixed PCA; test n={len(coords):,}',xlabel=f'PC1 ({ev[0]:.2%} development variance)',ylabel=f'PC2 ({ev[1]:.2%})')
    axes[1].set(title=f'Exploratory t-SNE; n={len(chosen):,}\np=30; seed=42; random initialization',xlabel='t-SNE 1',ylabel='t-SNE 2')
    for ax,row in zip(axes[:2],[pc,ts]):
        ax.text(.03,.97,f'Neighborhood audit: n=3,000; k=15\nT={row.trustworthiness:.4f}; C={row.continuity:.4f}',transform=ax.transAxes,va='top',fontsize=8,bbox=dict(boxstyle='round',facecolor='#fff3cd',alpha=.9,edgecolor='#b49c50'))
        ax.legend(loc='lower left',fontsize=8)
    for name in ['trustworthiness','continuity']:
        g=scores.groupby('perplexity')[name];axes[2].errorbar([15,30,50],g.mean(),yerr=g.std(),marker='o',label=name)
    axes[2].set(title='t-SNE fidelity: five seeds\nMean ± SD; no distance inference in t-SNE',xlabel='Perplexity',ylabel='Neighborhood fidelity at k=15');axes[2].legend(fontsize=8)
    fig.suptitle(f'Native-256 Human–LD: {qnote}; subjects unverified; descriptive',fontsize=11)
    fig.savefig(OUT/'pca_tsne_audit.png',dpi=300);plt.close(fig)
    fig=plt.figure(figsize=(8,6));ax=fig.add_subplot(111,projection='3d')
    for origin,color in colors.items():
        sub=coords[coords.origin.eq(origin)];ax.scatter(sub.PC1,sub.PC2,sub.PC3,s=3,alpha=.25,color=color,label=origin)
    ax.set(xlabel=f'PC1 ({ev[0]:.1%})',ylabel=f'PC2 ({ev[1]:.1%})',zlabel=f'PC3 ({ev[2]:.1%})',title=f'Fixed development-fitted PCA; test n={len(coords):,}\n{qnote}; subjects unverified; descriptive')
    ax.legend();fig.tight_layout();fig.savefig(OUT/'pca_3d.png',dpi=300);plt.close(fig)
    print('Rendered cached projection audit with fidelity badges',flush=True)
if __name__=='__main__':main()
