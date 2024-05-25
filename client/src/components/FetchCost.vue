<template>
    <div>
      <h1>Fare Information</h1>
      <div v-if="fare">
        <p>Fare per ride: {{ fare }}</p>
      </div>
      <div v-else>
        <p>Loading...</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'FareComponent',
    data() {
      return {
        fare: null,
        error: null,
      };
    },
    created() {
      this.fetchFare();
    },
    methods: {
      async fetchFare() {
        try {
            console.log("hello")
          const response = await axios.get('http://127.0.0.1:5000/run-script', {
            params: {
              type: 0,
              distance: 10
            }
          });
          this.fare = response.data.fare_per_ride;
          console.log("bye")
        } catch (error) {
          this.error = error.response ? error.response.data : error.message;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>
  