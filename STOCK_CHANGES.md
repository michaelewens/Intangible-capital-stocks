# Why historical stocks change between releases

Each release rebuilds every firm-year from the current Compustat file with the paper's parameter
estimates, which do not change. The inputs do change: Compustat restates past financials, revises a
firm's header industry code, and adds or re-dates firm-years; the deflator series is revised; and the
founding-year data are refreshed. Because each stock is a weighted sum of a firm's whole history,
an input change in one year moves the stock in every later year. This note reports how much the
September 2026 release differs from the September 2023 file and what drives the differences.

## How different are the two releases?

The two files share 422,328 firm-years (fiscal 1975 to 2019).

| | Knowledge capital | Organization capital |
|---|---|---|
| Same within 0.1 percent | 78.0% | 37.2% |
| Differ by more than 1 percent | 3.1% | 11.2% |

Most of the rest move by a fraction of a percent. Larger moves, above 5 percent in either stock, occur
in 13,654 firm-years belonging to 1,806 firms.

The differences are a property of the inputs, not of the new code. Running the paper's original Stata
code on a September 2024 Compustat pull produces the same pattern against the 2023 file (78.4 percent
and 37.3 percent identical within 0.1 percent). The Python code in `pipeline/` reproduces that Stata
run exactly on identical inputs.

## What drives the large changes

Three independent reviews (three different AI models, each given the same ten randomly drawn
firm-years with the full firm histories from the 2023, 2024 and 2026 builds) reached the same
conclusion on all ten cases: the firm's Fama-French industry assignment changed. The paper's method
assigns industry from the firm's current Compustat header SIC code, a single code per firm that
Compustat revises over time. A new code moves the firm to a different industry, which changes its
R&D depreciation rate and its SG&A investment share, and so rescales both stocks from the firm's
first year onward. In the ten cases this one input explained 87 to 108 percent of the change; the
deflator and the growth constants explained the small remainder, usually in the opposite direction.

Across all 34,998 firms in both files, 2,190 changed industry between the 2023 and 2026 builds:

* 1,438 had no header SIC in the 2023 Compustat pull and were assigned to "Other" by default (3,838
  firms were in that position in 2023). They now carry their actual industry.
* 752 have a different header SIC in the June 2026 file than in the 2023 file.

Those 2,190 firms account for 12,968 of the 13,654 firm-years that move by more than 5 percent.

The remaining 686 firm-years belong to 232 firms. For 64 percent of those firms the founding year
changed (the founding-year data now combine several Ritter files rather than one), for 34 percent
Compustat restated SG&A in a year before the case year, and for 10 percent the firm's first Compustat
year moved. Fourteen of the 232 firms show none of these and are not resolved.

## The ten examples

Published (September 2023) versus rebuilt (September 2026) values, nominal millions.

| gvkey | Fiscal year | Header SIC, 2023 to 2026 | Industry, 2023 to 2026 | Knowledge, old to new | Organization, old to new |
|---|---|---|---|---|---|
| 4321 | 1995 | 3600 to 3823 | Manuf. to High-tech | 645.7 to 750.0 | 1425.7 to 2502.4 |
| 7092 | 1993 | 3571 to 6500 | High-tech to Other | 75.9 to 90.2 | 103.3 to 61.1 |
| 7882 | 2003 | 5093 to 7359 | Consumer to Other | 0.0 to 0.0 | 6.1 to 6.7 |
| 11300 | 1996 | 4888 to 8200 | High-tech to Other | 0.0 to 0.0 | 729.6 to 433.5 |
| 12304 | 1990 | 7363 to 8090 | Other to Consumer | 0.6 to 0.5 | 1.6 to 1.5 |
| 21138 | 2015 | missing to 7370 | Other to High-tech | 44.5 to 40.3 | 24.4 to 41.0 |
| 25749 | 2012 | 7363 to 7370 | Other to High-tech | 0.0 to 0.0 | 165.0 to 277.5 |
| 27301 | 2014 | 100 to 1040 | Consumer to Other | 0.0 to 0.0 | 1.0 to 1.1 |
| 160592 | 2006 | 2990 to 6794 | Manuf. to Other | 0.6 to 0.7 | 2.4 to 2.5 |
| 217200 | 2004 | 7812 to 5961 | Other to Consumer | 1.2 to 1.1 | 52.4 to 47.8 |

Firms 4321 and 7092 show the mechanism most clearly. Their R&D and SG&A histories are the same in
every vintage. Only the industry code changed, and with it the depreciation rate and the SG&A share
applied to every year since the 1970s.

## Smaller drifts

Two inputs move almost every firm-year by a fraction of a percent.

* Deflator. The 2023 file used an OECD consumer price series that was discontinued after 2023. The
  current build uses the BLS CPI-U series (FRED code CPIAUCSL), which agrees with the old series within
  0.4 percent over 1960 to 2023.
* Growth constants. The rates used to backfill flows before a firm's first observation are estimated
  on fiscal years through 2017, as in the paper. Restated pre-2017 data move them slightly (the R&D
  rate 0.3461 in 2023, 0.3446 in 2026; the SG&A rate 0.3334 in 2023, 0.3280 in 2026).

## Practical advice

Cite the release date of the file you use, and keep a copy. The previous file remains in this
repository. If a project needs a fixed industry assignment across releases, the header SIC used for
each firm is not in the release file; the code in `pipeline/` shows where it is taken from, and a user
can substitute a fixed code there.
