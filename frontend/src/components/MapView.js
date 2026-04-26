import React, { useEffect } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet.heat";

function Heatmap({ hotspots }) {
  const map = useMap();

  useEffect(() => {
    if (!hotspots || hotspots.length === 0) return;

    const heatData = hotspots.map(p => [
      p.lat,
      p.lng,
      p.intensity / 100
    ]);

    const heatLayer = L.heatLayer(heatData, {
      radius: 25,
      blur: 20
    });

    heatLayer.addTo(map);

    return () => {
      map.removeLayer(heatLayer);
    };
  }, [hotspots, map]);

  return null;
}

function MapView({ data }) {
  const center = data?.lat ? [data.lat, data.lng] : [20.5937, 78.9629];

  return (
    <MapContainer center={center} zoom={12} style={{ height: "500px", width: "100%" }}>
      <TileLayer
        attribution="&copy; OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Heatmap hotspots={data?.hotspots || []} />
    </MapContainer>
  );
}

export default MapView;