<template>
  <div>
      <canvas :id="id"></canvas>
  </div>
</template>
<script>
export default {
  name: "chart",
  props: ["dataset", "id"],
  data: function() {
    return {
      ctx: this.id,
    };
  },
  watch: {
    dataset: function() {
      this.axios
        .get("/api/v1/chart/data/" + this.dataset.chart)
        .then((response) => {
          var Chart = require("chart.js");
          var myChart = new Chart(this.ctx, response.data);

          myChart.render();
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
