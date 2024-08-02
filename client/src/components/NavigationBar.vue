<template>
  <div class="col-md-2 navigation" v-if="isRendered">
    <!-- Data summary -->
    <div style="margin-top: 5px">
      <div class="inline-div" style="
          margin-bottom: 3px;
          margin-top: 3px;
          border-bottom: 2px solid gray;
          border-top: 2px solid gray;
        ">
        <div class="badge text-primary-emphasis text-wrap">Data summary</div>
      </div>
      <div id="horizon">
      </div>
    </div>
    <!-- Chart parameter area -->
    <div>
      <div class="inline-div" style="
          margin-bottom: 3px;
          margin-top: 3px;
          border-bottom: 2px solid gray;
          border-top: 2px solid gray;
        ">
        <div class="badge text-primary-emphasis text-wrap">
          Chart parameter panel
        </div>
      </div>
      <div>
        <div class="inline-div" style="margin-bottom: 3px; margin-top: 3px">
          <span class="badge bg-success" style="margin-right: 60px">X-Axis:</span>
          <span class="badge bg-info">operation:</span>
          <select class="custom-form-select" v-model="selectedXOperation" @change="xOperationSelectAttributeChange">
            <option v-for="option in selectedXOperationOptions" :value="option" :key="option">
              {{ option }}
            </option>
          </select>
        </div>
        <div class="inline-div">
          <span class="badge bg-info">attribute:</span>
          <select class="custom-form-select-1" v-model="selectedXValue" @change="ySelectAttributeChange">
            <option v-for="attr in selectedChart.table.x_delimited_attributes" :value="attr.name" :key="attr.name">
              {{ attr.name }}
            </option>
          </select>
        </div>
      </div>
      <div>
        <div class="inline-div" style="margin-bottom: 3px; margin-top: 3px">
          <span class="badge bg-success" style="margin-right: 60px">Y-Axis:</span>
          <span class="badge bg-info">operation:</span>
          <select class="custom-form-select" v-model="selectedYOperation" @change="yOperationSelectAttributeChange">
            <option v-for="option in selectedYOperationOptions" :value="option" :key="option">
              {{ option }}
            </option>
          </select>
        </div>
        <div class="inline-div">
          <span class="badge bg-info">attribute:</span>
          <select class="custom-form-select-1" v-model="selectedYValue" @change="ySelectAttributeChange">
            <option v-for="attr in selectedChart.table.y_delimited_attributes" :value="attr.name" :key="attr.name">
              {{ attr.name }}
            </option>
          </select>
        </div>
      </div>
      <div>
        <div class="inline-div" style="margin-bottom: 3px; margin-top: 3px">
          <span class="badge bg-success">filter</span>
        </div>
        <div class="inline-div">
          <span class="badge bg-info">attribute:</span>
          <select class="custom-form-select-1" v-model="selectedFilterAttribute" @change="filterSelectAttributeChange">
            <option v-for="attr in selectedChart.table.filter_delimited_attributes" :value="attr.name" :key="attr.name">
              {{ attr.name }}
            </option>
          </select>
        </div>
        <div v-if="selectedFilterAttribute">
          <!-- 当类型为 'oneOf' 时显示下拉列表 -->
          <div v-if="filterValueType === 'oneOf'">
            <div class="inline-div" style="margin-top: 3px">
              <span class="badge bg-info">value:</span>
              <select class="custom-form-select-2" v-model="selectedFilterValue" @change="filterSelectValueChange">
                <option v-for="option in filteredOptions" :value="option" :key="option">
                  {{ option }}
                </option>
              </select>
            </div>
            <!-- <div class="inline-div" style="margin-top: 3px">
              <span class="badge bg-info">find:</span>
              <input
                class="find"
                type="text"
                v-model="searchFliterText"
                @input="filterOptions"
                placeholder="search..."
              />
            </div> -->
          </div>

          <!-- 当类型为 'range' 时显示滑动条 -->
          <div v-else-if="filterValueType === 'range'">
            <div class="inline-div" style="margin-top: 3px">
              <span class="badge bg-info">scope</span>
              <div class="custom-form-select-2">
                <vue-slider v-model="selectedRangeAttributeScope" :min="selectedRangeAttributeMin"
                  :max="selectedRangeAttributeMax" :interval="stepSize" :enable-cross="false" :order="true"
                  :tooltip="'always'" :tooltip-placement="'top'" @change="filterSelectRangeChange" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Chart view area -->
    <div style="margin-top: 15px">
      <div class="inline-div" style="
          margin-bottom: 3px;
          margin-top: 3px;
          border-bottom: 2px solid gray;
          border-top: 2px solid gray;
        ">
        <div class="badge text-primary-emphasis text-wrap">Chart view</div>
      </div>
      <div>
        <svg ref="chartRef"></svg>
      </div>
      <div>
        <div class="inline-div" style="margin-top: 5px">
          <button @click="submitChartParameterEdit" type="button" class="btn btn-outline-success btn-xm"
            style="width: 300px">
            analyze
          </button>
          <button @click="cancelChartParameterEdit" type="button" class="btn btn-outline-secondary btn-xm">
            cancel
          </button>
        </div>
      </div>
    </div>
    <!-- Chart annotation area -->
    <!-- <div style="margin-top: 15px">
      <div class="inline-div" style="
          margin-bottom: 3px;
          margin-top: 3px;
          border-bottom: 2px solid gray;
          border-top: 2px solid gray;
        ">
        <div class="badge text-primary-emphasis text-wrap">
          Chart annotation summary
        </div>
      </div>
      <div>
        <p>>>>>>>>>>>>to do>>>>>>>>></p>
      </div>
    </div> -->
  </div>
  <FileLoaderComponent v-if="loading" name="spinning" loadingText="Analyzing..." textColor="#ffffff" textSize="18"
    textWeight="500" object="#ff9633" color1="#ffffff" color2="#17fd3d" size="5" speed="2" bg="#343a40"
    objectbg="#999793" opacity="80" :disableScrolling="true"></FileLoaderComponent>
