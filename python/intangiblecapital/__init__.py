"""Ewens, Peters and Wang (2024) intangible capital stocks for Compustat firms.

    import intangiblecapital as ic
    stocks = ic.load()                     # checks the manifest; downloads each release file once
    stocks = ic.load(release="20260924")   # a specific release, for reproducibility
    params = ic.parameters()               # depreciation rates and gamma by 4-digit SIC
    merged = ic.merge_compustat(funda)     # your Compustat frame with gvkey and fyear, stocks attached
    available = ic.releases()              # release dictionaries, newest date first

Columns of the stock file: gvkey, fyear, knowCapital, orgCapital, note (see ic.COLUMNS).
gvkey and fyear have pandas nullable Int64 dtype, stocks are float64 (NaN means
missing), and note is pandas string (empty when no note is supplied). Dollar
amounts are net stocks in nominal millions. Use merge_compustat for integer or
zero-padded string gvkeys and whole-number fiscal years, including 2019.0.
It preserves your key columns and their dtypes; missing keys do not match.
For a direct merge, normalize both frames' keys to Int64 first.

load() checks the online manifest every call, so new releases appear automatically.
Pinned releases reuse the cached manifest, checking online if the tag is absent.
load(refresh=True) downloads again. A cached pin works offline; an unpinned load
requires the manifest to be reachable. Cache: ~/.cache/intangiblecapital, overridden
by INTANGIBLECAPITAL_CACHE. Use releases(refresh=False) for the cached release list.
parameters() returns sic (Int64), knowDepr/organDepr/gamma (float64), industry5
(string), from the fixed 2023 parameter file; parameters(refresh=True) downloads it
again. The historical 090123 Stata release is supported, with empty notes.
Citation: Ewens, Peters and Wang, "Measuring Intangible Capital with Market Prices,"
Management Science 71.1 (2024): 407-427. https://doi.org/10.1287/mnsc.2021.02058
Site and documentation: https://intangiblesdata.org
"""
from __future__ import annotations

import json
import os
import urllib.request
from http.client import HTTPException
from pathlib import Path

import pandas as pd

__version__ = "2026.9.24"
__all__ = ["load", "parameters", "releases", "merge_compustat", "cache_dir", "COLUMNS", "CITATION"]

REPO_RAW = "https://github.com/michaelewens/Intangible-capital-stocks/raw/master/"
RELEASES_URL = REPO_RAW + "releases.json"
PARAMS_FILE = "capital_accum_parameters_2023.csv"

COLUMNS = {
    "gvkey": "Compustat firm identifier (nullable Int64, no leading zeroes)",
    "fyear": "fiscal year (nullable Int64)",
    "knowCapital": "knowledge capital stock, net, nominal $ millions (capitalized R&D)",
    "orgCapital": "organization capital stock, net, nominal $ millions (capitalized share of SG&A)",
    "note": "explanation of missing/interpolated stocks if supplied; empty when no note (including legacy data)",
}
CITATION = ('Ewens, Michael, Ryan Peters and Sean Wang. "Measuring Intangible Capital with Market Prices." '
            "Management Science 71.1 (2024): 407-427. https://doi.org/10.1287/mnsc.2021.02058")


