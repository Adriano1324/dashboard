<template>
  <div>
    <b-container fluid>
      <b-row>
        <b-col cols="2">
          <div class="field">
            <label>Chart name</label>
            <b-form-input
              type="text"
              class="input"
              v-model="dataset.name"
            ></b-form-input>
          </div>
        </b-col>
        <b-col cols="8">
          <div class="chart-container">
            <canvas id="chart"></canvas>
          </div>
        </b-col>
        <b-col cols="2">
          <center>
            <label>Delete selecred chart</label>
            <b-button squared variant="danger" @click="delete_chart()">
              delete chart
            </b-button>
          </center>
        </b-col>
      </b-row>

      <b-form>
        <b-row>
          <b-col cols="5">
            <b-button-group>
              <b-button @click="watch_chart()">Watch chart</b-button>

              <b-button @click="update_chart()">Update selected chart</b-button>

              <b-button @click="create_chart()">Create new chart</b-button>

              <b-button @click="add_dataset()">Add dataset</b-button>
            </b-button-group>
          </b-col>
          <b-col cols="3">
            <div class="field">
              <b-form-select
                v-model="dataset.typ"
                :options="type_options"
              ></b-form-select>
            </div>
          </b-col>
          <b-col cols="4">
            <div class="field">
              <b-form-select
                v-model="id"
                :options="chart_options"
                @change="get_chart_data(id)"
              ></b-form-select>
            </div>
          </b-col>
        </b-row>
      </b-form>
      <div>
        <h4><p>data:</p></h4>

        <b-form>
          <b-row>
            <b-col cols="3">
              <div class="field">
                <label class="label">select database</label>
                <b-form-select
                  v-model="dataset.data.database"
                  :options="db_options"
                ></b-form-select></div
            ></b-col>
            <b-col cols="5">
              <div class="field">
                <label class="label">query</label>
                <b-form-textarea
                  class="input"
                  v-model="dataset.data.query"
                  placeholder="Enter something..."
                  rows="3"
                  max-rows="6"
                ></b-form-textarea>
              </div>
            </b-col>
            <b-col>
              <div class="field">
                <label class="label">label column name</label>
                <b-form-input
                  type="text"
                  class="input"
                  v-model="dataset.data.labels_column_name"
                ></b-form-input>
              </div>
            </b-col>
          </b-row>
        </b-form>

        <h5><p>datasets:</p></h5>
        <b-row>
          <b-col
            cols="2"
            v-for="(item, index) in dataset.data.datasets"
            :key="index"
            class="p-1"
            style="border: solid 2px"
          >
            <b-button-group>
              <b-button squared @click="modal_show('background_color' + index)"
                >background color</b-button
              >
              <b-button squared @click="modal_show('border_color' + index)"
                >border color</b-button
              ></b-button-group
            >
            <b-modal
              :id="'background_color' + index"
              hide-footer
              title="background color"
            >
              <div v-for="(it, ind) in item.background_color" :key="ind">
                <b-form inline
                  ><colorpicker
                    :color="it"
                    v-model="item.background_color[ind]"
                  />
                  <b-button @click="delete_background_color(index, ind)">
                    delete</b-button
                  ></b-form
                >
              </div>
            </b-modal>

            <b-modal
              :id="'border_color' + index"
              hide-footer
              title="Border color"
            >
              <div v-for="(it, ind) in item.border_color" :key="ind">
                <b-form inline
                  ><colorpicker :color="it" v-model="item.border_color[ind]" />
                  <b-button @click="delete_border_color(index, ind)"
                    >delete</b-button
                  ></b-form
                >
              </div>
            </b-modal>
            <div class="field">
              <label class="label">border width</label>
              <b-form-input
                type="number"
                class="input"
                v-model="item.border_width"
              />
            </div>
            <div class="field">
              <label class="label">column name</label>
              <b-form-input
                type="text"
                class="input"
                v-model="item.column_name"
              />
            </div>
            <div class="field">
              <label class="label">label</label>
              <b-form-input type="text" class="input" v-model="item.label" />
            </div>
            <b-button
              squared
              style="width: 100%"
              variant="danger"
              @click="delete_dataset(index)"
              >Delete this dataset</b-button
            >
          </b-col>
        </b-row>
      </div>
      <div>
        <h4><p>Options:</p></h4>
        <h5><p>Legend:</p></h5>
        <b-row>
          <b-col>
            <div class="field">
              <label class="label">legend align</label>
              <b-form-input
                type="text"
                class="input"
                v-model="dataset.options.legend.align"
              />
            </div>
          </b-col>

          <b-col>
            <div class="field">
              <label class="label">legend diaplay</label>
              <b-form-checkbox
                class="input"
                v-model="dataset.options.legend.display"
              />
            </div>
          </b-col>
          <b-col>
            <div class="field">
              <label class="label">position</label>
              <b-form-input
                type="text"
                class="input"
                v-model="dataset.options.legend.position"
              />
            </div>
          </b-col>
          <b-col>
            <div class="field">
              <label class="label">labels font color</label>
              <colorpicker v-model="dataset.options.legend.labels.fontColor" />
            </div>
            <div class="field">
              <label class="label">labels font size</label>
              <b-form-input
                type="number"
                class="input"
                v-model="dataset.options.legend.labels.fontSize"
              />
            </div>
          </b-col>
        </b-row>
        <h5><p>Title:</p></h5>
        <b-row>
          <b-col>
            <div class="field">
              <label class="label">title display</label>
              <b-form-checkbox
                type="text"
                class="input"
                v-model="dataset.options.title.display"
              />
            </div>
          </b-col>
          <b-col>
            <div class="field">
              <label class="label">title position</label>
              <b-form-input
                type="text"
                class="input"
                v-model="dataset.options.title.position"
              />
            </div>
          </b-col>

          <b-col>
            <div class="field">
              <label class="label">title text</label>
              <b-form-input
                type="text"
                class="input"
                v-model="dataset.options.title.text"
              />
            </div>
          </b-col>
        </b-row>
      </div>
    </b-container>
  </div>
