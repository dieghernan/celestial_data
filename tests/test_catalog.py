"""Run after a Jekyll build: py -m unittest discover -s tests -p 'test_*.py'."""

import csv
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.downloads = []
        self.ids = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and "download" in attrs:
            self.downloads.append(attrs["href"])


def datasets_in(source):
    return [item for raw in re.findall(
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', source, re.S
    ) if (item := json.loads(raw)).get("@type") == "Dataset"]


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "_data/datasets.json").read_text(encoding="utf-8"))

    def test_every_data_file_has_one_distribution_with_current_size(self):
        expected = {p.name for p in (ROOT / "data").iterdir()
                    if p.suffix in {".geojson", ".gpkg", ".csv"}}
        actual = []
        for dataset in self.catalog:
            for file in dataset["distributions"]:
                actual.append(file["filename"])
                self.assertEqual(file["bytes"], (ROOT / "data" / file["filename"]).stat().st_size)
            path = ROOT / "data" / (dataset["id"] + (".geojson" if dataset["geometry"] else ".csv"))
            with path.open(encoding="utf-8", newline="") as stream:
                count = len(json.load(stream)["features"]) if dataset["geometry"] else sum(1 for _ in csv.DictReader(stream))
            self.assertEqual(dataset["count"], count)
        self.assertEqual(set(actual), expected)
        self.assertEqual(len(actual), len(expected))

    def test_landing_pages_have_matching_jsonld_and_downloads(self):
        for dataset in self.catalog:
            with self.subTest(dataset=dataset["id"]):
                source = (ROOT / "_site/datasets" / dataset["id"] / "index.html").read_text(encoding="utf-8")
                page = Page(source)
                self.assertEqual(len(page.ids), len(set(page.ids)))
                metadata, = datasets_in(source)
                self.assertEqual(metadata["name"], dataset["name"])
                self.assertNotIn("identifier", metadata)  # DOI belongs to collection.
                self.assertNotIn("spatialCoverage", metadata)
                self.assertEqual(len(page.downloads), len(dataset["distributions"]))
                for file, distribution, href in zip(dataset["distributions"], metadata["distribution"], page.downloads):
                    self.assertEqual(distribution["contentSize"], f'{file["bytes"]} bytes')
                    self.assertEqual(distribution["encodingFormat"], file["mime"])
                    self.assertTrue(distribution["contentUrl"].startswith("http"))
                    self.assertEqual(urlparse(distribution["contentUrl"]).path, href)
                    self.assertTrue((ROOT / "_site/data" / unquote(href.split("/")[-1])).is_file())

    def test_catalog_and_collection_link_all_datasets(self):
        source = (ROOT / "_site/data.html").read_text(encoding="utf-8")
        page = Page(source)
        self.assertEqual(len(page.downloads), 63)
        self.assertIn("downloads", page.ids)
        self.assertEqual(len(page.ids), len(set(page.ids)))
        metadata, = datasets_in((ROOT / "_site/index.html").read_text(encoding="utf-8"))
        self.assertEqual(metadata["identifier"], "https://doi.org/10.5281/zenodo.7561601")
        self.assertEqual(len(metadata["hasPart"]), len(self.catalog))
        for dataset in self.catalog:
            self.assertIn(f'/celestial_data/datasets/{dataset["id"]}/', source)


if __name__ == "__main__":
    unittest.main()
