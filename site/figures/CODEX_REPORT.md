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
| 08 | mb_win | 1977–2017 | 0.998443 | 0.032053 | 6/41 |
| 08 | epw | 1977–2017 | 0.996010 | 0.018861 | 3/41 |
| 09 | roe_inc2 | 1978–2023 | 0.922594 | 0.012390 | 13/46 |
| 09 | roe_inc_epw2 | 1978–2023 | 0.883872 | 0.006290 | 10/46 |
| 09 | diffUnadj | 1978–2023 | 0.896095 | 0.009077 | 30/46 |

## Matched historical input audit

The same figure functions were also run on figure1data.dta plus the authors’ stored stocks, using the exact final acquisition file. This checks the translation independently of current inputs. The ROE curves visually coincide with the published PNG; differences are within the stated image-reading precision.

| Figure | Series | Correlation | Mean absolute difference |
|---|---|---:|---:|
| 08 | mb_win | 0.999013 | 0.038252 |
| 08 | epw | 0.998608 | 0.012592 |
| 09 | roe_inc2 | 0.999966 | 0.000386 |
| 09 | roe_inc_epw2 | 0.999697 | 0.000337 |
| 09 | diffUnadj | 0.999978 | 0.000300 |

The numerical Figure 8 reference ends in 2017; it does not certify later years in the PNG. Replaying the newer historical source inputs against that earlier stored intermediate is not an exact same-input comparison. On common firm-years, the raw market-to-book MAE is 0.004266 and the stored winsorized MAE is 0.033191. This discrepancy predates the current Compustat rebuild and cannot be labeled a port error or dismissed as zero.

S&P membership spells actually end on 2019-12-31. Flags afterward are artifacts of the preserved Stata multi-spell expansion. Current and author membership counts by year are recorded in diagnostics.json. The current fiscal-year tail contains 33 raw observations, so it is incomplete.

## Fidelity and deviations

Preserved: calendar-year lags; figure-specific samples; pooled winsorization; missing-value propagation; R&D-from-SG&A stripping; sequential growth backfill; the hard-coded market CPI override; delta raised to the year gap for depreciation; the ineffective ppent missing-value replacement; OLS trend lines. The paper end-year cap is removed as requested. Current data are not calibrated to make the old pictures match.

The final deal keys were found in the authors’ local estimation file and staged under data/figures_work/author_deals.csv. Target deduplication precedes the Philips acquirer merge. The supplied extracts were also checked against the exact final deal sequence. The acquisition screen is in place. Current CRSP links are joined at Compustat datadates, reduced to the latest date per permno/calendar year, then all multiply mapped gvkey-years are dropped. Link intervals are inclusive; date ties use stable link-start ordering. The supplied gvkey founding file replaces the original permno file as an input-vintage difference. Current mthcap is not used: market cap follows the Stata price-times-shares formula in millions.

## Open issues, ranked by severity and implementation cost

- **Severity High; implementation cost Low — S&P membership history is outdated.** The port retains the supplied membership history and reproduces the Stata multi-spell numbering bug. Post-coverage observations are artifacts of that bug, so these outputs cannot be represented as current S&P membership. Minimum fix: provide updated membership spells; correcting the expansion bug should be identified as a separate method change.
- **Severity Medium; implementation cost Medium — Market-to-book reference is an older intermediate.** The stored market-to-book panel ends earlier than the supplied figure sample and stock panel. The report includes raw-ratio and same-historical-source replay differences, so the early-year discrepancies are not certified as harmless vintage noise. Minimum fix: supply the figure sample and stocks from the exact run that wrote dataForFigure8.dta, or a newer dataForFigure8.dta matching the supplied figure sample.
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

Historical stock-panel tail counts (the final year is incomplete):
```json
{
  "2022.0": 12289,
  "2023.0": 12050,
  "2024.0": 288
}
```

Acquisition extract audit against the staged final file:
```json
{
  "rows": 19269,
  "deal_order_matches": true,
  "target_order_matches": true,
  "completion_order_matches": true
}
```

Current reconstructed CCM map versus the authors’ dated map (different input vintages):
```json
{
  "join_counts": {
    "both": 305905,
    "right_only": 75867,
    "left_only": 6708
  },
  "matched_key_disagreements": 251,
  "original_year_min": 1950,
  "original_year_max": 2024
}
```

Numerical regression checks passed for calendar gaps, pooled clipping, depreciation across gaps, intensity timing, missing numerator handling and membership-screen timing. Re-run with `python3 site/figures/check_ports.py`.
- Figure 1: exported 1977–2026; last nonmissing plotted year 2025.
- Figure 7: exported 1977–2025; last nonmissing plotted year 2025.
- Figure 8: exported 1977–2025; last nonmissing plotted year 2025.
- Figure 9: exported 1977–2025; last nonmissing plotted year 2025.

## Visual review

Inspected the supplied PNGs and the generated comparison plots. The investment crossover and declining CAPEX path agree; the market-to-book peaks and adjusted levels broadly agree. The industry intensity lines overlap closely until the final partial historical year. Current ROE differs materially, whereas the historical-input replay overlays the published ROE chart. Plain matplotlib defaults are retained in the SVGs. No PDFs were opened.

## Files and reproduction

Plotted aggregates: `site/data/figNN.csv`; plots: `site/figures/out/figNN.svg`. Local-only sample, reference collapses and per-year validation: `data/figures_work/`. Scripts and this report are under `site/figures/`. Sample, figure and validator paths have CLI overrides. Dependencies: python3, pandas, numpy, matplotlib. Figures extend to their latest eligible fiscal year; no empty year is filled with invented observations.

```sh
python3 site/figures/prepare_author_inputs.py
python3 site/figures/sample.py
python3 site/figures/fig01_rd_capex.py
python3 site/figures/fig07_intensity.py
python3 site/figures/fig08_mb.py
python3 site/figures/fig09_roe.py
python3 site/figures/diagnose_validation.py
python3 site/figures/validate_figures.py
```

Validation does not pass merely because a correlation is high. Every relative discrepancy exceeding the requested threshold is listed in `data/figures_work/validation_by_year.csv`; systematic differences remain open until explained.

## Missing inputs

- Missing from the current stocks panel: BEA G and S stocks for direct evaluation of the BEA-equity support screen. Historical support equivalence is checked above; EPW stock availability supplies the documented current support proxy.
- Missing from the supplied CRSPdsp500list.dta: membership spells after its final actual end date. Later flags are artifacts, as explained above.