</template>

<script>
import color_picker from "../components/parts/color_picker";
export default {
  name: "Chart_view",
  data: function () {
    return {
      color: "",
      id: this.$route.params.id,
      error: true,
      db_options: [{ value: "default", text: "please choose database" }],
      selected_chart: null,
      chart_options: [],
      type_options: [
        { value: "line", text: "Line chart" },
        { value: "bar", text: "Bar chart" },
        { value: "radar", text: "Radar chart" },
        { value: "pie", text: "Doghnut/pie chart" },
        { value: "polarArea", text: "Polar area chart" },
      ],
      dataset: {
        name: "string",
        typ: "string",
        data: {
          database: "default",
          query: "string",
          labels_column_name: "string",
          datasets: [
            {
              label: "string",
              column_name: "string",
              background_color: ["string"],
              border_color: ["string"],
              border_width: 0,
            },
          ],
        },
        options: {
          legend: {
            position: "string",
            align: "string",
            display: true,
            labels: {
              fontColor: "string",
              fontSize: 0,
            },
          },
          title: {
            display: true,
            position: "string",
            text: "string",
          },
        },
      },
      myChart: "",
      Chart: "",
    };
  },
  components: {
    colorpicker: color_picker,
  },
  methods: {
    get_chart_data: function (id) {
      if ((this.id != "new")) {
        this.axios
          .get("/api/v1/chart/my/" + id)
          .then((response) => {
            this.dataset = response.data[0];
            delete this.dataset._id;
            delete this.dataset.owner;
            this.dataset.data.database = this.dataset.data.database.$oid;
            this.error = false;
            this.watch_chart();
          })
          .catch((err) => {
            console.error(err);
            this.error = true;
          });
      }
    },
    watch_chart: function () {
      const p = new Promise((resolve, reject) => {
        this.axios
          .post("/api/v1/chart/watch", this.dataset)
          .then((response) => {
            if (this.myChart != "") {
              this.myChart.destroy();
            }

            this.myChart = new this.Chart("chart", response.data);
            this.myChart.canvas.parentNode.style.height = "40vh";
            this.myChart.canvas.parentNode.style.width = "40vw";
            this.myChart.render();

            resolve(response);
          })
          .catch((err) => {
            reject(err);
          });
      });
      return p;
    },
    create_chart: function () {
      this.axios
        .post("api/v1/chart/create", this.dataset)
        .then((response) => {
          console.log(response);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    update_chart: function () {
      this.axios
        .patch("api/v1/chart/update/" + this.id, this.dataset)
        .then((response) => {
          console.log(response);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    delete_chart: function () {
      this.axios
        .delete("api/v1/chart/delete/" + this.id, this.dataset)
        .then((response) => {
          console.log(response);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    delete_background_color: function (dataset, index) {
      delete this.dataset.data.datasets[dataset].background_color.splice(
        index,
        1
      );
      this.modal_hide("background_color" + dataset);
      this.modal_show("background_color" + dataset);
    },
    delete_border_color: function (dataset, index) {
      delete this.dataset.data.datasets[dataset].border_color.splice(index, 1);
      this.modal_hide("border_color" + dataset);
      this.modal_show("border_color" + dataset);
    },
    add_dataset: function () {
      const dataset = {
        border_width: 1,
        column_name: "column name",
        label: "label",
        background_color: ["rgb(1,1,1,1)"],
        border_color: ["rgb(1,1,1,1)"],
      };
      this.dataset.data.datasets.push(dataset);
    },
    delete_dataset: function (index) {
      this.dataset.data.datasets.splice(index, 1);
    },
  },
  mounted: function () {
    this.axios
      .get("api/v1/my/databases")
      .then((response) => {
        for (const db of response.data) {
          const option = {
            value: db._id.$oid,
            text: db.typ + " " + db.server + " " + db.database,
          };
          this.db_options.push(option);
        }
      })
      .catch((err) => {
        console.error(err);
      });

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

    if (this.id != "create") {
      this.get_chart_data(this.id);
    }
    const Chart = require("chart.js");
    this.Chart = Chart;
  },
};
</script>

<style>
.chart-container {
  position: relative;
  margin: auto;
  height: 40vh;
  width: 40vw;
}

.current-color {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: #000;
  cursor: pointer;
}
</style>
