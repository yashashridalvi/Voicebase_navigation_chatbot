# maps_direction.py
import requests
from geopy.geocoders import Nominatim

# Initialize geocoder
geolocator = Nominatim(user_agent="voice_navigation_chatbot")

# 1. CLEAN & FIND COORDINATES

def get_coordinates(place):
    """
    Cleans place name and returns (lat, lon).
    Auto-adds 'India' if user does not mention a country.
    Handles lowercase and missing commas.
    """

    try:
        if not place:
            return None

        place = place.strip()

        # Clean formatting: Title Case
        place = place.title()

        # If no country is mentioned, assume India
        if "," not in place and "India" not in place:
            place = place + ", India"

        # Perform geocoding
        location = geolocator.geocode(place, timeout=10)

        if location:
            return (location.latitude, location.longitude)

        return None

    except Exception as e:
        print("Geocoding error:", e)
        return None


# -----------------------------------------------------------
# 2. FIND ROUTE USING OSRM (FREE)
# -----------------------------------------------------------
def get_route(start_coords, end_coords):
    try:
        start = f"{start_coords[1]},{start_coords[0]}"
        end = f"{end_coords[1]},{end_coords[0]}"

        url = f"http://router.project-osrm.org/route/v1/driving/{start};{end}?overview=false&steps=true"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print("Routing API Error:", response.status_code)
            return None, None, []

        data = response.json()

        if "routes" not in data or not data["routes"]:
            return None, None, []

        route = data["routes"][0]

        distance_km = route["distance"] / 1000
        duration_min = route["duration"] / 60

        steps = []

        for leg in route.get("legs", []):
            for step in leg.get("steps", []):
                maneuver = step.get("maneuver", {})
                turn_type = maneuver.get("type", "")
                modifier = maneuver.get("modifier", "")
                road = step.get("name", "")

                if turn_type == "depart":
                    text = "Start your journey"
                elif turn_type == "arrive":
                    text = "You have arrived at your destination"
                else:
                    if modifier and road:
                        text = f"Turn {modifier} onto {road}"
                    elif modifier:
                        text = f"Turn {modifier}"
                    elif road:
                        text = f"Continue on {road}"
                    else:
                        text = "Continue straight"

                steps.append(text)

        return distance_km, duration_min, steps

    except Exception as e:
        print("Error contacting routing API:", e)
        return None, None, []

