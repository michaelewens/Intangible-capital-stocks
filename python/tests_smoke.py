"""Smoke/regression tests; requires pandas. All outputs are temporary.

Offline: IC_LOCAL=1 python3 python/tests_smoke.py
Override data checkout with IC_REPO_ROOT=/path/to/repo.
Add --build for offline wheel/sdist checks with installed setuptools>=77 and wheel.
Without IC_LOCAL=1, the data smoke test uses the live repository.
"""
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
import intangiblecapital as ic


class LocalRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.source = root / "source"
        self.source.mkdir()
        self.cache = root / "cache"
        env = patch.dict(os.environ, {"INTANGIBLECAPITAL_CACHE": str(self.cache)})
        env.start()
        self.addCleanup(env.stop)
        repo = patch.object(ic, "REPO_RAW", self.source.as_uri() + "/")
        repo.start()
        self.addCleanup(repo.stop)
        self.old = {"tag": "123123", "date": "2023-12-31", "file": "old.csv"}
        self.new = {"tag": "20260924", "date": "2026-09-24", "file": "new.csv"}
        self.write_manifest([self.old])
        for entry, capital in [(self.old, 10), (self.new, 20)]:
            (self.source / entry["file"]).write_text(
                "gvkey,fyear,knowCapital,orgCapital,note\n"
                f"1004,2019,{capital},2,\n1004,2020,0,,interpolated\n"
            )

    def write_manifest(self, entries):
        (self.source / "releases.json").write_text(json.dumps({"releases": entries}))

    def test_current_updates_but_csv_downloaded_once(self):
        with patch.object(ic.urllib.request, "urlopen", wraps=ic.urllib.request.urlopen) as opened:
            first = ic.load()
            ic.load()
            urls = [call.args[0].full_url for call in opened.call_args_list]
            self.assertEqual(sum(url.endswith("old.csv") for url in urls), 1)
            self.assertEqual(sum(url.endswith("releases.json") for url in urls), 2)
        self.write_manifest([self.old, self.new])
        self.assertEqual(ic.load().attrs["release"], self.new["tag"])
        with patch.object(ic.urllib.request, "urlopen", side_effect=AssertionError("offline")):
            pd.testing.assert_frame_equal(ic.load(release=self.old["tag"]), first)
            self.assertEqual(ic.releases(refresh=False)[0], self.new)

    def test_new_pin_refreshes_stale_manifest(self):
        ic.releases()
        self.write_manifest([self.old, self.new])
        self.assertEqual(ic.load(release=self.new["tag"]).attrs["release"], self.new["tag"])
        with self.assertRaisesRegex(ValueError, "unknown release.*available"):
            ic.load(release="not-a-release")

    def test_refresh_replaces_cached_csv(self):
        self.assertEqual(ic.load().iloc[0]["knowCapital"], 10)
        p = self.source / "old.csv"
        p.write_text(p.read_text().replace("2019,10,", "2019,99,"))
        self.assertEqual(ic.load().iloc[0]["knowCapital"], 10)
        self.assertEqual(ic.load(refresh=True).iloc[0]["knowCapital"], 99)

    def test_schema_and_direct_nullable_merge(self):
        stocks = ic.load()
        self.assertEqual(list(stocks), list(ic.COLUMNS))
        self.assertEqual([str(t) for t in stocks.dtypes], ["Int64", "Int64", "float64", "float64", "string"])
        self.assertEqual(stocks.iloc[0]["note"], "")
        left = pd.DataFrame({"gvkey": pd.array([1004, 9999, None], dtype="Int64"),
                             "fyear": pd.array([2019, 2019, None], dtype="Int64")})
        result = left.merge(stocks, on=["gvkey", "fyear"], how="left")
        self.assertEqual(str(result.gvkey.dtype), "Int64")
        self.assertEqual(str(result.fyear.dtype), "Int64")
        self.assertEqual(str(result.note.dtype), "string")
        self.assertEqual(result.knowCapital.iloc[0], 10)
        self.assertTrue(result.knowCapital.iloc[1:].isna().all())

    def test_merge_key_representations_and_input_preservation(self):
        stocks = ic.load()
        cases = [([1004, 1004, 9999], [2019, 2020, 2019]),
                 (["001004", "001004", None], [2019.0, 2020.0, float("nan")]),
                 (pd.array([1004, 1004, None], dtype="Int64"), pd.array([2019, 2020, None], dtype="Int64")),
                 (pd.array(["001004", "001004", None], dtype="string"), ["2019", "2020", None])]
        for keys, years in cases:
            with self.subTest(dtype=str(getattr(keys, "dtype", type(keys)))):
                funda = pd.DataFrame({"firm": keys, "year": years, "at": [1, 2, 3]}, index=[7, 8, 9])
                before = funda.copy(deep=True)
                with patch.object(ic, "load", return_value=stocks):
                    merged = ic.merge_compustat(funda, gvkey="firm", fyear="year")
                    inner = ic.merge_compustat(funda, gvkey="firm", fyear="year", how="inner")
                pd.testing.assert_frame_equal(funda, before)
                pd.testing.assert_frame_equal(merged[list(funda)], funda.reset_index(drop=True))
                self.assertEqual(merged.knowCapital.iloc[:2].tolist(), [10, 0])
                self.assertTrue(pd.isna(merged.knowCapital.iloc[2]))
                self.assertEqual(len(inner), 2)

    def test_bad_merge_inputs_fail_before_download(self):
        base = pd.DataFrame({"gvkey": [1004], "fyear": [2019]})
        with patch.object(ic, "load", side_effect=AssertionError("should validate first")):
            for name in ["_ic_gvkey", "_ic_fyear", "note", "knowCapital", "orgCapital"]:
                with self.assertRaisesRegex(ValueError, "conflicting"):
                    ic.merge_compustat(base.assign(**{name: "keep"}))
            for name, value in [("gvkey", "oops"), ("fyear", 2019.5), ("fyear", float("inf"))]:
                with self.assertRaisesRegex(ValueError, "whole-number"):
                    ic.merge_compustat(base.assign(**{name: value}))
            with self.assertRaisesRegex(ValueError, "missing key"):
                ic.merge_compustat(base.drop(columns="gvkey"))
            for how in ["outer", "right", "cross"]:
                with self.assertRaisesRegex(ValueError, "how must"):
                    ic.merge_compustat(base, how=how)

    def test_duplicate_stock_keys_cannot_multiply_rows(self):
        stocks = ic.load()
        funda = pd.DataFrame({"gvkey": [1004, 1004], "fyear": [2019, 2019]})
        with patch.object(ic, "load", return_value=stocks):
            self.assertEqual(len(ic.merge_compustat(funda)), 2)
        with patch.object(ic, "load", return_value=pd.concat([stocks, stocks])):
            with self.assertRaises(pd.errors.MergeError):
                ic.merge_compustat(funda)

    def test_failed_download_preserves_old_cache_and_cleans_partial(self):
        target = ic._fetch("old.csv")
        original = target.read_bytes()
        from http.client import IncompleteRead
        for name in ["old.csv", "new.csv"]:
            for error in [OSError("connection lost"), IncompleteRead(b"partial", 10)]:
                with patch.object(ic.urllib.request, "urlopen") as opened:
                    opened.return_value.__enter__.return_value.read.side_effect = error
                    with self.assertRaisesRegex(OSError, "Could not download.*cache"):
                        ic._fetch(name, refresh=True)
                self.assertEqual(target.read_bytes(), original)
                self.assertFalse((self.cache / "new.csv").exists())
                self.assertFalse((self.cache / (name + ".tmp")).exists())

    def test_invalid_manifest_and_stock_schema_have_context(self):
        for text in ["not json", '{"releases": []}', '{"releases": [{}]}']:
            (self.source / "releases.json").write_text(text)
            with self.assertRaisesRegex(ValueError, "Invalid release manifest.*refresh=True"):
                ic.releases()
        self.write_manifest([self.old])
        for text in ["wrong,column\n1,2\n", "gvkey,fyear,knowCapital,orgCapital,note\n,2019,1,2,\n",
                     "gvkey,fyear,knowCapital,orgCapital,note\n1004,2019.5,1,2,\n"]:
            (self.source / "old.csv").write_text(text)
            with self.assertRaisesRegex(ValueError, "Invalid stock file.*123123.*refresh=True"):
                ic.load(refresh=True)

    def test_truncated_but_parseable_csv_is_rejected(self):
        self.old["rows"] = 3
        self.write_manifest([self.old])
        with self.assertRaisesRegex(ValueError, "expected 3 rows, got 2"):
            ic.load()

    def test_parameters_cached_and_refreshable(self):
        p = self.source / ic.PARAMS_FILE
        p.write_text("sic,knowDepr,organDepr,gamma,industry5\n0100,.2,.3,.4,Other\n")
        first = ic.parameters()
        self.assertEqual([str(t) for t in first.dtypes], ["Int64", "float64", "float64", "float64", "string"])
        p.write_text(p.read_text().replace(".4", ".5"))
        self.assertEqual(ic.parameters().gamma.iloc[0], .4)
        self.assertEqual(ic.parameters(refresh=True).gamma.iloc[0], .5)
        p.write_text("bad\n1\n")
        with self.assertRaisesRegex(ValueError, "Invalid parameters.*refresh=True"):
            ic.parameters(refresh=True)


