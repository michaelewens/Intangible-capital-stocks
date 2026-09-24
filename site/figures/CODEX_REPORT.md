# Figure ports: run report

Shared panel: 599,379 firm-years; latest fiscal year 2026. Results below were computed by this run. Absolute differences use chart ratio units; multiply ROE differences by 100 for percentage points.

| Figure | Series | Years | Correlation | Mean absolute difference | Years over 5% |
|---|---|---|---:|---:|---:|
| 01 | rdAssets | 1977–2023 | 0.999994 | 0.000267 | 0/47 |
| 01 | capxAssets | 1977–2023 | 0.999975 | 0.000179 | 0/47 |
| 07 | intensity2 industry=1 | 1977–2024 | 0.998878 | 0.001152 | 0/48 |
| 07 | intensity2 industry=2 | 1977–2024 | 0.995313 | 0.001501 | 1/48 |
| 07 | intensity2 industry=3 | 1977–2024 | 0.997847 | 0.001666 | 1/48 |
| 07 | intensity2 industry=4 | 1977–2024 | 0.994268 | 0.002046 | 1/48 |
| 07 | intensity2 industry=6 | 1977–2024 | 0.999937 | 0.000653 | 0/48 |
| 08 | mb_win | 1977–2017 | 0.999800 | 0.006447 | 0/41 |
| 08 | epw | 1977–2017 | 0.999319 | 0.011615 | 0/41 |
| 09 | roe_inc2 | 1978–2023 | 0.921889 | 0.012348 | 12/46 |
| 09 | roe_inc_epw2 | 1978–2023 | 0.884962 | 0.006414 | 11/46 |
| 09 | diffUnadj | 1978–2023 | 0.896819 | 0.008928 | 28/46 |

## Fidelity and deviations

Preserved: calendar-year lags; figure-specific samples; pooled winsorization; missing-value propagation; R&D-from-SG&A stripping; sequential growth backfill; the hard-coded market CPI override; delta raised to the year gap for depreciation; the ineffective ppent missing-value replacement; OLS trend lines. The paper end-year cap is removed as requested. Current data are not calibrated to make the old pictures match.

## Open issues, ranked by severity and implementation cost

- **Severity High; implementation cost Medium — Exact current-vintage CRSP map unavailable.** The supplied ccmlink.csv is a history of link intervals; the Stata uses a datadate-expanded CRSP_COMP_Linkfile2024.dta map. The port uses inclusive link calendar years and the latest link start to resolve permno-year overlaps, then drops all multiply mapped gvkey-years. Minimum fix: supply the same datadate-expanded map for a fully matched mapping audit.
- **Severity High; implementation cost Low — S&P history may stop before the Compustat panel.** The port retains the supplied membership history and reproduces the Stata multi-spell numbering bug. It never labels later nonmembers as members merely to extend the curve. Minimum fix: provide membership spells covering the requested latest year; if correcting the Stata bug, publish that as a separate method change.
- **Severity Medium; implementation cost Medium — Acquisition extracts precede the final estimation sample.** Completion years are recovered only after checking identical full deal-ID sequences in targetData.dta and acqData.dta, consistent with their consecutive preserve/save blocks. Target deduplication precedes the Philips acquirer merge. However, runPrereqs.do points the figure program to data/estimation/data_for_estimation_v4.dta, not these earlier extracts. Exact final deal selection and duplicate survivor order cannot be certified from the supplied extracts. Minimum fix: supply YearCompletedUnconditional, tgt_gvkey and sdc_dealno from that final estimation file.
- **Severity Medium; implementation cost Low — Upstream stock vintage and founding differences.** The existing stock builder uses current INDL Compustat, a current CPI series and gvkey-based founding years. Those inputs differ from the authors’ original run. No pipeline code was changed. Minimum fix: run these figure programs on identical vintage inputs before attributing discrepancies exclusively to the translation.
- **Severity Medium; implementation cost Low — BEA equity support screen.** Current stocks contain EPW stocks only. The port uses common nonmissing G2/S2 support for the otherwise unplotted BEA-equity screen. Historical support mismatches and negative BEA stocks are reported below. Minimum fix for strict certification: provide current G and S alongside the EPW panel.
- **Severity Low; implementation cost Low — Image-only ROE reference.** PNG marker centers are calibrated to inspected axes; estimated digitization uncertainty is about 0.0015 ROE. Minimum fix: obtain the authors’ collapsed ROE series for an exact comparison.

## Independent formula checks

```json
{
  "G2depr_mae": 3.6941537856192213e-07,
  "S2depr_mae": 6.427506053774614e-07,
  "intensity_formula_mae": 1.2048571118245217e-08,
  "bea_epw_stock_support_mismatches": 0,
  "negative_bea_stocks": 0
}
```

## Coverage

```json
{
  "rows": 599379,
  "first_year": 1950,
  "latest_year": 2026,
  "market_rows": 358288,
  "stock_rows": 359692,
  "target_rows": 51,
  "acquirer_rows": 1391,
  "sp500_last_year": 2025
}
```
- Figure 1: exported 1977–2026; last nonmissing plotted year 2025.
- Figure 7: exported 1977–2025; last nonmissing plotted year 2025.
- Figure 8: exported 1977–2025; last nonmissing plotted year 2025.
- Figure 9: exported 1977–2025; last nonmissing plotted year 2025.

## Files and reproduction

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
