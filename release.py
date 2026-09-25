#!/usr/bin/env python3
"""One-command release for the intangible capital stocks.

    python3 release.py                 # build everything for today's tag, stop before publishing
    python3 release.py --publish       # ... then commit, push, deploy the site, create the GitHub release
    python3 release.py --tag 20261215  # explicit tag (YYYYMMDD)
    python3 release.py --skip-figures  # data only

Before running: refresh the local WRDS snapshot (needs a Duo approval, run it yourself):
    ~/.venvs/wrds/bin/python ~/Dropbox/Research/wrds_ccm/build_wrds_ccm.py
and have FRED_API_KEY in the environment (the CPI deflator comes from FRED).

Steps: preflight -> pull inputs -> founding years -> stocks -> copy release file -> compare with the
previous release -> update releases.json, README, RELEASES.md, site/build.py -> figures -> site build
-> (publish) commit, push, wrangler deploy, gh release.
"""
import argparse, json, os, re, subprocess, sys
from datetime import date, datetime
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
PY = sys.executable
SNAPSHOT = Path(os.environ.get("WRDS_CCM_DUCKDB", "/Users/me2731/Dropbox/Research/wrds_ccm/wrds_ccm.duckdb"))
MAX_SNAPSHOT_AGE_DAYS = 45
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
    con.close()
    age = (datetime.now(pulled.tzinfo) - pulled).days
    print(f"  snapshot pulled {pulled.date()} ({age} days ago), funda datadate through {asof}")
    if age > MAX_SNAPSHOT_AGE_DAYS and not allow_stale:
        sys.exit(f"snapshot is {age} days old; refresh it first (see docstring) or pass --allow-stale")
    return str(asof)


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
    entry = {"tag": tag, "date": facts["date"], "file": facts["file"], "compustat_asof": facts["asof"],
             "fyear_min": facts["fy_min"], "fyear_max": facts["fy_max"], "rows": facts["rows"]}
    man["releases"] = [r for r in man["releases"] if r["tag"] != tag] + [entry]
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
    a = ap.parse_args()
    tag = a.tag; out_file = f"intangibleCapital_{tag}.csv"

    asof = preflight(a.allow_stale)
    step("pull inputs from the local snapshot and FRED"); run([PY, "pipeline/pull_inputs_local.py"])
    step("founding and IPO years"); run([PY, "pipeline/founding_years.py", "--bridge", "ccmlink"])
    step("build the stocks"); run([PY, "pipeline/epw_stocks.py", "--tag", tag, "--keep-panel"])

    step("copy the release file")
    df = pd.read_csv(ROOT / "data" / "output" / f"intangibleCapital_{tag}.csv")
    df["gvkey"] = df.gvkey.astype(int); df["fyear"] = df.fyear.astype(int); df["note"] = df.note.fillna("")
    df.to_csv(ROOT / out_file, index=False)
    d = date(int(tag[:4]), int(tag[4:6]), int(tag[6:]))
    facts = {"file": out_file, "date": d.isoformat(), "asof": asof, "asof_long": datetime.fromisoformat(asof).strftime("%B %-d, %Y"),
             "rows": int(len(df)), "firms": int(df.gvkey.nunique()), "fy_min": int(df.fyear.min()), "fy_max": int(df.fyear.max())}
    print("  " + json.dumps(facts))

    step("compare with the previous release")
    man = json.load(open(ROOT / "releases.json"))
    prev = sorted([r for r in man["releases"] if r["tag"] != tag], key=lambda r: r["date"])[-1]
    cmp = compare(ROOT / out_file, ROOT / prev["file"]); print("  " + json.dumps(cmp))
    notes = update_text_files(tag, facts, cmp, prev)

    if not a.skip_figures:
        step("figures"); run([PY, "site/figures/sample.py"])
        for f in FIGS: run([PY, f"{f}.py"], cwd=ROOT / "site" / "figures")
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
    run(["gh", "release", "create", f"v{tag}", "--title", f"Stocks release {tag}", "--notes", notes])
    print(f"\nReleased {tag}: repo pushed, site deployed, GitHub release v{tag} created.")


if __name__ == "__main__":
    main()
