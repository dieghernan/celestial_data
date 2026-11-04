---
title: Downloads
permalink: /downloads/
excerpt: Browse celestial datasets by category and download GeoJSON, GeoPackage and CSV files.
---

Browse datasets by category. Select a dataset name for its metadata or use the
buttons to download files directly. GeoJSON and GeoPackage contain J2000
celestial geometries. CSV files contain names and attributes without geometry.

For formats, coordinate conventions and field definitions, see the
[data description]({{ '/data' | relative_url }}).

<nav aria-label="Dataset categories" class="mb-4">
  <ul>
    {% assign groups = site.data.datasets | group_by: 'group' %}
    {% for group in groups %}
    <li><a href="#{{ group.name | slugify }}">{{ group.name | escape }}</a></li>
    {% endfor %}
  </ul>
</nav>

{% include custom/download_catalog.html %}
