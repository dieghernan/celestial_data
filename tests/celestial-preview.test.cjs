const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const source = fs.readFileSync(path.join(__dirname, "../assets/js/celestial-preview.js"), "utf8");
const collection = (id) => ({ type: "FeatureCollection", features: [{ id }] });
const tick = () => new Promise((resolve) => setImmediate(resolve));

function setup({ leaflet = true } = {}) {
  const nodes = {};
  for (const id of ["mapid", "geojson_file", "preview-status", "preview-error", "preview-error-text", "preview-download", "preview-reset", "preview-retry"]) {
    nodes[id] = {
      handlers: {},
      dataset: { url: "/celestial_data/data/" },
      setAttribute(name, value) { this[name] = value; },
      addEventListener(name, handler) { this.handlers[name] = handler; },
    };
  }
  const selected = nodes.geojson_file;
  selected.value = "mw";
  selected.selectedOptions = [{ textContent: "Milky Way" }];
  const pending = [];
  const layers = [];
  const map = {
    fitBounds() {},
    removeLayer(layer) { layers.splice(layers.indexOf(layer), 1); },
  };
  const L = {
    map: () => map,
    tileLayer: {},
    geoJSON: (data) => ({ data, addTo() { layers.push(this); } }),
  };
  const fetch = (url, options) => new Promise((resolve, reject) => pending.push({ url, options, resolve, reject }));
  vm.runInNewContext(source, {
    window: leaflet ? { L } : {}, L,
    document: { getElementById: (id) => nodes[id] },
    fetch, AbortController,
  });
  return {
    nodes, pending, layers,
    select(value) {
      selected.value = value;
      selected.selectedOptions = [{ textContent: value }];
      return selected.handlers.change();
    },
    async respond(index, data = collection(index)) {
      pending[index].resolve({ ok: true, json: async () => data });
      await tick();
    },
  };
}

test("loads the initial dataset under the project baseurl", async () => {
  const ui = setup();
  assert.equal(ui.pending[0].url, "/celestial_data/data/mw.min.geojson");
  await ui.respond(0);
  assert.equal(ui.layers.length, 1);
  assert.match(ui.nodes["preview-status"].textContent, /loaded: 1 feature\./);
  assert.equal(ui.nodes.mapid["aria-busy"], "false");
});

test("a late response cannot replace the most recently selected dataset", async () => {
  const ui = setup();
  ui.select("asterisms");
  assert.equal(ui.pending[0].options.signal.aborted, true);
  await ui.respond(1, collection("asterisms"));
  await ui.respond(0, collection("old"));
  assert.equal(ui.layers.length, 1);
  assert.equal(ui.layers[0].data.features[0].id, "asterisms");
  assert.match(ui.nodes["preview-status"].textContent, /^asterisms loaded/);
});

test("a failed replacement keeps the previous data and retry can recover", async () => {
  const ui = setup();
  await ui.respond(0);
  ui.select("stars.6");
  ui.pending[1].resolve({ ok: false, status: 503 });
  await tick();
  assert.equal(ui.layers.length, 1);
  assert.equal(ui.nodes["preview-error"].hidden, false);
  assert.match(ui.nodes["preview-error-text"].textContent, /previous dataset remains visible/);
  ui.nodes["preview-retry"].handlers.click();
  await ui.respond(2, collection("stars"));
  assert.equal(ui.layers.length, 1);
  assert.equal(ui.layers[0].data.features[0].id, "stars");
  assert.equal(ui.nodes["preview-error"].hidden, true);
});

test("malformed GeoJSON is reported rather than clearing the current map", async () => {
  const ui = setup();
  await ui.respond(0);
  ui.select("broken");
  await ui.respond(1, { message: "not a feature collection" });
  assert.equal(ui.layers.length, 1);
  assert.equal(ui.nodes["preview-error"].hidden, false);
});

test("downloads remain available if Leaflet fails to load", () => {
  const ui = setup({ leaflet: false });
  ui.select("messier");
  assert.equal(ui.pending.length, 0);
  assert.equal(ui.nodes["preview-download"].href, "/celestial_data/data/messier.min.geojson");
  assert.equal(ui.nodes["preview-reset"].disabled, true);
});


test("a stale failure cannot overwrite a successful newer selection", async () => {
  const ui = setup();
  ui.select("messier");
  await ui.respond(1, collection("messier"));
  ui.pending[0].reject(new Error("late network failure"));
  await tick();
  assert.equal(ui.nodes["preview-error"].hidden, true);
  assert.match(ui.nodes["preview-status"].textContent, /^messier loaded/);
  assert.equal(ui.nodes.mapid["aria-busy"], "false");
});
