"""Build Croissant descriptors and lossless JSON/WKT views of the 23 datasets."""

import argparse
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path

import shapely

ROOT = Path(__file__).resolve().parents[1]
HOME = "https://dieghernan.github.io/celestial_data/"
LANGUAGES = {"ar": "Arabic", "zh": "Chinese", "el": "Greek", "ja": "Japanese", "ko": "Korean", "ru": "Russian", "he": "Hebrew", "de": "German", "es": "Spanish", "fi": "Finnish", "fr": "French", "it": "Italian", "la": "Latin", "tr": "Turkish", "fa": "Persian", "hi": "Hindi", "en": "English", "cz": "Czech", "sw": "Swahili", "ee": "Estonian"}
DESCRIPTIONS = {
    "record_index": "One-based row position in this source snapshot; unique within this record set, not an astronomical catalog identifier or a persistent cross-release key.",
    "geometry_wkt": "Original geometry encoded as WKT without reprojection, rounding or simplification. J2000 celestial angles in degrees: x is right ascension converted from hours at 15 degrees/hour and wrapped to [-180,180]; y is declination. These are not terrestrial WGS84 positions. WKT itself does not carry this reference frame.",
    "name": "Name stored in the source; its convention depends on the catalog. Nulls and empty strings are preserved, not filled from another language.",
    "n": "Proper name of the asterism, as supplied by the source.",
    "id": "Identifier as stored in this source catalog, preserving its original text or numeric representation. It is not assumed unique across catalogs or records.",
    "ids": "Border identifier stored in the source; constellation pairs remain a single string, not a normalized relation.",
    "desig": "Source designation; its convention depends on the catalog. No catalog prefixes or missing values are inferred.",
    "mag": "Apparent magnitude in the source. The sentinel 999 means unavailable and is preserved; exclude it from magnitude filters and brightness calculations. JSON null also remains missing.",
    "bv": "Blue-minus-visual color index (B-V), a difference of magnitudes. Null means missing in this source, not zero.",
    "br": "Relative brightness stored in the source, normalized to magnitude zero: 100**(-mag/5). This is not calibrated physical flux. Values are preserved rather than recomputed, including missing values or source sentinel effects.",
    "dim": "Angular dimensions in arcminutes, retained as source text; compound dimension strings are not converted into a scalar. Null means missing.",
    "morph": "Morphological classification supplied by the source; interpretation depends on object type. Null means missing.",
    "type": "Source object-type code, such as g (galaxy), oc (open cluster) or pn (planetary nebula); no classification is inferred for missing values.",
    "rank": "Source display-priority rank, not a physical measurement; its scale depends on the constellation catalog.",
    "p": "Asterism display priority from 1 to 6; 6 denotes a guide line. This is a display parameter, not measured brightness.",
    "loc_lon": "Asterism label x position in the same celestial-angle encoding as the geometry, in degrees; not terrestrial longitude.",
    "loc_lat": "Asterism label y position (declination-like angle) in degrees; not terrestrial latitude.",
    "display_ra": "Right-ascension display-center parameter copied from the source; not a new position measurement or a current-epoch prediction.",
    "display_dec": "Declination display-center parameter copied from the source; not a new position measurement.",
    "display_scale": "Source display-scale parameter; not an angular size or a distance.",
    "gen": "Genitive name used for stellar naming, as supplied by the source.",
    "pinyin": "Pinyin transcription provided by the source.",
    "sub": "Local-group membership code from the source: MW, M31, N3109 or LG.",
    "pop": "Source population code for the Milky Way or M31; null means unspecified.",
    "str": "Source tidal-stream association code; null means unspecified.",
    "bayer": "Bayer designation stored as text in the names table.",
    "flam": "Flamsteed designation stored as text in the names table.",
    "var": "Variable-star designation stored as text in the names table.",
    "hd": "Henry Draper designation stored as text, without numeric conversion.",
    "hip": "Hipparcos designation stored as text, without numeric conversion.",
    "gliese": "Gliese designation stored as text in the names table.",
    "gl": "Source gl field from the names table, retained literally without inventing a catalog interpretation.",
    "c": "Source constellation field from the names table, retained as text.",
    "alt": "Alternative source designation, retained literally; null means unspecified.",
    "cl": "Source cl classification field, retained literally without imposing an undocumented classification scheme.",
}


def read_source(entry):
    path = ROOT / "data" / (entry["id"] + (".geojson" if entry["geometry"] else ".csv"))
    if entry["geometry"]:
        features = json.loads(path.read_text(encoding="utf-8"))["features"]
        columns = sorted(set().union(*(feature["properties"] for feature in features)))
        rows = []
        for index, feature in enumerate(features, 1):
            geom = shapely.geometry.shape(feature["geometry"])
            wkt = shapely.to_wkt(geom, rounding_precision=-1)
            if not shapely.equals_exact(geom, shapely.from_wkt(wkt), tolerance=0):
                raise ValueError(f"WKT changes coordinates in {entry['id']} row {index}.")
            rows.append({"record_index": index, **{column: feature["properties"].get(column) for column in columns}, "geometry_wkt": wkt})
    else:
        with path.open(encoding="utf-8", newline="") as stream:
            rows = [{"record_index": index, **row} for index, row in enumerate(csv.DictReader(stream), 1)]
    if len(rows) != entry["count"]:
        raise ValueError(f"Catalog count differs from source: {entry['id']}")
    return rows


