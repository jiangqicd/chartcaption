<template>
  <div id="table_data" class="row">
    <table class="table table-bordered table-striped">
        <thead class="thead-dark">
        <tr>
          <th v-for="(header, index) in headers" :key="index">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in items" :key="index">
          <td v-for="header in headers" :key="header">{{ item[header] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
  
<script>
import bus from "../assets/js/event-bus";

export default {
  name: "Table_Data",
  data() {
    return {
      items: [],
      headers: [],
    };
  },
  created() {
    bus.on("csv-data-loaded", (csvData) => {
      const jsonArray = JSON.parse(csvData);
      console.log(jsonArray);
      if (jsonArray.length > 0) {
        this.headers = Object.keys(jsonArray[0]);
        this.items = jsonArray;
      }
    });
  },
};
</script>