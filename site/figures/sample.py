"""Local-only shared inputs for the paper figures. Never publish sample.csv."""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
# Import without writing bytecode into the read-only pipeline directory.
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'pipeline'))
from epw_stocks import industry5, _backfill_by_growth
INPUTS = ROOT / 'data/inputs'
WORK = ROOT / 'data/figures_work'
PANEL = ROOT / 'data/output/panel_20260924.csv'
KEY = ['gvkey', 'fyear']


def ratio(a, b):
    return (a / b).replace([np.inf, -np.inf], np.nan)


def lag(d, col):
    """Stata L., unlike a row shift, requires the immediately preceding year."""
    g = d.groupby('gvkey', sort=False)
    return g[col].shift().where(d.fyear - g.fyear.shift() == 1)


def winsor(s, p, highonly=False):
    s = s.replace([np.inf, -np.inf], np.nan)
    return s.clip(lower=None if highonly else s.quantile(p), upper=s.quantile(1-p))


def sic_keep(s):
    return ~(s.between(6000, 6999) | s.between(4900, 4999) |
             s.between(1000, 1499) | (s >= 9000))


def deal_flags(inputs, final_deals=WORK/'author_deals.csv'):
    f = inputs / 'figures'
    if Path(final_deals).exists():
        t = pd.read_csv(final_deals)
        t['fyear'] = t.YearCompletedUnconditional
    else:
        raise FileNotFoundError(f'Missing exact final deal keys: {final_deals}. Run prepare_author_inputs.py; the supplied target/acquirer extracts precede final estimation selection.')
    t = t.rename(columns={'tgt_gvkey':'gvkey'}).drop_duplicates('gvkey', keep='first')
    links = pd.read_stata(f/'Philips_gvkey_link.dta', convert_categoricals=False)
    links['agvkey'] = pd.to_numeric(links.agvkey, errors='coerce')
    # Mirrors Stata: derive acquirers only AFTER retaining one deal per target.
    acq = t[['sdc_dealno','fyear']].merge(links[['sdc_dealno','agvkey']], on='sdc_dealno', how='left', validate='many_to_one')
    acq = acq.rename(columns={'agvkey':'gvkey'}).dropna(subset=['gvkey']).drop_duplicates(KEY)
    return t[KEY].dropna().assign(targetYear=True), acq[KEY].assign(acqYear=True)


def market_panel(inputs, funda_dates):
    m = pd.read_csv(inputs/'msf.csv', parse_dates=['mthcaldt'])
    m = m.sort_values(['permno','mthcaldt'])
    m['ym'] = m.mthcaldt.dt.year*12 + m.mthcaldt.dt.month
    m = m.drop_duplicates(['permno','ym'], keep='last')
    for src, dest in [('mthret','annualRet'), ('mthretx','annualRetX')]:
        r = pd.to_numeric(m[src], errors='coerce')
        prod = 1+r
        for i in range(1,12):
            prod = prod * (1+r.groupby(m.permno).shift(i))
        continuous = m.ym - m.groupby('permno').ym.shift(11) == 11
        m[dest] = (prod-1).where(continuous)
    m = m[m.mthprc.notna()].copy()
    # Mirrors Stata's price-times-shares formula; current mthcap is in $thousands.
    m['mktCap_crsp'] = m.mthprc.abs()*m.shrout/1000
    m['fyear'] = m.mthcaldt.dt.year
    m = m.drop_duplicates(['permno','fyear'], keep='last')
    sp = pd.read_stata(inputs/'figures/CRSPdsp500list.dta')
    end = 'end' if 'end' in sp else 'ending'
    sp['startyear'] = sp.start.dt.year
    sp['endyear'] = sp[end].dt.year
    sp['fyear'] = [list(range(int(a), int(b)+1)) for a,b in zip(sp.startyear,sp.endyear)]
    sp = sp.explode('fyear')
    # Mirrors the Stata bug: numbering is by permno, not membership spell.
    sp['fyear'] = sp.startyear + sp.groupby('permno', sort=False).cumcount()
    sp = sp[['permno','fyear']].drop_duplicates().assign(sp500=1)
    m = m.merge(sp, on=['permno','fyear'], how='left', validate='one_to_one')
    m['sp500'] = m.sp500.fillna(0)
    lk = pd.read_csv(inputs/'ccmlink.csv', parse_dates=['linkdt','linkenddt'])
    # Reconstruct the report-date-expanded link input from current link history.
    # Stata uses year(datadate), NOT fiscal year, to attach calendar CRSP data.
    lk = funda_dates[['gvkey','datadate']].drop_duplicates().merge(lk,on='gvkey',how='inner')
    lk = lk[(lk.datadate>=lk.linkdt)&(lk.linkenddt.isna()|(lk.datadate<=lk.linkenddt))].copy()
    lk = lk.rename(columns={'lpermno':'permno'})
    lk['fyear'] = lk.datadate.dt.year
    lk = lk.sort_values(['permno','fyear','datadate','linkdt']).drop_duplicates(['permno','fyear'],keep='last')
    m = m.merge(lk[['permno','fyear','gvkey']], on=['permno','fyear'], how='inner', validate='one_to_one')
    m = m[~m.duplicated(KEY, keep=False)].copy()
    fy = pd.read_csv(inputs/'ipo_year.csv').rename(columns={'ipo_year':'ipoyear'})
    m = m.merge(fy[['gvkey','foundingyear','ipoyear']],on='gvkey',how='left',validate='many_to_one')
    first = m.groupby('permno').fyear.transform('min')
    m['foundingyear'] = np.minimum(m.foundingyear.fillna(first-7), first)
    m['ipoyear'] = m.ipoyear.fillna(first)
    m['ager'] = m.fyear-m.foundingyear
    return m[KEY+['permno','mktCap_crsp','annualRet','annualRetX','sp500','foundingyear','ipoyear','ager']]


