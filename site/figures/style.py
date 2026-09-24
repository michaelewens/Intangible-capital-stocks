"""Shared chart style for intangiblesdata.org figures (imported by common.py and _common.py)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PALETTE = {"know": "#c0392b", "org": "#1f4e79", "phys": "#7f8c8d", "ind": ["#1f4e79", "#c0392b", "#27ae60", "#e6a100", "#6c3483", "#333333"]}
plt.rcParams.update({
    "figure.figsize": (9, 5), "figure.dpi": 100, "savefig.bbox": "tight", "svg.fonttype": "none",
    "font.family": "sans-serif", "font.size": 11, "axes.titlesize": 11, "axes.labelsize": 11,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#888888", "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": "#e6e6e6", "grid.linewidth": 0.6, "axes.axisbelow": True,
    "xtick.color": "#444444", "ytick.color": "#444444", "legend.frameon": False,
    "lines.linewidth": 1.8, "lines.markersize": 3.5,
    "axes.prop_cycle": matplotlib.cycler(color=PALETTE["ind"]),
})
