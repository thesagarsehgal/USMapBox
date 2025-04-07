import { useState, useRef, useEffect } from 'react'
import mapboxgl from 'mapbox-gl'

import './App.css'
import 'mapbox-gl/dist/mapbox-gl.css';
import MapControls from './components/MapControls';
import MapComponent from './components/MapComponent';
import DataSidebar from './components/DataSidebar';


function App() {
  const mapRef = useRef()
  const INITIAL_ZOOM = 4;
  const INITIAL_CENTER = [
    -97.9386, 39.5308
  ]
  const BE_HOST = import.meta.env.VITE_BE_HOST;
  

  const [boundaryType, setBoundaryType] = useState('state')
  const [center, setCenter] = useState(INITIAL_CENTER)
	const [zoom, setZoom] = useState(INITIAL_ZOOM)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [quickFactData, setQuickFactData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)


  const handleButtonClick = () => {
		mapRef.current.flyTo({
			center: INITIAL_CENTER,
			zoom: INITIAL_ZOOM
		})
	}

  const onMapClick = async (e) => {
    if (!e.features || e.features.length === 0) {
      setError('No features found at this location');
      setSidebarOpen(true);
      return;
    }

    try {
      const coordinates = e.features[0].geometry.coordinates.slice();
      const feature = e.features[0].properties;
      const geoid = feature["id"];
      
      if (!geoid) {
        throw new Error('Invalid geographic ID');
      }

      setIsLoading(true);
      setSidebarOpen(true);
      setError(null);

      const response = await fetch(`${BE_HOST}/api/v1/data?geo_id=${geoid}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data?.facts || !data?.location_id || !data?.location_name) {
        throw new Error('Invalid data format received from server');
      }

      setQuickFactData(data);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError(error.message || 'Failed to load data');
      setQuickFactData(null);
    } finally {
      setIsLoading(false);
    }
  }


  return (
    <>
      <MapControls 
        boundaryType={boundaryType}
        setBoundaryType={setBoundaryType}
        resetView={handleButtonClick}
        center={center}
        zoom={zoom}
      />
      <DataSidebar
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
        quickFactData={quickFactData}
        isLoading={isLoading}
        error={error}
      />
      <MapComponent 
        mapRef={mapRef}
        boundaryType={boundaryType}
        setBoundaryType={setBoundaryType}
        resetView={handleButtonClick} 
        center={center}
        setCenter={setCenter}
        zoom={zoom}
        setZoom={setZoom}
        onMapClick={onMapClick}
      />

    </>
  )
}

export default App
