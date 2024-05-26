import './assets/main.css';
import VueGoogleMaps from '@fawmi/vue-google-maps';
import { createApp } from 'vue';
import App from './App.vue';
import 'bootstrap/dist/css/bootstrap.min.css';

// Load the API key from the environment variable
const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

const app = createApp(App);
app.use(VueGoogleMaps, {
  load: {
    key: apiKey,
    libraries: 'places',
  },
}).mount('#app');
