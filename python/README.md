# intangiblecapital

Load the Ewens, Peters and Wang (2024) knowledge and organization capital stocks for Compustat firms.

```bash
pip install intangiblecapital
```

```python
import intangiblecapital as ic
stocks = ic.load()                    # checks the manifest; downloads each release file once
stocks = ic.load(release="20260924")  # pin a release for reproducibility
params = ic.parameters()              # depreciation rates and gamma by SIC
merged = ic.merge_compustat(funda)    # attach stocks to your Compustat frame on gvkey, fyear
ic.releases()                         # what releases exist
```

`load()` returns these columns in order:

| Column | pandas dtype | Meaning |
| --- | --- | --- |
| `gvkey` | `Int64` (nullable integer) | Compustat firm identifier; no leading zeroes |
| `fyear` | `Int64` (nullable integer) | Fiscal year |
| `knowCapital` | `float64` | Net knowledge capital, nominal $ millions |
| `orgCapital` | `float64` | Net organization capital, nominal $ millions |
| `note` | `string` | Explanation if supplied; otherwise empty string |

Missing stocks are `NaN`, not zero. The historical `release="090123"` reads the
Stata file and returns the same schema, with empty notes because that file has none.
`stocks.attrs` records `release`, `release_date`, `source`, and `citation`.

Use `ic.merge_compustat(funda)` when your `gvkey` is an integer or a zero-padded
string such as `"001004"`. Fiscal years can be integers or whole-number floats such
as `2019.0`. The function preserves your input key columns and their dtypes, leaves
the input unchanged, and returns a new frame with a reset index. Missing keys do
not match; nonnumeric or fractional keys raise `ValueError`.
For other input column names, use `gvkey="firm_id", fyear="year"`.
The default `how="left"` keeps all input rows; `how="inner"` keeps only matches.
Other join types are not supported. Duplicate input keys are allowed; duplicate
stock keys raise `pandas.errors.MergeError`. Rename or remove existing
`knowCapital`, `orgCapital`, `note`, `_ic_gvkey`, or `_ic_fyear` columns before calling.
For a direct pandas merge, normalize both frames' `gvkey` and `fyear` to `Int64`.

Every unpinned `load()` fetches the small release manifest, so a new release becomes
available automatically. Each release file is cached at `~/.cache/intangiblecapital`;
set `INTANGIBLECAPITAL_CACHE` to choose another directory, or inspect `ic.cache_dir()`.
`load(release="20260924")` uses the cached manifest and file, checking online if the
tag is absent. A cached pin works offline; an unpinned load requires a reachable
manifest. `load(refresh=True)` re-downloads the manifest and selected file.
Pins assume the maintainer keeps each published release file unchanged.

`releases()` returns release dictionaries newest date first, including `tag`, `file`,
`date`, and other manifest metadata. Use `releases(refresh=False)` for the cached list.
`parameters()` returns the fixed 2023 parameter table, independent of the stock
release: `sic` (`Int64`, without leading zeroes), `knowDepr`, `organDepr`, `gamma`
(`float64` rates/shares), and `industry5` (`string`). Use `parameters(refresh=True)`
to re-download it. Parameter files do not update automatically.

Unknown release tags and invalid schemas raise `ValueError`; download failures
raise `OSError` with the URL and cache location. Retry with `refresh=True` if a
cached file is damaged. Failed downloads preserve any previous cached file.

Requires Python 3.9+ and pandas 1.5+. To run the offline smoke/regression tests from
a checkout, use `IC_LOCAL=1 python3 python/tests_smoke.py` at the repository root.
Set `IC_REPO_ROOT=/path/to/checkout` to read data elsewhere. Add `--build` to also
check wheel and source-distribution packaging using already-installed
`setuptools>=77` and `wheel`; no dependencies are downloaded. Build/publish tooling
must target the `python/` subdirectory, which contains `pyproject.toml` and its README.

Documentation, figures and the LLM prompt: https://intangiblesdata.org. Method and code:
https://github.com/michaelewens/Intangible-capital-stocks.

Citation: Ewens, Michael, Ryan Peters and Sean Wang. "Measuring Intangible Capital with Market
Prices." *Management Science* 71.1 (2024): 407-427. https://doi.org/10.1287/mnsc.2021.02058

License: the package code is MIT. The data it downloads are released under Creative Commons Attribution-NonCommercial 4.0 (see license.md in the repository); cite the paper when you use them.
