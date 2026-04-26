import React, { useState } from "react";
import { predictCrowd } from "../services/api";

function SearchBar({ setResult }) {
  const [location, setLocation] = useState("");
  const [hour, setHour] = useState(12);
  const [day, setDay] = useState(0);

  const handleSubmit = async () => {
    const res = await predictCrowd({ location, hour, day });
    setResult(res.data);
  };

  return (
    <div>
      <input placeholder="Location" onChange={(e) => setLocation(e.target.value)} />
      <input type="number" placeholder="Hour" onChange={(e) => setHour(e.target.value)} />
      <input type="number" placeholder="Day" onChange={(e) => setDay(e.target.value)} />
      <button onClick={handleSubmit}>Predict</button>
    </div>
  );
}

export default SearchBar;