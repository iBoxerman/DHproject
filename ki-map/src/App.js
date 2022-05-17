import React, { useState, useEffect } from "react";
import {
  withGoogleMap,
  withScriptjs,
  GoogleMap,
  Marker,
  InfoWindow
} from "react-google-maps";
// import * as placesData from "./resources/data/places.json";
// import mapStyles from "./mapStyles";

const placesData = require('./resources/data/places.json')
function Map() {
  const [selectedPlace, setSelectedPlace] = useState(null);

  useEffect(() => {
    const listener = e => {
      if (e.key === "Escape") {
        setSelectedPlace(null);
      }
    };
    window.addEventListener("keydown", listener);

    return () => {
      window.removeEventListener("keydown", listener);
    };
  }, []);

  return (
      <GoogleMap
          defaultZoom={10}
          defaultCenter={{ lat: 45.4211, lng: -75.6903 }}
      >
        {placesData.map(place => (
            <Marker
                key={place.id}
                position={{
                  lat: parseFloat(place.geo.lat),
                  lng: parseFloat(place.geo.lng)
                }}
                onClick={() => {
                  setSelectedPlace(place);
                }}
                // icon={{
                //   url: `/skateboarding.svg`,
                //   scaledSize: new window.google.maps.Size(25, 25)
                // }}
            />
        ))}

        {selectedPlace && (
            <InfoWindow
                onCloseClick={() => {
                  setSelectedPlace(null);
                }}
                position={{
                  lat: parseFloat(selectedPlace.geo.lat),
                  lng: parseFloat(selectedPlace.geo.lng)
                }}
            >
              <div>
                <h2>{selectedPlace.primary_heb_full}</h2>
                <h3>{selectedPlace.primary_rom_full}</h3>
                  <p>{selectedPlace.desc}</p>
              </div>
            </InfoWindow>
        )}
      </GoogleMap>
  );
}

const MapWrapped =withScriptjs(withGoogleMap(Map));

export default function App() {
  return (
      <div style={{ width: "100vw", height: "100vh" }}>
        <MapWrapped
            googleMapURL={`https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=${
                process.env.REACT_APP_GOOGLE_KEY
            }`}
            loadingElement={<div style={{ height: `100vh`, width:`100vw` }} />}
            containerElement={<div style={{ height: `100vh`, width:`100vw` }} />}
            mapElement={<div style={{ height: `100vh`, width:`100vw`}} />}
        />
      </div>
  );
}
