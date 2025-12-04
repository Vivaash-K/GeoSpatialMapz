(function () {
  var token = window.MAPBOX_ACCESS_TOKEN;
  if (!token) {
    console.warn("Mapbox token not set; map will not initialize.");
    return;
  }

  mapboxgl.accessToken = token;
  var map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/streets-v12",
    center: [0, 20],
    zoom: 1.5,
  });

  map.addControl(new mapboxgl.NavigationControl(), "top-right");

  map.on("load", function () {
    // Add a simple marker in maroon theme at a sample location
    var el = document.createElement("div");
    el.style.width = "14px";
    el.style.height = "14px";
    el.style.borderRadius = "50%";
    el.style.background = "#800000"; // maroon
    el.style.border = "2px solid #ffffff";

    new mapboxgl.Marker({ element: el })
      .setLngLat([0, 0])
      .setPopup(new mapboxgl.Popup().setHTML("<b>GeoSpatialMapz</b>"))
      .addTo(map);
  });
})();


