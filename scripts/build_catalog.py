"""Refresh download metadata and dataset landing pages from the checked-in files.

Run from any directory with: py scripts/build_catalog.py
Editorial descriptions live here; file sizes and object counts come from data/.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = [
    ("asterisms", "Asterisms", "Asterisms and Milky Way", "Line patterns for asterisms in the J2000 celestial reference, with names and label positions from d3-celestial. GeoJSON and GeoPackage geometries support sky-map illustration; the coordinates describe celestial directions, not places on Earth."),
    ("mw", "Milky Way", "Asterisms and Milky Way", "Polygon outlines of the Milky Way in successive brightness bands, derived from d3-celestial for J2000 sky maps. Available as GeoJSON and GeoPackage with celestial angles encoded as geographic coordinates for GIS use, not as terrestrial locations."),
    ("constellations", "Constellation labels", "Constellations", "Constellation label positions in the J2000 celestial reference, with identifiers, multilingual names and display attributes from d3-celestial. GeoJSON and GeoPackage contain point geometries; the complementary CSV contains attributes without geometry."),
    ("constellations.cn", "Chinese constellation labels", "Constellations", "Label positions for traditional Chinese constellations in the J2000 celestial reference, with Chinese names, English translations, pinyin and display attributes. Available as point geometries in GeoJSON and GeoPackage, with complementary attributes in CSV."),
    ("constellations.borders", "Constellation borders", "Constellations", "Line geometries tracing constellation borders in the J2000 celestial reference, with identifiers for adjacent regions. Derived from d3-celestial and distributed as GeoJSON and GeoPackage for sky maps; the coordinates are not locations on Earth."),
    ("constellations.borders.cn", "Chinese constellation borders", "Constellations", "Line geometries tracing borders in the traditional Chinese constellation data from d3-celestial, with identifiers for adjacent regions. The J2000 celestial angles are encoded as geographic coordinates in GeoJSON and GeoPackage for sky-map displays."),
    ("constellations.bounds", "Constellation regions", "Constellations", "Polygon regions for constellations in the J2000 celestial reference, with identifiers, names and display ranks from d3-celestial. Available as GeoJSON and GeoPackage for sky-map displays; these regions are celestial, not terrestrial administrative areas."),
    ("constellations.bounds.cn", "Chinese constellation regions", "Constellations", "Polygon regions in the traditional Chinese constellation data from d3-celestial, with identifiers, Chinese names, English labels and display ranks. GeoJSON and GeoPackage encode J2000 celestial angles for GIS-compatible sky-map displays."),
    ("constellations.lines", "Constellation lines", "Constellations", "Line patterns connecting stars to illustrate constellation figures, with constellation identifiers, names and display ranks. Derived from d3-celestial in the J2000 reference and available as GeoJSON and GeoPackage; the lines illustrate figures rather than region borders."),
    ("constellations.lines.cn", "Chinese constellation lines", "Constellations", "Line patterns illustrating traditional Chinese constellation figures in the J2000 celestial reference, with identifiers, names and English labels. Available as GeoJSON and GeoPackage derived from d3-celestial; degenerate source lines were removed during processing."),
    ("dsos.6", "Deep-sky objects: magnitude 6", "Deep-sky objects", "Positions and attributes of deep-sky objects from d3-celestial with a nominal magnitude limit of 6, including entries with unknown magnitudes. J2000 point geometries are available in GeoJSON and GeoPackage, with object identifiers, classifications and dimensions where supplied."),
    ("dsos.14", "Deep-sky objects: magnitude 14", "Deep-sky objects", "Positions and attributes of deep-sky objects from d3-celestial with a nominal magnitude limit of 14, including entries with unknown magnitudes. J2000 point geometries are available in GeoJSON and GeoPackage, with object identifiers, classifications and dimensions where supplied."),
    ("dsos.20", "Deep-sky objects: magnitude 20", "Deep-sky objects", "Positions and attributes of deep-sky objects from d3-celestial with a nominal magnitude limit of 20, including entries with unknown magnitudes. J2000 point geometries are available in GeoJSON and GeoPackage, with object identifiers, classifications and dimensions where supplied."),
    ("dsos.bright", "Bright deep-sky objects", "Deep-sky objects", "A selection of bright deep-sky objects compiled by Olaf Frohn for d3-celestial, with identifiers, object types, magnitudes and dimensions where supplied. Available as J2000 point geometries in GeoJSON and GeoPackage; the selection is not a complete inventory of deep-sky objects."),
    ("lg", "Local Group and Milky Way halo", "Deep-sky objects", "Positions and attributes of objects in the Local Group and Milky Way halo, compiled by Olaf Frohn for d3-celestial. GeoJSON and GeoPackage contain J2000 point geometries with identifiers, classifications, magnitudes and dimensions where supplied."),
    ("messier", "Messier catalog", "Deep-sky objects", "J2000 positions and attributes of the 110 objects in the Messier catalog, derived from d3-celestial. GeoJSON and GeoPackage contain point geometries with names, catalog designations, object types, magnitudes and dimensions where supplied."),
    ("stars.6", "Stars: magnitude 6", "Stars", "Star positions and attributes from d3-celestial with a nominal apparent magnitude limit of 6. Available as J2000 point geometries in GeoJSON and GeoPackage, with source identifiers, magnitudes, color indices and names where supplied; not a calculation of the current sky."),
    ("stars.8", "Stars: magnitude 8", "Stars", "Star positions and attributes with a nominal apparent magnitude limit of 8 in this repository, derived from d3-celestial. GeoJSON and GeoPackage contain J2000 point geometries, identifiers, magnitudes and color indices; they do not calculate the current sky."),
    ("stars.14", "Stars: magnitude 14", "Stars", "The largest star catalog supplied by this repository, derived from d3-celestial with positions in the J2000 reference. GeoJSON and GeoPackage contain point geometries, source identifiers, magnitudes, color indices and names where supplied; the file name does not establish catalog completeness."),
    ("dsonames", "Deep-sky object names", "Name tables", "A CSV name table for deep-sky objects from d3-celestial, linking source object identifiers to names in several languages. The table contains no geometry and complements the deep-sky position catalogs; shared identifiers must be interpreted according to the source catalog conventions."),
    ("dsonames.cn", "Chinese deep-sky object names", "Name tables", "A CSV name table for Chinese deep-sky designations from d3-celestial, with identifiers, names, English translations and pinyin. It contains no geometry and complements the celestial object catalogs rather than providing another set of sky positions."),
    ("starnames", "Star names", "Name tables", "A CSV table linking star names and multilingual translations to source identifiers and catalog designations, including Bayer, Flamsteed, HD and Hipparcos fields where supplied. Derived from d3-celestial without geometry; it is independent of the magnitude-limited position subsets."),
    ("starnames.cn", "Chinese star names", "Name tables", "A CSV table of Chinese star names from d3-celestial, with source identifiers, designations, English translations and pinyin. It contains no geometry and complements the star position catalogs; identifiers should be matched using the source catalog conventions."),
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
