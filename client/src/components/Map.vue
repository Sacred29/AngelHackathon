<template>
    <div>
      <!-- Input search boxes for Google Places Autocomplete -->
      <div class="search-box">
        <GMapAutocomplete
          placeholder="Start location"
          @place_changed="updateStartPoint"
          style="font-size: medium"
        ></GMapAutocomplete>
      </div>
  
      <div class="search-box">
        <GMapAutocomplete
          placeholder="End location"
          @place_changed="updateEndPoint"
          style="font-size: medium"
        ></GMapAutocomplete>
      </div>
  
      <!-- Rendering the map on the page -->
      <div id="map" style="width: 80vw; height: 20rem"></div>
    </div>
  </template>
  
  <script>
  import { ref, watch, onMounted } from "vue";
  import { Loader } from "@googlemaps/js-api-loader";
  
  export default {
    name: "Map",
    setup() {
      const coords = ref({ lat: 51.5072, lng: 0.1276 }); // Default coordinates to London
      const markerDetails = ref({
        id: 1,
        position: coords.value,
      });
      const openedMarkerID = ref(null);
      const locationDetails = ref({
        address: "",
        url: "",
      });
  
      const directionsService = ref(null);
      const directionsRenderer = ref(null);
      const map = ref(null);
      const startCoords = ref(null);
      const endCoords = ref(null);
      const mapReady = ref(false);
  
      const getUserLocation = () => {
        const isSupported = "navigator" in window && "geolocation" in navigator;
        if (isSupported) {
          navigator.geolocation.getCurrentPosition((position) => {
            coords.value.lat = position.coords.latitude;
            coords.value.lng = position.coords.longitude;
          });
        }
      };
  
      const updateStartPoint = (place) => {
        if (place && place.geometry && place.geometry.location) {
          startCoords.value = {
            lat: place.geometry.location.lat(),
            lng: place.geometry.location.lng(),
          };
          console.log("Start point updated:", startCoords.value);
        } else {
          console.error("Invalid place object for start point:", place);
        }
      };
  
      const updateEndPoint = (place) => {
        if (place && place.geometry && place.geometry.location) {
          endCoords.value = {
            lat: place.geometry.location.lat(),
            lng: place.geometry.location.lng(),
          };
          console.log("End point updated:", endCoords.value);
        } else {
          console.error("Invalid place object for end point:", place);
        }
      };
  
      const calculateRoute = () => {
        if (!startCoords.value || !endCoords.value) {
          console.log("Start or end coordinates are not set.");
          return;
        }
  
        if (!mapReady.value) {
          console.error("Map is not ready. DirectionsService or DirectionsRenderer is not initialized.");
          return;
        }
  
        console.log("Calculating route between:", startCoords.value, endCoords.value);
  
        directionsService.value.route(
          {
            origin: startCoords.value,
            destination: endCoords.value,
            travelMode: "DRIVING",
          },
          (response, status) => {
            if (status === "OK") {
              directionsRenderer.value.setDirections(response);
              console.log("Route calculated successfully.");
            } else {
              console.error("Directions request failed due to " + status);
            }
          }
        );
      };
  
      const openMarker = (id) => {
        openedMarkerID.value = id;
      };
  
      const onMapReady = (mapInstance) => {
        map.value = mapInstance;
        directionsService.value = new google.maps.DirectionsService();
        directionsRenderer.value = new google.maps.DirectionsRenderer();
        directionsRenderer.value.setMap(mapInstance);
        mapReady.value = true;
        console.log("Map is ready and directions service/renderer initialized.");
        calculateRoute(); // Attempt to calculate route in case coordinates are already set
      };
  
      // Load the Google Maps API and initialize the map
      onMounted(() => {
        const loader = new Loader({
          apiKey: "AIzaSyDJHkiHhDBGTSd_AL1C5WCJXWYQaVgYV9M",
          libraries: ["places"]
        });
  
        loader.load().then(() => {
          const mapOptions = {
            center: coords.value,
            zoom: 10,
            mapTypeId: "terrain"
          };
  
          const mapInstance = new google.maps.Map(document.getElementById("map"), mapOptions);
          onMapReady(mapInstance);
        }).catch((e) => {
          console.error("Error loading Google Maps API:", e);
        });
      });
  
      // Watch for changes in startCoords, endCoords, and mapReady
      watch([startCoords, endCoords, mapReady], () => {
        if (mapReady.value && startCoords.value && endCoords.value) {
          calculateRoute();
        }
      });
  
      getUserLocation();
  
      return {
        coords,
        markerDetails,
        openedMarkerID,
        openMarker,
        getUserLocation,
        updateStartPoint,
        locationDetails,
        updateEndPoint,
        map,
        onMapReady,
        calculateRoute, // Add calculateRoute to return object
      };
    },
  };
  </script>
  
  <style scoped>
  .search-box {
    margin: 10px 0px;
    padding: 10px;
    border-radius: 5px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  }
  .location-details {
    color: blue;
    font-size: 12px;
    font-weight: 500;
  }
  </style>
  