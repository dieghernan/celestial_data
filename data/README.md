# Data formats

Geographic datasets are available as GeoJSON (`*.geojson`) and GeoPackage
(`*.gpkg`). Minified GeoJSON (`*.min.geojson`) removes whitespace without
simplifying geometries. CSV files contain names and attributes without geometry.

The coordinates use the J2000 celestial reference. Right ascension is converted
from hours to degrees (15 degrees per hour), then wrapped into [-180, 180].
Declination supplies the latitude-like angle in [-90, 90]. For example, 6h maps
to 90 degrees and 18h maps to -90 degrees.

EPSG:4326 is assigned for compatibility with GIS software. These angles describe
celestial directions, not terrestrial WGS84 locations. Earth-based distances,
areas and basemaps do not acquire astronomical meaning from this encoding.
J2000 is a reference epoch, not a file update date; the files do not calculate
current positions or a location-based view of the night sky.

Geometries were validated with GEOS 3.9.3. Geometric validity does not establish
astronomical accuracy or catalog completeness. Some degenerate source lines
were removed during conversion.

# Distribution

Browse download cards and sizes at
<https://dieghernan.github.io/celestial_data/data#downloads>.

The website, GitHub and jsDelivr provide alternative URLs for the same files.
These URLs follow the main branch. For an archived release, use the collection
DOI: <https://doi.org/10.5281/zenodo.7561601>.

For example, download the minified Milky Way dataset from:

``` html

<!-- From GitHub -->
https://raw.githubusercontent.com/dieghernan/celestial_data/main/data/mw.min.geojson

<!-- From the Website -->
https://dieghernan.github.io/celestial_data/data/mw.min.geojson

<!-- From jsDelivr -->
https://cdn.jsdelivr.net/gh/dieghernan/celestial_data@main/data/mw.min.geojson
```

# Data

## Asterisms

`asterisms.<data format>` (`MULTILINESTRING`) with 65 features and the following attributes:

-   **id**: Name without spaces

-   **n**: Proper name

-   **es**: Proper name in Spanish

-   **p**: Display priority (1–6), approximately related to brightness; 6
    denotes a guide line

-   **loc_lon**, **loc_lat**: Label position in the same angular encoding as the
    geometry

## Constellations

`constellations.<data format>` (`POINT`) with 89 objects. Additionally a
`constellations.csv` file with the attributes (no geometry) is also provided.
The points are label positions, not constellation regions. The 89 records
include separate entries for Serpens Caput and Serpens Cauda:

-   **id**: 3-letter designator

-   **name**: Full IAU name

-   **desig**: 3-letter designator again

-   **gen**: Genitive form used for naming stars

-   **rank**: 1-3 for differential name display by size/brightness

-   **en**: English name; other fields provide names in additional languages

-   **display_ra**, **display_dec**, **display_scale**: View center and scale
    for displaying a single constellation; these are display parameters

### Traditional Chinese constellations

`constellations.cn.<data format>` (`POINT`) with 312 objects. Additionally a
`constellations.cn.csv` file with the attributes (no geometry) is also provided:

-   **id**: Numerical identifier
-   **name**: Chinese name
-   **en**: English translation
-   **pinyin**: Pinyin transcription
-   **desig**: Chinese name repeated for compatibility
-   **rank**: Display priority; currently 1 in this dataset
-   **display_ra**, **display_dec**, **display_scale**: View center and scale
    for displaying a single constellation; these are display parameters

## Constellation boundaries

`constellations.borders.<data format>` (`MULTILINESTRING`) with 257 objects.

-   **ids**: String with format "3-letter designator A, 3-letter designator B"
    identifying the constellations surrounding the border.

`constellations.bounds.<data format>` (`MULTIPOLYGON`) with 89 objects. See
**Constellation lines** for field descriptions.

### Traditional Chinese constellations

`constellations.borders.cn.<data format>` (`LINESTRING`) with 84 objects.

-   **ids**: Border identifier

`constellations.bounds.cn.<data format>` (`POLYGON`) with 28 objects. See
**Constellation lines** for field descriptions.

## Constellation lines

`constellations.lines.<data format>` (`MULTILINESTRING`) with 89 objects.

-   **id**: 3-letter designator

-   **rank**: 1-3 for differential name display by size/brightness

-   **name**: Full IAU name

### Traditional Chinese constellations

`constellations.lines.cn.<data format>` (`MULTILINESTRING`) with 255
features.

