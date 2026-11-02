"""Verify Croissant loads every original value and celestial coordinate."""

import csv
import hashlib
import json
from pathlib import Path
import unittest
from urllib.parse import urlsplit, urljoin

import mlcroissant
import shapely
from shapely.geometry import mapping

ROOT = Path(__file__).resolve().parents[1]


class CroissantTests(unittest.TestCase):
    def verify_records(self, key):
        descriptor = json.loads((ROOT / "croissant" / (key + ".json")).read_text(encoding="utf-8"))
        resource, = [file for file in descriptor["distribution"] if file["@id"] == "records-json"]
        relative = urlsplit(resource["contentUrl"]).path.split("/celestial_data/", 1)[1]
        path = ROOT / relative
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), resource["sha256"])
        dataset = mlcroissant.Dataset(jsonld=descriptor, mapping={urljoin(descriptor["url"], "records-json"): path})
        source = ROOT / "data" / (key + ".geojson")
        spatial = source.exists()
        if spatial:
            features = json.loads(source.read_text(encoding="utf-8"))["features"]
            columns = sorted(set().union(*(feature["properties"] for feature in features)))
            expected = [{column: feature["properties"].get(column) for column in columns} for feature in features]
        else:
            with (ROOT / "data" / (key + ".csv")).open(encoding="utf-8", newline="") as stream:
                expected = list(csv.DictReader(stream))
        record_set = urljoin(descriptor["url"], "records")
        prefix = record_set + "/"
        count = 0
        for index, (actual, row) in enumerate(zip(dataset.records(record_set=record_set), expected, strict=True), 1):
            count += 1
            self.assertEqual(actual[prefix + "record_index"], index, (key, index))
            for column, value in row.items():
                loaded = actual[prefix + column]
                if isinstance(loaded, bytes):
                    loaded = loaded.decode("utf-8")
                self.assertEqual(loaded, value, (key, index, column))
            if spatial:
                geom = shapely.from_wkt(actual[prefix + "geometry_wkt"])
                # Compare to original nested GeoJSON arrays, independently of the generator.
                self.assertEqual(json.loads(json.dumps(mapping(geom))), features[index - 1]["geometry"], (key, index))
        self.assertEqual(count, len(expected), key)
        columns = [field["name"] for field in descriptor["recordSet"][0]["field"]]
        self.assertEqual(set(columns), {"record_index", *expected[0], *({"geometry_wkt"} if spatial else set())})

    def test_pilot_milky_way_preserves_all_five_polygons(self):
        self.verify_records("mw")

    def test_all_other_catalogs_preserve_records_and_missing_values(self):
        catalog = json.loads((ROOT / "_data/datasets.json").read_text(encoding="utf-8"))
        for entry in catalog:
            if entry["id"] != "mw":
                with self.subTest(dataset=entry["id"]):
                    self.verify_records(entry["id"])

    def test_generated_descriptors_are_published_and_embedded(self):
        from tests.test_catalog import datasets_in
        descriptors = json.loads((ROOT / "_data/croissant.json").read_text(encoding="utf-8"))
        self.assertEqual(len(descriptors), 23)
        for key, descriptor in descriptors.items():
            with self.subTest(dataset=key):
                published = json.loads((ROOT / "_site/croissant" / (key + ".json")).read_text(encoding="utf-8"))
                self.assertEqual(published, descriptor)
                embedded, = datasets_in((ROOT / "_site/datasets" / key / "index.html").read_text(encoding="utf-8"))
                self.assertEqual(embedded, descriptor)
                self.assertNotIn("spatialCoverage", descriptor)
                self.assertNotIn("geocr:coordinateReferenceSystem", descriptor)
                self.assertEqual(descriptor["isPartOf"]["@id"], "https://dieghernan.github.io/celestial_data/#collection")
                self.assertEqual(descriptor["@context"]["description"], "sc:description")
                self.assertEqual(descriptor["@context"]["@base"], descriptor["url"])
                for file in descriptor["distribution"]:
                    self.assertIn("sc:DataDownload", file["@type"])
                    self.assertTrue(file["contentUrl"].startswith("https://"))
                    self.assertEqual(len(file["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
