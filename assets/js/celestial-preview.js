(() => {
  "use strict";

  const container = document.getElementById("mapid");
  if (!container) return;

  const select = document.getElementById("geojson_file");
  const status = document.getElementById("preview-status");
  const error = document.getElementById("preview-error");
  const errorText = document.getElementById("preview-error-text");
  const download = document.getElementById("preview-download");

  if (!window.L) {
    document.getElementById("preview-reset").disabled = true;
    status.textContent = "The interactive map could not be initialized. Download the selected GeoJSON instead.";
    select.addEventListener("change", () => {
      download.href = `${container.dataset.url}${select.value}.min.geojson`;
    });
    return;
  }

  const map = L.map(container, {
    minZoom: 0,
    maxZoom: 18,
    preferCanvas: true,
    maxBounds: [[-90, -180], [90, 180]],
  });
  const resetView = () => map.fitBounds([[-85, -180], [85, 180]], { animate: false });
  resetView();
  document.getElementById("preview-reset").addEventListener("click", resetView);

  if (L.tileLayer.providerESP) {
    const background = L.tileLayer.providerESP("IDErioja.Oscuro", { noWrap: true }).addTo(map);
    L.control.layers({}, { "Geographic background": background }).addTo(map);
  }

  let activeLayer;
  let controller;
  let requestNumber = 0;

  async function loadSelected() {
    const request = ++requestNumber;
    if (controller) controller.abort();
    controller = new AbortController();
    const selectedLabel = select.selectedOptions[0].textContent;
    const url = `${container.dataset.url}${select.value}.min.geojson`;
    download.href = url;
    error.hidden = true;
    container.setAttribute("aria-busy", "true");
    status.textContent = `Loading ${selectedLabel}…`;

    try {
      const response = await fetch(url, { signal: controller.signal });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (request !== requestNumber) return;
      if (data.type !== "FeatureCollection" || !Array.isArray(data.features)) {
        throw new Error("Invalid GeoJSON feature collection");
      }
      const layer = L.geoJSON(data, {
        pointToLayer: (_feature, position) => L.circleMarker(position, {
          radius: 3,
          color: "#8ecfff",
          weight: 1,
          fillOpacity: 0.8,
        }),
        style: { color: "#8ecfff", weight: 1.5, fillOpacity: 0.2 },
      });
      layer.addTo(map);
      if (activeLayer) map.removeLayer(activeLayer);
      activeLayer = layer;
      const count = data.features.length;
      status.textContent = `${selectedLabel} loaded: ${count.toLocaleString()} ${count === 1 ? "feature" : "features"}.`;
    } catch (failure) {
      if (request !== requestNumber || failure.name === "AbortError") return;
      status.textContent = "Dataset loading failed.";
      errorText.textContent = `Could not load ${selectedLabel}. ${activeLayer ? "The previous dataset remains visible. " : ""}Retry or download the selected GeoJSON.`;
      error.hidden = false;
    } finally {
      if (request === requestNumber) container.setAttribute("aria-busy", "false");
    }
  }

  select.addEventListener("change", loadSelected);
  document.getElementById("preview-retry").addEventListener("click", loadSelected);
  loadSelected();
})();
