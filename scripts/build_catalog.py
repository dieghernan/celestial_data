"""Refresh download metadata and dataset landing pages from the checked-in files.

Run from any directory with: py scripts/build_catalog.py
Editorial descriptions live here; file sizes and object counts come from data/.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = [
    ("asterisms", "Asterisms", "Asterisms and Milky Way", "Line patterns representing 65 asterisms, with names and label positions."),
    ("mw", "Milky Way", "Asterisms and Milky Way", "Milky Way outlines represented as polygons in five brightness steps."),
    ("constellations", "Constellation labels", "Constellations", "Label positions and multilingual names for constellation map displays."),
    ("constellations.cn", "Chinese constellation labels", "Constellations", "Label positions, Chinese names and English translations for traditional Chinese constellations."),
    ("constellations.borders", "Constellation borders", "Constellations", "Line geometries tracing the borders between constellations."),
    ("constellations.borders.cn", "Chinese constellation borders", "Constellations", "Line geometries tracing borders in the traditional Chinese constellation data."),
    ("constellations.bounds", "Constellation regions", "Constellations", "Polygon geometries representing constellation regions for map displays."),
    ("constellations.bounds.cn", "Chinese constellation regions", "Constellations", "Polygon geometries representing regions in the traditional Chinese constellation data."),
    ("constellations.lines", "Constellation lines", "Constellations", "Line patterns connecting stars to illustrate constellation figures."),
    ("constellations.lines.cn", "Chinese constellation lines", "Constellations", "Line patterns illustrating traditional Chinese constellation figures; degenerate source lines were removed."),
    ("dsos.6", "Deep-sky objects: magnitude 6", "Deep-sky objects", "Deep-sky object positions with a nominal magnitude limit of 6, including entries with unknown magnitudes."),
    ("dsos.14", "Deep-sky objects: magnitude 14", "Deep-sky objects", "Deep-sky object positions with a nominal magnitude limit of 14, including entries with unknown magnitudes."),
    ("dsos.20", "Deep-sky objects: magnitude 20", "Deep-sky objects", "Deep-sky object positions with a nominal magnitude limit of 20, including entries with unknown magnitudes."),
    ("dsos.bright", "Bright deep-sky objects", "Deep-sky objects", "A selection of bright deep-sky objects compiled by Olaf Frohn."),
    ("lg", "Local Group and Milky Way halo", "Deep-sky objects", "Positions and attributes of Local Group and Milky Way halo objects compiled by Olaf Frohn."),
    ("messier", "Messier catalog", "Deep-sky objects", "Positions and attributes of the 110 objects in the Messier catalog."),
    ("stars.6", "Stars: magnitude 6", "Stars", "Star positions and attributes with a nominal apparent magnitude limit of 6."),
    ("stars.8", "Stars: magnitude 8", "Stars", "Star positions and attributes with a nominal apparent magnitude limit of 8 in this repository."),
    ("stars.14", "Stars: magnitude 14", "Stars", "Star positions and attributes from the largest star catalog provided in this repository."),
    ("dsonames", "Deep-sky object names", "Name tables", "A complementary CSV table of deep-sky object identifiers and names in several languages."),
    ("dsonames.cn", "Chinese deep-sky object names", "Name tables", "A complementary CSV table of deep-sky object designations, Chinese names and translations."),
    ("starnames", "Star names", "Name tables", "A complementary CSV table of star names, catalog designations and translations, independent of the magnitude subsets."),
    ("starnames.cn", "Chinese star names", "Name tables", "A complementary CSV table of star identifiers, Chinese names, English translations and pinyin."),
]


def build():
    datasets = []
    for key, name, group, description in CATALOG:
        geojson = ROOT / "data" / f"{key}.geojson"
        if geojson.exists():
            features = json.loads(geojson.read_text(encoding="utf-8"))["features"]
            count = len(features)
            geometry = ", ".join(sorted({f["geometry"]["type"] for f in features}))
        else:
            with (ROOT / "data" / f"{key}.csv").open(encoding="utf-8", newline="") as source:
                count = sum(1 for _ in csv.DictReader(source))
            geometry = None
        distributions = []
        for suffix, label, mime in [
            (".geojson", "GeoJSON", "application/geo+json"),
            (".min.geojson", "GeoJSON (minified)", "application/geo+json"),
            (".gpkg", "GeoPackage", "application/geopackage+sqlite3"),
            (".csv", "CSV", "text/csv"),
        ]:
            path = ROOT / "data" / f"{key}{suffix}"
            if path.exists():
                size = path.stat().st_size
                distributions.append(dict(filename=path.name, label=label, mime=mime,
                                          bytes=size, size=f"{size / 1_000_000:.2f} MB" if size >= 1_000_000 else f"{size / 1000:.1f} kB"))
        datasets.append(dict(id=key, name=name, group=group, description=description,
                             count=count, geometry=geometry, distributions=distributions))
        target = ROOT / "_pages" / "datasets" / f"{key}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("---\n" + f"title: {json.dumps(name)}\npermalink: /datasets/{key}/\ndataset_id: {key}\nexcerpt: {json.dumps(description)}\n" + "---\n\n{% include custom/dataset_detail.html %}\n", encoding="utf-8")
    target = ROOT / "_data" / "datasets.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(datasets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