def prepare_market(d, inputs=INPUTS, final_deals=WORK/'author_deals.csv'):
    """Sample portion of createFigures8_9.do; keep all years until figure collapse."""
    d = d.loc[sic_keep(d.sic)].copy().sort_values(KEY).reset_index(drop=True)
    d['industry5'] = industry5(d.sic)
    t,a = deal_flags(inputs,final_deals)
    d = d.merge(t,on=KEY,how='left',validate='one_to_one').merge(a,on=KEY,how='left',validate='one_to_one')
    d['at'] = d['at'].fillna(0)
    d['rdip'] = d.rdip.fillna(0)
    incogs = (d.xrd+d.rdip>d.xsga)&(d.xrd+d.rdip<d.cogs)&d[['xrd','xsga','cogs']].notna().all(axis=1)
    strip = d.xrd.notna() & d.xsga.notna() & ~incogs
    d.loc[strip,'xsga'] = (d.xsga-d.xrd-d.rdip).clip(lower=0)
    with np.errstate(divide='ignore',invalid='ignore'):
        d['grow_rd'] = np.log(d.groupby('gvkey').xrd.shift(-1)/d.xrd).replace([np.inf,-np.inf],np.nan)
    d['m_grow_rd'] = d.groupby('agei',dropna=False).grow_rd.transform('mean')
    ages = d.agei.dropna()
    if len(ages):
        d = _backfill_by_growth(d,'xrd',range(int(ages.max()),-1,-1),'m_grow_rd')
        d['m_grow_rd'] = d.loc[d.agei.between(-2,-1)&d.xrd.notna(),'grow_rd'].mean()
        d = _backfill_by_growth(d,'xrd',range(-1,int(ages.min())-1,-1),'m_grow_rd')
        with np.errstate(divide='ignore',invalid='ignore'):
            growth = np.log(d.groupby('gvkey').xsga.shift(-1)/d.xsga).replace([np.inf,-np.inf],np.nan)
        d['m_grow_sga'] = growth[d.agei.between(-2,-1)&d.xsga.notna()].mean()
        d = _backfill_by_growth(d,'xsga',range(-1,int(ages.min())-1,-1),'m_grow_sga')
    # Mirrors Stata's hard-coded override, only in the market sample.
    d.loc[d.fyear==2018,'cpidef'] = 1.024354026777191*1.8762723
    for c in 'mkvalt lt at ppent intan act xrd xsga dcpstk ao ppegt sale cogs capx ni oancf ceq'.split():
        d[c] = d[c]/d.cpidef
    d['act'] = d.act.fillna(0)
    d['intan'] = d.intan.fillna(0)
    # Mirrors Stata's ineffective ppent replacement AFTER filling intan.
    d.loc[d.intan.isna(),'ppent'] = 0
    d['dcpstk'] = d.dcpstk.fillna(0)
    d['dontPick'] = (d.ppegt<5)|d.ppegt.isna()|(d.sale<=0)|d.sale.isna()|d['at'].isna()
    # dontPick is generated but NEVER used as a sample screen in these figures.
    markups = pd.read_stata(inputs/'figures/tangibleMB_ind.dta',convert_categoricals=False)
    d = d.merge(markups,on='industry5',how='inner',validate='many_to_one')
    d['marketValue'] = d.mkvalt+d['lt']+d.dcpstk
    d['mb'] = ratio(d.mkvalt,d['at'])
    d = d[~(d.targetYear.eq(True)|d.acqYear.eq(True))].copy()
    d['mb_win'] = winsor(d.mb,.025)  # Mirrors pooled Stata winsorization before year screen.
    return d


def stock_fields(panel):
    p = pd.read_csv(panel, usecols=['gvkey','fyear','G2','S2','knowDepr','gamma','sic','industry5','cpidef','intan','ppegt'])
    p = p.sort_values(KEY).reset_index(drop=True)
    g = p.groupby('gvkey',sort=False)
    gap = p.fyear-g.fyear.shift()
    # Mirrors Stata: delta**gap, NOT 1-(1-delta)**gap.
    p['G2depr'] = p.knowDepr**gap*g.G2.shift()
    p['S2depr'] = .2**gap*g.S2.shift()
    p.loc[g.cumcount()==0,['G2depr','S2depr']] = 0
    p['intan2'] = p.G2+p.S2
    p['intan_bs'] = p.intan.fillna(0).clip(lower=0)/p.cpidef
    p['ati2'] = p.ppegt/p.cpidef+p.intan2+p.intan_bs
    # intensity is constructed before ati2 is winsorized in the stock program.
    p['intensity2'] = ratio(lag(p,'intan2')+lag(p,'intan_bs'),lag(p,'ati2'))
    p['stock_sample'] = sic_keep(p.sic)
    return p[KEY+['G2','S2','G2depr','S2depr','gamma','intan2','ati2','intensity2','stock_sample']]


