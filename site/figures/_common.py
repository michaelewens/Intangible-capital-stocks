"""Shared helpers for the website figures. Sample columns come from site/figures/sample.py."""
from pathlib import Path
import pandas as pd
import style  # noqa: F401  (shared rcParams)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "data" / "figures_work" / "sample.csv"
DATA_OUT = ROOT / "site" / "data"
SVG_OUT = ROOT / "site" / "figures" / "out"
IND = {1: "Consumer", 2: "Manufacturing", 3: "High Tech", 4: "Healthcare", 5: "Other", 6: "All"}


def load_sample():
    return pd.read_csv(SAMPLE)


def save(df, fig, name):
    DATA_OUT.mkdir(parents=True, exist_ok=True); SVG_OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_OUT / f"{name}.csv", index=False)
    fig.savefig(SVG_OUT / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {name}: {len(df)} rows")


def new_fig():
    return plt.subplots(figsize=(9, 5))

# Columns the site's own figures (fig02, fig03, fig04) expect in sample.csv, in addition to what the
# paper figures need: gvkey fyear industry5 at ppegt_nom prcc_f csho dltt dlc dcpstk targetYear acqYear
# knowCapital_nom orgCapital_nom (nominal $M) intensity (Figure 7 definition, firm-year).
