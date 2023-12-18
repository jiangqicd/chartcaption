<template>
  <div class="row">
    <NavigationBar
      :chartInfo="chartInfo"
      :annotationStats="annotationStats"
    ></NavigationBar>
  </div>
</template>
  
<script>
import NavigationBar from "./NavigationBar.vue";

export default {
  components: {
    NavigationBar,
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