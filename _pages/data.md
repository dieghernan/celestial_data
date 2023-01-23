---
title: Data description
permalink: /data
excerpt: Description of the data provided
show_sidetoc: true
project_links:
    - url: https://github.com/dieghernan/celestial_data/tree/main/data
      icon: fab fa-github         
      label: View on Github       
h_max: 3
---

## Data Formats

Data is provided in GeoJSON (`*.geojson`) and GeoPackage (`*.gpkg`) format.
Additionally, for GeoJSON formats a minified version (`*.min.geojson`) is also
provided.

All data complies with the GeoJSON format (provided in
[EPSG:4326](https://epsg.io/4326), bounded to $$[-180, -90, 180, 90]$$ and
geometries valid as per [ST_IsValid](https://postgis.net/docs/ST_IsValid.html)
on GEOS **3.9.3**).

All data provided at J2000 epoch, positions converted from 0...24h right
ascension to -180...180 degrees longitude as per GeoJSON requirements, so
0...12h becomes 0...180 degrees, and 12...24h becomes -180...0 degrees.

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

## Description

### Asterisms

`asterisms.<data format>` (`MULTILINESTRING`) with 65 objects the following attributes:

-   **id**: Name without spaces

-   **n**: Proper name

-   **es**: Proper name in Spanish

-   **p**: Priority 1..6 (\~Average brightness)

-   **loc_lon**, **loc_lat**: Center location of name string

### Constellations

`constellations.<data format>` (`POINT`) with 89 objects. Additionally a
`constellations.csv` file with the data (no coordinates) is also provided:

-   **id**: 3-letter designator

-   **name**: full IAU name

-   **desig**: 3-letter designator again

-   **gen**: genitive for naming stars.

-   **rank**: 1-3 for differential name display by size/brightness

-   **en**: English name ... and names in 18 further languages

-   **display_ra**, **display_dec**, **display_scale**: for single constellation
    display

#### Traditional Chinese constellations

`constellations.cn.<data format>` (`POINT`) with 312 objects. Additionally a
`constellations.cn.csv` file with the data (no coordinates) is also provided:

-   **id:** numerical id
-   **name**: Chinese name
-   **en**: English translation
-   **pinyin**: pinyin transcription
-   **desig**: also Chinese name, for compatibility
-   **rank**: so far only 1; differential name display by size/brightness
-   **display_ra**, **display_dec**, **display_scale**: for single constellation
    display

### Constellation boundaries

`constellations.borders.<data format>` (`MULTILINESTRING`) with 257 objects.

-   **ids**: String with format "3-letter designator A, 3-letter designator B"
    identifying the constellations surrounding the border.

`constellations.bounds.<data format>` (`MULTIPOLYGON`) with 89 objects. See
**Constellation lines** for field descriptions.

#### Traditional Chinese constellations

`constellations.borders.cn.<data format>` (`LINESTRING`) with 84 objects.

-   **ids**: border id.

`constellations.bounds.cn.<data format>` (`POLYGON`) with 28 objects. See
**Constellation lines** for field descriptions.

### Constellation lines

`constellations.lines.<data format>` (`MULTILINESTRING`) with 89 objects.

-   **id**: 3-letter designator

-   **rank**: 1-3 for differential name display by size/brightness

-   **name**: full IAU name

#### Traditional Chinese constellations

`constellations.lines.cn.<data format>` (`MULTILINESTRING`) with 255
objects[^readme-1]:

[^readme-1]: Some constellations have been removed from the [original dataset](<https://github.com/ofrohn/d3-celestial/blob/master/data/constellations.lines.cn.json>)
    since the `MULTILINESTRING` object consisted only on a single point, that
    does not conform with the GeoJSON standard (`POINT` as `MULTILINESTRING` are
    not valid).

-   **id:** numerical id
-   **rank**: so far only 1; differential name display by size/brightness
-   **name**: Chinese name
-   **en**: English translation

### DSOs

Deep Space Objects

#### DSOnames

`dsonames.csv` with 724 rows:

-   **id**: Short designator

-   **name**: Proper name... and names in several languages.

#### Traditional Chinese DSO names

`dsonames.cn.<data format>` with 6 rows

-   **id**: Hipparcos number
-   **name**: Chinese name
-   **desig**: IAU designation
-   **en**: English translation
-   **pinyin**: Pinyin transcription

#### DSOs

Several files:

-   `dsos.6.<data format>`, `dsos.14.<data format>`, `dsos.20.<data format>`:
    the number indicates limit magnitude.

-   `dsos.bright.<data format>`: hand selected DSOs.

-   `lg.<data format>`: Local group .

-   `messier.<data format>` Messier objects.

All objects are `POINT`:

-   **id**: Short designator

-   **desig**: Designator

-   **type**: Object type: gg *(galaxy cluster)*, g: *(galaxy)*, s: *(spiral
    galaxy)*, s0: *(lenticular gal.)*, sd: *(dwarf spheroidal gal.)*, i:
    *(irregular gal.)*, e: *(elliptical gal.)*, oc: *(open cluster)*, gc:
    *(globular cluster)*, dn: *(dark nebula)*, bn: *(bright nebula)*, sfr:
    *(star forming region)*, rn: *(reflection nebula)*, en: *(emission nebula)*,
    pn: *(planetary nebula)*, snr: *(supernova remnant)*.

-   **morph**: Morphology classification depending on type

-   **mag**: Apparent magnitude, 999 if n.a.

-   **dim**: Angular dimensions in arcminutes

-   **bv**: Blue minus visual magnitude color inder (b-v)

-   **br**: Relative brightness to magnitude 0, computed as $$100^{-1 * mag / 5}$$

-   **name**: Proper name

Additional fields on `lg.<data format>`:

-   **sub**: Sub group membership: `MW|M31|N3109|LG` (Milky Way, Andromeda, NGC
    3109, gen. LG)

-   **pop**: MW populations `OH|YH|BD` (Old halo, young halo, bulge & disk), M31
    populations `M31|GP` (gen. M31, great plane)

-   **str**: Tidal streams `Mag|Sgr|CMa|FLS` (Magellanic Stream, Sagittarius
    Stream, Canis Major/Monoceros Stream, Fornax-Leo-Sculptor Great Circle)

### Stars

#### Starnames

`starnames.csv`: Magnitude independent, all stars with a name/designation other
than HIP/HD

-   **id**: Hipparcos number
-   **name**: , Proper name and names in 17 further languages
-   **desig**: , Standard designation, first from list below
-   **bayer**: , Bayer
-   **flam**: , Flamsteed
-   **var**: , Variable star
-   **gliese**: , Gliese
-   **hd**: , Henry Draper
-   **hip**: Hipparcos number again

#### Traditional Chinese star names

`starnames.cn.<data format>` with 3056 rows

-   **id**: Hipparcos number
-   **name**: Chinese name
-   **desig**: IAU designation
-   **en**: English translation
-   **pinyin**: Pinyin transcription

#### Stars

`stars.6.<data format>`, `stars.8.<data format>`, `stars.14.<data format>`: the
number indicates limit magnitude:

-   **id**: Short designator

-   **mag**: Apparent magnitude, 999 if n.a.

-   **bv**: b-v color index.

-   **br**: Relative brightness to magnitude 0, computed as $$100^{-1 * mag / 5}$$

-   **name**: Proper name

### Milky Way

`mw.<data format>` with 5 rows:

-   **id**: Milky Way outlines in 5 brightness steps (ol1-ol5).
