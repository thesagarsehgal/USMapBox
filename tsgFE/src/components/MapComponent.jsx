import React, { useState, useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import { CircularProgress, Typography } from '@mui/material';

export default function MapComponent({
  mapRef,
  boundaryType,
  setBoundaryType,
  handleButtonClick,
  center,
  setCenter,
  zoom,
  setZoom,
  onMapClick
}) {
  const mapContainerRef = useRef();
  const [mapLoading, setMapLoading] = useState(true);
  const [mapError, setMapError] = useState(null);
  const [roundedArea, setRoundedArea] = useState()

  const cleanupMapResources = (map) => {
    if (!map || !map.getStyle()) return;

    try {
      if (map.getLayer('us-state-data-fill')) {
        map.removeLayer('us-state-data-fill');
      }
      if (map.getLayer('us-state-data-outline')) {
        map.removeLayer('us-state-data-outline');
      }
      
      if (map.getSource('us-state-data')) {
        map.removeSource('us-state-data');
      }
    } catch (error) {
      console.error('Cleanup error:', error);
    }
  };

  useEffect(() => {
    if (!mapboxgl.accessToken) {
      mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN;
    }

    try {
      const map = new mapboxgl.Map({
        container: mapContainerRef.current,
        zoom: zoom,
        center: center,
        style: 'mapbox://styles/mapbox/streets-v11',
        failIfMajorPerformanceCaveat: true
      });

      map.on('load', () => {
        setMapLoading(false);
        initializeMapLayers(map);
      });

      map.on('error', (e) => {
        console.error('Map error:', e.error);
        setMapError('Failed to load map. Please try refreshing the page.');
      });

      map.on('move', () => {
        const mapCenter = map.getCenter();
        const mapZoom = map.getZoom();
        setCenter([mapCenter.lng, mapCenter.lat]);
        setZoom(mapZoom);
      });

      mapRef.current = map;

      return () => {
        if (mapRef.current) {
          mapRef.current.remove();
        }
      };
    } catch (error) {
      console.error('Map initialization error:', error);
      setMapError('Failed to initialize map. Please check your connection.');
    }
  }, []);

  const initializeMapLayers = (map) => {
    if (!boundaryType) return;
    cleanupMapResources(map);

    try {
      const boundariesUrl = `${import.meta.env.VITE_BE_HOST}/api/v1/boundaries?boundary_type=${boundaryType}`;
      
      map.addSource('us-state-data', {
        type: 'geojson',
        data: boundariesUrl
      });

      map.addLayer({
        id: 'us-state-data-fill',
        type: 'fill',
        source: 'us-state-data',
        paint: {
          'fill-color': '#0080ff',
          'fill-opacity': 0.2
        }
      });

      map.addLayer({
        id: 'us-state-data-outline',
        type: 'line',
        source: 'us-state-data',
        paint: {
          'line-color': '#000',
          'line-width': 3
        }
      });

      map.on('mouseenter', 'us-state-data-fill', () => {
        map.getCanvas().style.cursor = 'pointer';
      });

      map.on('mouseleave', 'us-state-data-fill', () => {
        map.getCanvas().style.cursor = '';
      });

      map.on('click', 'us-state-data-fill', onMapClick);
    } catch (error) {
      console.error('Layer initialization error:', error);
      setMapError('Failed to load map data.');
    }
  };

  useEffect(() => {
    if (mapRef.current && mapRef.current.isStyleLoaded() && boundaryType) {
      initializeMapLayers(mapRef.current);
    }
  }, [boundaryType]);

  return (
    <div style={{ position: 'relative', height: '100%', width: '100%' }}>
      {mapLoading && <CircularProgress />}
      {mapError && (
        <div className="map-error">
          <Typography color="error">{mapError}</Typography>
        </div>
      )}
      <div id='map-container' ref={mapContainerRef} style={{ height: '100%', width: '100%' }} />
    </div>
  );
}