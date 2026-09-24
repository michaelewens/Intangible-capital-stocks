"""Figure 3 (site): explanatory power of book capital for market enterprise value, with and without the
intangible stocks. Port of createFigure3.do's regression, without the BEA-HH benchmark and the Matlab
t-statistics. For each fiscal year: OLS of log(market cap + dltt + dlc + dcpstk) on log(at + .01)
and on log(knowCapital + orgCapital + at + .01); the series is the difference in R-squared.
Screens as in the Stata: market cap >= $5M, firm-years in the paper's estimation sample excluded."""
import numpy as np, pandas as pd
from _common import load_sample, save, new_fig


def _r2(y, x):
    X = np.column_stack([np.ones(len(x)), x]); b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b; return 1 - r @ r / ((y - y.mean()) @ (y - y.mean()))


def compute(s):
    d = s.copy(); d["knowCapital_nom"] = d.G2 * d.cpidef; d["orgCapital_nom"] = d.S2 * d.cpidef
    d = d[~(d.targetYear.fillna(0).astype(bool) | d.acqYear.fillna(0).astype(bool))]
    d["mktcap"] = d.prcc_f.abs() * d.csho
    d = d[d.mktcap >= 5]
    for c in ["dltt", "dlc", "dcpstk", "ppegt"]: d[c] = d[c].fillna(0)
    d["logEV"] = np.log(d.mktcap + d.dltt + d.dlc + d.dcpstk)
    d["logBook"] = np.log(d["at"] + .01)
    d["logBookIntan"] = np.log(d.knowCapital_nom + d.orgCapital_nom + d["at"] + .01)
    d = d.replace([np.inf, -np.inf], np.nan).dropna(subset=["logEV", "logBook", "logBookIntan"])
    d = d[d.fyear >= 1977]
    rows = []
    for y, g in d.groupby("fyear"):
        if len(g) < 100: continue
        r_book = _r2(g.logEV.to_numpy(), g.logBook.to_numpy()); r_int = _r2(g.logEV.to_numpy(), g.logBookIntan.to_numpy())
        rows.append({"fyear": int(y), "n_firms": len(g), "r2_book": r_book, "r2_book_plus_intangibles": r_int, "r2_gain": r_int - r_book})
    return pd.DataFrame(rows)


def plot(df):
    fig, ax = new_fig()
    ax.plot(df.fyear, df.r2_gain, marker="o", ms=3, color="#1f4e79")
    ax.axhline(0, color="#9a9a9a", lw=0.8)
    ax.set_xlabel("Fiscal year"); ax.set_ylabel("Gain in R-squared from adding intangible stocks")
    return fig


if __name__ == "__main__":
    df = compute(load_sample()); save(df, plot(df), "fig03")
