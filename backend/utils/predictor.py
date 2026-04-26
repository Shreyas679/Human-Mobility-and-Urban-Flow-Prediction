import joblib
import numpy as np

# =========================
# LOAD MODEL + ENCODERS
# =========================
model = joblib.load("model/model.pkl")

location_encoder = joblib.load("model/location_encoder.pkl")
location_type_encoder = joblib.load("model/location_type_encoder.pkl")
context_type_encoder = joblib.load("model/context_type_encoder.pkl")


# =========================
# HELPER FUNCTIONS
# =========================

def get_location_type(location):
    loc = location.lower()

    if any(x in loc for x in ["mall", "city", "market", "center", "nagar"]):
        return "urban"
    elif any(x in loc for x in ["beach", "hill", "tourist", "temple"]):
        return "tourist"
    elif any(x in loc for x in ["village", "mandal", "rural"]):
        return "rural"
    else:
        return "urban"


def get_context_type(location):
    loc = location.lower()

    if any(x in loc for x in ["mall", "market"]):
        return "commercial"
    elif any(x in loc for x in ["nagar", "colony"]):
        return "residential"
    elif any(x in loc for x in ["office", "tech", "hitech"]):
        return "business"
    else:
        return "general"


# =========================
# MAIN PREDICT FUNCTION
# =========================

def predict_crowd(location, date, time):

    try:
        # 🔥 TIME FEATURES
        hour = int(time.split(":")[0])
        weekday = 3   # default (can be improved)
        month = 4     # default

        # 🔥 FLAGS
        is_weekend = 1 if weekday >= 5 else 0
        is_holiday = 0

        is_sunset_time = 1 if 17 <= hour <= 19 else 0
        is_nightlife_time = 1 if hour >= 20 else 0
        is_office_rush = 1 if (8 <= hour <= 10 or 17 <= hour <= 19) else 0

        season_factor = 1.0

        # 🔥 LOCATION TYPE
        location_type = get_location_type(location)
        context_type = get_context_type(location)

        # =========================
        # ENCODING (SAFE)
        # =========================
        try:
            location_enc = location_encoder.transform([location])[0]
        except:
            location_enc = 0  # fallback

        try:
            location_type_enc = location_type_encoder.transform([location_type])[0]
        except:
            location_type_enc = 0

        try:
            context_type_enc = context_type_encoder.transform([context_type])[0]
        except:
            context_type_enc = 0

        # =========================
        # CREATE FEATURE VECTOR
        # =========================
        features = np.array([[
            location_enc,
            location_type_enc,
            context_type_enc,
            hour,
            weekday,
            month,
            is_weekend,
            is_holiday,
            is_sunset_time,
            is_nightlife_time,
            is_office_rush,
            season_factor
        ]])

        # =========================
        # MODEL PREDICTION
        # =========================
        prediction = model.predict(features)[0]

        # =========================
        # RULE-BASED ADJUSTMENTS
        # =========================
        if location_type == "rural":
            prediction *= 0.6

        if location_type == "tourist":
            prediction *= 1.1

        if is_nightlife_time and location_type == "urban":
            prediction *= 1.15

        # clamp between 0–100
        prediction = max(5, min(100, prediction))

        # =========================
        # LABEL
        # =========================
        if prediction < 40:
            label = "Low"
        elif prediction < 70:
            label = "Medium"
        else:
            label = "High"

        # =========================
        # REASON
        # =========================
        reason = f"Predicted based on {location_type} area and time patterns"

        return {
            "value": int(prediction),
            "label": label,
            "reason": reason
        }

    except Exception as e:
        return {
            "value": 50,
            "label": "Medium",
            "reason": "Fallback prediction due to error"
        }