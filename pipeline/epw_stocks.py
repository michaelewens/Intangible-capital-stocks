"""Build Ewens, Peters and Wang (2023) knowledge and organization capital stocks.

Python port of the Stata builder (createIntangibleStocks.do, Joseph Choi's Oct 2024 revision)
restricted to the paper's headline stocks:
  knowCapital  = G2  (R&D capitalised with the industry knowledge-depreciation estimates)
  orgCapital   = S2  (gamma x SG&A capitalised at a 20% depreciation rate)

Inputs (data/inputs/, see pull_inputs_local.py):
  funda.csv, company.csv, ccmlink.csv, cpi.csv
  pipeline/data/ritter_founding_ipo.csv  (Jay Ritter's founding and IPO years by permno)

Output (data/output/):
  intangibleCapital_<YYYYMMDD>.csv  - gvkey, fyear, orgCapital, knowCapital (nominal, net)
  capital_accum_parameters.csv      - sic, knowDepr, organDepr, gamma, industry5
  build_stats.json                  - growth constants and counts for the log
"""
import argparse, json
from datetime import date
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "data" / "inputs"
OUT = ROOT / "data" / "output"
RITTER = ROOT / "data" / "inputs" / "founding" / "ritter_founding_ipo.csv"
IPO_YEAR = ROOT / "data" / "inputs" / "ipo_year.csv"

# Ewens, Peters and Wang (2023) baseline estimates, Fama-French 5 industries (Oct 2023 revision)
KNOW_DEPR = {1: 0.43, 2: 0.50, 3: 0.42, 4: 0.33, 5: 0.35}
GAMMA = {1: 0.20, 2: 0.21, 3: 0.37, 4: 0.51, 5: 0.22}
ORG_DEPR = 0.20
GROWTH_SAMPLE_LAST_YEAR = 2017   # growth-rate constants are estimated on fyear <= 2017, as in the paper
FF5_LABELS = {1: "Consumer", 2: "Manuf.", 3: "High-tech", 4: "Health", 5: "Other"}

# industry5.do: SIC ranges (inclusive). Order matters: later assignments overwrite earlier ones.
_MANUF = [(2520, 2589), (2600, 2699), (2750, 2769), (2800, 2829), (2840, 2899), (3000, 3099), (3200, 3569),
          (3580, 3621), (3623, 3629), (3700, 3709), (3712, 3713), (3715, 3715), (3717, 3749), (3752, 3791),
          (3793, 3799), (3860, 3899), (1200, 1399), (2900, 2999), (4900, 4949)]
_HITEC = [(3570, 3579), (3622, 3622), (3660, 3692), (3694, 3699), (3810, 3839), (7370, 7379), (7391, 7391),
          (8730, 8734), (4800, 4899)]
_HLTH = [(2830, 2839), (3693, 3693), (3840, 3859)]
_CNSMR = [(100, 999), (2000, 2399), (2700, 2749), (2770, 2799), (3100, 3199), (3940, 3989), (2500, 2519),
          (2590, 2599), (3630, 3659), (3710, 3711), (3714, 3714), (3716, 3716), (3750, 3751), (3792, 3792),
          (3900, 3939), (3990, 3999), (5000, 5999), (7200, 7299), (7600, 7699), (8000, 8099),
          (4813, 4813), (4812, 4812), (4841, 4841), (4833, 4833), (4832, 4832)]


def industry5(sic: pd.Series) -> pd.Series:
    s = pd.to_numeric(sic, errors="coerce")
    out = pd.Series(np.nan, index=s.index)
    for code, ranges in ((2, _MANUF), (3, _HITEC), (4, _HLTH), (1, _CNSMR)):
        m = np.zeros(len(s), dtype=bool)
        for lo, hi in ranges:
            m |= (s >= lo) & (s <= hi)
        out[m] = code
    return out.fillna(5).astype(int)


def _group_interpolate(df, col):
    """Stata `bysort gvkey: ipolate col fyear` - linear in fyear, interior points only."""
    x = df["fyear"].to_numpy(float)
    y = df[col].to_numpy(float)
    g = df["gvkey"].to_numpy()
    out = y.copy()
    # group boundaries (df sorted by gvkey, fyear)
    starts = np.flatnonzero(np.r_[True, g[1:] != g[:-1]])
    ends = np.r_[starts[1:], len(g)]
    for a, b in zip(starts, ends):
        yy = y[a:b]
        miss = np.isnan(yy)
        if not miss.any() or miss.all():
            continue
        xx = x[a:b]
        known = ~miss
        fill = np.interp(xx[miss], xx[known], yy[known], left=np.nan, right=np.nan)
        out[a:b][miss] = fill
    df[col] = out
    return df