def cache_dir() -> Path:
    """Where downloaded files are kept. Override with the INTANGIBLECAPITAL_CACHE environment variable."""
    d = Path(os.environ.get("INTANGIBLECAPITAL_CACHE", Path.home() / ".cache" / "intangiblecapital"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _fetch(name: str, refresh: bool = False) -> Path:
    """Download a repository file into the cache once; return its local path."""
    target = cache_dir() / name
    if refresh or not target.exists():
        req = urllib.request.Request(REPO_RAW + name, headers={"User-Agent": f"intangiblecapital/{__version__}"})
        temporary = target.with_name(target.name + ".tmp")
        try:
            with urllib.request.urlopen(req, timeout=120) as r, open(temporary, "wb") as f:
                f.write(r.read())
            temporary.replace(target)
        except (OSError, HTTPException) as exc:
            raise OSError(f"Could not download {REPO_RAW + name} to {target}: {exc}. "
                          "Check the connection and cache permissions, then retry.") from exc
        finally:
            temporary.unlink(missing_ok=True)
    return target


def releases(refresh: bool = True) -> list[dict]:
    """Release dictionaries, newest date first (tag, file, date, and metadata).

    Fetch the manifest every call unless refresh=False and a cached copy exists.
    File formats include CSV and Stata; pass a tag unchanged to load(release=tag).
    """
    p = _fetch("releases.json", refresh=refresh)
    try:
        entries = json.loads(p.read_text())["releases"]
        if not isinstance(entries, list) or not entries:
            raise ValueError("expected a nonempty releases list")
        for entry in entries:
            for field in ("tag", "file", "date"):
                if not isinstance(entry[field], str) or not entry[field]:
                    raise ValueError(f"expected a nonempty {field} string")
        return sorted(entries, key=lambda r: r["date"], reverse=True)
    except (ValueError, KeyError, TypeError) as exc:
        raise ValueError(f"Invalid release manifest at {p}: {exc}. "
                         "Retry releases(refresh=True).") from exc


def load(release: str | None = None, refresh: bool = False) -> pd.DataFrame:
    """Return the stock file as a DataFrame with columns gvkey, fyear, knowCapital, orgCapital, note.

    gvkey/fyear: nullable Int64; knowCapital/orgCapital: float64 (NaN for missing);
    note: pandas string, empty if no note. Stocks are net, nominal $ millions.
    release: a tag such as "20260924" or "090123"; None checks the manifest online
    for the newest release each call. Files are cached after the first download;
    refresh=True re-downloads the manifest and file. A cached pin works offline.
    attrs contains release, release_date, source, citation. Cache location:
    cache_dir(), overridden by INTANGIBLECAPITAL_CACHE. Invalid tags/schema raise
    ValueError; download failures raise OSError with the URL and cache path.
    """
    rel = releases(refresh=refresh or release is None)
    if release is None:
        entry = rel[0]
    else:
        match = [r for r in rel if r["tag"] == str(release)]
        if not match and not refresh:
            rel = releases(refresh=True)
            match = [r for r in rel if r["tag"] == str(release)]
        if not match:
            raise ValueError(f"unknown release {release!r}; available: {[r['tag'] for r in rel]}")
        entry = match[0]
    p = _fetch(entry["file"], refresh=refresh)
    try:
        if p.suffix == ".dta":
            df = pd.read_stata(p, convert_categoricals=False)
            if "note" not in df:
                df["note"] = ""
        elif p.suffix == ".csv":
            df = pd.read_csv(p, dtype={"note": "string"})
        else:
            raise ValueError(f"unsupported file format {p.suffix!r}")
        if "rows" in entry and len(df) != entry["rows"]:
            raise ValueError(f"expected {entry['rows']} rows, got {len(df)}")
        df = df[list(COLUMNS)].astype({"gvkey": "Int64", "fyear": "Int64",
                                      "knowCapital": "float64", "orgCapital": "float64", "note": "string"})
        if df[["gvkey", "fyear"]].isna().any().any():
            raise ValueError("stock identifiers must not be missing")
        df["note"] = df["note"].fillna("")
    except (ValueError, TypeError, KeyError, OverflowError) as exc:
        raise ValueError(f"Invalid stock file for release {entry['tag']} at {p}: {exc}. "
                         "Retry load with refresh=True.") from exc
    df.attrs.update(release=entry["tag"], release_date=entry.get("date"), source=REPO_RAW + entry["file"], citation=CITATION)
    return df


def parameters(refresh: bool = False) -> pd.DataFrame:
    """Fixed 2023 parameters by SIC: sic (Int64), knowDepr, organDepr, gamma
    (float64 annual depreciation rates/investment share), industry5 (string).
    Cached after the first download; refresh=True downloads again. SIC codes are
    numeric, so leading zeroes are not retained. This table is not release-specific.
    """
    p = _fetch(PARAMS_FILE, refresh=refresh)
    dtypes = {"sic": "Int64", "knowDepr": "float64", "organDepr": "float64",
              "gamma": "float64", "industry5": "string"}
    try:
        return pd.read_csv(p)[list(dtypes)].astype(dtypes)
    except (ValueError, TypeError, KeyError, OverflowError) as exc:
        raise ValueError(f"Invalid parameters at {p}: {exc}. "
                         "Retry parameters(refresh=True).") from exc


def merge_compustat(funda: pd.DataFrame, release: str | None = None, gvkey: str = "gvkey", fyear: str = "fyear",
                    how: str = "left") -> pd.DataFrame:
    """Attach knowCapital, orgCapital, note on (gvkey, fyear), preserving input keys
    and dtypes. gvkey may be integer or zero-padded string; fyear may be an integer
    or whole-number float (2019.0). Missing keys remain unmatched; nonnumeric or
    fractional keys raise ValueError. Input is not mutated; the index is reset.

    gvkey/fyear name the input key columns. how is 'left' (keep every input row)
    or 'inner' (matched rows only). Duplicate input keys are allowed; duplicate
    stock keys raise pandas.errors.MergeError. Existing stock columns or reserved
    _ic_gvkey/_ic_fyear columns raise ValueError to avoid overwriting data.
    release pins a tag; None checks online for the current release (see load).
    """
    if how not in ("left", "inner"):
        raise ValueError("how must be 'left' or 'inner' when attaching stocks to Compustat")
    if gvkey == fyear or not funda.columns.is_unique:
        raise ValueError("Compustat requires distinct key names and unique column labels")
    missing = {gvkey, fyear} - set(funda.columns)
    if missing:
        raise ValueError(f"Compustat is missing key columns: {sorted(missing)}")
    conflicts = set(funda.columns) & {"knowCapital", "orgCapital", "note", "_ic_gvkey", "_ic_fyear"}
    if conflicts:
        raise ValueError(f"Rename or remove conflicting Compustat columns before merging: {sorted(conflicts)}")
    out = funda.copy()
    try:
        key = pd.to_numeric(out[gvkey], errors="raise").astype("Int64")
        yr = pd.to_numeric(out[fyear], errors="raise").astype("Int64")
    except (ValueError, TypeError, OverflowError) as exc:
        raise ValueError(f"Compustat {gvkey!r} and {fyear!r} must contain whole-number "
                         "numeric identifiers or missing values.") from exc
    out["_ic_gvkey"], out["_ic_fyear"] = key, yr
    stocks = load(release)
    stocks = stocks.rename(columns={"gvkey": "_ic_gvkey", "fyear": "_ic_fyear"})
    out = out.merge(stocks, on=["_ic_gvkey", "_ic_fyear"], how=how, validate="many_to_one")
    return out.drop(columns=["_ic_gvkey", "_ic_fyear"])
