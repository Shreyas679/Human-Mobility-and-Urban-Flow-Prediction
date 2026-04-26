from flask import Blueprint, jsonify
from utils.predictor import predict_crowd

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/trend", methods=["GET"])
def trend():
    hours = ["06:00","09:00","12:00","15:00","18:00","21:00"]

    result = []

    for h in hours:
        val = predict_crowd("Gachibowli", "2026-04-15", h)
        result.append({
            "time": h,
            "crowd": val["value"]
        })

    return jsonify(result)