def _stata_max_missing_last(s):
    """Sort key where missing sorts last (Stata convention)."""
    return s.fillna(pd.Timestamp("2262-01-01"))


def _backfill_by_growth(df, col, ages, rate_col):
    """xrd = xrd[_n+1] / exp(rate) if xrd == . & agei == i, applied for i in `ages` in order."""
    nxt_gvkey = df["gvkey"].shift(-1)
    same = (nxt_gvkey == df["gvkey"]).to_numpy()
    for i in ages:
        nxt = df[col].shift(-1).to_numpy()
        m = df[col].isna().to_numpy() & (df["agei"] == i).to_numpy() & same
        if m.any():
            vals = nxt[m] / np.exp(df[rate_col].to_numpy()[m])
            df.loc[df.index[m], col] = vals
    return df


def _accumulate(df, flow, first_stock, depr):
    """Perpetual inventory: K_t = (1-depr)^(gap) K_{t-1} + flow_t, seeded with first_stock at the firm's
    first observation. Vectorised over position-within-firm; NaN propagates as in Stata."""
    n = len(df)
    pos = df.groupby("gvkey").cumcount().to_numpy()
    gap = df["fyear"].diff().to_numpy()
    K = np.full(n, np.nan)
    K[pos == 0] = first_stock[pos == 0]
    f = flow.to_numpy(float) if hasattr(flow, "to_numpy") else flow
    d = depr.to_numpy(float) if hasattr(depr, "to_numpy") else np.full(n, depr, float)
    for k in range(1, pos.max() + 1):
        idx = np.flatnonzero(pos == k)
        K[idx] = (1 - d[idx]) ** gap[idx] * K[idx - 1] + f[idx]
    return K


