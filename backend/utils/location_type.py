def get_location_type(location):
    loc = location.lower()

    # 🔥 party beaches
    if any(x in loc for x in ["baga", "calangute", "goa"]):
        return "party_beach"

    if "beach" in loc:
        return "beach"

    if any(x in loc for x in [
        "gachibowli", "hitec", "madhapur",
        "financial district", "tech", "it", "cyber"
    ]):
        return "office"

    if any(x in loc for x in ["market", "bazaar", "mall"]):
        return "market"

    if any(x in loc for x in ["valley", "hill", "fort", "temple"]):
        return "tourist"

    if any(x in loc for x in ["nagar", "colony", "giri", "enclave"]):
        return "residential"

    if any(x in loc for x in ["village", "mandal"]):
        return "rural"

    return "urban"