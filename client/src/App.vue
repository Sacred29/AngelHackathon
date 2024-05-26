<script>
import Map from "./components/Map.vue";
import FetchMRTDensity from "./components/FetchMRTDensity.vue";
import FetchCost from "./components/FetchCost.vue";

export default {
  name: "App",
  components: {
    Map,
    // FetchCost
  },
};
</script>

<template>
  <header>
    <div class="wrapper">
    </div>
  </header>
  <div id="app" class="app-container">
    <Map />
    <!-- <FetchCost /> -->
  </div>
  <!-- <FetchMRTDensity /> -->

  <main>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
  text-align: center; /* Center align text */
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

#app {
  display: flex;
  justify-content: center; /* Center align flex items horizontally */
  align-items: center; /* Center align flex items vertically */
}

.wrapper {
  max-width: 1200px;
  margin: 0 auto; /* Center align wrapper horizontally */
}
</style>

<style>
/* Global styles */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
}

.app-container {
  padding-right: 2rem; /* Add padding on the right side */
}

@media (min-width: 1024px) {
  .app-container {
    padding-right: 2rem; /* Adjust padding for larger screens if needed */
  }
}
</style>
