#!/usr/bin/env python3
"""One-command release for the intangible capital stocks.

    python3 release.py                 # build everything for today's tag, stop before publishing
    python3 release.py --publish       # ... then commit, push, deploy the site, create the GitHub release
    python3 release.py --tag 20261215  # explicit tag (YYYYMMDD)
    python3 release.py --skip-figures  # data only (not with --publish)

Before running: back up the local WRDS snapshot, then refresh it (needs a Duo approval, run it yourself):
    caffeinate -is ~/.venvs/wrds/bin/python ~/Dropbox/Research/wrds_ccm/build_wrds_ccm.py --force
and have FRED_API_KEY in the environment (the CPI deflator comes from FRED).

Steps: preflight -> pull inputs -> founding years -> stocks -> copy release file -> archive this release's
inputs -> change check against the previous release (pipeline/change_check.py; stops the release on a
failed reproduction or an unexplained change) -> compare -> update releases.json, README, RELEASES.md,
site/build.py -> S&P 500 list -> figures -> diagnostics -> validation -> site build
-> (publish) commit, push, wrangler deploy, gh release. --publish reruns every step, so the check
always covers what is published.
"""
import argparse, json, os, re, shutil, subprocess, sys
from datetime import date, datetime
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
PY = sys.executable
SNAPSHOT = Path(os.environ.get("WRDS_CCM_DUCKDB", "/Users/me2731/Dropbox/Research/wrds_ccm/wrds_ccm.duckdb"))
MAX_SNAPSHOT_AGE_DAYS = 45
ARCHIVE = Path(os.environ.get("RELEASE_INPUTS", Path.home() / "Dropbox/projects/Research/Intangible Capital Data/release_inputs"))
ARCHIVED = ["funda.csv", "company.csv", "ccmlink.csv", "cpi.csv", "ipo_year.csv"]   # everything epw_stocks.py reads
SP500_DTA = ROOT / "data" / "inputs" / "figures" / "CRSPdsp500list.dta"
FIGS = ["fig01_rd_capex", "fig02_stocks_vs_ppe", "fig03_r2_gain", "fig04_cross_section", "fig07_intensity", "fig08_mb", "fig09_roe"]


def run(cmd, cwd=ROOT, **kw):
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    subprocess.run([str(c) for c in cmd], cwd=cwd, check=True, **kw)


def step(msg):
    print(f"\n== {msg}")


def preflight(allow_stale):
    step("preflight")
    if not os.environ.get("FRED_API_KEY"):
        sys.exit("FRED_API_KEY is not set (eval \"$(grep -E '^export FRED_API_KEY=' ~/.zshrc)\")")
    import duckdb
    con = duckdb.connect(str(SNAPSHOT), read_only=True)
    pulled = con.sql("select max(pulled_at) from _meta").fetchone()[0]
    asof = con.sql("select max(datadate) from funda").fetchone()[0]
    crsp_asof = con.sql("select max(mthcaldt) from msf").fetchone()[0]
    con.close()
    age = (datetime.now(pulled.tzinfo) - pulled).days
    print(f"  snapshot pulled {pulled.date()} ({age} days ago), funda datadate through {asof}, CRSP monthly through {crsp_asof}")
    if age > MAX_SNAPSHOT_AGE_DAYS and not allow_stale:
        sys.exit(f"snapshot is {age} days old; refresh it first (see docstring) or pass --allow-stale")
    return str(asof)[:10], str(crsp_asof)[:10]


def sp500_list():
    """S&P 500 membership spells for the ROE figure, from the snapshot's CRSP dsp500list_v2 (crspq)."""
    import duckdb
    con = duckdb.connect(str(SNAPSHOT), read_only=True)
    v = con.sql("select permno, mbrstartdt, mbrenddt from dsp500list_v2").df()
    con.close()
    out = pd.DataFrame({"permno": v.permno.astype(float), "start": pd.to_datetime(v.mbrstartdt),
                        "ending": pd.to_datetime(v.mbrenddt)}).sort_values(["permno", "start"])
    if out.isna().any().any() or (out.ending < out.start).any():
        sys.exit("S&P 500 list: missing or out-of-order membership dates in dsp500list_v2")
    out.to_stata(SP500_DTA, write_index=False, convert_dates={"start": "td", "ending": "td"})
    print(f"  {len(out):,} membership spells through {out.ending.max().date()}")


