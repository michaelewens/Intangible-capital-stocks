"""Dump the pipeline inputs from the local WRDS snapshot (DuckDB) and FRED.

Writes to data/inputs/:
  funda.csv    - Compustat annual, standard screen (INDL/STD/D/C), one row per gvkey-fyear
  company.csv  - header SIC per gvkey
  ccmlink.csv  - CRSP/Compustat link history
  cpi.csv      - annual CPI deflator (last available quarter of each year, 1990 = 1)

Quarterly refresh: re-pull the DuckDB snapshot from WRDS (see _Data.md §7), then rerun this.
"""
import json, os, sys, urllib.request
from pathlib import Path
import duckdb, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "inputs"
DB = os.environ.get("WRDS_CCM_DUCKDB", "/Users/me2731/Dropbox/Research/wrds_ccm/wrds_ccm.duckdb")
FUNDA_COLS = ["cast(gvkey as int) as gvkey", "datadate", "cast(fyear as int) as fyear", "xrd", "xsga", "rdip", "cogs",
              '"at" as at', "prcc_f", "sich", "curcd",
              # extra columns for the website figures (site/figures/)
              "acqintan", "intan", "intano", "lt", "mkvalt", "ppent", "ppegt", "act", "dcpstk", "ao", "sale", "capx",
              "dp", "dpact", "ni", "oancf", "ceq", "csho", "dltt", "dlc", "pstk", "gdwl"]


def pull_compustat():
    con = duckdb.connect(DB, read_only=True)
    q = f"""
        select {", ".join(FUNDA_COLS)} from funda_std
        where fyear is not null
        qualify row_number() over (partition by gvkey, cast(fyear as int) order by datadate desc) = 1
    """
    con.sql(q).df().to_csv(OUT / "funda.csv", index=False)
    con.sql("select cast(gvkey as int) as gvkey, sic, conm from company").df().to_csv(OUT / "company.csv", index=False)
    con.sql("select cast(gvkey as int) as gvkey, lpermno, linkdt, linkenddt from ccmlink where lpermno is not null").df().to_csv(OUT / "ccmlink.csv", index=False)
    # CRSP monthly (for market cap fallback, annual returns, and the ROE figure), 1970 onward
    con.sql("""select permno, mthcaldt, mthcap, mthprc, shrout, mthret, mthretx from msf
               where mthcaldt >= '1970-01-01'""").df().to_csv(OUT / "msf.csv", index=False)
    meta = con.sql("select * from _meta").df()
    con.close()
    return meta


def pull_cpi():
    key = os.environ.get("FRED_API_KEY")
    if not key:
        sys.exit("FRED_API_KEY not set")
    url = ("https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL"
           f"&api_key={key}&file_type=json&frequency=q")
    obs = json.load(urllib.request.urlopen(url))["observations"]
    df = pd.DataFrame(obs)[["date", "value"]]
    df = df[df.value != "."].copy()
    df["value"] = df.value.astype(float)
    df["fyear"] = df.date.str[:4].astype(int)
    # Joe Choi's rule: last quarter available in each year, normalised to 1990
    cp = df.groupby("fyear").value.last()
    cp = cp / cp.loc[1990]
    cp.rename("cpidef").reset_index().to_csv(OUT / "cpi.csv", index=False)
    return cp.index.max()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    meta = pull_compustat()
    last = pull_cpi()
    f = pd.read_csv(OUT / "funda.csv", usecols=["gvkey", "fyear", "datadate"])
    print(f"funda rows {len(f)}, gvkeys {f.gvkey.nunique()}, fyear {f.fyear.min()}-{f.fyear.max()}, max datadate {f.datadate.max()}")
    print(f"cpi through {last}")
    print(meta.to_string(index=False))
