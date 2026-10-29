
# Celestial Data

[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.7561601-blue)](https://doi.org/10.5281/zenodo.7561601)
![GitHub release (latest
SemVer)](https://img.shields.io/github/v/release/dieghernan/celestial_data)

This repository contains several datasets in GeoJSON and GeoPackage
format of celestial objects for the J2000 epoch.

The source files come from
[d3-celestial](https://github.com/ofrohn/d3-celestial/) ([Frohn
2015](#ref-frohn2015)) and are distributed under the [BSD 3-Clause
license](https://opensource.org/licenses/BSD-3-Clause). They were
processed with **R** and **sf** ([Pebesma 2018](#ref-pebesma2018)) to
repair and validate geometries. The conversion preserves the source
attributes where possible, but some invalid constellation lines were
removed.

Coordinates describe the J2000 celestial reference, encoded as
longitude-like and latitude-like angles for GIS software. Assigning
EPSG:4326 is a storage convention here: these are not terrestrial WGS84
locations. J2000 does not indicate when the files were downloaded or
updated, and these static catalogs do not calculate the current sky for
an observer.

Geometry validation was performed with GEOS 3.9.3. It checks geometric
validity, not the astronomical accuracy or completeness of the source
catalogs.

## Distribution

The same files are available through the website, GitHub and jsDelivr.
These URLs follow the main branch and may differ from an archived
release identified by the collection DOI.

The following example downloads the minified Milky Way dataset:

``` html

<!-- From GitHub -->
https://raw.githubusercontent.com/dieghernan/celestial_data/main/data/mw.min.geojson

<!-- From the Website -->
https://dieghernan.github.io/celestial_data/data/mw.min.geojson

<!-- From jsDelivr -->
https://cdn.jsdelivr.net/gh/dieghernan/celestial_data@main/data/mw.min.geojson
```

## Citation

Please cite these datasets as:

Frohn O, Hernangómez D (2023). “Celestial Data.”
<doi:10.5281/zenodo.7561601> <https://doi.org/10.5281/zenodo.7561601>,
<https://dieghernan.github.io/celestial_data/>.

The DOI above identifies the collection across releases. To cite the
archived `v1.0.1` release specifically, use
<https://doi.org/10.5281/zenodo.7568546>. Downloads from the main branch
may differ from that release.

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

## Data

Data is provided in GeoJSON (`*.geojson`) and GeoPackage (`*.gpkg`)
format. Minified GeoJSON (`*.min.geojson`) removes whitespace without
simplifying geometries. Complementary CSV files contain names and
attributes without geometry.

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

Browse download cards, file sizes and dataset descriptions at
<https://dieghernan.github.io/celestial_data/data>.

Maintainers can refresh file sizes, feature counts and dataset pages
with `py scripts/build_catalog.py` after updating the data. The
generator keeps the download catalog and structured metadata consistent.

## Original data sources

The following original data sources are cited by Frohn
([2015](#ref-frohn2015)):

- `asterisms.*`:

  - [Saguaro Astronomy Club
    Asterisms](http://saguaroastro.org/sac-downloads/)

- `constellations.*` and `constellations.lines.*`:

  - [IAU Constellation
    page](https://www.iau.org/IAU/Astronomy-FAQs/Constellations.aspx),
    with label positions and some line modifications by Olaf Frohn.
    Multilingual names are inherited from
    [d3-celestial](https://github.com/ofrohn/d3-celestial/), whose
    source notes credit Wikipedia.

- `constellations.bounds.*`:

  - Davenhall, A. C., and S. K. Leggett. 1989. “Catalogue of
    Constellation Boundary Data.”
    <https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=VI/49>.

- Traditional Chinese constellations and stars: `constellations.cn.*`,
  `constellations.bounds.cn.*`, `constellations.lines.cn.*`,
  `starnames.cn.*`:

  - [Stellarium skycultures
    data](https://github.com/Stellarium/stellarium/tree/master/skycultures/chinese)

- `dsos.6.*`, `dsos.14.*`, `dsos.20.*`:

  - [Saguaro Astronomy Club Database version
    8.1](http://www.saguaroastro.org/sac-downloads/)

- `dsos.bright.*`

  - Frohn, Olaf. 2015. “d3-celestial.”
    <https://github.com/ofrohn/d3-celestial/>.

- `messier.*` Messier objects:

  - [Messier Objects with Data](http://messier.seds.org/data.html),
    H.Frommert/seds.org

- `lg.*` Local group and Milky Way halo:

  - Frohn, Olaf. 2015. “d3-celestial.”
    <https://github.com/ofrohn/d3-celestial/>, from different sources:
    see
    [blog](https://armchairastronautics.blogspot.com/p/milky-way-halo.html),
    [pages](https://armchairastronautics.blogspot.com/p/local-group.html)
    for complete list.

- `stars.6.*`, `stars.8.*`, `stars.14.*`:

  - Anderson, E., and Ch. Francis. 2012. “XHIP: An Extended Hipparcos
    Compilation.” *Astronomy Letters* 38 (5): 331–46.
    <https://doi.org/10.1134/S1063773712050015>.

- `starnames.*` Star names and designations:

  - Kostjuk, N. D. 2002. “VizieR Online Data Catalog:
    HD-DM-GC-HR-HIP-Bayer-Flamsteed Cross Index.” *VizieR Online Data
    Catalog*, IV/27A.
    <https://ui.adsabs.harvard.edu/abs/2004yCat.4027....0K>.

  - [Stellarium skycultures
    data](https://github.com/Stellarium/stellarium/tree/master/po/stellarium-skycultures)
    for star name translations

## Webmentions

After each successful deployment, the `Send outgoing Webmentions` workflow
checks external links in published page content and sends mentions to
destinations that advertise a compatible endpoint. It uses the HTML built from
the repository root and stores delivery state in the `webmention-state` branch
to avoid repeated submissions while the content is unchanged. Failed requests
are retried on later runs. The workflow can also be run manually from GitHub
Actions.

## References

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-anderson_xhip_2012" class="csl-entry">

Anderson, E., and Ch. Francis. 2012. “XHIP: An Extended Hipparcos
Compilation.” *Astronomy Letters* 38 (5): 331–46.
<https://doi.org/10.1134/S1063773712050015>.

</div>

<div id="ref-butler_geojson_2016" class="csl-entry">

Butler, H., M. Daly, A. Doyle, S. Gillies, S. Hagen, and T. Schaub.
2016. *The GeoJSON Format*. RFC No. 7946. RFC Editor.
<https://doi.org/10.17487/RFC7946>.

</div>

<div id="ref-davenhall1989misc" class="csl-entry">

Davenhall, A. C., and S. K. Leggett. 1989. *Catalogue of Constellation
Boundary Data*.
<https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=VI/49>.

</div>

<div id="ref-frohn2015" class="csl-entry">

Frohn, Olaf. 2015. *<span class="nocase">d3-celestial</span>*.
<https://github.com/ofrohn/d3-celestial/>.

</div>

<div id="ref-gliese_preliminary_1991" class="csl-entry">

Gliese, W., and H. Jahreiß. 1991. *Preliminary Version of the Third
Catalogue of Nearby Stars*.
<https://ui.adsabs.harvard.edu/abs/1991adc..rept.....G>.

</div>

<div id="ref-kostjuk_vizier_2002" class="csl-entry">

Kostjuk, N. D. 2002. “VizieR Online Data Catalog:
HD-DM-GC-HR-HIP-Bayer-Flamsteed Cross Index.” *VizieR Online Data
Catalog*, IV/27A.
<https://ui.adsabs.harvard.edu/abs/2004yCat.4027....0K>.

</div>

<div id="ref-pebesma2018" class="csl-entry">

Pebesma, Edzer. 2018. “Simple Features for R: Standardized Support for
Spatial Vector Data.” *The R Journal* 10 (1): 439–46.
<https://doi.org/10.32614/RJ-2018-009>.

</div>

<div id="ref-samus_general_2017" class="csl-entry">

Samus’, N. N., E. V. Kazarovets, O. V. Durlevich, N. N. Kireeva, and E.
N. Pastukhova. 2017. “General Catalogue of Variable Stars: Version GCVS
5.1.” *Astronomy Reports* 61 (1): 80–88.
<https://doi.org/10.1134/S1063772917010085>.

</div>

<div id="ref-smith_vizier_1996" class="csl-entry">

Smith, W. B. 1996. “VizieR Online Data Catalog: FK5 - SAO - HD - Common
Name Cross Index.” *VizieR Online Data Catalog*, August, IV/22.
<https://ui.adsabs.harvard.edu/abs/1996yCat.4022....0S>.

</div>

</div>
