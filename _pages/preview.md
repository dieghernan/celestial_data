---
title: Preview
permalink: /preview
excerpt: Preview data
leaflet: true
---


Preview selected data sets using [Leaflet](https://leafletjs.com/). Some 
data (as `dsos` or `stars`) have a large number of features, so they can take
some time before they are loaded.

## Leaflet preview

<form>
  <div class="form-group">
    <label for="geojson_file">Select a file</label>
    <select id="geojson_file" onChange="update()">
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
        <option value="stars.6">Stars (magnitude 6 or less), wait for it</option>
      </optgroup>
    </select>
  </div>
</form>
<!-- Create map -->
<div class="embed-responsive embed-responsive-16by9">
  <div class="embed-responsive-item" id="mapid"></div>
</div>

<script>
var mymap = L.map('mapid', {
    maxZoom: 18,
    minZoom: 1,
    maxBounds: [
      //south west
      [-90, -180],
      //north east
      [90, 180]
    ],
  })
  .setView([0, 0], 1);
L.tileLayer.provider('CartoDB.DarkMatterNoLabels')
  .addTo(mymap);
var geojsonLayer = new L.GeoJSON.AJAX(
  "https://cdn.jsdelivr.net/gh/dieghernan/celestial_data@main/data/mw.min.geojson"
  );
geojsonLayer.addTo(mymap);

function update() {
  mymap.eachLayer(function(layer) {
    if (layer instanceof L.GeoJSON) mymap.removeLayer(layer);
  });
  var select = document.getElementById('geojson_file');
  var option = select.options[select.selectedIndex];
  var newgeo = option.value;
  var geourl =
    'https://cdn.jsdelivr.net/gh/dieghernan/celestial_data@main/data/' +
    newgeo + '.min.geojson';
  var geojsonLayer2 = new L.GeoJSON.AJAX(geourl);
  geojsonLayer2.addTo(mymap);
}

</script>