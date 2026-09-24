"""Render the intangiblesdata.org page from the current release.

Reads: the release CSV named in RELEASE, data/output/build_stats.json, site/data/figNN.csv and
site/figures/out/figNN.svg (written by site/figures/*.py), site/template.html, site/figures.json.
Writes: site/dist/index.html, site/dist/llms.txt, site/dist/prompt.txt, site/dist/figures/*.svg,
site/dist/data/*.csv. No dependencies beyond pandas.
"""
import json, shutil
from datetime import date
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DIST = SITE / "dist"
REPO_RAW = "https://github.com/michaelewens/Intangible-capital-stocks/raw/master/"
REPO = "https://github.com/michaelewens/Intangible-capital-stocks"
RELEASE = "intangibleCapital_20260924"          # updated by the release script
PARAMS = "capital_accum_parameters_2023.csv"


def release_facts():
    df = pd.read_csv(ROOT / f"{RELEASE}.csv")
    d = date(int(RELEASE[-8:-4]), int(RELEASE[-4:-2]), int(RELEASE[-2:]))
    return {
        "release_tag": RELEASE, "release_date": d.strftime("%B %-d, %Y"),
        "n_rows": f"{len(df):,}", "n_firms": f"{df.gvkey.nunique():,}",
        "fy_min": int(df.fyear.min()), "fy_max": int(df.fyear.max()),
        "csv_url": REPO_RAW + RELEASE + ".csv",
        "params_url": REPO_RAW + PARAMS, "repo": REPO,
        "csv_mb": f"{(ROOT / f'{RELEASE}.csv').stat().st_size / 1e6:.0f}",
    }


def params_table():
    p = pd.read_csv(ROOT / PARAMS).groupby("industry5")[["knowDepr", "organDepr", "gamma"]].first()
    order = ["Consumer", "Manuf.", "High-tech", "Health", "Other"]
    rows = "".join(f"<tr><td>{i}</td><td>{p.loc[i,'knowDepr']:.2f}</td><td>{p.loc[i,'organDepr']:.2f}</td><td>{p.loc[i,'gamma']:.2f}</td></tr>" for i in order if i in p.index)
    return rows


def llm_prompt(f):
    return f"""You are working with the Ewens, Peters and Wang intangible capital stocks for U.S. public firms.

DATA: {f['csv_url']}
One row per Compustat firm and fiscal year. {f['n_rows']} rows, {f['n_firms']} firms, fiscal years {f['fy_min']}-{f['fy_max']}. Release {f['release_date']}.
Columns:
  gvkey        Compustat firm identifier (integer)
  fyear        fiscal year
  knowCapital  knowledge capital stock, net, nominal $ millions (capitalized R&D)
  orgCapital   organization capital stock, net, nominal $ millions (capitalized share of SG&A)
  note         blank when computed from reported data; otherwise explains a missing or interpolated stock
Stocks are net (after depreciation), so year-on-year changes are net investment. Merge to Compustat on (gvkey, fyear).

PARAMETERS: {f['params_url']} gives, by 4-digit SIC, the knowledge depreciation rate (knowDepr), organization depreciation rate (organDepr, 0.20), the share of SG&A treated as investment (gamma), and the Fama-French 5 industry. Baseline by industry (knowDepr / gamma): Consumer 0.43 / 0.20, Manufacturing 0.50 / 0.21, High-tech 0.42 / 0.37, Health 0.33 / 0.51, Other 0.35 / 0.22.

METHOD: perpetual inventory. Knowledge capital: K_t = (1 - knowDepr) K_(t-1) + R&D_t. Organization capital: O_t = 0.8 O_(t-1) + gamma x SG&A_t (SG&A net of R&D). Initial stocks imputed from firm age. Details: {f['repo']}/blob/master/pipeline/README.md

CAVEAT: every release rebuilds all years from current Compustat, so a firm's history can change between releases (industry code revisions, restated financials). Cite the release date. Details: {f['repo']}/blob/master/STOCK_CHANGES.md

CITATION: Ewens, Michael, Ryan Peters and Sean Wang. "Measuring Intangible Capital with Market Prices." Management Science 71.1 (2024): 407-427. https://doi.org/10.1287/mnsc.2021.02058
"""