def build(asof_year: int, verbose=True, inputs: Path = IN, link_expanded: bool = False, founding: str = "gvkey"):
    """link_expanded=True: ccmlink.csv already holds one (gvkey, fyear, lpermno) row per firm-year."""
    IN = inputs
    stats = {}
    df = pd.read_csv(IN / "funda.csv", parse_dates=["datadate"])
    df["gvkey"] = df.gvkey.astype(int)
    comp = pd.read_csv(IN / "company.csv")
    comp["gvkey"] = comp.gvkey.astype(int)
    # Header SIC: the WRDS web download of funda carries `sic`; the raw comp.funda table does not,
    # so fall back to comp.company. Both are the same header field.
    if "sic" in df.columns:
        df["sic"] = pd.to_numeric(df.sic, errors="coerce")
        df = df.merge(comp[["gvkey", "sic"]].rename(columns={"sic": "_sic_c"}), on="gvkey", how="left")
        df["sic"] = df.sic.fillna(pd.to_numeric(df._sic_c, errors="coerce"))
        df = df.drop(columns="_sic_c")
    else:
        df = df.merge(comp[["gvkey", "sic"]], on="gvkey", how="left")
        df["sic"] = pd.to_numeric(df.sic, errors="coerce")
    df["industry5"] = industry5(df.sic)
    df = df.sort_values(["gvkey", "fyear"]).reset_index(drop=True)
    stats["rows_raw"] = int(len(df))

    df["report_rd"] = df.xrd.notna()
    df["report_sga"] = df.xsga.notna()
    df["rdip"] = df.rdip.fillna(0)
    # Strip R&D from SG&A when R&D is not inside COGS
    rdincogs = (df.xrd + df.rdip > df.xsga) & (df.xrd + df.rdip < df.cogs) & df.xrd.notna() & df.xsga.notna() & df.cogs.notna()
    m = df.xrd.notna() & df.xsga.notna() & ~rdincogs
    df.loc[m, "xsga"] = np.maximum(df.loc[m, "xsga"] - (df.loc[m, "xrd"] + df.loc[m, "rdip"]), 0)

    # Deflate (1990 dollars)
    cpi = pd.read_csv(IN / "cpi.csv")
    df = df.merge(cpi, on="fyear", how="left")
    for v in ["xrd", "xsga", "at", "prcc_f"]:
        df[v] = df[v] / df.cpidef

    # Missing R&D and SG&A rules
    df.loc[(df.xrd.isna() & (df.fyear >= 1977) & df["at"].notna()) | (df.xrd < 0), "xrd"] = 0
    nord77 = df.assign(_z=(df.fyear == 1977) & (df.xrd == 0)).groupby("gvkey")["_z"].transform("max")
    df.loc[df.xrd.isna() & nord77 & df["at"].notna(), "xrd"] = 0
    df.loc[(df.xsga.isna() & df["at"].notna()) | (df.xsga < 0), "xsga"] = 0
    df = _group_interpolate(df, "xrd")
    df = _group_interpolate(df, "xsga")

    # Firm ages
    df["fycomp"] = df.groupby("gvkey").fyear.transform("min")
    df["fycrsp"] = df.fyear.where(df.prcc_f.notna()).groupby(df.gvkey).transform("min")

    # CRSP permno via the link history, expanded to gvkey-fyear (updateLink.do)
    if link_expanded:
        lk = pd.read_csv(IN / "ccmlink.csv")
        lk["gvkey"] = lk.gvkey.astype(int)
    else:
        lk = pd.read_csv(IN / "ccmlink.csv", parse_dates=["linkdt", "linkenddt"])
        lk["gvkey"] = lk.gvkey.astype(int)
        lk["startyear"] = lk.linkdt.dt.year
        lk["endyear"] = lk.linkenddt.dt.year.fillna(asof_year).astype(int) - 1
        lk = lk[lk.endyear >= lk.startyear].copy()
        lk["fyear"] = [np.arange(a, b + 1) for a, b in zip(lk.startyear, lk.endyear)]
        lk = lk.explode("fyear")
        lk["fyear"] = lk.fyear.astype(int)
        lk["_end"] = _stata_max_missing_last(lk.linkenddt)
        lk = lk.sort_values(["gvkey", "fyear", "_end", "linkdt"]).drop_duplicates(["gvkey", "fyear"], keep="last")
    df = df.merge(lk[["gvkey", "fyear", "lpermno"]], on=["gvkey", "fyear"], how="left").rename(columns={"lpermno": "permno"})
    df["permno"] = df.groupby("gvkey").permno.bfill()

    if founding == "gvkey":
        # Corporate-hierarchy builder (founding_years.py): Ritter sources combined, keyed on gvkey
        fy = pd.read_csv(IPO_YEAR)[["gvkey", "foundingyear", "ipo_year"]].rename(columns={"ipo_year": "ipoyear"})
        df = df.merge(fy, on="gvkey", how="left")
    else:
        # Paper's original: Ritter founding/IPO years keyed on CRSP permno
        rit = pd.read_csv(RITTER)
        df = df.merge(rit[["permno", "foundingyear", "ipoyear"]], on="permno", how="left")
    df["founding_source"] = np.where(df.foundingyear.notna(), "ritter", "imputed")
    df["foundingyear"] = df.foundingyear.fillna(np.fmin(df.fycomp, df.fycrsp - 7))
    df.loc[df.fycomp < df.foundingyear, "foundingyear"] = df.fycomp
    df["ager"] = df.fyear - df.foundingyear
    df.loc[df.fycrsp.notna() & (df.ipoyear.isna() | (df.fycrsp < df.ipoyear)), "ipoyear"] = df.fycrsp
    df["agei"] = df.fyear - df.ipoyear
    df = df.sort_values(["gvkey", "fyear"]).reset_index(drop=True)

    # ---- Knowledge capital (G2) ----
    sub = df[df.fyear <= GROWTH_SAMPLE_LAST_YEAR]
    nxt = sub.groupby("gvkey").xrd.shift(-1)
    with np.errstate(divide="ignore", invalid="ignore"):
        grow_rd = np.log(nxt / sub.xrd)
    grow_rd = grow_rd.replace([np.inf, -np.inf], np.nan)
    m_grow_rd = grow_rd.groupby(sub.agei, dropna=False).mean().rename("m_grow_rd").reset_index()
    df = df.merge(m_grow_rd, on="agei", how="left")
    df = _backfill_by_growth(df, "xrd", range(int(np.nanmax(df.agei)), -1, -1), "m_grow_rd")
    const_rd = df.loc[(df.agei >= -2) & (df.agei < 0) & df.report_rd, "m_grow_rd"].mean()
    df["m_grow_rd"] = const_rd
    df = _backfill_by_growth(df, "xrd", range(-1, int(np.nanmin(df.agei)) - 1, -1), "m_grow_rd")
    stats["m_grow_rd"] = float(const_rd)

    df["knowDepr"] = df.industry5.map(KNOW_DEPR)
    eta2 = (1 - df.knowDepr) / np.exp(const_rd)
    first = df.xrd * (1 / (1 - eta2)) * (1 - eta2 ** (df.ager + 1))
    df["G2"] = _accumulate(df, df.xrd, first.to_numpy(), df.knowDepr)

    # ---- Organization capital (S2) ----
    sub = df[df.fyear <= GROWTH_SAMPLE_LAST_YEAR]
    nxt = sub.groupby("gvkey").xsga.shift(-1)
    with np.errstate(divide="ignore", invalid="ignore"):
        grow_sga = np.log(nxt / sub.xsga).replace([np.inf, -np.inf], np.nan)
    const_sga = grow_sga[(sub.agei >= -2) & (sub.agei < 0) & sub.report_sga].mean()
    df["m_grow_sga"] = const_sga
    df = _backfill_by_growth(df, "xsga", range(-1, int(np.nanmin(df.agei)) - 1, -1), "m_grow_sga")
    stats["m_grow_sga"] = float(const_sga)

    df["gamma"] = df.industry5.map(GAMMA)
    eta2sga = (1 - ORG_DEPR) / np.exp(const_sga)
    first = df.gamma * df.xsga * (1 / (1 - eta2sga)) * (1 - eta2sga ** (df.ager + 1))
    df["S2"] = _accumulate(df, df.gamma * df.xsga, first.to_numpy(), ORG_DEPR)

    # ---- Public output (createPublicOutput.do): nominal, fyear >= 1975 ----
    # Note field: why a stock is missing, or that its flows were interpolated
    at_missing = df["at"].isna()
    stock_missing = df.G2.isna() | df.S2.isna()
    prev_present = df.groupby("gvkey").G2.shift(1).notna()
    df["note"] = ""
    df.loc[at_missing & ~stock_missing, "note"] = "assets missing; R&D and SG&A interpolated"
    df.loc[stock_missing & at_missing, "note"] = "assets missing; no stock computed"
    df.loc[stock_missing & ~at_missing, "note"] = "stock missing because an earlier year had no flows"
    out = df[df.fyear >= 1975][["gvkey", "fyear", "S2", "G2", "cpidef", "datadate", "note"]].copy()
    out["orgCapital"] = out.S2 * out.cpidef
    out["knowCapital"] = out.G2 * out.cpidef
    out = out.sort_values(["gvkey", "fyear", "datadate"]).drop_duplicates(["gvkey", "fyear"], keep="last")
    out = out[["gvkey", "fyear", "orgCapital", "knowCapital", "note"]].reset_index(drop=True)
    out["fyear"] = out.fyear.astype(int)

    params = (df[["sic", "knowDepr", "gamma", "industry5"]].dropna(subset=["sic"]).drop_duplicates("sic")
              .assign(organDepr=ORG_DEPR, sic=lambda d: d.sic.astype(int))
              .sort_values("sic")[["sic", "knowDepr", "organDepr", "gamma", "industry5"]])
    params["industry5"] = params.industry5.map(FF5_LABELS)

    firms = df.drop_duplicates("gvkey")
    stats["firms_with_ritter_founding"] = int((firms.founding_source == "ritter").sum())
    stats["firms_total"] = int(len(firms))
    stats.update(rows_out=int(len(out)), gvkeys_out=int(out.gvkey.nunique()),
                 fyear_min=int(out.fyear.min()), fyear_max=int(out.fyear.max()),
                 know_nonmissing=int(out.knowCapital.notna().sum()), org_nonmissing=int(out.orgCapital.notna().sum()),
                 cpi_last_year=int(cpi.fyear.max()))
    if verbose:
        print(json.dumps(stats, indent=1))
    return out, params, stats, df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--asof-year", type=int, default=date.today().year)
    ap.add_argument("--tag", default=date.today().strftime("%Y%m%d"))
    ap.add_argument("--keep-panel", action="store_true", help="also save the full working panel (large)")
    ap.add_argument("--inputs", default=str(IN))
    ap.add_argument("--link-expanded", action="store_true")
    ap.add_argument("--founding", choices=["gvkey", "permno"], default="gvkey", help="founding/IPO year source: gvkey = founding_years.py output (default); permno = paper original")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    out, params, stats, panel = build(a.asof_year, inputs=Path(a.inputs), link_expanded=a.link_expanded, founding=a.founding)
    out.to_csv(OUT / f"intangibleCapital_{a.tag}.csv", index=False)
    params.to_csv(OUT / "capital_accum_parameters.csv", index=False)
    (OUT / "build_stats.json").write_text(json.dumps(stats, indent=1))
    if a.keep_panel:
        panel.to_csv(OUT / f"panel_{a.tag}.csv", index=False)
    print(f"wrote {OUT / f'intangibleCapital_{a.tag}.csv'}")
