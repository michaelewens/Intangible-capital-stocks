"""Figure 1: pooled upper-tail winsorized investment / lagged assets."""
from sample import lag, ratio, winsor
from common import plt, save, cli


def compute(sample):
    d=sample.sort_values(['gvkey','fyear']).copy()
    for c in ['at','xrd','xsga','capx']:
        if 'fig01_'+c in d: d[c]=d['fig01_'+c]
    last=lag(d,'at')
    for src,dest,denom in [('xrd','rdAssets',last),('capx','capxAssets',last),('xsga','sgaAssets',d['at'])]:
        d[dest]=ratio(d[src],denom)
        d.loc[d[src].isna()&last.notna(),dest]=0
        d[dest]=winsor(d[dest],.01,highonly=True)
    return d[d.fyear>=1977].groupby('fyear')[['rdAssets','capxAssets','sgaAssets']].mean().reset_index()


def plot(df,out_svg):
    fig,ax=plt.subplots()
    ax.plot(df.fyear,df.rdAssets,'o-',label='R&D/Assets')
    ax.plot(df.fyear,df.capxAssets,'o--',label='CAPEX/Assets')
    ax.set(xlabel='Year',ylabel='Investment / lagged assets')
    ax.legend()
    save(fig,out_svg)

if __name__=='__main__': cli('01',compute,plot)
