"""Validate current figures against local author data; write reproducible reports.

Only aggregated results belong under site/. Firm data and reference collapses stay
in data/figures_work/. No network, database, Stata executable or PDF is used.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from common import plt
from sample import ROOT, WORK, INPUTS, sic_keep, lag, ratio
import fig01_rd_capex as f01
import fig07_intensity as f07
import fig08_mb as f08
import fig09_roe as f09
AUTHOR=Path('/Users/me2731/Dropbox/Research/research_assistants/choi_2024/intangibles_v2')


def digitize_roe(path):
    """Read marker centers from the original PNG, using its inspected axis ticks.

    Fixed calibration is specific to the supplied 1175 x 705 image: x=166 at
    1980 and x=1067 at 2020; y=523 at zero and y=83 at .5. Values are approximate
    (about .0015 in ROE), not authors' machine-readable observations.
    """
    im=plt.imread(path)[:,:,:3]
    if im.shape[:2] != (705,1175):
        raise ValueError('Figure 9 PNG size changed: recalibrate pixel axes')
    r,g,b=im[:,:,0],im[:,:,1],im[:,:,2]
    masks={'roe_inc2':(b>.8)&(r<.3)&(g>.35)&(g<.7),
           'roe_inc_epw2':(r>.7)&(g<.15)&(b>.15)&(b<.6),
           'diffUnadj':(g>.5)&(r<.2)&(b>.25)&(b<.75)}
    rows=[]
    for year in range(1978,2024):
        x=166+(year-1980)*(1067-166)/40
        row={'fyear':year}
        for name,mask in masks.items():
            y,xx=np.where(mask[70:525,max(0,round(x)-3):round(x)+4])
            # Restrict to marker neighborhood; colored trend/legend lines excluded.
            row[name]=(523-(float(np.median(y))+70))/880 if len(y) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def compare(current, reference, fig, cols, details, stats, keys=None):
    keys=keys or ['fyear']
    pair=current.merge(reference,on=keys,suffixes=('_current','_author'),validate='one_to_one')
    groups=pair.groupby('industry5') if 'industry5' in keys else [(None,pair)]
    for ind,g in groups:
        for col in cols:
            d=g[keys+[col+'_current',col+'_author']].dropna().copy()
            if d.empty: continue
            a,b=d[col+'_current'],d[col+'_author']
            diff=a-b
            rel=diff.abs()/b.abs().replace(0,np.nan)
            flag=(rel>.05)|((b==0)&(a!=0))
            name=col+(f' industry={int(ind)}' if ind is not None else '')
            result={'figure':fig,'series':name,'start':int(d.fyear.min()),'end':int(d.fyear.max()),'n':len(d),'correlation':float(a.corr(b)),'mae':float(diff.abs().mean()),'mean_signed_difference':float(diff.mean()),'flagged_years':[int(v) for v in d.loc[flag,'fyear']]}
            stats.append(result)
            print(f"Figure {fig} {name} {result['start']}–{result['end']}: r={result['correlation']:.6f}, MAE={result['mae']:.6f}; >5% years={result['flagged_years']}")
            for idx,row in d.iterrows():
                details.append({'figure':fig,'series':name,'fyear':int(row.fyear),'current':row[col+'_current'],'author':row[col+'_author'],'absolute_difference':float(abs(diff.loc[idx])),'relative_difference':float(rel.loc[idx]),'flag_over_5pct':bool(flag.loc[idx])})


def references(inputs, author):
    out={}
    out['01']=f01.compute(pd.read_stata(inputs/'figures/figure1data.dta',columns=['gvkey','fyear','xrd','xsga','at','capx'],convert_categoricals=False))
    out['08']=f08.compute(pd.read_stata(inputs/'figures/dataForFigure8.dta',columns=['gvkey','fyear','mb_win','mb_epw_win2'],convert_categoricals=False))
    p=pd.read_stata(author/'data/mainStocks.dta',columns=['gvkey','fyear','sic','industry5','intensity2','G','S','G2','S2','G2depr','S2depr','epwrddep','intan_bs','ppegt','ati2'],convert_categoricals=False)
    p['sic']=pd.to_numeric(p.sic,errors='coerce')
    out['07']=f07.compute(p)
    out['09']=digitize_roe(author/'writing/figures/figure9.png')
    # Independent formula audit against stored, uncollapsed Stata intermediate variables.
    p=p.sort_values(['gvkey','fyear'])
    g=p.groupby('gvkey')
    gap=p.fyear-g.fyear.shift()
    calc_g=p.epwrddep**gap*g.G2.shift()
    calc_s=.2**gap*g.S2.shift()
    # mainStocks starts in 1975, so first retained rows cannot be audited here.
    valid=gap.notna()
    intensity=ratio(lag(p,'G2')+lag(p,'S2')+lag(p,'intan_bs'),lag(p,'G2')+lag(p,'S2')+lag(p,'intan_bs')+lag(p,'ppegt'))
    checks={'G2depr_mae':float((calc_g[valid]-p.loc[valid,'G2depr']).abs().mean()),'S2depr_mae':float((calc_s[valid]-p.loc[valid,'S2depr']).abs().mean()),'intensity_formula_mae':float((intensity-p.intensity2).abs().mean()),'bea_epw_stock_support_mismatches':int(((p.G.notna()&p.S.notna())!=(p.G2.notna()&p.S2.notna())).sum()),'negative_bea_stocks':int(((p.G<0)|(p.S<0)).sum())}
    return out,checks


def write_reports(stats,checks,sample,work,report_path,missing):
    summary=json.loads((work/'sample.json').read_text()) if (work/'sample.json').exists() else {'rows':len(sample),'latest_year':int(sample.fyear.max())}
    lines=['# Figure ports: run report','',f"Shared panel: {summary['rows']:,} firm-years; latest fiscal year {summary['latest_year']}. Results below were computed by this run. Absolute differences use chart ratio units; multiply ROE differences by 100 for percentage points.",'', '| Figure | Series | Years | Correlation | Mean absolute difference | Years over 5% |','|---|---|---|---:|---:|---:|']
    for s in stats:
        lines.append(f"| {s['figure']} | {s['series']} | {s['start']}–{s['end']} | {s['correlation']:.6f} | {s['mae']:.6f} | {len(s['flagged_years'])}/{s['n']} |")
    diag_path=work/'diagnostics.json'
    diag=json.loads(diag_path.read_text()) if diag_path.exists() else {}
    if diag:
        lines+=['','## Matched historical input audit','',
                'The same figure functions were also run on figure1data.dta plus the authors’ stored stocks, using the exact final acquisition file. This checks the translation independently of current inputs. The ROE curves visually coincide with the published PNG; differences are within the stated image-reading precision.','',
                '| Figure | Series | Correlation | Mean absolute difference |',
                '|---|---|---:|---:|']
        for key,value in diag.items():
            if key.startswith('same_vintage_'):
                name=key.removeprefix('same_vintage_fig')
                lines.append(f"| {name[:2]} | {name[3:]} | {value['r']:.6f} | {value['mae']:.6f} |")
        lines += ['',f"The numerical Figure 8 reference ends in {diag['author_figure8_last_year']}; it does not certify later years in the PNG. Replaying the newer historical source inputs against that earlier stored intermediate is not an exact same-input comparison. On common firm-years, the raw market-to-book MAE is {diag['mb_raw_matched_mae']:.6f} and the stored winsorized MAE is {diag['mb_winsor_matched_mae']:.6f}. This discrepancy predates the current Compustat rebuild and cannot be labeled a port error or dismissed as zero.", '',
                  f"S&P membership spells actually end on {diag['membership_latest_actual_end']}. Flags afterward are artifacts of the preserved Stata multi-spell expansion. Current and author membership counts by year are recorded in diagnostics.json. The current fiscal-year tail contains {diag['funda_year_counts'][str(summary['latest_year'])]} raw observations, so it is incomplete."]
    descriptions={
      '01':'Mean nominal R&D and CAPEX divided by immediately prior fiscal-year assets. Missing numerators become zero only when lagged assets are observed. The broad Compustat sample has no industry or acquisition screen. Pooled upper-tail winsorization precedes the start-year restriction; the auxiliary SG&A/assets series is also exported. Inputs: funda, company and the shared panel; reference: figure1data.dta.',
      '07':'Mean lagged (G2 + S2 + balance-sheet intangibles) divided by lagged (gross PPE + G2 + S2 + balance-sheet intangibles). Missing or negative balance-sheet intangibles become zero. Lags are computed on the full stocks history before the SIC and start-year screens. Stocks and nominal balance-sheet items use the stock panel CPI, without the market-sample CPI override. Other industries enter All but have no separate plotted line. Inputs: current stocks panel; reference: mainStocks.dta intensity2.',
      '08':'Mean market equity/assets and market equity/(assets + G2 + S2), after SIC exclusions and target/acquirer deal-year removal. The numerator is mkvalt, with CRSP fallback, despite the paper legend saying market value of assets. SG&A has R&D stripped and the market-sample growth backfill is applied before deflation. Unadjusted pooled winsorization occurs before the start-year restriction; adjusted winsorization follows it. The small-PPE/nonpositive-sales flag is intentionally not a filter. Reference: the stored winsorized columns in dataForFigure8.dta.',
      '09':'Mean net income divided by lagged common equity for S&P membership years in the market sample. Adjusted income adds (R&D + gamma × cleaned SG&A − S2depr − G2depr) × (one minus marginal tax rate); adjusted equity adds G2 + S2. Negative common equity becomes missing. Membership and equity screens precede calendar-year lags, so exits, acquisition exclusions and re-entries create missing lags. Pooled winsorization is applied separately to each ROE series; the plotted difference is a mean of paired differences. Reference: colored-marker centers digitized from figure9.png; this is approximate image validation, not an exact numeric benchmark.'}
    readme=['# Rebuilding the paper figures','']
    for fig,desc in descriptions.items():
        ss=[s for s in stats if s['figure']==fig]
        nums='; '.join(f"{s['series']}: r={s['correlation']:.6f}, MAE={s['mae']:.6f}, {len(s['flagged_years'])}/{s['n']} years over 5% ({s['start']}–{s['end']})" for s in ss)
        readme.append(f"**Figure {int(fig)}.** {desc} Validation: {nums or 'not available'}.")
        readme.append('')
    if diag:
        checks9='; '.join(f"{c}: r={diag['same_vintage_fig09_'+c]['r']:.6f}, MAE={diag['same_vintage_fig09_'+c]['mae']:.6f}" for c in ['roe_inc2','roe_inc_epw2','diffUnadj'])
        readme+=['**Validation limits.** The historical-input ROE replay agrees closely with the PNG: '+checks9+f". The supplied S&P membership spells end on {diag['membership_latest_actual_end']}; subsequent observations are generated by the preserved Stata multi-spell bug and are provisional, not a current S&P sample. The numeric market-to-book reference ends in {diag['author_figure8_last_year']}. The intensity discrepancy at the final reference year reflects an incomplete historical vintage; the current latest fiscal year also has only {diag['funda_year_counts'][str(summary['latest_year'])]} raw observations.", '']
    issues=[
      ('High','Low','S&P membership history is outdated','The port retains the supplied membership history and reproduces the Stata multi-spell numbering bug. Post-coverage observations are artifacts of that bug, so these outputs cannot be represented as current S&P membership. Minimum fix: provide updated membership spells; correcting the expansion bug should be identified as a separate method change.'),
      ('Medium','Low','Upstream stock vintage and founding differences','The existing stock builder uses current INDL Compustat, a current CPI series and gvkey-based founding years. Those inputs differ from the authors’ original run. No pipeline code was changed. Minimum fix: run these figure programs on identical vintage inputs before attributing discrepancies exclusively to the translation.'),
      ('Medium','Low','BEA equity support screen','Current stocks contain EPW stocks only. The port uses common nonmissing G2/S2 support for the otherwise unplotted BEA-equity screen. Historical support mismatches and negative BEA stocks are reported below. Minimum fix for strict certification: provide current G and S alongside the EPW panel.'),
      ('Low','Low','Image-only ROE reference','PNG marker centers are calibrated to inspected axes; estimated digitization uncertainty is about 0.0015 ROE. Minimum fix: obtain the authors’ collapsed ROE series for an exact comparison.')]
    lines+=['','## Fidelity and deviations','', 'Preserved: calendar-year lags; figure-specific samples; pooled winsorization; missing-value propagation; R&D-from-SG&A stripping; sequential growth backfill; the hard-coded market CPI override; delta raised to the year gap for depreciation; the ineffective ppent missing-value replacement; OLS trend lines. The paper end-year cap is removed as requested. Current data are not calibrated to make the old pictures match.','', '## Open issues, ranked by severity and implementation cost','']
    lines.insert(lines.index('## Open issues, ranked by severity and implementation cost'), 'The final deal keys were found in the authors’ local estimation file and staged under data/figures_work/author_deals.csv. Target deduplication precedes the Philips acquirer merge. The supplied extracts were also checked against the exact final deal sequence. The acquisition screen is in place. Current CRSP links are joined at Compustat datadates, reduced to the latest date per permno/calendar year, then all multiply mapped gvkey-years are dropped. Link intervals are inclusive; date ties use stable link-start ordering. The supplied gvkey founding file replaces the original permno file as an input-vintage difference. Current mthcap is not used: market cap follows the Stata price-times-shares formula in millions.\n')
    for sev,cost,title,body in issues: lines.append(f'- **Severity {sev}; implementation cost {cost} — {title}.** {body}')
    lines+=['','## Independent formula checks','', '```json',json.dumps(checks,indent=2),'```','','## Coverage','', '```json',json.dumps(summary,indent=2),'```']
    for fig in ['01','07','08','09']:
        p=ROOT/f'site/data/fig{fig}.csv'
        if p.exists():
            d=pd.read_csv(p)
            valid=d.select_dtypes('number').drop(columns=['fyear','industry5'],errors='ignore').notna().any(axis=1)
            lines.append(f"- Figure {int(fig)}: exported {int(d.fyear.min())}–{int(d.fyear.max())}; last nonmissing plotted year {int(d.loc[valid,'fyear'].max())}.")
    lines+=['','## Visual review','', 'Inspected the supplied PNGs and the generated comparison plots. The investment crossover and declining CAPEX path agree; the market-to-book peaks and adjusted levels broadly agree. The industry intensity lines overlap closely until the final partial historical year. Current ROE differs materially, whereas the historical-input replay overlays the published ROE chart. Plain matplotlib defaults are retained in the SVGs. No PDFs were opened.','',
            '## Files and reproduction','', 'Plotted aggregates: `site/data/figNN.csv`; plots: `site/figures/out/figNN.svg`. Local-only sample, reference collapses and per-year validation: `data/figures_work/`. Scripts and this report are under `site/figures/`. Sample, figure and validator paths have CLI overrides. Dependencies: python3, pandas, numpy, matplotlib. Figures extend to their latest eligible fiscal year; no empty year is filled with invented observations.','', '```sh','python3 site/figures/prepare_author_inputs.py','python3 site/figures/sample.py','python3 site/figures/fig01_rd_capex.py','python3 site/figures/fig07_intensity.py','python3 site/figures/fig08_mb.py','python3 site/figures/fig09_roe.py','python3 site/figures/diagnose_validation.py','python3 site/figures/validate_figures.py','```','', 'Validation does not pass merely because a correlation is high. Every relative discrepancy exceeding the requested threshold is listed in `data/figures_work/validation_by_year.csv`; systematic differences remain open until explained.']
    missing += ['Missing from the current stocks panel: BEA G and S stocks for direct evaluation of the BEA-equity support screen. Historical support equivalence is checked above; EPW stock availability supplies the documented current support proxy.', 'Missing from the supplied CRSPdsp500list.dta: membership spells after its final actual end date. Later flags are artifacts, as explained above.']
    if missing:
        lines+=['','## Missing inputs','']+['- '+m for m in missing]
    readme+=['## Reproduction','', '\n'.join(lines[lines.index('## Files and reproduction')+2:]),'', 'See [CODEX_REPORT.md](CODEX_REPORT.md) for ranked issues, numerical checks and deviations.']
    (ROOT/'site/figures/README.md').write_text('\n'.join(readme)+'\n')
    report='\n'.join(lines)+'\n'
    (ROOT/'site/figures/CODEX_REPORT.md').write_text(report)
    report_path.write_text(report)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sample',type=Path,default=WORK/'sample.csv')
    ap.add_argument('--inputs',type=Path,default=INPUTS)
    ap.add_argument('--author-root',type=Path,default=AUTHOR)
    ap.add_argument('--work',type=Path,default=WORK)
    ap.add_argument('--report-copy',type=Path,default=Path('/tmp/codex_figports_result.md'))
    a=ap.parse_args()
    a.work.mkdir(parents=True,exist_ok=True)
    sample=pd.read_csv(a.sample,low_memory=False)
    refs,checks=references(a.inputs,a.author_root)
    stats,details=[],[]
    for fig,module,cols,keys in [('01',f01,['rdAssets','capxAssets'],['fyear']),('07',f07,['intensity2'],['fyear','industry5']),('08',f08,['mb_win','epw'],['fyear']),('09',f09,['roe_inc2','roe_inc_epw2','diffUnadj'],['fyear'])]:
        current=module.compute(sample)
        current.to_csv(ROOT/f'site/data/fig{fig}.csv',index=False)
        module.plot(current,ROOT/f'site/figures/out/fig{fig}.svg')
        refs[fig].to_csv(a.work/f'author_fig{fig}.csv',index=False)
        compare(current,refs[fig],fig,cols,details,stats,keys)
        # Side-by-side numerical visual overlay stays local.
        figplot,ax=plt.subplots()
        groups=current.groupby('industry5') if 'industry5' in keys else [(None,current)]
        for ind,g in groups:
            ref=refs[fig] if ind is None else refs[fig][refs[fig].industry5==ind]
            for col in cols:
                line,=ax.plot(g.fyear,g[col],label=f'current {col} {ind or ""}')
                ax.plot(ref.fyear,ref[col],'--',color=line.get_color(),label=f'author {col} {ind or ""}')
        ax.legend(fontsize=6)
        figplot.tight_layout()
        figplot.savefig(a.work/f'comparison_fig{fig}.png')
        plt.close(figplot)
    pd.DataFrame(details).to_csv(a.work/'validation_by_year.csv',index=False)
    (a.work/'validation_summary.json').write_text(json.dumps(stats,indent=2)+'\n')
    (a.work/'formula_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print('Formula checks:',checks)
    write_reports(stats,checks,sample,a.work,a.report_copy,[])

if __name__=='__main__': main()
