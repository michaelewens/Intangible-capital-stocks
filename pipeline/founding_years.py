"""Firm founding year and IPO year by gvkey.

Python port of processIPO.do from the Corporate hierarchy project (corp-hierarchy-mvr,
stata/paper/processIPO.do, 2026-08-07 revision with merge fixes a-c). Same inputs, same
precedence:
  foundingyear: Ritter_IPO_cik > age7517 > IPO-age.xlsx
  ipo_year:     gvkey_ipo_year.csv > Ritter_IPO_cik > earliest of age7517 / IPO-age.xlsx
  vc:           gvkey_ipo_year.csv > IPO-age.xlsx  (2 -> 1, >2 -> 0)

Inputs (data/inputs/founding/): IPO-age.xlsx, age7517.dta, Ritter_IPO_cik.dta, gvkey_ipo_year.csv,
and a permno-gvkey-fyear bridge (crsp_cs.dta, or built from ccmlink.csv with --bridge ccmlink).
Output: data/inputs/ipo_year.csv (gvkey, ipo_year, foundingyear, vc, permno, ipo_date, new_fy, new_vc)
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIN = ROOT / "data" / "inputs" / "founding"
OUT = ROOT / "data" / "inputs" / "ipo_year.csv"


def _keep_first(df, by, sort):
    """Stata `bys by (sort): keep if _n == 1` with missing sorting last."""
    return (df.sort_values([by, sort], na_position="last", kind="mergesort")
              .drop_duplicates(by, keep="first"))


def load_bridge(kind: str, asof_year: int):
    if kind == "crsp_cs":
        b = pd.read_stata(FIN / "crsp_cs.dta")
    else:  # from ccmlink history, same expansion as epw_stocks.py
        lk = pd.read_csv(ROOT / "data" / "inputs" / "ccmlink.csv", parse_dates=["linkdt", "linkenddt"])
        lk["startyear"] = lk.linkdt.dt.year
        lk["endyear"] = lk.linkenddt.dt.year.fillna(asof_year).astype(int)
        lk = lk[lk.endyear >= lk.startyear]
        lk["fyear"] = [np.arange(a, b + 1) for a, b in zip(lk.startyear, lk.endyear)]
        b = lk.explode("fyear")[["gvkey", "lpermno", "fyear"]].rename(columns={"lpermno": "permno"}).drop_duplicates()
    b = b.dropna(subset=["gvkey", "permno", "fyear"]).astype({"gvkey": int, "permno": int, "fyear": int})
    b = b.drop_duplicates(["permno", "fyear"])            # 1:1 on (permno, fyear) as the Stata merge requires
    pairs = b[["permno", "gvkey"]].drop_duplicates()
    n = pairs.groupby("permno").gvkey.transform("size")
    fallback = pairs[n == 1].rename(columns={"gvkey": "gvkeyPn"})
    return b[["permno", "fyear", "gvkey"]], fallback, int((n > 1).sum() and pairs[n > 1].permno.nunique())


def attach_gvkey(df, exact, fallback):
    """fix (a): exact (permno, fyear) match first, then permno-only fallback; drop unresolved."""
    df = df.merge(exact, on=["permno", "fyear"], how="left")
    df = df.merge(fallback, on="permno", how="left")
    df["gvkey"] = df.gvkey.fillna(df.gvkeyPn)
    return df.drop(columns="gvkeyPn").dropna(subset=["gvkey"]).astype({"gvkey": int})


def build(bridge_kind="crsp_cs", asof_year=2026, verbose=True):
    exact, fallback, n_ambig = load_bridge(bridge_kind, asof_year)
    stats = {"ambiguous_permnos_excluded": n_ambig}

    # --- A: Ritter IPO-age.xlsx (2022 list)
    a = pd.read_excel(FIN / "IPO-age.xlsx")
    a = a.rename(columns={"CRSP perm": "permno", "Founding": "foundingyear", "offer date": "offerdate", "VC": "new_vc"})
    a = a[["permno", "foundingyear", "offerdate", "new_vc"]].copy()
    a["new_vc"] = pd.to_numeric(a.new_vc, errors="coerce")
    a["foundingyear"] = pd.to_numeric(a.foundingyear, errors="coerce")
    a["fyear"] = (pd.to_numeric(a.offerdate, errors="coerce") / 10000).round().astype("Int64")
    a["permno"] = pd.to_numeric(a.permno, errors="coerce")
    a = a.dropna(subset=["permno"]).astype({"permno": int})
    a = a[~(a.foundingyear <= 0)]                      # drops -99, -9, 0; keeps missing
    a = _keep_first(a, "permno", "foundingyear")
    a["fyear"] = a.fyear.astype(int)
    a = attach_gvkey(a, exact, fallback).drop(columns="offerdate")
    stats["A_rows"] = len(a)

    # --- B: age7517.dta (older Ritter founding dates)
    b = pd.read_stata(FIN / "age7517.dta").rename(columns={"ipoyear": "fyear"})
    b = b.dropna(subset=["fyear"]).astype({"permno": int, "fyear": int})
    b = attach_gvkey(b, exact, fallback)
    stats["B_rows"] = len(b)
    for name, d in (("A", a), ("B", b)):
        dup = d.duplicated(["gvkey", "fyear"]).sum()
        if dup:
            raise ValueError(f"{name}: {dup} duplicate gvkey-fyear rows; Stata merge 1:1 would fail")

    # merge 1:1 gvkey fyear, B master: B's foundingyear and permno win on matches
    ab = b.merge(a, on=["gvkey", "fyear"], how="outer", suffixes=("", "_a"))
    ab["foundingyear"] = ab.foundingyear.fillna(ab.foundingyear_a)
    ab["permno"] = ab.permno.fillna(ab.permno_a)
    ab = ab.drop(columns=["foundingyear_a", "permno_a"]).rename(columns={"fyear": "ipo_year", "foundingyear": "new_fy"})
    ab = _keep_first(ab, "gvkey", "ipo_year")           # fix (b)
    founding_years = ab[["permno", "new_fy", "ipo_year", "gvkey", "new_vc"]]
    stats["founding_years_rows"] = len(founding_years)

    # --- C: Ritter_IPO_cik.dta
    c = pd.read_stata(FIN / "Ritter_IPO_cik.dta", columns=["ipoyear", "gvkey", "foundingyear"])
    c["gvkey"] = pd.to_numeric(c.gvkey, errors="coerce")
    c = c.dropna(subset=["gvkey"]).astype({"gvkey": int}).rename(columns={"ipoyear": "ipo_year"})
    c = _keep_first(c, "gvkey", "ipo_year")

    # --- D: gvkey_ipo_year.csv (master)
    d = pd.read_csv(FIN / "gvkey_ipo_year.csv")
    d = d.rename(columns={"VC": "vc"})
    d["vc"] = pd.to_numeric(d.vc, errors="coerce")
    d["gvkey"] = pd.to_numeric(d.gvkey, errors="coerce")
    d = d.dropna(subset=["gvkey"]).astype({"gvkey": int})
    d = _keep_first(d, "gvkey", "ipo_year")

    m = d.merge(c, on="gvkey", how="outer", suffixes=("", "_c"))   # fix (c): keep(1 2 3)
    m["ipo_year"] = m.ipo_year.fillna(m.ipo_year_c)
    m = m.drop(columns="ipo_year_c")
    m = m.merge(founding_years, on="gvkey", how="outer", suffixes=("", "_f"))
    m["ipo_year"] = m.ipo_year.fillna(m.ipo_year_f)
    m = m.drop(columns="ipo_year_f")
    m["foundingyear"] = m.foundingyear.fillna(m.new_fy)
    m["vc"] = m.vc.fillna(m.new_vc)
    m.loc[m.vc == 2, "vc"] = 1
    m.loc[m.vc > 2, "vc"] = 0
    m = m[["gvkey", "ipo_year", "foundingyear", "vc", "permno", "ipo_date", "new_fy", "new_vc"]].sort_values("gvkey")
    stats.update(gvkeys=len(m), with_foundingyear=int(m.foundingyear.notna().sum()),
                 with_ipo_year=int(m.ipo_year.notna().sum()),
                 founding_after_ipo=int((m.foundingyear > m.ipo_year).sum()))
    if verbose:
        print(stats)
    return m, stats


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bridge", choices=["crsp_cs", "ccmlink"], default="crsp_cs")
    ap.add_argument("--asof-year", type=int, default=2026)
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    m, _ = build(a.bridge, a.asof_year)
    m.to_csv(a.out, index=False)
    print("wrote", a.out)
