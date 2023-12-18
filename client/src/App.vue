<template>
  <AppHeader />
  <ChartCaption />
  <Table_Data />
</template>

<script>
import AppHeader from "./components/AppHeader.vue";
import ChartCaption from "./components/ChartCaption.vue";
import Table_Data from "./components/Table.vue";

export default {
  name: "App",
  components: {
    AppHeader,
    ChartCaption,
    Table_Data,
  },
};
</script>

<style>

</style>
