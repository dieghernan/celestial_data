# Croissant descriptors

Each of the 23 dataset landing pages embeds its descriptor once. Standalone
metadata is published at `croissant/<dataset-id>.json`. The collection retains
its existing Dataset identity, collection DOI and 23 `hasPart` entries; those
entries link to the children's descriptors through `subjectOf`. Children retain
`isPartOf` pointing to the collection's stable `#collection` identifier. The
collection is an index, not a claim that all catalogs form one homogeneous table.

## Records and field semantics

The official mlcroissant reader does not directly load GeoPackage or interpret
celestial GeoJSON geometries. Each dataset therefore has one additional gzip
JSON download with its attributes and, for spatial datasets, `geometry_wkt`.
The original 63 GeoJSON, GeoPackage and CSV downloads remain unchanged. Every
resource has a SHA-256 checksum and both FileObject and DataDownload types.
There are no internal archive members masquerading as direct downloads.

The pilot was `mw`: all five original MultiPolygon features were loaded and
compared with the original nested GeoJSON coordinates before extending the
pattern to all datasets. Tests now compare every attribute and geometry across
all 23 datasets using the official library, not just descriptor syntax.

- Original attributes retain their source names and numeric or text types.
- Absent GeoJSON properties and explicit nulls are represented as JSON null;
  no values are filled. Croissant reading preserves nulls.
- CSV cells remain text. Empty strings and the literal `NA` are kept unchanged,
  so catalog identifiers, multilingual names and missing-value markers are not
  silently interpreted as numbers or nulls.
- Magnitude sentinel `999` is preserved and documented as unavailable. The
  conversion does not filter records or recompute relative brightness.
- `record_index` is a one-based source row position and the local record key.
  It is not an astronomical identifier or a persistent key across releases.
- WKT preserves all coordinates and geometry ordering without reprojection,
  rounding or simplification. Tests compare its nested arrays with GeoJSON.

Coordinates are J2000 celestial directions encoded as geographic angles:
right ascension is converted from hours to degrees and wrapped to [-180,180];
declination supplies the second angle. EPSG:4326 in the original files is a GIS
compatibility label, not a claim of terrestrial locations. The descriptor does
not add Earth spatial coverage or a misleading terrestrial GeoCroissant CRS.
WKT does not carry this celestial reference frame; consumers must retain it.

Publication dates and version come from the existing collection metadata.
J2000 is an epoch, not a publication date. The DOI identifies the archived
collection; child datasets do not acquire invented individual DOIs. Public
original-file URLs follow the repository's current publication, as documented
by the collection; checksums identify the exact file contents described.

The context's `@base` is the dataset landing URL. Resource, record-set and field
identifiers therefore resolve consistently in the standalone descriptor and
embedded page, without colliding with another dataset. Use the expanded IDs
reported by the library:

```python
import mlcroissant as mlc

dataset = mlc.Dataset("https://dieghernan.github.io/celestial_data/croissant/mw.json")
record_set = dataset.metadata.record_sets[0].uuid
row = next(iter(dataset.records(record_set=record_set)))
outline = row[record_set + "/id"]
wkt = row[record_set + "/geometry_wkt"]
# Text can be UTF-8 bytes; decode it when needed.
```

## Generate and verify

Use Python 3.12:

```sh
pip install -r scripts/requirements-croissant.txt
python scripts/build_croissant.py --dataset mw
mlcroissant validate --jsonld croissant/mw.json
python -m unittest tests.test_croissant.CroissantTests.test_pilot_milky_way_preserves_all_five_polygons
python scripts/build_croissant.py
python scripts/build_croissant.py --check
bundle exec jekyll build
python -m unittest discover -s tests -p 'test_*.py'
node --test tests/celestial-preview.test.cjs
```

Sources are `_data/datasets.json`, `_data/structured_data.json`, the original
files under `data/` and the field dictionary in `scripts/build_croissant.py`.
Unknown fields or unsupported mixed types stop generation for documentation
review. See `data/README.md` and the upstream data-format documentation for
field meanings; undocumented classifications are retained literally.

Generated metadata lives in `_data/croissant.json` and `croissant/*.json`.
Content-addressed record downloads live under
`assets/croissant/<sha256>/records.json.gz`, ignored by Git and generated in CI.
Fixed gzip metadata and JSON Unicode escapes make output reproducible and avoid
the Windows gzip reader's legacy default-encoding problem. JSON escapes decode
to the original multilingual names. Do not edit generated metadata by hand.

CI checks regeneration, validates all descriptors, builds Jekyll and compares
all original rows with records loaded through mlcroissant before deployment.
Tests map URLs to local generated files; after deployment readers use the same
URLs without mapping. The schema aliases for `name` and `description` avoid the
language-container objects that Google Rich Results rejects. Chulapa templates,
microformats, existing visible pages and original data files are not edited.

Specifications and source documentation:

- https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html
- https://github.com/ofrohn/d3-celestial/blob/master/data/readme.md
