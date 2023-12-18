import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle'
import { selectedChart,tableData } from './assets/js/chart'

const app = createApp(App);
app.provide('selectedChart', selectedChart);
app.provide('tableData', tableData);
app.mount('#app')