def data_smoke():
    repo_root = Path(os.environ.get("IC_REPO_ROOT", Path(__file__).resolve().parents[1]))
    raw = repo_root.resolve().as_uri() + "/" if os.environ.get("IC_LOCAL") == "1" else ic.REPO_RAW
    with tempfile.TemporaryDirectory() as cache, patch.dict(os.environ, {"INTANGIBLECAPITAL_CACHE": cache}), patch.object(ic, "REPO_RAW", raw):
        releases = ic.releases()
        stocks = ic.load()
        assert list(stocks) == list(ic.COLUMNS), stocks.columns
        assert len(stocks) == releases[0]["rows"], (len(stocks), releases[0])
        assert stocks.attrs["release"] == releases[0]["tag"]
        assert [str(t) for t in stocks.dtypes] == ["Int64", "Int64", "float64", "float64", "string"]
        params = ic.parameters()
        assert list(params) == ["sic", "knowDepr", "organDepr", "gamma", "industry5"]
        funda = pd.DataFrame({"gvkey": ["001004", "001004"], "fyear": [2019.0, 2020.0], "at": [1.0, 2.0]})
        merged = ic.merge_compustat(funda)
        expected = stocks.loc[(stocks.gvkey == 1004) & stocks.fyear.isin([2019, 2020]), "knowCapital"]
        assert merged.knowCapital.tolist() == expected.tolist()
        assert len(merged) == 2
        historical = ic.load(release="090123")
        entry = next(r for r in releases if r["tag"] == "090123")
        assert len(historical) == entry["rows"]
        assert list(historical) == list(stocks)
        assert historical.dtypes.equals(stocks.dtypes)
        assert historical.note.eq("").all()
        print(f"ok: {len(stocks)} current rows; {len(historical)} historical rows; merge values verified")


