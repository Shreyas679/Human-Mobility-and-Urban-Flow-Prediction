def get_location_context(location):
    loc = location.lower()

    if any(x in loc for x in ["hyderabad", "delhi", "mumbai", "bangalore", "chennai"]):
        return {"type": "urban", "weight": 1.5}

    elif any(x in loc for x in ["goa", "manali", "shimla", "ooty", "laitlum"]):
        return {"type": "tourist", "weight": 1.0}

    elif any(x in loc for x in ["beach", "hill", "valley", "falls"]):
        return {"type": "tourist", "weight": 0.9}

    else:
        return {"type": "rural", "weight": 0.7}