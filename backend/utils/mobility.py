import random

def get_mobility_factor(hour, weekday, context):
    base = 1.0

    if 17 <= hour <= 21:
        base += 0.4
    elif 10 <= hour <= 16:
        base += 0.2
    else:
        base -= 0.2

    if weekday >= 5:
        base += 0.3

    if context["type"] == "tourist" and 9 <= hour <= 17:
        base += 0.5

    base += random.uniform(-0.1, 0.1)

    return max(0.5, min(2.0, base))