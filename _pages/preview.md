---
title: Preview
permalink: /preview
excerpt: Preview data
leaflet: true
---

Preview selected datasets using [Leaflet](https://leafletjs.com/). Large star and
deep-sky catalogs may take longer to load. You can download the selected GeoJSON
file even if the interactive preview is unavailable.

These are J2000 celestial coordinates represented as geographic geometries.
The geographic background is a visual reference, not a map of the night sky
as seen from your location; the Mercator view does not show the poles.

## Leaflet preview

<div class="celestial-preview-controls">
  <div class="form-group">
    <label for="geojson_file">Select a file</label>
    <select id="geojson_file" class="custom-select" aria-describedby="preview-help">
      <optgroup label="Polygons">
        <option value="mw" selected>Milky Way</option>
        <option value="constellations.bounds">Constellations (Bounds)</option>
        <option value="constellations.bounds.cn">Chinese Constellations (Bounds)</option>
      </optgroup>
      <optgroup label="Lines">
        <option value="asterisms">Asterisms</option>
        <option value="constellations.borders">Constellations (Borders)</option>
        <option value="constellations.lines">Constellations (Lines)</option>
        <option value="constellations.borders.cn">Chinese Constellations (Borders)</option>
        <option value="constellations.lines.cn">Chinese Constellations (Lines)</option>
      </optgroup>
      <optgroup label="Points">
        <option value="constellations">Constellations</option>
        <option value="constellations.cn">Chinese Constellations</option>
        <option value="dsos.bright">DSOs Bright</option>
        <option value="lg">Local Group</option>
        <option value="messier">Messier Objects</option>
        <option value="stars.6">Stars (magnitude 6 or less)</option>
      </optgroup>
    </select>
  </div>
  <div class="d-flex flex-wrap mb-3">
    <button id="preview-reset" class="btn btn-secondary mr-2 mb-2" type="button">Reset view</button>
    <a id="preview-download" class="btn btn-outline-primary mb-2"
       href="{{ '/data/mw.min.geojson' | relative_url }}">Download selected GeoJSON</a>
  </div>
</div>
<p id="preview-help" class="small">Choose a dataset to load it. Use the map's zoom
buttons or focus the map to pan with the arrow keys and zoom with + and −.
The previous dataset remains visible until its replacement has loaded.</p>
<p id="preview-status" role="status" aria-live="polite" aria-atomic="true">The interactive preview requires JavaScript.</p>
<div id="preview-error" role="alert" hidden>
  <p id="preview-error-text"></p>
  <button id="preview-retry" class="btn btn-secondary mb-3" type="button">Retry loading</button>
</div>
<div id="mapid" class="celestial-preview-map" role="region"
     aria-label="Interactive preview of celestial geometry" aria-describedby="preview-help"
     data-url="{{ '/data/' | relative_url }}"></div>
