"""Figure 8: market equity / assets, with and without EPW stocks."""
from sample import market_view, ratio, winsor
from common import plt, save, fit, cli


def compute(sample):
    d=market_view(sample) if 'market_sample' in sample else sample.copy()
    d=d[d.fyear>=1977].copy()
    # The unadjusted winsorization already occurred BEFORE the year screen.
    if 'mb_epw_win2' not in d:
        d['mb_epw_win2']=winsor(ratio(d.mkvalt,d.S2+d.G2+d['at']),.025)
    return d.groupby('fyear')[['mb_win','mb_epw_win2']].mean().rename(columns={'mb_epw_win2':'epw'}).reset_index()


def plot(df,out_svg):
    fig,ax=plt.subplots()
    ax.scatter(df.fyear,df.mb_win,label='Market equity / Assets')
    ax.scatter(df.fyear,df.epw,marker='D',label='Market equity / (Assets + EPW stocks)')
    for col in ['mb_win','epw']: fit(ax,df,col)
    ax.set(xlabel='Year',ylabel='Market-to-book')
    ax.legend()
    save(fig,out_svg)

if __name__=='__main__': cli('08',compute,plot)