def field_type(values):
    types = {type(value) for value in values if value is not None}
    if not types or types == {str}:
        return "sc:Text"
    if types == {int}:
        return "sc:Integer"
    if types <= {int, float}:
        return "sc:Float"
    raise ValueError(f"Unsupported field types: {types}")


def build(check=False, only=None):
    catalog = json.loads((ROOT / "_data/datasets.json").read_text(encoding="utf-8"))
    common = json.loads((ROOT / "_data/structured_data.json").read_text(encoding="utf-8"))
    context = json.loads((ROOT / "_data/croissant_context.json").read_text(encoding="utf-8"))
    collection = {"@id": HOME + "#collection"}
    descriptors = {}
    for entry in catalog:
        key = entry["id"]
        if only and key != only:
            continue
        rows = read_source(entry)
        content = json.dumps(rows, ensure_ascii=True, separators=(",", ":"), allow_nan=False).encode("ascii")
        buffer = io.BytesIO()
        with gzip.GzipFile(filename="", fileobj=buffer, mode="wb", compresslevel=6, mtime=0) as stream:
            stream.write(content)
        content = buffer.getvalue()
        digest = hashlib.sha256(content).hexdigest()
        relative = f"assets/croissant/{digest}/records.json.gz"
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        landing = HOME + "datasets/" + key + "/"
        descriptor = {"@context": {**context, "@base": landing}, "@type": "Dataset", "@id": landing + "#dataset", "url": landing,
            "name": entry["name"], "description": entry["description"], **common["publication"], "keywords": entry["keywords"],
            "license": common["license"], "creator": common["creator"], "isAccessibleForFree": common["isAccessibleForFree"],
            "isBasedOn": common["isBasedOn"], "isPartOf": collection, "conformsTo": "http://mlcommons.org/croissant/1.1",
            "citeAs": "Part of Celestial Data (1.0.1), collection DOI: https://doi.org/10.5281/zenodo.7561601. The DOI identifies the archived collection, not a separate DOI for this dataset.",
            "distribution": [], "recordSet": []}
        for file in entry["distributions"]:
            original = (ROOT / "data" / file["filename"]).read_bytes()
            if len(original) != file["bytes"]:
                raise ValueError(f"Stale catalog size: {file['filename']}")
            descriptor["distribution"].append({"@type": ["cr:FileObject", "sc:DataDownload"], "@id": file["filename"], "name": file["label"], "encodingFormat": file["mime"], "contentSize": f"{len(original)} bytes", "contentUrl": HOME + "data/" + file["filename"], "sha256": hashlib.sha256(original).hexdigest()})
        descriptor["distribution"].append({"@type": ["cr:FileObject", "sc:DataDownload"], "@id": "records-json", "name": entry["name"] + " (JSON/WKT, gzip)", "contentUrl": HOME + relative, "encodingFormat": "application/json", "contentSize": f"{len(content)} bytes", "sha256": digest})
        fields = []
        for column in rows[0]:
            description = DESCRIPTIONS.get(column)
            if column in LANGUAGES:
                description = "Source name in " + LANGUAGES[column] + "; no translation or normalization is added."
            if description is None:
                raise ValueError(f"Document field before publishing: {key}/{column}")
            if not entry["geometry"]:
                description += " CSV text is preserved literally: empty cells remain empty strings and the literal NA is not converted to JSON null."
            else:
                description += " Absent properties and JSON null are represented as null; missing values are not imputed."
            fields.append({"@type": "cr:Field", "@id": "records/" + column, "name": column, "description": description,
                "dataType": field_type(row[column] for row in rows),
                "source": {"fileObject": {"@id": "records-json"}, "extract": {"jsonPath": "$[*]." + column}}})
        descriptor["recordSet"] = [{"@type": "cr:RecordSet", "@id": "records", "name": "records",
            "description": "One record per source feature or CSV row in its original order. No values are imputed. Publication dates describe the collection release, not observations; J2000 is a celestial reference epoch, not a file date. The row-position key is local to this snapshot.",
            "key": {"@id": "records/record_index"}, "field": fields}]
        descriptors[key] = descriptor
        write_json(ROOT / "croissant" / (key + ".json"), descriptor, check)
    if only and not descriptors:
        raise ValueError(f"Unknown dataset: {only}")
    if not only:
        write_json(ROOT / "_data/croissant.json", descriptors, check)
    return descriptors


def write_json(path, value, check):
    output = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if check:
        if not path.exists() or path.read_text(encoding="utf-8") != output:
            raise ValueError(f"Stale descriptor: {path}. Run scripts/build_croissant.py.")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--dataset", help="Build one pilot descriptor before generating the whole collection.")
    args = parser.parse_args()
    build(check=args.check, only=args.dataset)