def build_smoke():
    """Build a staged copy with installed tools; no install or network access."""
    import email
    import tarfile
    import zipfile
    from setuptools import build_meta

    source = Path(__file__).resolve().parent
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as temporary:
        stage = Path(temporary)
        for name in ["README.md", "pyproject.toml"]:
            shutil.copy2(source / name, stage / name)
        shutil.copytree(source / "intangiblecapital", stage / "intangiblecapital", ignore=shutil.ignore_patterns("__pycache__"))
        try:
            os.chdir(stage)
            wheel = build_meta.build_wheel(str(stage / "dist"))
            sdist = build_meta.build_sdist(str(stage / "dist"))
        finally:
            os.chdir(previous)
        with zipfile.ZipFile(stage / "dist" / wheel) as archive:
            assert "intangiblecapital/__init__.py" in archive.namelist()
            metadata_name = next(n for n in archive.namelist() if n.endswith(".dist-info/METADATA"))
            metadata = email.message_from_bytes(archive.read(metadata_name))
            assert metadata["Name"] == "intangiblecapital"
            assert metadata["Version"] == ic.__version__
            assert metadata["License-Expression"] == "MIT"
            assert "pandas" in metadata["Requires-Dist"]
            assert "# intangiblecapital" in metadata.get_payload()
        with tarfile.open(stage / "dist" / sdist) as archive:
            assert any(n.endswith("/README.md") for n in archive.getnames())
            assert any(n.endswith("/intangiblecapital/__init__.py") for n in archive.getnames())
        print("ok: offline wheel and sdist builds; metadata, README, package inclusion verified")


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(LocalRegressionTests))
    if not result.wasSuccessful():
        sys.exit(1)
    data_smoke()
    if "--build" in sys.argv:
        build_smoke()
