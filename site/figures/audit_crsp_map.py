"""Audit the dated CCM map against the authors' actual stored map, offline."""
from pathlib import Path
import json
import pandas as pd
from sample import INPUTS, WORK, KEY
from validate_figures import AUTHOR
original=pd.read_stata(AUTHOR/'data/intermediate/private/CRSP_COMP_Linkfile2024.dta',columns=['gvkey','lpermno','datadate'],convert_categoricals=False)
original['gvkey']=pd.to_numeric(original.gvkey,errors='coerce')
original['fyear']=original.datadate.dt.year
original=original.dropna(subset=['gvkey']).sort_values(['lpermno','fyear','datadate']).drop_duplicates(['lpermno','fyear'],keep='last')
dates=pd.read_csv(INPUTS/'funda.csv',usecols=['gvkey','datadate'],parse_dates=['datadate'])
lk=pd.read_csv(INPUTS/'ccmlink.csv',parse_dates=['linkdt','linkenddt'])
m=dates.merge(lk,on='gvkey')
m=m[(m.datadate>=m.linkdt)&(m.linkenddt.isna()|(m.datadate<=m.linkenddt))].copy()
m['fyear']=m.datadate.dt.year
m=m.sort_values(['lpermno','fyear','datadate','linkdt']).drop_duplicates(['lpermno','fyear'],keep='last')
j=original.merge(m,on=['lpermno','fyear'],suffixes=('_author','_current'),how='outer',indicator=True)
metric={'join_counts':j._merge.value_counts().to_dict(),'matched_key_disagreements':int((j.gvkey_author!=j.gvkey_current)[j._merge=='both'].sum()),'original_year_min':int(original.fyear.min()),'original_year_max':int(original.fyear.max())}
(WORK/'crsp_map_audit.json').write_text(json.dumps(metric,indent=2)+'\n')
print(json.dumps(metric,indent=2))
print(j[(j._merge=='both')&(j.gvkey_author!=j.gvkey_current)].head(10).to_string(index=False))
