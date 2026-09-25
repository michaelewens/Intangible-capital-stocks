# Pipeline: Compustat to EPW intangible capital stocks

Python port of the Stata builder used for Ewens, Peters and Wang (2023), restricted to the
paper's headline stocks. Verified against the October 2024 Stata run on identical inputs:
507,638 firm-years, correlation 1.000000, median relative difference below 1e-6.

## Files

| File | Role |
|---|---|
| `pull_inputs_local.py` | Dumps `funda`, `company`, `ccmlink` from the local WRDS snapshot (DuckDB) and the CPI deflator from FRED into `data/inputs/` |
| `epw_stocks.py` | Cleaning, imputation and perpetual-inventory accumulation. Writes `data/output/intangibleCapital_<tag>.csv`, `capital_accum_parameters.csv`, `build_stats.json` |
| `validate.py` | Compares a build with the Oct 2024 Stata run and the Sept 2023 public file |
| `founding_years.py` | Port of the Corporate hierarchy project's `processIPO.do`: combines four Ritter-derived files through a permno-gvkey bridge into one founding year and IPO year per gvkey. Writes `data/inputs/ipo_year.csv` |
| (local only) `data/inputs/founding/` | Founding-year inputs; not published |

## Run

For a release, `python3 release.py` at the repository root runs every step below plus the figures, the site build, and the release notes; `--publish` then commits, pushes, deploys, and tags. The manual steps are:

```bash
export FRED_API_KEY=...
python3 pipeline/pull_inputs_local.py
python3 pipeline/founding_years.py --bridge ccmlink
python3 pipeline/epw_stocks.py --tag YYYYMMDD
python3 pipeline/validate.py YYYYMMDD
```

`--inputs DIR --link-expanded` runs the builder on a hand-built input set (used for the
same-input verification against the Stata run).

## Method, in the order the code applies it

1. Compustat annual, standard screen (INDL, STD, D, C), latest `datadate` per gvkey-fiscal year.
2. Header SIC to modified Fama-French 5 industries (`industry5.do`).
3. Strip R&D (plus in-process R&D) from SG&A when R&D is not inside COGS.
4. Deflate flows to 1990 dollars with CPI-U (last quarter of each year).
5. Missing R&D set to zero from 1977 when assets are reported; pre-1977 zeros if the firm reported
   zero in 1977; missing SG&A set to zero when assets are reported; remaining gaps interpolated
   linearly within firm.
6. Firm age from the founding year in `ipo_year.csv` (Ritter sources combined as in the Corporate
   hierarchy project, keyed on gvkey), else min(first Compustat year, first price year minus 7).
   IPO year from the same file, else first price year. `--founding permno` restores the paper's
   original permno-keyed Ritter file.
7. Growth-rate constants for backfilling pre-sample flows are estimated on fiscal years through
   2017 (the paper's rule), by years-since-IPO for R&D and as a single pre-IPO mean for SG&A.
8. Perpetual inventory. Knowledge capital: industry depreciation from the paper, R&D as the flow.
   Organization capital: 20 percent depreciation, gamma times SG&A as the flow. Initial stocks
   assume steady growth since founding.
9. Output is nominal, net stocks for fiscal years from 1975.

Parameters (Oct 2023 estimates) are constants at the top of `epw_stocks.py`.

## Known differences from the Stata builder

- The Stata run kept an arbitrary row when a gvkey-year had both INDL and FS formats. The port
  keeps INDL only. This affects about 7 percent of firm-years, mostly financials.
- The Stata run deflated with the OECD CPI series on FRED (USACPALTT01IXNBQ), discontinued after
  2023. The port uses CPIAUCSL; the two agree within 0.4 percent over 1960-2023.
- The founding-year builder needs a permno-gvkey-fyear bridge. `--bridge crsp_cs` uses the Corporate
  hierarchy project's file (reproduces its output on all 13,758 firms it covers); `--bridge ccmlink`
  builds the bridge from the current CCM link history and covers 716 more firms.
