<template>
  <header class="header row">
    <div class="right-section">
      <nav class="select-box">
        <span class="input-group-btn">
          <select
            class="select-input"
            id="datasetSelect"
            v-model="selectedOption"
          >
            <option value="olympic_medals.csv">Olympic Medals</option>
            <option value="entrepreneurship.csv">Entrepreneurship</option>
            <option value="movies-w-year.csv">Movies</option>
            <option value="cars-w-year.csv">Cars</option>
            <option value="housing.csv">Housing</option>
            <option value="colleges.csv">Colleges</option>
            <option value="euro.csv">Euro</option>
            <option value="economic.csv">Economic</option>
            <option value="bill.csv">Bill</option>
            <option value="pubg.csv">Pubg</option>
            <option value="happiness.csv">Happiness</option>
            <option value="vaccine_correlation.csv">Vaccine</option>
          </select>
        </span>
      </nav>
      <div class="submit-button">
        <button
          class="btn btn-success"
          type="button"
          id="queryBtn"
          @click="handleSubmit"
        >
          Submit
        </button>
      </div>
      <h1 class="title">|Auto-annotator</h1>
    </div>
  </header>
</template>

<script>
import axios from "axios";
import bus from "../assets/js/event-bus";
import { inject, ref } from "vue";

export default {
  name: "AppHeader",
  setup() {
    const selectedOption = ref("vaccine_correlation.csv");
    const selectedChart = inject("selectedChart");
    const tableData = inject("tableData");
    const handleSubmit = () => {
      let url = "/get-table-csv";
      axios
        .post("/api" + url, {
          selected_table: selectedOption,
        })
        .then((res) => {
          //初始化表格数据
          Object.assign(selectedChart, res.data.selectedChart);
          updateTableData(res.data.map_attr_type, res.data.tableRecords);
          //将表格数据传给Table.vue组件绘制表格详情
          bus.emit("csv-data-loaded", res.data.tableRecords);
        })
        .catch((error) => {
          console.log(error);
        });
    };
    const updateTableData = (map_attr_type, tableRecords) => {
      //先将tableRecords由字符串转成json数组
      tableRecords = JSON.parse(tableRecords);

      // 遍历 map_attr_type 中的每个属性
      for (const attr in map_attr_type) {
        const attrType = map_attr_type[attr];
        // 初始化该属性的数据数组
        tableData[attr] = { type: attrType, data: [] };

        // 遍历 tableRecords 中的每一行数据，将对应属性的值添加到数据数组中
        for (const record of tableRecords) {
          tableData[attr].data.push(record[attr]);
        }
      }
      selectedChart.table.data = {
        form_of_records: tableRecords,
        form_of_attributes_lists: tableData,
      };
    };
    return { selectedOption, tableData, handleSubmit };
  },
};
</script>

<style scoped>
.header {
  background: #161616;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.right-section {
  display: flex;
  align-items: center;
  justify-content: center; /* 居中对齐 */
}

.select-box {
  position: center;
  top: 4px;
}

.select-input {
  height: 30px;
}

.submit-button {
  padding-left: 10px;
  padding-right: 10px;
  float: left;
}

.title {
  color: white;
  font-size: 25px;
}
</style>