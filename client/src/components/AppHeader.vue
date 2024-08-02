<template>
  <header class="header row">
    <div class="right-section">
      <nav class="select-box">
        <span class="input-group-btn">
          <select class="select-input" id="datasetSelect" v-model="selectedOption">
            <option value="olympic_medals.csv">Olympic Medals</option>
            <option value="movies-w-year.csv">Movies</option>
            <option value="cars-w-year.csv">Cars</option>
            <option value="vaccine_correlation.csv">Vaccine</option>
            <option value="energy_data_1990_2020.csv">Energy</option>
          </select>
        </span>
      </nav>
      <div class="submit-button">
        <button class="btn btn-success" type="button" id="queryBtn" @click="handleSubmit">
          Submit
        </button>
      </div>
      <h1 class="title">|Auto-annotator</h1>
    </div>
  </header>
  <FileLoaderComponent v-if="loading" name="spinning" loadingText="Loading..." textColor="#ffffff" textSize="18"
    textWeight="500" object="#ff9633" color1="#ffffff" color2="#17fd3d" size="5" speed="2" bg="#343a40"
    objectbg="#999793" opacity="80" :disableScrolling="true"></FileLoaderComponent>
</template>

<script>
import axios from "axios";
import bus from "../assets/js/event-bus";
import * as d3 from 'd3';
import * as Plot from '@observablehq/plot';
// import { axisFy } from '@observablehq/plot';
import { inject, ref, reactive } from "vue";
// import { annotatedChartList } from "@/assets/js/chart";

export default {
  name: "AppHeader",
  setup() {
    const selectedOption = ref("vaccine_correlation.csv");
    const selectedChart = inject("selectedChart");
    const annotatedChartList = inject("annotatedChartList");
    const tableData = inject("tableData");
    let selectedTable = inject("selectedTable");
    const loading = ref(false);
    var data = reactive([]);
    const handleSubmit = () => {
      loading.value = true
      Object.keys(annotatedChartList).forEach(key => {
        delete annotatedChartList[key];
      });
      // annotatedChartList.splice(0);
      let url = "/get-table-csv";
      selectedTable.value = selectedOption.value
      axios
        .post("/api" + url, {
          selected_table: selectedOption,
        })
        .then((res) => {
          //初始化表格数据
          Object.assign(selectedChart, res.data.selectedChart);
          data = JSON.parse(res.data.ts)
          console.log(data)
          // drawHorizonChart(data)
          updateTableData(res.data.map_attr_type, res.data.tableRecords);
          //将表格数据传给Table.vue组件绘制表格详情
          bus.emit("csv-data-loaded", res.data.tableRecords);
        })
        .catch((error) => {
          console.log(error);
        }).finally(() => {
          loading.value = false
          drawHorizonChart(data)
        })
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
    const drawHorizonChart = (data) => {

      const horizonDiv = document.getElementById('horizon');
      horizonDiv.innerHTML = ""

      Object.keys(data[0]).forEach(key => {
        const values = data.map(item => item[key]);
        const binds = 4
        const step = (d3.max(values) - d3.min(values)) / binds
        const chart = Plot.plot({
          x: { axis: null, },
          y: {
            domain: [d3.min(values), d3.max(values)],
            axis: null,
            label: key, // 设置 Y 轴标签为当前的 key
            // tickFormat: "", // 不显示刻度值
            // grid: false // 不显示网格线
          },
          color: {
            type: "ordinal",
            scheme: "YlGnBu",
            label: "Vehicles per hour",
            // tickFormat: (i) => ((i + 1) * step).toLocaleString("en"),
            legend: false
          },
          marks: [
            d3.range(binds).map((band) => Plot.areaY(values, { x: (d, i) => i, y: (d) => d - band * step, axis: "left", label: key, fill: band })),
          ],
          height: 30, // Horizon chart typically uses small height
          width: 300 // Set a specific width for each chart
        });
        const svg = d3.select(chart)
        svg.append("g").append("text")
          .attr("x", 0)
          .attr("y", 10)
          .attr("font-size", "10px")
          .attr("text-anchor", "start")
          .text(function () {
            if (key.length > 15) {
              return key.slice(0, 15) + "...";
            } else {
              return key;
            }
          })
        horizonDiv.appendChild(chart);
      });
    };
    return { selectedOption, tableData, handleSubmit, selectedTable, loading };
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
  justify-content: center;
  /* 居中对齐 */
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