"""Check the public author identity on the collection and every dataset page."""

import json
from pathlib import Path
import unittest

import mf2py

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
HOME = "https://dieghernan.github.io/"
PROJECT = HOME + "celestial_data/"


class AuthorshipTests(unittest.TestCase):
    def test_collection_tools_and_datasets_share_the_canonical_author(self):
        catalog = json.loads((ROOT / "_data/datasets.json").read_text(encoding="utf-8"))
        pages = [("index.html", ""), ("downloads/index.html", "downloads/"),
                 ("data.html", "data"), ("preview.html", "preview"), ("sources.html", "sources")]
        pages += [(f"datasets/{item['id']}/index.html", f"datasets/{item['id']}/") for item in catalog]
        for filename, route in pages:
            with self.subTest(page=filename):
                url = PROJECT + route
                parsed = mf2py.parse(doc=(SITE / filename).read_text(encoding="utf-8"), url=url)
                entry, = [item for item in parsed["items"] if "h-entry" in item["type"]]
                self.assertEqual(entry["properties"]["url"], [url])
                author, = entry["properties"]["author"]
                self.assertIn("h-card", author["type"])
                self.assertEqual(author["properties"]["name"], ["Diego HH"])
                self.assertEqual(author["properties"]["url"][0], HOME)


if __name__ == "__main__":
    unittest.main()
