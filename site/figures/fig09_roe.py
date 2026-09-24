"""Figure 9: S&P membership-year ROE with sample lag and tax adjustment."""
from sample import market_view, lag, ratio, winsor
from common import plt, save, fit, cli


def compute(sample):
    d=market_view(sample) if 'market_sample' in sample else sample.copy()
    d=d[(d.fyear>=1977)&d.sp500.eq(1)].copy().sort_values(['gvkey','fyear'])
    d['ceq']=d.ceq.where(d.ceq>=0)
    d['equity_epw']=(d.ceq+d.G2+d.S2).where(lambda s:s>=0)
    # Stata drops missing BEA equity, even though BEA ROE is not drawn.
    # On current inputs G/S and G2/S2 have the same missing support: same flows,
    # nonnegative ages and strictly positive decay factors. Historical check in validator.
    if {'G','S'}.issubset(d):
        eq=d.ceq+d.G+d.S
        keep=eq.notna()&(eq>=0)
    else:
        keep=d.ceq.notna()&d.G2.notna()&d.S2.notna()
    d=d[keep].copy()
    d['equity']=d.ceq
    d['ni_adj_epw']=d.ni+(d.xrd+d.gamma*d.xsga-d.S2depr-d.G2depr)*(1-d.marginal_tax_after_int)
    d['roe_inc2']=winsor(ratio(d.ni,lag(d,'equity')),.01)
    d['roe_inc_epw2']=winsor(ratio(d.ni_adj_epw,lag(d,'equity_epw')),.01)
    # Mean paired difference is NOT the difference of the two marginal means.
    d['diffUnadj']=d.roe_inc2-d.roe_inc_epw2
    return d.groupby('fyear')[['roe_inc2','roe_inc_epw2','diffUnadj']].mean().reset_index()


def plot(df,out_svg):
    fig,ax=plt.subplots()
    ax.plot(df.fyear,df.roe_inc2,'o--',label='Unadjusted ROE')
    ax.plot(df.fyear,df.roe_inc_epw2,'o-',label='EPW ROE')
    ax.scatter(df.fyear,df.diffUnadj,label='Unadjusted − EPW')
    fit(ax,df,'diffUnadj')
    ax.set(xlabel='Year',ylabel='Net income / lagged equity')
    ax.legend()
    save(fig,out_svg)

if __name__=='__main__': cli('09',compute,plot)
