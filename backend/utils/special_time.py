def get_special_time_boost(hour, context, location):
    loc = location.lower()

    # 🔥 nightlife override
    if ("beach" in loc or "goa" in loc) and (20 <= hour <= 23):
        return 70

    # sunset boost
    if context["type"] == "tourist" and 16 <= hour <= 18:
        return 40

    return 0