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

    <!-- Tabs to switch between driving and transit modes -->
    <div class="tabs">
      <button
        @click="setTravelMode('DRIVING')"
        :class="{ active: travelMode === 'DRIVING' }"
      >
        Driving
      </button>
      <button
        @click="setTravelMode('TRANSIT')"
        :class="{ active: travelMode === 'TRANSIT' }"
      >
        Transit
      </button>
    </div>

    <!-- Button to calculate route -->
    <button @click="calculateRoute" class="calculate-route-button">
      Calculate Route
    </button>

    <!-- Box to display route details -->
    <div class="route-details" v-if="routeDetails && routeDetails.length">
      <h3>Route Details</h3>
      <div v-for="(route, index) in routeDetails" :key="index">
        <p>Route {{ index + 1 }}</p>
        <p>Distance: {{ route.distance / 1000 }}km</p>
        <p>Duration: {{ route.duration }}</p>
        <p>Fare: ${{ route.fare / 100 }}</p>
        <div v-if="route.steps">
          <h4>Route Steps</h4>
          <ul>
            <li
              v-for="(step, stepIndex) in route.steps"
              :key="stepIndex"
              v-html="step"
            ></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted } from "vue";
import { Loader } from "@googlemaps/js-api-loader";
import axios from "axios";

export default {
  name: "Map",
  setup() {
    const coords = ref({ lat: 1.29027, lng: 103.851959 }); // Default coordinates to Singapore
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
    const geocoder = ref(null);
    const map = ref(null);
    const startCoords = ref(null);
    const endCoords = ref(null);
    const mapReady = ref(false);
    const routeDetails = ref(null); // Data property to store route details
    const travelMode = ref("DRIVING"); // Data property to store travel mode
    const busStops = ref({}); // Store bus stop data

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

    const reverseGeocode = (lat, lng) => {
      return new Promise((resolve, reject) => {
        geocoder.value.geocode(
          { location: { lat, lng } },
          (results, status) => {
            if (status === "OK" && results[0]) {
              resolve(results[0].formatted_address);
            } else {
              reject(status);
            }
          }
        );
      });
    };

    const fetchBusStops = async () => {
      try {
        const response = await fetch(
          "https://data.busrouter.sg/v1/stops.min.json"
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        busStops.value = data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    
    const getBusStopNumber = (busStopName) => {
      for (const stopNumber in busStops.value) {
        const details = busStops.value[stopNumber];
        if (details[2] === busStopName) {
          return stopNumber;
        }
      }
      return null;
    };


    const calculateRoute = () => {
      if (!startCoords.value || !endCoords.value) {
        console.log("Start or end coordinates are not set.");
        return;
      }

      if (!mapReady.value) {
        console.error(
          "Map is not ready. DirectionsService or DirectionsRenderer is not initialized."
        );
        return;
      }

      console.log(
        "Calculating route between:",
        startCoords.value,
        endCoords.value
      );

      directionsService.value.route(
        {
          origin: startCoords.value,
          destination: endCoords.value,
          travelMode: travelMode.value,
          provideRouteAlternatives: true,
        },
        async (response, status) => {
          if (status === "OK") {
            directionsRenderer.value.setDirections(response);
            console.log("Route calculated successfully.");

            // Update route details
            const routes = response.routes;
            console.log(routes);
            let allRoutesDetails = [];

            for (let i = 0; i < response.routes.length; i++) {
              const distance = routes[i].legs[0].distance.value; // Distance in meters
              const duration = routes[i].legs[0].duration.text; // Duration as text

              let fare; // Declare the fare variable
if (distance != null) {
await axios.get('http://127.0.0.1:5000/run-script', {
    params: {
        type: 0,
        distance: distance
    }
})
.then(response => {
    fare = response.data.fare_per_ride; // Assign the fare value
})
.catch(error => {
    console.error('Error fetching fare:', error);
    this.error = error.response ? error.response.data.error : error.message;
});
}

              // Add transit steps if travel mode is transit
              let steps = await Promise.all(
                routes[i].legs[0].steps.map(async (step) => {
                  var instructionString;
                  if (step.travel_mode === "TRANSIT") {
                    if (step.transit.line.vehicle.name === "Bus") {
                      let busStopNumber = getBusStopNumber("Opp Parkway Parade");
                      instructionString = `Take bus ${step.transit.line.name} from ${step.transit.departure_stop.name} (${busStopNumber}) to ${step.transit.arrival_stop.name} (${busStopNumber})`;
                    } else if (["Tram", "Subway"].includes(step.transit.line.vehicle.name)) {
                      instructionString = `Take train from ${step.transit.departure_stop.name} to ${step.transit.arrival_stop.name}`;
                    } else {
                      instructionString = step.instructions;
                    }
                  } else if (step.travel_mode === "WALKING") {
                    instructionString = step.instructions;
                  }
                  return instructionString;
                })
              )
              allRoutesDetails.push({
                distance,
                duration,
                steps,
                fare
              });
              console.log(allRoutesDetails);
            };

            routeDetails.value = allRoutesDetails;
            console.log("Route details updated:", routeDetails.value);
          } else {
            console.error("Directions request failed due to " + status);
          }
        }
      );
    };

    const setTravelMode = (mode) => {
      travelMode.value = mode;
    };

    const openMarker = (id) => {
      openedMarkerID.value = id;
    };

    const onMapReady = (mapInstance) => {
      map.value = mapInstance;
      directionsService.value = new google.maps.DirectionsService();
      directionsRenderer.value = new google.maps.DirectionsRenderer();
      geocoder.value = new google.maps.Geocoder();
      directionsRenderer.value.setMap(mapInstance);
      mapReady.value = true;
      console.log("Map is ready and directions service/renderer initialized.");
    };

    onMounted(() => {
      const loader = new Loader({
        apiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
        libraries: ["places"],
      });

      loader
        .load()
        .then(() => {
          const mapOptions = {
            center: coords.value,
            zoom: 10,
            mapTypeId: "terrain",
          };

          const mapInstance = new google.maps.Map(
            document.getElementById("map"),
            mapOptions
          );
          onMapReady(mapInstance);
          fetchBusStops(); // Fetch bus stop data once the map is ready
        })
        .catch((e) => {
          console.error("Error loading Google Maps API:", e);
        });
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
      calculateRoute,
      routeDetails, // Add routeDetails to the return object
      travelMode, // Add travelMode to the return object
      setTravelMode, // Add setTravelMode to the return object
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
.tabs {
  margin-top: 10px;
}
.tabs button {
  padding: 10px 20px;
  margin-right: 5px;
  cursor: pointer;
  background-color: #f0f0f0;
  border: none;
  border-radius: 5px;
  font-size: 14px;
}
.tabs button.active {
  background-color: #4285f4;
  color: white;
}
.calculate-route-button {
  margin-top: 10px;
  padding: 10px 20px;
  cursor: pointer;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 14px;
}
.route-details {
  margin-top: 20px;
  padding: 10px;
  border-radius: 5px;
  background-color: #000000;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}
</style>
