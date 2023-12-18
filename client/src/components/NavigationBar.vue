<template>
  <div class="col-md-2 navigation" v-if="isRendered">
    <div>
      <div class="inline-div" style="margin-bottom: 1px; margin-top: 1px;">
        <span class="badge bg-success" style="margin-right: 60px;">X-Axis:</span>
        <span class="badge bg-info">operation:</span>
        <select class="custom-form-select" v-model="selectedChart.x.name">
          <option
            v-for="attr in selectedChart.table.x_delimited_attributes"
            :value="attr.name"
            :key="attr.name"
          >
            {{ attr.name }}
          </option>
        </select>
      </div>
      <div class="inline-div">
        <span class="badge bg-info">attribute:</span>
        <select class="custom-form-select-1" v-model="selectedChart.x.name">
          <option
            v-for="attr in selectedChart.table.x_delimited_attributes"
            :value="attr.name"
            :key="attr.name"
          >
            {{ attr.name }}
          </option>
        </select>
      </div>
    </div>
    <div>
      <div class="inline-div" style="margin-bottom: 1px; margin-top: 1px;">
        <span class="badge bg-success" style="margin-right: 60px;">Y-Axis:</span>
        <span class="badge bg-info">operation:</span>
        <select class="custom-form-select" v-model="selectedChart.y.operation">
          <option
            v-for="attr in selectedChart.table.x_delimited_attributes"
            :value="attr.name"
            :key="attr.name"
          >
            {{ attr.name }}
          </option>
        </select>
      </div>
      <div class="inline-div">
        <span class="badge bg-info">attribute:</span>
        <select class="custom-form-select-1" v-model="selectedChart.y.name">
          <option
            v-for="attr in selectedChart.table.y_delimited_attributes"
            :value="attr.name"
            :key="attr.name"
          >
            {{ attr.name }}
          </option>
        </select>
      </div>
    </div>
    <div>
      <div class="inline-div" style="margin-bottom: 1px; margin-top: 1px;">
        <span class="badge bg-success" >filter</span>
      </div>
      <div class="inline-div">
        <span class="badge bg-info">attribute:</span>
        <select class="custom-form-select-1" v-model="selectedChart.y.name">
          <option
            v-for="attr in selectedChart.table.y_delimited_attributes"
            :value="attr.name"
            :key="attr.name"
          >
            {{ attr.name }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>
  
<script>
import { inject, computed } from "vue";
export default {
  name: "NavigationBar",
  setup() {
    const selectedChart = inject("selectedChart");

    const isRendered = computed(() => {
      return Object.keys(selectedChart).length > 0;
    });

    return {
      isRendered,
      selectedChart,
    };
  },
};
</script>
  
<style>
.navigation {
  border-right: 2px solid gray;
  border-bottom: 2px solid gray;
  height: 600px;
}
.inline-div {
  display: flex;
}
.badge {
  flex: 1; /* 使 <span> 和 <select> 具有相同的宽度 */
  display: inline-flex; /* 将 <span> 设置为 inline-flex */
  align-items: center; /* 垂直居中 <span> 内容 */
  height: 20px; /* 设置高度为 40px 或适当的值 */
}
.custom-form-select {
  flex: 2; /* 调整 <select> 的长度，这里设置为 <span> 的两倍 */
  padding: 0px;
  font-size: 15px;
  height: 20px;
  margin: 0; /* 如有必要，移除外边距 */
  /* 其他必要的样式调整 */
}
.custom-form-select-1 {
  flex: 3; /* 调整 <select> 的长度，这里设置为 <span> 的两倍 */
  padding: 0px;
  font-size: 15px;
  height: 20px;
  margin: 0; /* 如有必要，移除外边距 */
  /* 其他必要的样式调整 */
}
</style>
  