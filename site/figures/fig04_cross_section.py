"""Figure 4 (site): distribution of intangible intensity across firms in the latest full fiscal year,
by Fama-French industry. Intensity = (knowCapital + orgCapital + balance-sheet intangibles) /
(that + gross PP&E), the Figure 7 definition, evaluated in the latest year with at least 1,000 firms."""
import numpy as np, pandas as pd
from _common import load_sample, save, new_fig, IND


def compute(s):
    d = s.rename(columns={"intensity2": "intensity"}).dropna(subset=["intensity"]).copy()
    counts = d.groupby("fyear").gvkey.nunique()
    year = int(counts[counts >= 1000].index.max())
    d = d[d.fyear == year]
    q = d.groupby("industry5").intensity.describe(percentiles=[.1, .25, .5, .75, .9])
    q = q[["count", "10%", "25%", "50%", "75%", "90%"]].reset_index()
    q["industry"] = q.industry5.map(IND); q["fyear"] = year
    return q


def plot(df):
    fig, ax = new_fig()
    x = np.arange(len(df))
    ax.vlines(x, df["10%"], df["90%"], color="#9a9a9a", lw=1)
    ax.vlines(x, df["25%"], df["75%"], color="#1f4e79", lw=8)
    ax.scatter(x, df["50%"], color="white", zorder=3, s=20)
    ax.set_xticks(x); ax.set_xticklabels(df.industry); ax.set_ylim(0, 1)
    ax.set_ylabel("Intangible assets / capital stock"); ax.set_title(f"Fiscal year {int(df.fyear.iloc[0])}: 10th to 90th percentile, box = 25th to 75th, dot = median", fontsize=10)
    return fig


if __name__ == "__main__":
    df = compute(load_sample()); save(df, plot(df), "fig04")
