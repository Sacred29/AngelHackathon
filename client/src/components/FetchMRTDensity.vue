<template>
    <div>
      <div v-for="station in jsonData.value" :key="station.Station">
        <h2>Station: {{ station.Station }}</h2>
        <p>Crowd Level: {{ station.CrowdLevel }}</p>
      </div>
    </div>
  </template>

<script>
import jsonData from '../json/ewl.json';

export default {
  data() {
    return {
      jsonData,
    };
  },
};
</script>

<style scoped>
/* Your styles here */
</style>
