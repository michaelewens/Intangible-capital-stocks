"""Figure 2 (site): aggregate knowledge capital, organization capital and gross PP&E by fiscal year,
nominal $ billions, across the figure sample (paper's screens). Not in the paper."""
import numpy as np, pandas as pd
from _common import load_sample, save, new_fig


def compute(s):
    d = s.copy(); d["knowCapital_nom"] = d.G2 * d.cpidef; d["orgCapital_nom"] = d.S2 * d.cpidef; d["ppegt_nom"] = d.ppegt.fillna(0)
    d = d[d.fyear >= 1977].dropna(subset=["knowCapital_nom", "orgCapital_nom"])
    g = d.groupby("fyear")[["knowCapital_nom", "orgCapital_nom", "ppegt_nom"]].sum() / 1000
    g.columns = ["knowledge_bn", "organization_bn", "ppegt_bn"]
    g["n_firms"] = d.groupby("fyear").gvkey.nunique()
    return g.reset_index()


def plot(df):
    fig, ax = new_fig()
    ax.plot(df.fyear, df.ppegt_bn, label="Gross PP&E", color="#9a9a9a", ls="--")
    ax.plot(df.fyear, df.organization_bn, label="Organization capital", color="#1f4e79")
    ax.plot(df.fyear, df.knowledge_bn, label="Knowledge capital", color="#c0392b")
    ax.set_xlabel("Fiscal year"); ax.set_ylabel("$ billions, nominal"); ax.legend(frameon=False)
    return fig


if __name__ == "__main__":
    df = compute(load_sample()); save(df, plot(df), "fig02")
