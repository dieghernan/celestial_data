# Project structured data

These includes generate only the project's Dataset JSON-LD. They do not
replace or modify Chulapa's WebSite, WebPage, Person or breadcrumb markup.

- `_data/structured_data.json` holds the publication metadata, collection
  description, creators, license and provenance.
- `scripts/build_catalog.py` generates `_data/datasets.json`, including each
  dataset's keywords and the formats and sizes of its downloadable files.
- `collection.html` describes the collection and its 23 members. Its summary
  form supplies the collection identity in a child dataset's `isPartOf`.
- `dataset.html` describes a dataset, with a summary form for `hasPart`.
- `distribution.html` describes a downloadable file.
- `release.html` supplies the shared publication dates and version.

The publication metadata refers to the archived release, not the website build
date. Downloads follow `main`; review these values when data content changes.
The collection DOI must not be assigned as an individual dataset's identifier.

After changing metadata, run `py scripts/build_catalog.py`, build the site with
`bundle exec jekyll build`, then run `py -m unittest discover -s tests`.
