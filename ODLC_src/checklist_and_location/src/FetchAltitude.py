import requests


def fetch_altitude_and_gps():
    try:
        response = requests.get("http://telemetry_module:5000/gps")
        if response.status_code == 200:
            data = response.json()
            altitude = data.get("altitude")
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            print(f"Altitude: {altitude} meters, Latitude: {latitude}, Longitude: {longitude}")
            return altitude, latitude, longitude
        else:
            print(f"Failed to get GPS data: {response.status_code}")
            return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
        return None, None, None
