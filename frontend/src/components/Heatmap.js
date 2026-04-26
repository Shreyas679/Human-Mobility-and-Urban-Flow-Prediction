import React from "react";

const Heatmap = ({ data }) => {

  const getColor = (value) => {
    if (value < 40) return "#0ca131";     // green
    if (value < 70) return "#f59e0b";     // orange
    return "#ef4444";                     // red
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>🔥 Crowd Heatmap</h3>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(6, 1fr)",
        gap: "10px"
      }}>
        {data.map((item, index) => (
          <div
            key={index}
            style={{
              padding: "15px",
              textAlign: "center",
              borderRadius: "10px",
              background: getColor(item.crowd),
              color: "white"
            }}
          >
            <div>{item.time}</div>
            <strong>{item.crowd}%</strong>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Heatmap;