</template>

<script>
import axios from "axios";
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/antd.css";
import { inject, computed, ref, watchEffect, onMounted } from "vue";
import * as d3 from "d3";
export default {
  name: "NavigationBar",
  components: { VueSlider },
  setup() {
    const selectedChart = inject("selectedChart");
    let selectedTable = inject("selectedTable");
    const annotatedChart = inject("annotatedChart");
    var annotatedChartList = inject("annotatedChartList");
    const selectedXOperationOptions = computed(() => {
      const selectedAttr = selectedChart.x.name;
      const attrObject = selectedChart.table.x_delimited_attributes.find(
        (attr) => attr.name === selectedAttr
      );
      return attrObject ? attrObject.operation.options : [];
    });

    const selectedYOperationOptions = computed(() => {
      const selectedAttr = selectedChart.y.name;
      const attrObject = selectedChart.table.y_delimited_attributes.find(
        (attr) => attr.name === selectedAttr
      );
      return attrObject ? attrObject.operation.options : [];
    });

    const isRendered = computed(() => {
      return Object.keys(selectedChart).length > 0;
    });

    const selectedXValue = ref("");
    const selectedYValue = ref("");
    const selectedXOperation = ref("");
    const selectedYOperation = ref("");

    const chartRef = ref(null);

    watchEffect(() => {
      if (Object.keys(selectedChart).length > 0) {
        selectedXValue.value = selectedChart.x.name;
        selectedYValue.value = selectedChart.y.name;
        selectedXOperation.value = selectedChart.x.operation;
        selectedYOperation.value = selectedChart.y.operation;
      }
    });
    const loading = ref(false);

    const submitChartParameterEdit = () => {

      loading.value = true

      selectedChart.x.name = selectedXValue.value;
      selectedChart.y.name = selectedYValue.value;
      selectedChart.x.operation = selectedXOperation.value;
      selectedChart.y.operation = selectedYOperation.value;
      selectedChart.filter.selectedAttribute = selectedFilterAttribute.value
      selectedChart.filter.type = filterValueType.value

      if (selectedChart.filter.type == "oneOf") {
        if (!Array.isArray(selectedFilterValue))
          selectedChart.filter.values = [selectedFilterValue.value]
      } else {
        selectedChart.filter.values = selectedRangeAttributeScope.value
      }


      let url = "/get-pattern-annotation";
      axios
        .post("/api" + url, {
          selectedChart: selectedChart,
          selectedTable: selectedTable.value
        })
        .then((res) => {
          //初始化表格数据
          // print("111")
          Object.assign(annotatedChart, res.data.annotatedChart);

          var id = selectedChart["x"]["name"] + selectedChart["y"]["name"] + selectedChart["filter"]["selectedAttribute"] + selectedChart["filter"]["values"].join()
          id = id.replace(/[ ,.]+/g, '');

          annotatedChartList[id] = res.data.annotatedChart
        })
        .catch((error) => {
          console.log(error);
        }).finally(() => {
          loading.value = false
          var selectedChartID = selectedChart["x"]["name"] + selectedChart["y"]["name"] + selectedChart["filter"]["selectedAttribute"] + selectedChart["filter"]["values"].join()
          selectedChartID = selectedChartID.replace(/[ ,.]+/g, '')
          const divElement = document.getElementById('annotationarea');
          const allSvgElements = divElement.querySelectorAll('svg');
          allSvgElements.forEach(svg => {
            if (svg&&d3.select(svg).attr("id") == selectedChartID) {
              addGlowEffect(svg)
            } else if(svg){
              d3.select(svg).selectAll('.halation').remove();
            }
          });
        });
    };

    const addGlowEffect = (svg) => {
      d3.select(svg).append('rect')
        .attr("class", "halation")
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('fill', 'none')
        .attr('stroke', "green")
        .attr('stroke-width', '4px')
        .attr('filter', 'url(#focus)');

    };

    const cancelChartParameterEdit = () => {
      selectedXValue.value = selectedChart.x.name;
      selectedYValue.value = selectedChart.y.name;
      selectedXOperation.value = selectedChart.x.operation;
      selectedYOperation.value = selectedChart.y.operation;
      selectedFilterAttribute.value = "";
      selectedFilterValue.value = "";
      selectedRangeAttributeScope.value = [];
      filterValueType.value = ""
      // if (selectedChart.filter.type !== "") {
      //   if (selectedChart.filter.type !== "oneOf") {
      //     selectedFilterValue.value = "";
      //   } else {
      //     selectedRangeAttributeScope.value = ["", ""];
      //   }
      // }
      if (chartRef.value) {
        drawLineChart(chartRef.value);
      }
    };

    const selectedFilterAttribute = ref("");
    const filterValueType = ref("");
    const searchFliterText = ref("");
    const selectedFilterValue = ref("");
    const filteredOptions = ref([]);
    const selectedRangeAttributeScope = ref([]);
    const selectedRangeAttributeMin = ref(0);
    const selectedRangeAttributeMax = ref(0);

    const xOperationSelectAttributeChange = (event) => {
      selectedXOperation.value = event.target.value;
      if (chartRef.value) {
        drawLineChart(chartRef.value);
      }
    };

    const yOperationSelectAttributeChange = (event) => {
      selectedYOperation.value = event.target.value;
      if (chartRef.value) {
        drawLineChart(chartRef.value);
      }
    };

    const xSelectAttributeChange = (event) => {
      selectedXValue.value = event.target.value;
      if (chartRef.value) {
        drawLineChart(chartRef.value);
      }
    };

    const ySelectAttributeChange = (event) => {
      selectedYValue.value = event.target.value;
      if (chartRef.value) {
        drawLineChart(chartRef.value);
      }
    };

    const filterSelectAttributeChange = (event) => {
      selectedFilterAttribute.value = event.target.value;
      filterValueType.value =
        selectedChart.table.filter_delimited_attributes.find(
          (attr) => attr.name === event.target.value
        ).type;
      filteredOptions.value =
        selectedChart.table.filter_delimited_attributes.find(
          (attr) => attr.name === event.target.value
        ).scope;
      selectedRangeAttributeScope.value =
        selectedChart.table.filter_delimited_attributes.find(
          (attr) => attr.name === event.target.value
        ).scope;
      selectedRangeAttributeMin.value =
        selectedChart.table.filter_delimited_attributes.find(
          (attr) => attr.name === event.target.value
        ).scope[0];
      selectedRangeAttributeMax.value =
        selectedChart.table.filter_delimited_attributes.find(
          (attr) => attr.name === event.target.value
        ).scope[1];
      selectedFilterValue.value = "";
    };

    const filterSelectValueChange = (event) => {
      selectedFilterValue.value = event.target.value;
      if (chartRef.value) {
        drawLineChart(chartRef.value);
      }
    };

    const filterSelectRangeChange = () => {
      if (chartRef.value) {
        drawLineChart(chartRef.value);
      }
    };

    const stepSize = computed(() => {
      // 定义时间关键字数组
      const time_keywords = ["year", "time", "date", "day", "week", "month"];

      // 检查转换为小写的 selectedFilterAttribute.value 是否在 time_keywords 中
      if (time_keywords.includes(selectedFilterAttribute.value.toLowerCase())) {
        return 1; // 如果存在于数组中，返回 1
      }
      const range =
        selectedRangeAttributeMax.value - selectedRangeAttributeMin.value;
      const step = range / 100;

      // 如果步长小于 0.01，返回浮点数，否则往上取整
      return parseFloat(step);
    });

    watchEffect(() => {
      if (Object.keys(selectedChart).length > 0) {
        drawLineChart(chartRef.value);
      }
    });

    onMounted(() => {
      if (chartRef.value) {
        drawLineChart(chartRef.value);
      }
    });

    function drawLineChart(element) {
      // console.log("------------------");
      // console.log(selectedChart.table.data.form_of_records)
      // 假设selectedChart包含了必要的数据和配置
      let rawdata = selectedChart.table.data.form_of_records; // 你的数据数组
      rawdata.sort((a, b) =>
        d3.ascending(a[selectedXValue.value], b[selectedXValue.value])
      );

      let data = [];

      // console.log(selectedRangeAttributeScope.value);

      if (selectedFilterAttribute.value !== "") {
        if (filterValueType.value === "oneOf") {
          if (selectedFilterValue.value !== "") {
            rawdata = rawdata.filter(
              (d) =>
                d[selectedFilterAttribute.value] === selectedFilterValue.value
            );
          }
        } else {
          const [min, max] = selectedRangeAttributeScope.value;
          rawdata = rawdata.filter(
            (d) =>
              d[selectedFilterAttribute.value] >= min &&
              d[selectedFilterAttribute.value] <= max
          );
        }
      }

      if (selectedYOperation.value === "mean") {
        data = Array.from(
          d3.group(rawdata, (d) => d[selectedXValue.value]),
          ([key, value]) => ({
            [selectedXValue.value]: key,
            [selectedYValue.value]: d3.mean(
              value,
              (d) => d[selectedYValue.value]
            ),
          })
        );
      } else if (selectedYOperation.value === "sum") {
        data = Array.from(
          d3.group(rawdata, (d) => d[selectedXValue.value]),
          ([key, value]) => ({
            [selectedXValue.value]: key,
            [selectedYValue.value]: d3.sum(
              value,
              (d) => d[selectedYValue.value]
            ),
          })
        );
      } else if (selectedYOperation.value === "min") {
        data = Array.from(
          d3.group(rawdata, (d) => d[selectedXValue.value]),
          ([key, value]) => ({
            [selectedXValue.value]: key,
            [selectedYValue.value]: d3.min(
              value,
              (d) => d[selectedYValue.value]
            ),
          })
        );
      } else if (selectedYOperation.value === "max") {
        data = Array.from(
          d3.group(rawdata, (d) => d[selectedXValue.value]),
          ([key, value]) => ({
            [selectedXValue.value]: key,
            [selectedYValue.value]: d3.max(
              value,
              (d) => d[selectedYValue.value]
            ),
          })
        );
      } else {
        data = rawdata;
      }

      const width = 300; // 图表的宽度
      const height = 300; // 图表的高度
      const margin = { top: 10, right: 20, bottom: 30, left: 40 };

      // 首先，清空 SVG 容器中的所有内容
      d3.select(element).selectAll("*").remove();

      // 创建SVG容器
      const svg = d3
        .select(element)
        .attr("width", width)
        .attr("height", height);

      // 设置x和y轴的比例尺
      const xScale = d3
        .scaleLinear()
        .domain(d3.extent(data, (d) => d[selectedXValue.value])) // d.x是你的数据中x轴的值
        .range([margin.left, width - margin.right]);

      const yScale = d3
        .scaleLinear()
        .domain([0, d3.max(data, (d) => d[selectedYValue.value])]) // d.y是你的数据中y轴的值
        .range([height - margin.bottom, margin.top]);

      // 添加x轴
      const xAxisGroup = svg
        .append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(xScale));

      xAxisGroup
        .selectAll(".tick text")
        .style("text-anchor", "end") // 为了让文本右对齐，以保证旋转后文本的定位更合理
        .attr("transform", "rotate(-45)")
        .attr("dx", "-.8em") // 调整x位置以避免标签重叠，根据实际情况调整
        .attr("dy", ".15em"); // 微调y位置以保持视觉上的居中，根据实际情况调整

      // 添加y轴
      svg
        .append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(yScale));

      // 网格线
      svg
        .selectAll(".grid-line.x")
        .data(xScale.ticks(10))
        .enter()
        .append("line")
        .attr("class", "grid-line")
        .attr("x1", (d) => xScale(d))
        .attr("x2", (d) => xScale(d))
        .attr("y1", margin.top)
        .attr("y2", height - margin.bottom)
        .style("stroke", "#ddd")
        .style("stroke-opacity", 0.7);

      svg
        .selectAll(".grid-line.y")
        .data(yScale.ticks(10))
        .enter()
        .append("line")
        .attr("class", "grid-line")
        .attr("x1", margin.left)
        .attr("x2", width - margin.right)
        .attr("y1", (d) => yScale(d))
        .attr("y2", (d) => yScale(d))
        .style("stroke", "#ddd")
        .style("stroke-opacity", 0.7);

      // 自定义轴样式
      svg
        .selectAll(".axis path, .axis line")
        .style("fill", "none")
        .style("stroke", "#000")
        .style("shape-rendering", "crispEdges");

      svg
        .selectAll(".axis text")
        .style("font-family", "Arial, sans-serif")
        .style("font-size", "12px");

      // 添加 x 轴标签
      svg
        .append("text")
        .attr("transform", `translate(${width / 2}, ${height + 10})`) // 将文本定位在 x 轴下方正中央
        .style("text-anchor", "middle") // 文本居中对齐
        .style("font-size", "12px")
        .text(selectedXValue.value); // 替换为你的 x 轴标签文本

      // 添加 y 轴标签
      svg
        .append("text")
        .attr(
          "transform",
          `rotate(-90) translate(${-height / 2}, ${margin.left - 28})`
        ) // 旋转并定位文本至 y 轴左侧
        .style("text-anchor", "middle") // 文本垂直居中对齐
        .style("font-size", "12px")
        .text(selectedYValue.value); // 替换为你的 y 轴标签文本

      // 定义线生成器
      const line = d3
        .line()
        .x((d) => xScale(d[selectedXValue.value]))
        .y((d) => yScale(d[selectedYValue.value]));

      // 绘制线
      svg
        .append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", line);
    }

    return {
      chartRef,
      stepSize,
      isRendered,
      selectedChart,
      selectedXOperation,
      selectedXOperationOptions,
      selectedYOperation,
      selectedYOperationOptions,
      selectedXValue,
      selectedYValue,
      selectedFilterAttribute,
      filterValueType,
      xOperationSelectAttributeChange,
      yOperationSelectAttributeChange,
      xSelectAttributeChange,
      ySelectAttributeChange,
      filterSelectAttributeChange,
      filterSelectValueChange,
      filterSelectRangeChange,
      searchFliterText,
      filteredOptions,
      selectedFilterValue,
      selectedRangeAttributeMin,
      selectedRangeAttributeMax,
      selectedRangeAttributeScope,
      submitChartParameterEdit,
      cancelChartParameterEdit,
      loading,
    };
  },
};
</script>

