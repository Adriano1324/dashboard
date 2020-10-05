<template>
  <div>
    <b-button href="/dashboard/edit/new">Create dashboard</b-button>

    <b-card-group>
      <dashboardcard
        v-for="dash of dashboards"
        :data="dash"
        :key="dash._id.$oid"
      />
    </b-card-group>
  </div>
</template>

<script>
import dashboard_card from "../components/parts/dashboard_card";
export default {
  name: "Dashboards",
  components: {
    dashboardcard: dashboard_card,
  },
  data: function () {
    return {
      dashboards: "",
    };
  },
  mounted: function () {
    this.axios
      .get("api/v1/my/dashboards")
      .then((response) => {
        this.dashboards = response.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

<style>
</style>