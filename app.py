import os
from flask import Flask, render_template_string
import folium


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        mapbox_token = os.getenv("MAPBOX_ACCESS_TOKEN", "")

        # Create a Folium map centered globally with explicit size
        base_map = folium.Map(location=[20, 0], zoom_start=2, width="100%", height="70vh", tiles=None)

        # If a Mapbox token is provided, use Mapbox tiles; otherwise fallback to OpenStreetMap
        if mapbox_token:
            mapbox_tiles = (
                "https://api.mapbox.com/styles/v1/mapbox/streets-v12/tiles/"
                "{z}/{x}/{y}?access_token=" + mapbox_token
            )
            folium.TileLayer(
                tiles=mapbox_tiles,
                attr="Mapbox",
                name="Mapbox Streets",
                control=False,
            ).add_to(base_map)
        else:
            folium.TileLayer(
                tiles="OpenStreetMap",
                name="OpenStreetMap",
                control=False,
            ).add_to(base_map)

        # Add a sample marker with maroon styling
        folium.Marker(
            location=[12.9249, 80.1000],
            popup="GeoSpatialMapz",
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(base_map)

        map_html = base_map.get_root().render()
        map_name = base_map.get_name()

        # Cities with coordinates
        cities = [
            {"name": "Dharamshala", "lat": 32.2190, "lng": 76.3234},
            {"name": "Keylong", "lat": 32.5710, "lng": 77.0320},
            {"name": "Tambaram", "lat": 12.9249, "lng": 80.1000},
            {"name": "Shimla", "lat": 31.1050, "lng": 77.1640},
            {"name": "Mumbai", "lat": 18.9582, "lng": 72.8321},
            {"name": "Jaipur", "lat": 26.9124, "lng": 75.7873},
            {"name": "Chandigarh", "lat": 30.7333, "lng": 76.7794},
            {"name": "Delhi", "lat": 28.7041, "lng": 77.1025},
            {"name": "Gurugram", "lat": 28.4595, "lng": 77.0266},
            {"name": "Faridabad", "lat": 28.4089, "lng": 77.3178},
            {"name": "Dehradun", "lat": 30.3165, "lng": 78.0322},
            {"name": "Nagpur", "lat": 21.1458, "lng": 79.0882},
            {"name": "Pune", "lat": 18.5246, "lng": 73.8786},
            {"name": "Bangalore", "lat": 12.9629, "lng": 77.5775},
            {"name": "Chennai", "lat": 13.0843, "lng": 80.2705},
            {"name": "Vishakhapatnam", "lat": 17.6868, "lng": 83.2185},
            {"name": "Kolkata", "lat": 22.5744, "lng": 88.3629},
            {"name": "Patna", "lat": 25.5941, "lng": 85.1376},
            {"name": "Puri", "lat": 19.8135, "lng": 85.8312},
            {"name": "Ahmedabad", "lat": 23.0225, "lng": 72.5714},
            {"name": "Goa", "lat": 15.2993, "lng": 74.1240},
        ]

        # Entire UI rendered from Python with red/white theme
        html = render_template_string(
            """
            <!doctype html>
            <html lang=\"en\">
              <head>
                <meta charset=\"utf-8\" />
                <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
                <title>GeoSpatialMapz</title>
                <style>
                  :root { --red: #e53935; --maroon: #800000; --orange: #fb8c00; --white: #ffffff; --bg: #fff7f7; --text: #2a2a2a; }
                  * { box-sizing: border-box; }
                  body { margin: 0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica, Arial, 'Apple Color Emoji', 'Segoe UI Emoji'; color: var(--text); background: var(--bg); }
                  .container { width: min(1100px, 92%); margin: 0 auto; }
                  .site-header { background: linear-gradient(90deg, var(--maroon), var(--red), var(--orange)); color: var(--white); padding: 28px 0; border-bottom: 4px solid #b71c1c; }
                  .title { margin: 0; font-size: 40px; letter-spacing: 0.5px; }
                  .subtitle { margin: 6px 0 0; opacity: 0.9; }
                  .map-wrap { margin: 18px 0; border-radius: 12px; border: 2px solid var(--maroon); overflow: hidden; box-shadow: 0 8px 24px rgba(128,0,0,0.18); }
                  .notice { margin-top: 14px; background: #fff0f0; border-left: 4px solid var(--red); padding: 10px 12px; }
                  /* Ensure Folium map takes height */
                  #map { height: 70vh; }
                  .buttons { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 10px; margin: 10px 0 22px; }
                  .btn { appearance: none; border: 0; background: var(--maroon); color: var(--white); padding: 10px 12px; border-radius: 8px; cursor: pointer; transition: transform 0.04s ease, background 0.2s ease; }
                  .btn:hover { background: var(--red); }
                  .btn:active { transform: translateY(1px); }
                  .controls { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; margin: 8px 0 20px; }
                  .input, .select { width: 100%; padding: 10px 12px; border: 2px solid var(--maroon); border-radius: 8px; background: #fff; color: var(--text); }
                  .action-row { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin: 8px 0 14px; }
                  .directions { border: 2px solid var(--maroon); border-radius: 8px; padding: 10px 12px; background: #fff; }
                  .directions h3 { margin: 0 0 8px 0; color: var(--maroon); }
                  .meta { margin: 6px 0 10px 0; color: #555; }
                  .directions ol { margin: 0; padding-left: 18px; }
                </style>
              </head>
              <body>
                <header class=\"site-header\">
                  <div class=\"container\">
                    <h1 class=\"title\">GeoSpatialMapz</h1>
                    <p class=\"subtitle\">Interactive geospatial visualization</p>
                  </div>
                </header>
                <main class=\"container\">
                  <div class=\"map-wrap\">{{ map_html|safe }}</div>
                  <div class=\"buttons\">
                    {% for c in cities %}
                      <button class=\"btn\" data-lat=\"{{ '%.6f' % c.lat }}\" data-lng=\"{{ '%.6f' % c.lng }}\">{{ c.name }}</button>
                    {% endfor %}
                  </div>
                  <!-- Route controls: dropdowns and coordinate inputs -->
                  <div class=\"controls\">
                    <select id=\"originSelect\" class=\"select\">
                      <option value=\"\">Select origin city</option>
                      {% for c in cities %}
                        <option value=\"{{ '%.6f' % c.lat }},{{ '%.6f' % c.lng }}\">{{ c.name }}</option>
                      {% endfor %}
                    </select>
                    <select id=\"destSelect\" class=\"select\">
                      <option value=\"\">Select destination city</option>
                      {% for c in cities %}
                        <option value=\"{{ '%.6f' % c.lat }},{{ '%.6f' % c.lng }}\">{{ c.name }}</option>
                      {% endfor %}
                    </select>
                  </div>
                  <div class=\"controls\">
                    <input id=\"originLat\" class=\"input\" type=\"text\" placeholder=\"Origin latitude\" />
                    <input id=\"originLng\" class=\"input\" type=\"text\" placeholder=\"Origin longitude\" />
                    <input id=\"destLat\" class=\"input\" type=\"text\" placeholder=\"Destination latitude\" />
                    <input id=\"destLng\" class=\"input\" type=\"text\" placeholder=\"Destination longitude\" />
                  </div>
                  <div class=\"action-row\">
                    <button id=\"btnShowRoute\" class=\"btn\">Show route</button>
                    <button id=\"btnClearRoute\" class=\"btn\">Clear route</button>
                  </div>
                  <div id=\"directions\" class=\"directions\" style=\"display:none\">
                    <h3>Directions</h3>
                    <div class=\"meta\" id=\"dirMeta\"></div>
                    <ol id=\"dirList\"></ol>
                  </div>
                  {% if not mapbox_token %}
                  <div class=\"notice\"><strong>Tip:</strong> Set <code>MAPBOX_ACCESS_TOKEN</code> to use Mapbox tiles.</div>
                  {% endif %}
                  <script>
                    (function() {
                      var map = window[\"{{ map_name }}\"]; // Folium Leaflet map instance
                      var activeMarker = null;
                      var routeLine = null;
                      var routeMarkers = [];

                      function showCity(lat, lng, name) {
                        if (!map) return;
                        if (activeMarker) {
                          activeMarker.setLatLng([lat, lng]).bindPopup(name).openPopup();
                        } else {
                          activeMarker = L.marker([lat, lng]).addTo(map).bindPopup(name).openPopup();
                        }
                        map.flyTo([lat, lng], 10);
                      }

                      var buttons = document.querySelectorAll('.btn[data-lat][data-lng]');
                      buttons.forEach(function(btn){
                        btn.addEventListener('click', function(){
                          var lat = parseFloat(btn.getAttribute('data-lat'));
                          var lng = parseFloat(btn.getAttribute('data-lng'));
                          var name = btn.textContent.trim();
                          showCity(lat, lng, name);
                        });
                      });

                      function clearRoute() {
                        if (routeLine) { map.removeLayer(routeLine); routeLine = null; }
                        routeMarkers.forEach(function(m){ map.removeLayer(m); });
                        routeMarkers = [];
                        var dir = document.getElementById('directions');
                        var list = document.getElementById('dirList');
                        var meta = document.getElementById('dirMeta');
                        list.innerHTML = '';
                        meta.textContent = '';
                        dir.style.display = 'none';
                      }

                      function drawLine(coords) {
                        clearRoute();
                        routeLine = L.polyline(coords, { color: '#800000', weight: 4 }).addTo(map);
                        routeMarkers.push(L.marker(coords[0]).addTo(map).bindPopup('Origin').openPopup());
                        routeMarkers.push(L.marker(coords[coords.length - 1]).addTo(map).bindPopup('Destination'));
                        map.fitBounds(routeLine.getBounds(), { padding: [30, 30] });
                      }

                      function showStraightLine(aLat, aLng, bLat, bLng) {
                        drawLine([[aLat, aLng], [bLat, bLng]]);
                      }

                      function fmtKm(m) { return (m/1000).toFixed(1) + ' km'; }
                      function fmtMin(s) { return Math.round(s/60) + ' min'; }

                      function renderDirections(route, provider) {
                        var dir = document.getElementById('directions');
                        var list = document.getElementById('dirList');
                        var meta = document.getElementById('dirMeta');
                        dir.style.display = '';
                        meta.textContent = 'Distance: ' + fmtKm(route.distance) + ' · Duration: ' + fmtMin(route.duration) + (provider ? ' · ' + provider : '');
                        list.innerHTML = '';
                        var steps = [];
                        try {
                          if (route.legs && route.legs[0] && route.legs[0].steps) {
                            steps = route.legs[0].steps;
                          }
                        } catch(e) {}
                        if (steps.length === 0) return;
                        steps.forEach(function(step){
                          var text = '';
                          if (step.maneuver && step.maneuver.instruction) {
                            text = step.maneuver.instruction; // Mapbox
                          } else {
                            var road = step.name || '';
                            var type = step.maneuver && step.maneuver.type ? step.maneuver.type : '';
                            var mod = step.maneuver && step.maneuver.modifier ? step.maneuver.modifier : '';
                            text = [type, mod, road].filter(Boolean).join(' ');
                          }
                          var li = document.createElement('li');
                          li.textContent = text;
                          list.appendChild(li);
                        });
                      }

                      function requestRoadRoute(aLat, aLng, bLat, bLng) {
                        var hasMapbox = {{ 'true' if mapbox_token else 'false' }};
                        var mapboxToken = {{ mapbox_token|tojson if mapbox_token else 'null' }};
                        var url;
                        if (hasMapbox && mapboxToken) {
                          url = 'https://api.mapbox.com/directions/v5/mapbox/driving/' +
                                [aLng, aLat].join(',') + ';' + [bLng, bLat].join(',') +
                                '?geometries=geojson&overview=full&steps=true&access_token=' + mapboxToken;
                        } else {
                          url = 'https://router.project-osrm.org/route/v1/driving/' +
                                [aLng, aLat].join(',') + ';' + [bLng, bLat].join(',') +
                                '?geometries=geojson&overview=full&steps=true';
                        }
                        return fetch(url).then(function(r){
                          if (!r.ok) {
                            return r.text().then(function(text){
                              throw new Error('HTTP ' + r.status + ': ' + text);
                            });
                          }
                          return r.json();
                        }).then(function(data){
                          if (!data) throw new Error('No data received');
                          if (data.code && data.code !== 'Ok') throw new Error('Routing error: ' + data.code);
                          if (!data.routes || !data.routes[0]) throw new Error('No route found');
                          var route = data.routes[0];
                          if (!route.geometry) throw new Error('No geometry in route');
                          var coords;
                          if (route.geometry.type === 'LineString' && Array.isArray(route.geometry.coordinates)) {
                            coords = route.geometry.coordinates.map(function(c){ return [c[1], c[0]]; });
                          } else if (Array.isArray(route.geometry)) {
                            coords = route.geometry.map(function(c){ return [c[1], c[0]]; });
                          } else {
                            throw new Error('Invalid geometry format');
                          }
                          if (coords.length < 2) throw new Error('Route has insufficient coordinates');
                          drawLine(coords);
                          renderDirections(route, hasMapbox && mapboxToken ? 'Mapbox Directions' : 'OSRM');
                        }).catch(function(err){
                          console.error('Routing failed:', err);
                          alert('Could not calculate road route: ' + err.message + '. Showing straight line instead.');
                          showStraightLine(aLat, aLng, bLat, bLng);
                        });
                      }

                      function parseLatLng(value) {
                        if (!value) return null;
                        var parts = value.split(',');
                        if (parts.length !== 2) return null;
                        var lat = parseFloat(parts[0]);
                        var lng = parseFloat(parts[1]);
                        if (!isFinite(lat) || !isFinite(lng)) return null;
                        return { lat: lat, lng: lng };
                      }

                      document.getElementById('btnShowRoute').addEventListener('click', function(){
                        var selA = parseLatLng(document.getElementById('originSelect').value);
                        var selB = parseLatLng(document.getElementById('destSelect').value);
                        var aLat = parseFloat(document.getElementById('originLat').value);
                        var aLng = parseFloat(document.getElementById('originLng').value);
                        var bLat = parseFloat(document.getElementById('destLat').value);
                        var bLng = parseFloat(document.getElementById('destLng').value);

                        var useSelects = selA && selB;
                        if (useSelects) {
                          requestRoadRoute(selA.lat, selA.lng, selB.lat, selB.lng);
                        } else if ([aLat, aLng, bLat, bLng].every(function(v){ return isFinite(v); })) {
                          requestRoadRoute(aLat, aLng, bLat, bLng);
                        } else {
                          alert('Pick two cities OR enter all four coordinates.');
                        }
                      });

                      document.getElementById('btnClearRoute').addEventListener('click', clearRoute);
                    })();
                  </script>
                </main>
              </body>
            </html>
            """,
            map_html=map_html,
            mapbox_token=mapbox_token,
            cities=cities,
            map_name=map_name,
        )

        return html

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)


