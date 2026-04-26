import React from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  CartesianGrid, BarChart, Bar, ResponsiveContainer
} from "recharts";
import Heatmap from "./Heatmap";

const Dashboard = ({ trendData, compareData }) => {

  // 🔥 INSIGHTS LOGIC
  const generateInsights = () => {
    if (!trendData || trendData.length === 0) return null;

    const max = trendData.reduce((a, b) =>
      a.crowd > b.crowd ? a : b
    );

    const min = trendData.reduce((a, b) =>
      a.crowd < b.crowd ? a : b
    );

    return {
      peak: `${max.time} (${max.crowd}%)`,
      low: `${min.time} (${min.crowd}%)`
    };
  };

  const insights = generateInsights();

  return (
    <div style={{ padding: "20px", color: "white" }}>

      <h2>📊 Analytics Dashboard</h2>

      {/* 📈 TREND GRAPH */}
      <div style={{ marginTop: "20px" }}>
        <h3>📈 Crowd Trend (Hourly)</h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={trendData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="crowd"
              stroke="#3b1282"
              strokeWidth={3}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* 📊 COMPARISON GRAPH */}
      <div style={{ marginTop: "40px" }}>
        <h3>📊 Location Comparison</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={compareData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="location" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="crowd" fill="#4603b2" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* 🔥 HEATMAP */}
      <Heatmap data={trendData} />

      {/* 💡 INSIGHTS */}
      {insights && (
        <div style={{ marginTop: "25px" }}>
          <h3>💡 Smart Insights</h3>

          <p>
            📈 Peak crowd time: <b>{insights.peak}</b>
          </p>

          <p>
            📉 Least crowded time: <b>{insights.low}</b>
          </p>
        </div>
      )}

      {/* 🎯 SUGGESTIONS */}
      <div style={{ marginTop: "20px" }}>
        <h3>🎯 Suggestions</h3>

        <ul>
          <li>Visit during low crowd time for a better experience</li>
          <li>Avoid peak hours to reduce congestion</li>
          <li>Weekends and holidays may significantly increase crowd levels</li>
          <li>Plan travel during early morning or late evening when possible</li>
        </ul>
      </div>

    </div>
  );
};

export default Dashboard;