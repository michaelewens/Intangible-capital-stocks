"""Matched-vintage audits to separate translation errors from new input data."""
import json
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sample import ROOT, INPUTS, WORK, prepare_market, KEY, winsor, ratio
from validate_figures import AUTHOR, digitize_roe
import fig08_mb as f08
import fig09_roe as f09

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--inputs',type=Path,default=INPUTS)
ap.add_argument('--work',type=Path,default=WORK)
ap.add_argument('--author-root',type=Path,default=AUTHOR)
args=ap.parse_args()
INPUTS,WORK,AUTHOR=args.inputs,args.work,args.author_root
s=pd.read_csv(WORK/'sample.csv',low_memory=False)
a=pd.read_stata(INPUTS/'figures/figure1data.dta',convert_categoricals=False)
a['gvkey']=pd.to_numeric(a.gvkey)
a['sic']=pd.to_numeric(a.sic,errors='coerce')
old=prepare_market(a,INPUTS,WORK/'author_deals.csv')
p=pd.read_stata(AUTHOR/'data/mainStocks.dta',columns=KEY+['G','S','G2','S2','G2depr','S2depr','epwxi'],convert_categoricals=False).rename(columns={'epwxi':'gamma'})
p['gvkey']=pd.to_numeric(p.gvkey)
old=old.merge(p,on=KEY,how='left',validate='one_to_one')
ref=pd.read_stata(INPUTS/'figures/dataForFigure8.dta',convert_categoricals=False)
ref['gvkey']=pd.to_numeric(ref.gvkey)
old8=f08.compute(old)
old9=f09.compute(old)
old8.to_csv(WORK/'same_vintage_fig08.csv',index=False)
old9.to_csv(WORK/'same_vintage_fig09.csv',index=False)
joined=old[old.fyear>=1977].merge(ref,on=KEY,how='outer',suffixes=('_port','_author'),indicator=True)
metric={'sample_overlap':joined._merge.value_counts().to_dict(),'mb_raw_matched_mae':float((joined.mb_port-joined.mb_author).abs().mean()),'mb_winsor_matched_mae':float((joined.mb_win_port-joined.mb_win_author).abs().mean()),'figure1_author_formats':a.indfmt.value_counts().to_dict(),'funda_year_counts':s.fyear.value_counts().sort_index().tail(6).to_dict(),'sp500_year_counts':s[s.sp500.eq(1)].fyear.value_counts().sort_index().tail(10).to_dict()}
c=f08.compute(ref)
j=old8.merge(c,on='fyear',suffixes=('_port','_author'))
for col in ['mb_win','epw']:
    metric['same_vintage_fig08_'+col]={'r':float(j[col+'_port'].corr(j[col+'_author'])),'mae':float((j[col+'_port']-j[col+'_author']).abs().mean())}
roe_ref=digitize_roe(AUTHOR/'writing/figures/figure9.png')
roe=old9.merge(roe_ref,on='fyear',suffixes=('_port','_author'))
for col in ['roe_inc2','roe_inc_epw2','diffUnadj']:
    metric['same_vintage_fig09_'+col]={'r':float(roe[col+'_port'].corr(roe[col+'_author'])),'mae':float((roe[col+'_port']-roe[col+'_author']).abs().mean())}
metric['author_sp500_year_counts']=a[a.sp500.eq(1)].fyear.value_counts().sort_index().tail(10).to_dict()
sp=pd.read_stata(INPUTS/'figures/CRSPdsp500list.dta')
metric['membership_latest_actual_end']=str(sp.ending.max().date())
metric['membership_spells']=len(sp)
spmatch=s[KEY+['sp500']].merge(a[KEY+['sp500']],on=KEY,suffixes=('_current','_author'))
metric['sp500_flag_matched_disagreements']=int((spmatch.sp500_current.eq(1)!=spmatch.sp500_author.eq(1)).sum())
metric['author_figure8_last_year']=int(ref.fyear.max())
metric['current_bea_support_conditions']={'negative_G2':int((s.G2<0).sum()),'negative_S2':int((s.S2<0).sum())}
years=pd.read_stata(AUTHOR/'data/mainStocks.dta',columns=['fyear'],convert_categoricals=False)
metric['author_stock_year_counts']=years.fyear.value_counts().sort_index().tail(3).to_dict()
final=pd.read_csv(WORK/'author_deals.csv')
t=pd.read_stata(INPUTS/'figures/targetData.dta',convert_categoricals=False)
ac=pd.read_stata(INPUTS/'figures/acqData.dta',convert_categoricals=False)
metric['final_deals_vs_extracts']={
    'rows':len(final),
    'deal_order_matches':bool(np.array_equal(final.sdc_dealno,t.sdc_dealno)),
    'target_order_matches':bool(np.array_equal(final.tgt_gvkey,t.tgt_gvkey)),
    'completion_order_matches':bool(np.array_equal(final.YearCompletedUnconditional,ac.YearCompletedUnconditional,equal_nan=True))}
from common import plt
fig,ax=plt.subplots()
for col in ['roe_inc2','roe_inc_epw2','diffUnadj']:
    line,=ax.plot(old9.fyear,old9[col],label='same vintage '+col)
    ax.plot(roe_ref.fyear,roe_ref[col],'--',color=line.get_color(),label='PNG '+col)
ax.legend(fontsize=6)
fig.tight_layout()
fig.savefig(WORK/'same_vintage_fig09.png')
plt.close(fig)
for name in ['targetData','acqData']:
    d=pd.read_stata(INPUTS/f'figures/{name}.dta',convert_categoricals=False)
    metric[name]={'rows':len(d),'negative_deal_ids':int((d.sdc_dealno<0).sum()),'missing_gvkey':int(d.iloc[:,-1].isna().sum()),'unique_gvkeys':int(d.iloc[:,-1].nunique())}
(WORK/'diagnostics.json').write_text(json.dumps(metric,indent=2)+'\n')
print(json.dumps(metric,indent=2))