def build_sample(inputs=INPUTS, panel=PANEL, final_deals=WORK/'author_deals.csv'):
    inputs, panel = Path(inputs),Path(panel)
    d = pd.read_csv(inputs/'funda.csv',parse_dates=['datadate'])
    d = d.sort_values(KEY+['datadate']).drop_duplicates(KEY,keep='last')
    company = pd.read_csv(inputs/'company.csv').rename(columns={'SIC':'sic'})
    d = d.merge(company[['gvkey','sic']],on='gvkey',how='left',validate='many_to_one')
    d['sic'] = pd.to_numeric(d.sic,errors='coerce')
    d['industry5'] = industry5(d.sic)
    for c in ['xrd','xsga','dp']: d[c] = d[c].clip(lower=0)
    d['dpact'] = d.dpact.fillna(0)
    d = d.merge(market_panel(inputs,d),on=KEY,how='left',validate='one_to_one')
    for c in ['ipoyear','foundingyear']:
        d[c] = d[c].fillna(d.groupby('gvkey')[c].transform('max'))
    d['mkvalt'] = d.mkvalt.fillna(d.mktCap_crsp)
    d['agei'] = d.fyear-d.ipoyear
    cpi = pd.read_csv(inputs/'cpi.csv')
    d = d.merge(cpi,on='fyear',how='left',validate='many_to_one')
    cy = d[['fyear','cpidef']].drop_duplicates().sort_values('fyear')
    cy['cpirate'] = cy.cpidef/cy.cpidef.shift()-1
    d = d.merge(cy[['fyear','cpirate']],on='fyear',how='left',validate='many_to_one')
    tx = pd.read_csv(inputs/'figures/marginal_tax_rates.txt',sep=r'\s+',header=None,usecols=[1,2,3,5],na_values='.')
    tx.columns = ['fyear','marginal_tax_before_int','marginal_tax_after_int','gvkey']
    tx = tx[tx.gvkey!=-999]
    d = d.merge(tx,on=KEY,how='left',validate='one_to_one')
    d['marginal_tax_after_int'] = d.marginal_tax_after_int.fillna(pd.Series(np.where(d.fyear<2018,.35,.21),index=d.index))
    # Keep nominal Figure-1 values independent of later market sample transformations.
    for c in ['at','xrd','xsga','capx']: d['fig01_'+c] = d[c]
    stocks = stock_fields(panel)
    d = d.merge(stocks,on=KEY,how='left',validate='one_to_one')
    market = prepare_market(d,inputs,final_deals)
    market['market_sample'] = True
    cols = KEY+['market_sample','mb_win','targetYear','acqYear','dontPick','tangibleMB_win']
    real = 'mkvalt lt at ppent intan act xrd xsga dcpstk ao ppegt sale cogs capx ni oancf ceq cpidef'.split()
    market = market[cols+real].rename(columns={c:'market_'+c for c in real})
    # Excluded observations stay in the wide shared panel for Figures 1 and 7.
    d = d.merge(market,on=KEY,how='left',validate='one_to_one')
    for c in ['market_sample','stock_sample']: d[c] = d[c].eq(True)
    # Preserve deal flags on excluded rows too.
    t,a = deal_flags(inputs,final_deals)
    d = d.drop(columns=['targetYear','acqYear']).merge(t,on=KEY,how='left').merge(a,on=KEY,how='left')
    for c in ['targetYear','acqYear']: d[c] = d[c].eq(True)
    return d.sort_values(KEY).reset_index(drop=True)


def market_view(sample):
    d = sample.loc[sample.market_sample.eq(True)].copy()
    for c in [c for c in d if c.startswith('market_') and c!='market_sample']:
        d[c[7:]] = d[c]
    return d.sort_values(KEY)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inputs',type=Path,default=INPUTS)
    ap.add_argument('--panel',type=Path,default=PANEL)
    ap.add_argument('--final-deals',type=Path,default=WORK/'author_deals.csv')
    ap.add_argument('--out',type=Path,default=WORK/'sample.csv')
    a=ap.parse_args()
    d=build_sample(a.inputs,a.panel,a.final_deals)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    d.to_csv(a.out,index=False)
    summary={'rows':len(d),'first_year':int(d.fyear.min()),'latest_year':int(d.fyear.max()),'market_rows':int(d.market_sample.sum()),'stock_rows':int(d.stock_sample.sum()),'target_rows':int(d.targetYear.sum()),'acquirer_rows':int(d.acqYear.sum()),'sp500_last_year':int(d.loc[d.sp500.eq(1),'fyear'].max())}
    a.out.with_suffix('.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(summary)

if __name__=='__main__': main()
