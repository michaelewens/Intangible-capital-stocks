"""Figure 7: lagged total intangibles / lagged total capital."""
import pandas as pd
from sample import sic_keep
from common import plt, save, cli
LABELS={1:'Consumer',2:'Manufacturing',3:'High-tech',4:'Healthcare',6:'All'}


def compute(sample):
    keep=sample.stock_sample.eq(True) if 'stock_sample' in sample else sic_keep(sample.sic)
    d=sample[keep&(sample.fyear>=1977)]
    industry=d.groupby(['fyear','industry5']).intensity2.mean().reset_index()
    # All includes Other, although the Stata chart does not draw Other separately.
    all_=d.groupby('fyear').intensity2.mean().reset_index().assign(industry5=6)
    return pd.concat([industry[industry.industry5.isin([1,2,3,4])],all_]).sort_values(['industry5','fyear']).reset_index(drop=True)


def plot(df,out_svg):
    fig,ax=plt.subplots()
    for i,d in df.groupby('industry5'):
        ax.plot(d.fyear,d.intensity2,'--' if i==6 else '-',label=LABELS[i])
    ax.set(xlabel='Fiscal year',ylabel='Intangible assets / Capital stock')
    ax.legend()
    save(fig,out_svg)

if __name__=='__main__': cli('07',compute,plot)
