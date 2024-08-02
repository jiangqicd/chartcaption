import { createApp } from 'vue';
import App from './App.vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle';
import loader from "vue3-ui-preloader";
import "vue3-ui-preloader/dist/loader.css";
import { selectedChart, tableData, annotatedChart, selectedTable,annotatedChartList } from './assets/js/chart';
import { ContextMenu } from '@imengyu/vue3-context-menu';
import ToggleButton from 'vue-js-toggle-button'


const app = createApp(App);
app.component('FileLoaderComponent', loader);
app.provide('selectedChart', selectedChart);
app.provide('annotatedChart', annotatedChart);
app.provide('tableData', tableData);
app.provide('selectedTable', selectedTable);
app.provide('annotatedChartList', annotatedChartList);
app.use(ContextMenu);
app.use(ToggleButton)
app.mount('#app');
