---
layout: default
title: Celestial Data
header_type: hero
subtitle: A compilation of celestial data files
header_img: https://dieghernan.github.io/celestial_data/assets/img/ogimage.png
---


[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.7561601-blue)](https://doi.org/10.5281/zenodo.7561601)

This project provides several datasets in GeoJSON and GeoPackage
format of celestial objects as of J2000 epoch.

The original files were provided on the [d3-celestial
plugin](https://github.com/ofrohn/d3-celestial/) ([Frohn
2015](#ref-frohn2015)) under [BSD
3-Clause](https://opensource.org/licenses/BSD-3-Clause). The datasets produced 
on this project consists on the same data provided on [d3-celestial plugin](https://github.com/ofrohn/d3-celestial/) processed with the
**R** package **sf** ([Pebesma 2018](#ref-pebesma2018)) to ensure its
validity:

- The spatial data objects are bounded to $$[-180, -90, 180, 90]$$.

- Date is provided on WGS84 - World Geodetic System 1984
  ([EPSG:4326](https://epsg.io/4326)).

- All geometries valid as per
  [ST_IsValid](https://postgis.net/docs/ST_IsValid.html) (GEOS
  **3.9.3**).

## Distribution

The data can be accessed from several API endpoints:

``` html

<!-- From GitHub -->
https://raw.githubusercontent.com/dieghernan/celestial_data/main/data/mw.min.geojson

<!-- From the Website -->
https://dieghernan.github.io/celestial_data/data/mw.min.geojson

<!-- From jsDelivr -->
https://cdn.jsdelivr.net/gh/dieghernan/celestial_data@main/data/mw.min.geojson
```

## Data

Data is provided in GeoJSON (`*.geojson`) and GeoPackage (`*.gpkg`) format.
Additionally, for GeoJSON formats a minified version (`*.min.geojson`) is
also provided.

The data source can be found on
<https://github.com/dieghernan/celestial_data/tree/main/data>.

<details>
<summary>
List of files provided
</summary>

- `asterisms.geojson`
- `asterisms.gpkg`
- `asterisms.min.geojson`
- `constellations.borders.cn.geojson`
- `constellations.borders.cn.gpkg`
- `constellations.borders.cn.min.geojson`
- `constellations.borders.geojson`
- `constellations.borders.gpkg`
- `constellations.borders.min.geojson`
- `constellations.borders.min.min.geojson`
- `constellations.bounds.cn.geojson`
- `constellations.bounds.cn.gpkg`
- `constellations.bounds.cn.min.geojson`
- `constellations.bounds.geojson`
- `constellations.bounds.gpkg`
- `constellations.bounds.min.geojson`
- `constellations.cn.csv`
- `constellations.cn.geojson`
- `constellations.cn.gpkg`
- `constellations.cn.min.geojson`
- `constellations.csv`
- `constellations.geojson`
- `constellations.gpkg`
- `constellations.lines.cn.geojson`
- `constellations.lines.cn.gpkg`
- `constellations.lines.cn.min.geojson`
- `constellations.lines.geojson`
- `constellations.lines.gpkg`
- `constellations.lines.min.geojson`
- `constellations.min.geojson`
- `dsonames.cn.csv`
- `dsonames.csv`
- `dsos.14.geojson`
- `dsos.14.gpkg`
- `dsos.14.min.geojson`
- `dsos.20.geojson`
- `dsos.20.gpkg`
- `dsos.20.min.geojson`
- `dsos.6.geojson`
- `dsos.6.gpkg`
- `dsos.6.min.geojson`
- `dsos.bright.geojson`
- `dsos.bright.gpkg`
- `dsos.bright.min.geojson`
- `lg.geojson`
- `lg.gpkg`
- `lg.min.geojson`
- `messier.geojson`
- `messier.gpkg`
- `messier.min.geojson`
- `mw.geojson`
- `mw.gpkg`
- `mw.min.geojson`
- `starnames.cn.csv`
- `starnames.csv`
- `stars.14.geojson`
- `stars.14.gpkg`
- `stars.14.min.geojson`
- `stars.6.geojson`
- `stars.6.gpkg`
- `stars.6.min.geojson`
- `stars.8.geojson`
- `stars.8.gpkg`
- `stars.8.min.geojson`

</details>

See additional details on <https://dieghernan.github.io/celestial_data/data>


## Citation

Please cite these datasets as:

Frohn O, Hernangómez D (2023). "Celestial Data." <doi:10.5281/zenodo.7561601>
<https://doi.org/10.5281/zenodo.7561601>,
<https://dieghernan.github.io/celestial_data/>.

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

<div id="refs" class="references csl-bib-body hanging-indent" markdown=1>

<div id="ref-frohn2015" class="csl-entry">

Frohn, Olaf. 2015. “<span class="nocase">d3-celestial</span>.”
<https://github.com/ofrohn/d3-celestial/>.

</div>


<div id="ref-pebesma2018" class="csl-entry">

Pebesma, Edzer. 2018. “Simple Features for R: Standardized Support for
Spatial Vector Data.” *The R Journal* 10 (1): 439446.
<https://doi.org/10.32614/RJ-2018-009>.

</div>

</div>
