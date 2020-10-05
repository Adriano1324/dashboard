<template>
  <div>
    <b-button href="/chart/new">Create dashboard</b-button>
    <b-row>
      <b-col cols="10" offset="1">
        <b-card-group class="justify-content-center">
          <chardcard
            v-for="chart of charts"
            :data="chart"
            :key="chart._id.id"
          ></chardcard>
        </b-card-group> </b-col
    ></b-row>
  </div>
</template>

<script>
import chart_card from "../components/parts/chart_card";
export default {
  name: "Charts",
  data: function () {
    return {
      charts: null,
    };
  },
  components: {
    chardcard: chart_card,
  },
  mounted: function () {
    this.get_charts();
  },
  methods: {
    get_charts: function () {
      this.axios.get("/api/v1/charts/my").then((response) => {
        this.charts = response.data;
      });
    },
  },
};
</script>

<style></style>
