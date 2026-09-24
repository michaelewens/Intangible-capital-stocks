"""Figure 4 (site): distribution of intangible intensity across firms in the latest full fiscal year,
by Fama-French industry. Intensity = (knowCapital + orgCapital + balance-sheet intangibles) /
(that + gross PP&E), the Figure 7 definition, evaluated in the latest year with at least 1,000 firms."""
import numpy as np, pandas as pd
from _common import load_sample, save, new_fig, IND


def compute(s):
    d = s.rename(columns={"intensity2": "intensity"}).dropna(subset=["intensity"]).copy()
    counts = d.groupby("fyear").gvkey.nunique()
    year = int(counts[counts >= 1000].index.max())
    d = d[(d.fyear == year) & d.industry5.isin([1, 2, 3, 4])]
    q = d.groupby("industry5").intensity.describe(percentiles=[.1, .25, .5, .75, .9])
    q = q[["count", "mean", "10%", "25%", "50%", "75%", "90%"]].reset_index()
    q["industry"] = q.industry5.map(IND); q["fyear"] = year
    compute.firm_level = d[["industry5", "intensity"]]   # kept for the violin; not published
    return q


def plot(df):
    fig, ax = new_fig()
    fl = compute.firm_level
    groups = [fl.loc[fl.industry5 == i, "intensity"].to_numpy() for i in df.industry5]
    parts = ax.violinplot(groups, positions=range(len(groups)), showextrema=False, showmedians=False, widths=0.85)
    for body, c in zip(parts["bodies"], ["#1f4e79", "#c0392b", "#27ae60", "#e6a100"]):
        body.set_facecolor(c); body.set_edgecolor("none"); body.set_alpha(0.75)
    ax.scatter(range(len(groups)), df["mean"], marker="x", s=60, color="#7b1e1e", zorder=3, label="Mean")
    ax.set_xticks(range(len(groups))); ax.set_xticklabels(df.industry); ax.set_ylim(0, 1)
    ax.set_ylabel("Intangible assets / capital stock"); ax.set_xlabel("Fama-French industry")
    ax.set_title(f"Fiscal year {int(df.fyear.iloc[0])}; x marks the mean", loc="left")
    return fig


if __name__ == "__main__":
    df = compute(load_sample()); save(df, plot(df), "fig04")
