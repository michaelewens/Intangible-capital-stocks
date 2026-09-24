"""Print local figure input schemas; no data are written or published."""
from pathlib import Path
import argparse
import pandas as pd
ROOT = Path(__file__).resolve().parents[2]
AUTHOR = Path('/Users/me2731/Dropbox/Research/research_assistants/choi_2024/intangibles_v2')
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--root',type=Path,default=ROOT)
ap.add_argument('--author-root',type=Path,default=AUTHOR)
args=ap.parse_args()
ROOT,AUTHOR=args.root,args.author_root
for p in sorted((ROOT/'data/inputs/figures').glob('*.dta')):
    if p.name not in ['dataForFigure3.dta', 'figure4data.dta']:
        with pd.read_stata(p, iterator=True, convert_categoricals=False) as r:
            d = r.read(3)
            print(p.name, list(d.columns), '\n', d.to_string(index=False) if len(d.columns)<15 else '')
for p in [ROOT/'data/inputs'/n for n in ['funda.csv','company.csv','ccmlink.csv','msf.csv']] + [ROOT/'data/output/panel_20260924.csv', AUTHOR/'data/mainStocks.dta']:
    if p.suffix == '.csv': d=pd.read_csv(p,nrows=2)
    else:
        with pd.read_stata(p,iterator=True,convert_categoricals=False) as r: d=r.read(1)
    print(p.name, list(d.columns))
print((ROOT/'data/inputs/figures/marginal_tax_rates.txt').read_text().splitlines()[:2])
