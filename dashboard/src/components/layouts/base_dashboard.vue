<template>
  <div>
    <b-container fluid id="topDiv">
      <b-row>
        <b-col cols="6" class="chart-container">
          <chart v-if="mode == 'watch'" :dataset="position1" id="position1" />
          <div v-if="mode == 'edit'">
            <div class="field">
              <b-form-select
                v-model="config.charts[0].chart"
                :options="chart_options"
              ></b-form-select>
            </div>
            <div class="field">
              <b-form-input v-model="config.name"></b-form-input>
            </div>
            <b-button @click="edit_dashboard()">
              Edit dashboard
            </b-button>
            <b-button @click="create_dashboard()">
              Create dashboard
            </b-button>
          </div>
        </b-col>
        <b-col cols="6" class="chart-container">
          <chart v-if="mode == 'watch'" :dataset="position2" id="position2" />
          <div v-if="mode == 'edit'">
            <div class="field">
              <b-form-select
                v-model="config.charts[1].chart"
                :options="chart_options"
              ></b-form-select>
            </div>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="6" class="chart-container">
          <chart v-if="mode == 'watch'" :dataset="position3" id="position3" />
          <div v-if="mode == 'edit'">
            <div class="field">
              <b-form-select
                v-model="config.charts[2].chart"
                :options="chart_options"
              ></b-form-select>
            </div>
          </div>
        </b-col>
        <b-col cols="6" class="chart-container">
          <chart v-if="mode == 'watch'" :dataset="position4" id="position4" />
          <div v-if="mode == 'edit'">
            <div class="field">
              <b-form-select
                v-model="config.charts[3].chart"
                :options="chart_options"
              ></b-form-select>
            </div>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import chart from "../charts/chart";
export default {
  name: "base_dashboard",
  data: function() {
    return {
      position1: "",
      position2: "",
      position3: "",
      position4: "",
      mode: this.$route.params.mode,
      id: this.$route.params.id,
      config: {
        charts: [
          {
            chart: "",
            place_id: "position1",
            refresh_time: 0,
          },
          {
            chart: "",
            place_id: "position2",
            refresh_time: 0,
          },
          {
            chart: "",
            place_id: "position3",
            refresh_time: 0,
          },
          {
            chart: "",
            place_id: "position4",
            refresh_time: 0,
          },
        ],
        layout_name: "baselayout",
        name: "name",
      },
      chart_options: [],
    };
  },
  watch: {
    dataset: function(val) {
      for (var chart of val.charts) {
        chart.chart = chart.chart.$oid;
        console.log(chart);
        if (chart.place_id == "position1") {
          this.position1 = chart;
        }
        if (chart.place_id == "position2") {
          this.position2 = chart;
        }
        if (chart.place_id == "position3") {
          this.position3 = chart;
        }
        if (chart.place_id == "position4") {
          this.position4 = chart;
        }
      }
      this.config = val;
      var element = document.getElementById("topDiv");
      var top = element.offsetTop;
      window.scrollTo(0, top);
    },
  },
  methods: {
    edit_dashboard: function() {
      this.axios
        .patch("api/v1/my/dashboard/update/" + this.id, this.config)
        .then((response) => {
          console.log(response);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    create_dashboard: function() {
      this.axios
        .post("api/v1/dashboard/create", this.config)
        .then((response) => {
          console.log(response);
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  components: {
    chart: chart,
  },
  props: ["dataset"],
  mounted: function() {
    this.axios
      .get("api/v1/charts/my")
      .then((response) => {
        for (const chart of response.data) {
          const option = { value: chart._id.$oid, text: chart.name };
          this.chart_options.push(option);
        }
      })
      .catch((err) => {
        console.error(err);
      });
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
  margin: auto;
  height: 50vh;
  width: 50vw;
}
</style>
