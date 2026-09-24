# Rebuilding the paper figures

**Figure 1.** Mean nominal R&D and CAPEX divided by immediately prior fiscal-year assets. Missing numerators become zero only when lagged assets are observed. The broad Compustat sample has no industry or acquisition screen. Pooled upper-tail winsorization precedes the start-year restriction; the auxiliary SG&A/assets series is also exported. Inputs: funda, company and the shared panel; reference: figure1data.dta. Validation: rdAssets: r=0.999994, MAE=0.000267, 0/47 years over 5% (1977–2023); capxAssets: r=0.999975, MAE=0.000179, 0/47 years over 5% (1977–2023).

**Figure 7.** Mean lagged (G2 + S2 + balance-sheet intangibles) divided by lagged (gross PPE + G2 + S2 + balance-sheet intangibles). Missing or negative balance-sheet intangibles become zero. Lags are computed on the full stocks history before the SIC and start-year screens. Stocks and nominal balance-sheet items use the stock panel CPI, without the market-sample CPI override. Other industries enter All but have no separate plotted line. Inputs: current stocks panel; reference: mainStocks.dta intensity2. Validation: intensity2 industry=1: r=0.998878, MAE=0.001152, 0/48 years over 5% (1977–2024); intensity2 industry=2: r=0.995313, MAE=0.001501, 1/48 years over 5% (1977–2024); intensity2 industry=3: r=0.997847, MAE=0.001666, 1/48 years over 5% (1977–2024); intensity2 industry=4: r=0.994268, MAE=0.002046, 1/48 years over 5% (1977–2024); intensity2 industry=6: r=0.999937, MAE=0.000653, 0/48 years over 5% (1977–2024).

**Figure 8.** Mean market equity/assets and market equity/(assets + G2 + S2), after SIC exclusions and target/acquirer deal-year removal. The numerator is mkvalt, with CRSP fallback, despite the paper legend saying market value of assets. SG&A has R&D stripped and the market-sample growth backfill is applied before deflation. Unadjusted pooled winsorization occurs before the start-year restriction; adjusted winsorization follows it. The small-PPE/nonpositive-sales flag is intentionally not a filter. Reference: the stored winsorized columns in dataForFigure8.dta. Validation: mb_win: r=0.999800, MAE=0.006447, 0/41 years over 5% (1977–2017); epw: r=0.999319, MAE=0.011615, 0/41 years over 5% (1977–2017).

**Figure 9.** Mean net income divided by lagged common equity for S&P membership years in the market sample. Adjusted income adds (R&D + gamma × cleaned SG&A − S2depr − G2depr) × (one minus marginal tax rate); adjusted equity adds G2 + S2. Negative common equity becomes missing. Membership and equity screens precede calendar-year lags, so exits, acquisition exclusions and re-entries create missing lags. Pooled winsorization is applied separately to each ROE series; the plotted difference is a mean of paired differences. Reference: colored-marker centers digitized from figure9.png; this is approximate image validation, not an exact numeric benchmark. Validation: roe_inc2: r=0.921889, MAE=0.012348, 12/46 years over 5% (1978–2023); roe_inc_epw2: r=0.884962, MAE=0.006414, 11/46 years over 5% (1978–2023); diffUnadj: r=0.896819, MAE=0.008928, 28/46 years over 5% (1978–2023).

## Reproduction

Public-safe plotted aggregates: `site/data/figNN.csv`; plots: `site/figures/out/figNN.svg`. Local-only sample, reference collapses and per-year validation: `data/figures_work/`. Scripts and this report are under `site/figures/`. All paths can be overridden with CLI options. Dependencies: python3, pandas, numpy, matplotlib.

```sh
python3 site/figures/sample.py
python3 site/figures/fig01_rd_capex.py
python3 site/figures/fig07_intensity.py
python3 site/figures/fig08_mb.py
python3 site/figures/fig09_roe.py
python3 site/figures/validate_figures.py
```

Validation does not pass merely because a correlation is high. Every relative discrepancy exceeding the requested threshold is listed in `data/figures_work/validation_by_year.csv`; systematic differences remain open until explained.

See [CODEX_REPORT.md](CODEX_REPORT.md) for ranked issues, numerical checks and deviations.
