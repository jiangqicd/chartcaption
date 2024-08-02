<template>
  <div class="row">
    <NavigationBar
      :chartInfo="chartInfo"
      :annotationStats="annotationStats"
    ></NavigationBar>
    <PlotArea></PlotArea>
  </div>
</template>
  
<script>
import NavigationBar from "./NavigationBar.vue";
import PlotArea from "./PlotArea_v1.vue";

export default {
  components: {
    NavigationBar,
    PlotArea,
  },
  data() {
    return {
      chartInfo: {
        visualEncoding: "某种编码方式",
        dataRange: "数据区间信息",
      },
      annotationStats: {
        total: 10,
        approved: 7,
        pending: 3,
      },
    };
  },
};
</script>