<style>
.navigation {
  border-right: 2px solid gray;
  height: 900px;
}

.inline-div {
  display: flex;
}

.badge {
  flex: 1;
  /* 使 <span> 和 <select> 具有相同的宽度 */
  display: inline-flex;
  /* 将 <span> 设置为 inline-flex */
  align-items: center;
  /* 垂直居中 <span> 内容 */
  height: 20px;
  /* 设置高度为 40px 或适当的值 */
}

.find {
  flex: 4;
  height: 20px;
}

.custom-form-select {
  flex: 2;
  /* 调整 <select> 的长度，这里设置为 <span> 的两倍 */
  padding: 0px;
  font-size: 15px;
  height: 20px;
  margin: 0;
  /* 如有必要，移除外边距 */
  /* 其他必要的样式调整 */
}

.custom-form-select-1 {
  flex: 3;
  /* 调整 <select> 的长度，这里设置为 <span> 的两倍 */
  padding: 0px;
  font-size: 15px;
  text-overflow: ellipsis;
  width: 220px;
  height: 20px;
  margin: 0;
  /* 如有必要，移除外边距 */
  /* 其他必要的样式调整 */
}

.custom-form-select-2 {
  flex: 4;
  /* 调整 <select> 的长度，这里设置为 <span> 的两倍 */
  padding: 0px;
  font-size: 15px;
  max-width: 220px;
  text-overflow: ellipsis;
  height: 20px;
  margin: 0;
  /* 如有必要，移除外边距 */
  /* 其他必要的样式调整 */
}

#horizon {
  overflow-y: hidden;
  /* 默认情况下隐藏垂直滚动条 */
  height: 320px;
  /* 可以设置一个固定高度,或者使用其他方法来确定高度 */
}

#horizon:hover {
  overflow-y: auto;
  /* 当鼠标悬停时显示垂直滚动条 */
}

#horizon::-webkit-scrollbar {
  width: 4px;
  /* 设置滚动条宽度 */
}

#horizon::-webkit-scrollbar-track {
  background-color: #f1f1f1;
  /* 设置滚动条背景色 */
}

#horizon::-webkit-scrollbar-thumb {
  background-color: #cbc7c7;
  /* 设置滚动条滑块颜色 */
  border-radius: 6px;
  /* 设置滑块圆角 */
}

#horizon::-webkit-scrollbar-thumb:hover {
  background-color: #cbc7c7;
  /* 设置鼠标悬停时滑块颜色 */
}
</style>