def compare(new_csv, old_file):
    """Share of shared firm-years whose stocks are unchanged / changed, new vs previous release."""
    new = pd.read_csv(new_csv)
    old = pd.read_stata(old_file) if str(old_file).endswith(".dta") else pd.read_csv(old_file)
    for d in (new, old):
        d["gvkey"] = pd.to_numeric(d.gvkey).astype(int); d["fyear"] = pd.to_numeric(d.fyear).astype(int)
    m = old.merge(new, on=["gvkey", "fyear"], suffixes=("_old", "_new"))
    out = {"shared_firm_years": int(len(m)), "new_firm_years": int(len(new) - len(m)),
           "dropped_firm_years": int(len(old) - len(m))}
    for v in ["knowCapital", "orgCapital"]:
        a, b = m[f"{v}_old"], m[f"{v}_new"]; both = a.notna() & b.notna()
        rel = (b - a).abs() / a.abs().clip(lower=1e-9); tiny = (a.abs() <= 1) & (b.abs() <= 1)
        out[f"{v}_same_within_0.1pct"] = round(float(((rel <= 1e-3) | tiny)[both].mean()), 4)
        out[f"{v}_changed_over_1pct"] = round(float(((rel > .01) & ~tiny)[both].mean()), 4)
        out[f"{v}_changed_over_5pct"] = round(float(((rel > .05) & ~tiny)[both].mean()), 4)
    return out


