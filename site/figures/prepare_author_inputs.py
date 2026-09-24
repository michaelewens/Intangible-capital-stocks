"""Stage only the final deal keys needed for exact exclusions, locally and offline.

Run before sample.py. These proprietary keys stay in data/figures_work/.
"""
import argparse
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
AUTHOR=Path('/Users/me2731/Dropbox/Research/research_assistants/choi_2024/intangibles_v2')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--author-root',type=Path,default=AUTHOR)
    ap.add_argument('--out',type=Path,default=ROOT/'data/figures_work/author_deals.csv')
    a=ap.parse_args()
    source=a.author_root/'data/estimation/data_for_estimation_v4.dta'
    d=pd.read_stata(source,columns=['YearCompletedUnconditional','tgt_gvkey','sdc_dealno'],convert_categoricals=False)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    d.to_csv(a.out,index=False)
    print(f'{len(d)} final deal rows staged at {a.out}')

if __name__=='__main__': main()
