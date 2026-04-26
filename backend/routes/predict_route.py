from flask import Blueprint, request, jsonify
from utils.predictor import predict_crowd
from utils.geocode import get_coordinates
import random

predict_bp = Blueprint("predict", __name__)

# =========================
# EXISTING ROUTE
# =========================
@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        location = data["location"]
        date = data["date"]
        time = data["time"]

        lat, lng = get_coordinates(location)

        result = predict_crowd(location, date, time)

        hotspots = []
        for _ in range(40):
            hotspots.append({
                "lat": lat + random.uniform(-0.01, 0.01),
                "lng": lng + random.uniform(-0.01, 0.01),
                "intensity": result["value"]
            })

        return jsonify({
            "lat": lat,
            "lng": lng,
            "crowd_density": result["value"],
            "label": result["label"],
            "reason": result["reason"],
            "hotspots": hotspots
        })

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# =========================
# 🔥 NEW ANALYTICS ROUTE
# =========================
@predict_bp.route("/analytics", methods=["POST"])
def analytics():
    try:
        data = request.json

        location = data["location"]
        date = data["date"]
        time = data["time"]

        # 🔥 TREND
        times = ["06:00","09:00","12:00","15:00","18:00","21:00"]

        trend = []
        for t in times:
            val = predict_crowd(location, date, t)
            trend.append({
                "time": t,
                "crowd": val["value"]
            })

        # 🔥 COMPARISON
        nearby_map = {

    # 🔵 HYDERABAD
    "nagole": ["Uppal", "LB Nagar"],
    "gachibowli": ["Hitech City", "Madhapur"],
    "kukatpally": ["Miyapur", "Ameerpet"],
    "secunderabad": ["Malkajgiri", "Alwal"],
    "ameerpet": ["Punjagutta", "Begumpet"],
    "jubilee hills": ["Banjara Hills", "Film Nagar"],
    "banjara hills": ["Jubilee Hills", "Somajiguda"],
    "lb nagar": ["Dilsukhnagar", "Hayathnagar"],
    "uppal": ["Nagole", "Boduppal"],
    "madhapur": ["Hitech City", "Gachibowli"],

    # 🔵 BANGALORE
    "whitefield": ["Marathahalli", "Brookefield"],
    "electronic city": ["BTM Layout", "Silk Board"],
    "btm layout": ["Jayanagar", "HSR Layout"],
    "indiranagar": ["Domlur", "Ulsoor"],
    "koramangala": ["BTM Layout", "HSR Layout"],
    "yelahanka": ["Hebbal", "Devanahalli"],

    # 🔵 CHENNAI
    "t nagar": ["Nungambakkam", "Kodambakkam"],
    "velachery": ["Adyar", "Guindy"],
    "adyar": ["Besant Nagar", "Velachery"],
    "tambaram": ["Chromepet", "Pallavaram"],
    "anna nagar": ["Mogappair", "Koyambedu"],

    # 🔵 MUMBAI
    "bandra": ["Khar", "Santacruz"],
    "andheri": ["Jogeshwari", "Vile Parle"],
    "powai": ["Vikhroli", "Ghatkopar"],
    "thane": ["Mulund", "Kalwa"],
    "dadar": ["Parel", "Worli"],

    # 🔵 DELHI
    "connaught place": ["Karol Bagh", "India Gate"],
    "dwarka": ["Janakpuri", "Uttam Nagar"],
    "rohini": ["Pitampura", "Shalimar Bagh"],
    "saket": ["Malviya Nagar", "Mehrauli"],
    "lajpat nagar": ["Defence Colony", "Nehru Place"],

    # 🔵 VISAKHAPATNAM
    "vizag": ["Rushikonda", "Bheemunipatnam"],
    "rushikonda": ["MVP Colony", "Madhurawada"],
    "bheemunipatnam": ["Anandapuram", "Tagarapuvalasa"],

    # 🔵 TOURIST LOCATIONS
    "goa": ["Baga", "Calangute"],
    "manali": ["Solang Valley", "Old Manali"],
    "ooty": ["Coonoor", "Kotagiri"],
    "darjeeling": ["Kalimpong", "Kurseong"],
    "shimla": ["Kufri", "Chail"],

    # 🔵 BEACHES
    "suryalanka": ["Bapatla", "Chirala"],
    "kovalam": ["Vizhinjam", "Poovar"],
    "marina beach": ["Besant Nagar", "Triplicane"],
    "juhu beach": ["Versova", "Andheri"],

    # 🔵 GENERIC AREAS
    "village": ["Nearby Town 1", "Nearby Town 2"],
    "rural": ["Nearby Area A", "Nearby Area B"]
}

        base = location.lower().strip()

        if base in nearby_map:
            compare_locations = [location] + nearby_map[base]
        else:
            compare_locations = [
                location,
                location + " area 1",
                location + " area 2"
            ]
        compare = []
        for loc in compare_locations:
            val = predict_crowd(loc, date, time)
            compare.append({
                "location": loc,
                "crowd": val["value"]
            })

        return jsonify({
            "trend": trend,
            "compare": compare
        })

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500