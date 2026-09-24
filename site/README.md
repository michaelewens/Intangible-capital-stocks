# intangiblesdata.org

Static page for the data release. Built by `build.py` from the current release file and the figure
outputs; deployed to Cloudflare from `dist/`.

```
python3 pipeline/epw_stocks.py --tag YYYYMMDD --keep-panel   # stocks + working panel
python3 site/figures/sample.py                                # figure sample (paper's screens)
python3 site/figures/figNN_*.py                               # each figure -> site/data/, site/figures/out/
python3 site/build.py                                         # -> site/dist/
```

`figures/` holds the Python ports of the paper's figure programs. Their inputs (Compustat, CRSP, the
paper's deal lists) are local and never published; the plotted numbers and the SVGs are.