def update_text_files(tag, facts, cmp, prev):
    step("update releases.json, README.md, RELEASES.md, site/build.py")
    man_p = ROOT / "releases.json"; man = json.load(open(man_p))
    old = next((r for r in man["releases"] if r["tag"] == tag), {})   # a rerun keeps fields added by hand
    entry = {**old, "tag": tag, "date": facts["date"], "file": facts["file"], "compustat_asof": facts["asof"],
             "crsp_asof": facts["crsp_asof"], "fyear_min": facts["fy_min"], "fyear_max": facts["fy_max"], "rows": facts["rows"]}
    man["releases"] = sorted([r for r in man["releases"] if r["tag"] != tag] + [entry], key=lambda r: r["date"])
    json.dump(man, open(man_p, "w"), indent=2); print("  releases.json updated")

    # README: the block between the markers is regenerated
    p = ROOT / "README.md"; s = p.read_text()
    block = (f"<!-- release:begin -->\nCurrent release: [`{facts['file']}`]({facts['file']}). One row per Compustat firm and "
             f"fiscal year, {facts['rows']:,} firm-years, {facts['firms']:,} firms, fiscal years {facts['fy_min']} to "
             f"{facts['fy_max']}, built from Compustat as of {facts['asof_long']}.\n<!-- release:end -->")
    if "<!-- release:begin -->" in s:
        s = re.sub(r"<!-- release:begin -->.*?<!-- release:end -->", block, s, flags=re.S)
    else:
        s = re.sub(r"Current release: \[`intangibleCapital_\d+\.csv`\].*?Columns:", block + " Columns:", s, count=1, flags=re.S)
    s = re.sub(r"intangibleCapital_\d{8}\.csv", facts["file"], s)
    p.write_text(s); print("  README.md updated")

    # RELEASES.md: prepend an entry (numbers computed above, never typed)
    p = ROOT / "RELEASES.md"
    head = "# Release notes\n\nEach entry is written by `release.py` from the comparison of the new file with the previous release. Shares are over firm-years present in both files.\n\n"
    body = p.read_text()[len(head):] if p.exists() and p.read_text().startswith(head) else (p.read_text() if p.exists() else "")
    body = re.sub(rf"## {tag} \(.*?\)\n.*?(?=## |\Z)", "", body, flags=re.S)   # rerun of the same tag replaces its entry
    entry_md = (f"## {tag} ({facts['date']})\n\n"
                f"* File: `{facts['file']}`, {facts['rows']:,} firm-years, {facts['firms']:,} firms, fiscal {facts['fy_min']}-{facts['fy_max']}, Compustat as of {facts['asof']}.\n"
                f"* Versus {prev['tag']}: {cmp['shared_firm_years']:,} shared firm-years, {cmp['new_firm_years']:,} new, {cmp['dropped_firm_years']:,} no longer present.\n"
                f"* Knowledge capital: {cmp['knowCapital_same_within_0.1pct']:.1%} unchanged within 0.1%, {cmp['knowCapital_changed_over_1pct']:.1%} changed by more than 1%, {cmp['knowCapital_changed_over_5pct']:.1%} by more than 5%.\n"
                f"* Organization capital: {cmp['orgCapital_same_within_0.1pct']:.1%} unchanged within 0.1%, {cmp['orgCapital_changed_over_1pct']:.1%} changed by more than 1%, {cmp['orgCapital_changed_over_5pct']:.1%} by more than 5%.\n"
                f"* Why history moves: see STOCK_CHANGES.md.\n\n")
    p.write_text(head + entry_md + body); print("  RELEASES.md updated")

    p = ROOT / "site" / "build.py"; s = p.read_text()
    s = re.sub(r'RELEASE = "intangibleCapital_\d{8}"', f'RELEASE = "intangibleCapital_{tag}"', s); p.write_text(s)
    print("  site/build.py RELEASE updated")
    return entry_md


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default=date.today().strftime("%Y%m%d"))
    ap.add_argument("--publish", action="store_true", help="commit, push, deploy the site, create the GitHub release")
    ap.add_argument("--skip-figures", action="store_true")
    ap.add_argument("--allow-stale", action="store_true")
    ap.add_argument("--allow-unexplained", action="store_true", help="publish despite unexplained changes (only after reading the change report)")
    a = ap.parse_args()
    tag = a.tag; out_file = f"intangibleCapital_{tag}.csv"
    if a.publish and a.skip_figures:
        sys.exit("--publish rebuilds and publishes the figures; it cannot be combined with --skip-figures")

    asof, crsp_asof = preflight(a.allow_stale)
    step("pull inputs from the local snapshot and FRED"); run([PY, "pipeline/pull_inputs_local.py"])
    year = tag[:4]   # founding years and stocks use the same as-of year
    step("founding and IPO years"); run([PY, "pipeline/founding_years.py", "--bridge", "ccmlink", "--asof-year", year])
    step("build the stocks"); run([PY, "pipeline/epw_stocks.py", "--tag", tag, "--keep-panel", "--asof-year", year])

    step("copy the release file")
    df = pd.read_csv(ROOT / "data" / "output" / f"intangibleCapital_{tag}.csv")
    df["gvkey"] = df.gvkey.astype(int); df["fyear"] = df.fyear.astype(int); df["note"] = df.note.fillna("")
    df.to_csv(ROOT / out_file, index=False)
    d = date(int(tag[:4]), int(tag[4:6]), int(tag[6:]))
    facts = {"file": out_file, "date": d.isoformat(), "asof": asof, "crsp_asof": crsp_asof, "asof_long": datetime.fromisoformat(asof).strftime("%B %-d, %Y"),
             "rows": int(len(df)), "firms": int(df.gvkey.nunique()), "fy_min": int(df.fyear.min()), "fy_max": int(df.fyear.max())}
    print("  " + json.dumps(facts))

    step("archive this release's inputs")
    (ARCHIVE / tag).mkdir(parents=True, exist_ok=True)
    for f in ARCHIVED: shutil.copy2(ROOT / "data" / "inputs" / f, ARCHIVE / tag / f)
    print(f"  {ARCHIVE / tag}")

    man = json.load(open(ROOT / "releases.json"))
    prev = sorted([r for r in man["releases"] if r["tag"] != tag], key=lambda r: r["date"])[-1]
    step(f"change check against {prev['tag']}")
    run([PY, "pipeline/change_check.py", "--old", prev["tag"], "--new", tag] + (["--allow-unexplained"] if a.allow_unexplained else []))

    step("compare with the previous release")
    cmp = compare(ROOT / out_file, ROOT / prev["file"]); print("  " + json.dumps(cmp))
    notes = update_text_files(tag, facts, cmp, prev)

    if not a.skip_figures:
        step("S&P 500 list"); sp500_list()
        step("figures"); run([PY, "site/figures/sample.py", "--panel", f"data/output/panel_{tag}.csv"])
        for f in FIGS: run([PY, f"{f}.py"], cwd=ROOT / "site" / "figures")
        step("figure diagnostics and validation")
        run([PY, "site/figures/diagnose_validation.py"])
        run([PY, "site/figures/validate_figures.py"])
    step("site build"); run([PY, "site/build.py"])

    if not a.publish:
        print("\nBuilt. Review `git status`, RELEASES.md and site/dist/index.html, then rerun with --publish.")
        return
    step("publish")
    run(["git", "add", "-A"])
    run(["git", "commit", "-m", f"Release {tag}\n\n{notes}\nDesigned by Michael Ewens. Built with release.py."])
    run(["git", "push", "origin", "master"])
    run(["wrangler", "deploy"], cwd=ROOT / "site")
    step("check the live page")   # curl: Cloudflare blocks urllib's user agent
    live = subprocess.run(["curl", "-sL", f"https://intangiblesdata.org/?v={tag}"], capture_output=True, text=True).stdout
    sys.path.insert(0, str(ROOT / "site")); from build import check_page
    check_page(live)
    if f"intangibleCapital_{tag}.csv" not in live:
        sys.exit(f"live page does not link intangibleCapital_{tag}.csv")
    print("  live page passes the page check and links this release")
    if subprocess.run(["gh", "release", "view", f"v{tag}"], cwd=ROOT, capture_output=True).returncode == 0:
        print(f"  GitHub release v{tag} already exists; not recreated")
    else:
        run(["gh", "release", "create", f"v{tag}", "--title", f"Stocks release {tag}", "--notes", notes])
    print(f"\nReleased {tag}: repo pushed, site deployed, GitHub release v{tag} in place.")


if __name__ == "__main__":
    main()
