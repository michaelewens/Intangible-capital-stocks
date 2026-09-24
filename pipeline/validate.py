"""Compare the Python build against (a) Joe Choi's Oct 2024 Stata run (mainStocks.dta, real 1990$)
and (b) the Sept 2023 public file in this repo (nominal). Prints counts, correlations and the
distribution of relative differences on overlapping gvkey-fyears."""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
JOE = "/Users/me2731/Dropbox/Research/research_assistants/choi_2024/intangibles_v2/data/mainStocks.dta"
PUB = ROOT / "intangibleCapital_090123.dta"


def compare(a, b, key, cols, label):
    m = a.merge(b, on=key, suffixes=("_py", "_ref"))
    print(f"\n== {label}: py rows {len(a)}, ref rows {len(b)}, overlap {len(m)}")
    for c in cols:
        x, y = m[f"{c}_py"], m[f"{c}_ref"]
        both = x.notna() & y.notna()
        print(f"  {c}: both nonmissing {both.sum()}, py-only-missing {(x.isna() & y.notna()).sum()}, ref-only-missing {(x.notna() & y.isna()).sum()}")
        xx, yy = x[both], y[both]
        print(f"     corr {np.corrcoef(xx, yy)[0,1]:.6f}; ", end="")
        rel = ((xx - yy).abs() / yy.abs().clip(lower=1e-6))[yy.abs() > 1]
        print(f"rel diff (|ref|>1): median {rel.median():.2e}, p99 {rel.quantile(.99):.2e}, share>1% {(rel > .01).mean():.4f}")
    return m


if __name__ == "__main__":
    tag = sys.argv[1]
    py = pd.read_csv(ROOT / "data" / "output" / f"intangibleCapital_{tag}.csv")
    cpi = pd.read_csv(ROOT / "data" / "inputs" / "cpi.csv")
    joe = pd.read_stata(JOE, columns=["gvkey", "fyear", "G2", "S2", "cpidef"])
    joe = joe.dropna(subset=["fyear"]); joe["gvkey"] = joe.gvkey.astype(int); joe["fyear"] = joe.fyear.astype(int)
    joe["knowCapital"] = joe.G2 * joe.cpidef; joe["orgCapital"] = joe.S2 * joe.cpidef
    joe = joe.drop_duplicates(["gvkey", "fyear"], keep="last")
    m = compare(py, joe[["gvkey", "fyear", "knowCapital", "orgCapital"]], ["gvkey", "fyear"], ["knowCapital", "orgCapital"], "vs Joe Choi Oct 2024 (nominal, his deflator)")
    # by-year missing pattern
    print(m.assign(pymiss=m.knowCapital_py.isna(), refmiss=m.knowCapital_ref.isna()).groupby("fyear")[["pymiss", "refmiss"]].mean().tail(6).round(3).to_string())
    pub = pd.read_stata(PUB); pub["gvkey"] = pub.gvkey.astype(int); pub["fyear"] = pub.fyear.astype(int)
    compare(py, pub, ["gvkey", "fyear"], ["knowCapital", "orgCapital"], "vs Sept 2023 public file")
