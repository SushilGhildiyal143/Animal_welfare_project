from flask import Flask, request, jsonify
import folium

app = Flask(__name__)

# Store location history
locations = []

# ✅ FRONTEND (phone UI)
@app.route('/')
def home():
    return """
    <h2>📍 Live Location Tracker</h2>
    <button onclick="track()">Start Tracking</button>

    <script>
    function sendLocation(position) {
        fetch('/location', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            })
        })
        .then(res => console.log("Sent"))
        .catch(err => alert("Error: " + err));
    }

    function track() {
        navigator.geolocation.watchPosition(
            sendLocation,
            function(error) {
                alert("GPS Error: " + error.message);
            },
            { enableHighAccuracy: true }
        );
        alert("Tracking started");
    }
    </script>
    """

# ✅ RECEIVE LOCATION
@app.route('/location', methods=['POST'])
def location():
    data = request.json
    lat = data['latitude']
    lon = data['longitude']

    locations.append((lat, lon))
    print(f"Received: {lat}, {lon}")

    return jsonify({"status": "success"})

# ✅ SHOW MAP
@app.route('/map')
def show_map():
    if not locations:
        return "No data yet"

    m = folium.Map(location=locations[-1], zoom_start=15)

    for loc in locations:
        folium.Marker(loc).add_to(m)

    folium.PolyLine(locations).add_to(m)

    m.save("map.html")
    return open("map.html").read()

# ✅ RUN SERVER
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)