def md_to_html(md: str, base_blob: str, base_raw: str) -> str:
    """Small Markdown renderer for the repo README: headings, paragraphs, bullets, links, images,
    inline code, bold, code fences. Relative links resolve to the GitHub blob/raw URLs."""
    import re, html as _h
    def inline(t):
        t = _h.escape(t, quote=False)
        t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", lambda m: f'<img src="{m.group(2) if m.group(2).startswith("http") else base_raw + m.group(2)}" alt="{m.group(1)}">', t)
        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2) if m.group(2).startswith("http") else base_blob + m.group(2)}">{m.group(1)}</a>', t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<![\w*])_([^_]+)_(?![\w*])", r"<em>\1</em>", t)
        return t
    out, para, lst, code = [], [], [], None
    def flush():
        nonlocal para, lst
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if lst: out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in lst) + "</ul>"); lst = []
    for line in md.splitlines():
        if line.startswith("```"):
            if code is None: flush(); code = []
            else: out.append("<pre>" + _h.escape("\n".join(code)) + "</pre>"); code = None
            continue
        if code is not None: code.append(line); continue
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            flush(); lvl = min(len(m.group(1)) + 1, 4)   # README h1 -> h2 on the page
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); continue
        if re.match(r"^\s*[*-]\s+", line):
            if para: flush()
            lst.append(re.sub(r"^\s*[*-]\s+", "", line)); continue
        if not line.strip(): flush(); continue
        if lst: lst[-1] += " " + line.strip()
        else: para.append(line.strip())
    flush()
    return "\n".join(out)


def figures_html():
    spec = json.load(open(SITE / "figures.json"))
    out = []
    for fg in spec:
        svg = SITE / "figures" / "out" / f"{fg['id']}.svg"
        csv = SITE / "data" / f"{fg['id']}.csv"
        if svg.exists():
            img = f'<img src="figures/{fg["id"]}.svg?v={int(svg.stat().st_mtime)}" alt="{fg["title"]}">'
        else:
            img = f'<div class="placeholder">Figure pending: {fg["title"]}</div>'
        link = f' <a href="data/{fg["id"]}.csv">Download the plotted numbers (CSV)</a>' if csv.exists() else ""
        cls = ' class="wide"' if fg.get("wide") else ""
        out.append(f'<figure id="{fg["id"]}"{cls}><h3>{fg["title"]}</h3>{img}<figcaption>{fg["caption"]}{link}</figcaption></figure>')
    return "\n".join(out)


def main(theme="academic", out_name="index.html"):
    f = release_facts()
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "figures").mkdir(exist_ok=True); (DIST / "data").mkdir(exist_ok=True)
    for p in (SITE / "figures" / "out").glob("*.svg"): shutil.copy(p, DIST / "figures" / p.name)
    for p in (SITE / "data").glob("*.csv"): shutil.copy(p, DIST / "data" / p.name)
    prompt = llm_prompt(f)
    (DIST / "prompt.txt").write_text(prompt)
    (DIST / "llms.txt").write_text("# intangiblesdata.org\n\n> Firm-year knowledge and organization capital stocks for U.S. public firms (Ewens, Peters and Wang 2024), updated as fiscal years close in Compustat.\n\n" + prompt)
    html = (SITE / "template.html").read_text().replace("{{theme_css}}", (SITE / "themes" / f"{theme}.css").read_text())
    for k, v in f.items(): html = html.replace("{{" + k + "}}", str(v))
    readme = md_to_html((ROOT / "README.md").read_text(), REPO + "/blob/master/", REPO_RAW)
    html = html.replace("{{readme}}", readme).replace("{{params_rows}}", params_table()).replace("{{figures}}", figures_html()).replace("{{prompt}}", prompt.replace("<", "&lt;"))
    (DIST / out_name).write_text(html)
    print("built", DIST / out_name, "theme", theme)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--all-themes":
        for t in ["academic", "editorial", "modern"]:
            main(t, "index.html" if t == "academic" else f"theme_{t}.html")
    else:
        main(*sys.argv[1:])
