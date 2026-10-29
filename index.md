---
layout: default
dataset_collection: true
title: Celestial Data
header_type: hero
subtitle: Celestial datasets in GeoJSON and GeoPackage formats
excerpt: This project provides several datasets in GeoJSON
  and GeoPackage format of celestial objects for the J2000 epoch.
header_img: https://dieghernan.github.io/celestial_data/assets/img/ogimage.webp
project_links:
    - url: https://github.com/dieghernan/celestial_data/tree/main/data
      icon: fab fa-github
      label: View on GitHub
---

[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.7561601-blue)](https://doi.org/10.5281/zenodo.7561601)

This project provides several datasets in GeoJSON and GeoPackage
format of celestial objects for the J2000 epoch.

The source files come from [d3-celestial](https://github.com/ofrohn/d3-celestial/)
and are distributed under the [BSD 3-Clause license](https://opensource.org/licenses/BSD-3-Clause).
They were processed with **R** and **sf** to repair and validate geometries.
The conversion preserves the source attributes where possible, but some
invalid constellation lines were removed.

Coordinates describe the J2000 celestial reference, encoded as longitude-like
and latitude-like angles for GIS software. Assigning EPSG:4326 is a storage
convention here: these are not terrestrial WGS84 locations. J2000 does not
indicate when the files were downloaded or updated, and these static catalogs
do not calculate the current sky for an observer.

Geometry validation was performed with GEOS 3.9.3. It checks geometric validity,
not the astronomical accuracy or completeness of the source catalogs.

## Distribution

The same files are available through the website, GitHub and jsDelivr.
These URLs follow the main branch and may differ from an archived release
identified by the collection DOI.

The following example downloads the minified Milky Way dataset:

``` html

<!-- From GitHub -->
https://raw.githubusercontent.com/dieghernan/celestial_data/main/data/mw.min.geojson

<!-- From the Website -->
https://dieghernan.github.io/celestial_data/data/mw.min.geojson

<!-- From jsDelivr -->
https://cdn.jsdelivr.net/gh/dieghernan/celestial_data@main/data/mw.min.geojson
```

## Data

Browse **19 geographic datasets** and **six complementary CSV tables**.
Each dataset page provides direct downloads, file sizes and metadata.

<a class="btn btn-primary mb-3" href="{{ '/data' | relative_url }}#downloads">Browse datasets and downloads</a>
<a class="btn btn-outline-primary mb-3" href="{{ '/preview' | relative_url }}">Preview selected datasets</a>

GeoJSON and GeoPackage contain spatial features. Minified GeoJSON removes
whitespace without simplifying geometries. The CSV files contain attributes
and names without geometry.

## Citation

Please cite these datasets as:

Frohn, O., & Hernangómez, D. (2023). Celestial Data [Data set].
<https://doi.org/10.5281/zenodo.7561601>

The DOI above identifies the collection across releases. To cite the archived
`v1.0.1` release specifically, use <https://doi.org/10.5281/zenodo.7568546>.
Downloads from the main branch may differ from that release.

A BibTeX entry:

``` bibtex

@misc{frohnhernangomez:2023,
    title        = {Celestial Data},
    author       = {Olaf Frohn and Diego Hernangómez},
    year         = 2023,
    doi          = {10.5281/zenodo.7561601},
    url          = {https://dieghernan.github.io/celestial_data/},
}

```

## References

<div id="ref-frohn2015" class="csl-entry" markdown=1>

Frohn, Olaf. 2015. "d3-celestial" <https://github.com/ofrohn/d3-celestial/>.

</div>

<div id="ref-pebesma2018" class="csl-entry" markdown=1>

Pebesma, Edzer. 2018. "Simple Features for R: Standardized Support for
Spatial Vector Data." *The R Journal* 10 (1): 439–446.
<https://doi.org/10.32614/RJ-2018-009>.

</div>
