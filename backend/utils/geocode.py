from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="urban-flow")

def get_coordinates(place):
    try:
        # Try with India
        location = geolocator.geocode(place + ", India")

        # Fallback with Hyderabad (you can change city if needed)
        if not location:
            location = geolocator.geocode(place + ", Hyderabad, India")

        if location:
            return location.latitude, location.longitude

        return None, None

    except:
        return None, None