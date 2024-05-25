import './assets/main.css'
import VueGoogleMaps from '@fawmi/vue-google-maps';
import https from 'https'

import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App);
app.use(VueGoogleMaps, {
    load: {
        key: 'AIzaSyDJHkiHhDBGTSd_AL1C5WCJXWYQaVgYV9M',
        libraries: "places"
    },
}).mount('#app');