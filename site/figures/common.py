"""Small shared CLI and plotting helpers."""
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(__file__).resolve().parents[2]/'data/figures_work/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(Path(__file__).resolve().parents[2]/'data/figures_work/cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sample import ROOT, WORK


def fit(ax, df, col):
    d=df[['fyear',col]].dropna()
    if len(d)>1:
        ax.plot(d.fyear,np.polyval(np.polyfit(d.fyear,d[col],1),d.fyear),':',linewidth=1)


def save(fig,out_svg):
    out_svg=Path(out_svg)
    out_svg.parent.mkdir(parents=True,exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_svg)
    plt.close(fig)


def cli(number,compute,plot):
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--sample',type=Path,default=WORK/'sample.csv')
    ap.add_argument('--out-csv',type=Path,default=ROOT/f'site/data/fig{number}.csv')
    ap.add_argument('--out-svg',type=Path,default=ROOT/f'site/figures/out/fig{number}.svg')
    a=ap.parse_args()
    df=compute(pd.read_csv(a.sample,low_memory=False))
    a.out_csv.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(a.out_csv,index=False)
    plot(df,a.out_svg)
    print(f'Figure {number}: {len(df)} rows, {df.fyear.min()}–{df.fyear.max()}')