Some records were removed from the
[original dataset](https://github.com/ofrohn/d3-celestial/blob/master/data/constellations.lines.cn.json)
because their line geometry contained only one position. A GeoJSON
LineString requires at least two positions; a MultiLineString contains
arrays of such lines.

-   **id**: Numerical identifier
-   **rank**: Display priority; currently 1 in this dataset
-   **name**: Chinese name
-   **en**: English translation

## DSOs

Deep-sky objects (DSOs) include galaxies, nebulae and star clusters.

### DSO names

`dsonames.csv` with 724 rows:

-   **id**: Short designator

-   **name**: Proper name; other fields provide translations

### Traditional Chinese DSO names

`dsonames.cn.csv` with 6 rows:

-   **id**: Deep-sky catalog designation, such as NGC 224
-   **name**: Chinese name
-   **desig**: Catalog designation
-   **en**: English translation
-   **pinyin**: Pinyin transcription

### DSOs

Several files:

-   `dsos.6.<data format>`, `dsos.14.<data format>`, `dsos.20.<data format>`:
    the number indicates the nominal limiting magnitude.

-   `dsos.bright.<data format>`: hand selected DSOs.

-   `lg.<data format>`: Local group.

-   `messier.<data format>` Messier objects.

These catalogs contain `POINT` geometries. Attributes vary between catalogs;
for example, Messier includes `alt` and `cl` but does not include `bv` or
`morph`. Unknown magnitudes (`999`) must be excluded from numeric magnitude
filters and brightness calculations.

Common attributes include:

-   **id**: Short designator

-   **desig**: Designator

-   **type**: Object type: gg *(galaxy cluster)*, g: *(galaxy)*, s: *(spiral
    galaxy)*, s0: *(lenticular gal.)*, sd: *(dwarf spheroidal gal.)*, i:
    *(irregular gal.)*, e: *(elliptical gal.)*, oc: *(open cluster)*, gc:
    *(globular cluster)*, dn: *(dark nebula)*, bn: *(bright nebula)*, sfr:
    *(star forming region)*, rn: *(reflection nebula)*, en: *(emission nebula)*,
    pn: *(planetary nebula)*, snr: *(supernova remnant)*.

-   **morph**: Morphology classification depending on type

-   **mag**: Apparent magnitude; 999 indicates an unavailable value

-   **dim**: Angular dimensions in arcminutes

-   **bv**: Blue-minus-visual color index (B−V)

-   **br**: Relative brightness compared with magnitude 0, computed as $100^{-1
    * mag / 5}$

-   **name**: Proper name

Additional fields on `lg.<data format>`:

-   **sub**: Sub group membership: `MW|M31|N3109|LG` (Milky Way, Andromeda, NGC
    3109, gen. LG)

-   **pop**: MW populations `OH|YH|BD` (Old halo, young halo, bulge & disk), M31
    populations `M31|GP` (gen. M31, great plane)

-   **str**: Tidal streams `Mag|Sgr|CMa|FLS` (Magellanic Stream, Sagittarius
    Stream, Canis Major/Monoceros Stream, Fornax-Leo-Sculptor Great Circle)

## Stars

### Star names

`starnames.csv` has 4869 rows of names and designations, independent of the
star catalog magnitude subsets. Some name fields are empty or unavailable.

-   **id**: Hipparcos number
-   **name**: Proper name; other fields provide translations
-   **desig**: Preferred display designation from the available catalog names
-   **bayer**: Bayer designation
-   **flam**: Flamsteed designation
-   **var**: Variable star designation
-   **gliese**: Gliese designation
-   **hd**: Henry Draper catalog designation
-   **hip**: Hipparcos number again

### Traditional Chinese star names

`starnames.cn.csv` with 3056 rows:

-   **id**: Hipparcos number
-   **name**: Chinese name
-   **desig**: Catalog designation
-   **en**: English translation
-   **pinyin**: Pinyin transcription

### Stars

`stars.6.<data format>`, `stars.8.<data format>`, `stars.14.<data format>`: the
number indicates the nominal limiting magnitude. Smaller magnitudes indicate
brighter objects. The local `stars.8` file reaches magnitude 8.0, although the
upstream project describes its current counterpart as reaching 8.5. These
subsets do not guarantee a complete survey of all objects to that magnitude:

-   **id**: Star identifier (Hipparcos number)

-   **mag**: Apparent magnitude; 999 indicates an unavailable value

-   **bv**: Blue-minus-visual color index (B−V)

-   **br**: Relative brightness compared with magnitude 0, computed as $100^{-1
    * mag / 5}$

-   **name**: Proper name

## Milky Way

`mw.<data format>` with 5 rows:

-   **id**: Milky Way outlines in 5 brightness steps (ol1-ol5).
