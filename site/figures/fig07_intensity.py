"""Figure 7: lagged total intangibles / lagged total capital."""
import pandas as pd
from sample import sic_keep
from common import plt, save, cli
LABELS={1:'Consumer',2:'Manufacturing',3:'High-tech',4:'Healthcare',6:'All'}


def compute(sample):
    keep=sample.stock_sample.eq(True) if 'stock_sample' in sample else sic_keep(sample.sic)
    d=sample[keep].copy()
    # Companion series for the published CSV only: same ratio with NET PP&E (ppent) in place of the
    # paper's gross PP&E (ppegt). Lagged one fiscal year within firm, as the Stata does with L.
    d=d.sort_values(['gvkey','fyear'])
    bs=d.intan.fillna(0)/d.cpidef; ppent_r=d.ppent.fillna(0)/d.cpidef
    d['_net']=(d.intan2+bs)/(ppent_r+d.intan2+bs)
    prev_year=d.groupby('gvkey').fyear.shift(1)
    d['intensity_net']=d.groupby('gvkey')._net.shift(1).where(prev_year==d.fyear-1)
    d=d[d.fyear>=1977]
    industry=d.groupby(['fyear','industry5'])[['intensity2','intensity_net']].mean().reset_index()
    # All includes Other, although the Stata chart does not draw Other separately.
    all_=d.groupby('fyear')[['intensity2','intensity_net']].mean().reset_index().assign(industry5=6)
    out=pd.concat([industry[industry.industry5.isin([1,2,3,4])],all_]).sort_values(['industry5','fyear']).reset_index(drop=True)
    return out.rename(columns={'intensity2':'intensity_gross_ppe','intensity_net':'intensity_net_ppe'})


def plot(df,out_svg):
    fig,ax=plt.subplots()
    for i,d in df.groupby('industry5'):
        ax.plot(d.fyear,d.intensity_gross_ppe,'--' if i==6 else '-',label=LABELS[i])
    ax.set(xlabel='Fiscal year',ylabel='Intangible assets / Capital stock')
    ax.legend()
    save(fig,out_svg)

if __name__=='__main__': cli('07',compute,plot)
