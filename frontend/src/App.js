import React, { useState } from "react";
import axios from "axios";
import MapView from "./components/MapView";
import Dashboard from "./components/Dashboard";
import "./App.css";

function App() {
  const [location, setLocation] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");

  const [data, setData] = useState(null);
  const [trendData, setTrendData] = useState([]);
  const [compareData, setCompareData] = useState([]);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("map");

  const handleSubmit = async () => {
    try {
      setError("");
      setData(null);
      setTrendData([]);
      setCompareData([]);

      if (!location || !date || !time) {
        setError("Please fill all fields");
        return;
      }

      setLoading(true);

      // 🔥 MAIN PREDICTION
      const predictRes = await axios.post("http://127.0.0.1:5000/predict", {
        location,
        date,
        time,
      });

      setData(predictRes.data);

      // 🔥 ANALYTICS (SINGLE CALL)
      const analyticsRes = await axios.post("http://127.0.0.1:5000/analytics", {
        location,
        date,
        time,
      });

      setTrendData(analyticsRes.data.trend);
      setCompareData(analyticsRes.data.compare);

    } catch (err) {
      if (err.response && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError("Server error. Try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  const getColorClass = (label) => {
    if (label === "Low") return "low";
    if (label === "Medium") return "medium";
    if (label === "High") return "high";
    return "";
  };

  return (
    <div className="app">
      <div className="dashboard">

        {/* LEFT PANEL */}
        <div className="left-panel">
          <h1 className="title">🌆 Human Mobility & Urban Flow Prediction</h1>

          <div className="card">
            <input
              placeholder="📍 Enter location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />

            <input
              type="date"
              onChange={(e) => setDate(e.target.value)}
            />

            <input
              type="time"
              onChange={(e) => setTime(e.target.value)}
            />

            <button onClick={handleSubmit}>
              {loading ? "⏳ Predicting..." : "🚀 Predict"}
            </button>

            {error && <p className="error">{error}</p>}
          </div>

          {/* RESULT */}
          {data && (
            <div className={`result-card ${getColorClass(data.label)}`}>
              <h2>
                {data.label === "High" && "🔴 "}
                {data.label === "Medium" && "🟠 "}
                {data.label === "Low" && "🟢 "}
                {data.crowd_density}% ({data.label})
              </h2>

              <p>{data.reason}</p>
            </div>
          )}
        </div>

        {/* RIGHT PANEL */}
        <div className="right-panel">

          {/* 🔥 TABS */}
          {data && (
            <div className="tabs">
              <button
                className={activeTab === "map" ? "active" : ""}
                onClick={() => setActiveTab("map")}
              >
                🗺️ Map
              </button>

              <button
                className={activeTab === "dashboard" ? "active" : ""}
                onClick={() => setActiveTab("dashboard")}
              >
                📊 Dashboard
              </button>
            </div>
          )}

          {/* 🔥 CONTENT */}
          {data ? (
            activeTab === "map" ? (
              <MapView data={data} />
            ) : (
              <Dashboard
                trendData={trendData}
                compareData={compareData}
              />
            )
          ) : (
            <div className="map-placeholder">
              📍 Map will appear here
            </div>
          )}

        </div>

      </div>
    </div>
  );
}

export default App;