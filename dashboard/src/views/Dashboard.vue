<template>
  <div>
    <div :is="current_layout" :dataset="dashboard"></div>
  </div>
</template>

<script>
import base_layout from "../components/layouts/base_dashboard";
import test_layout from "../components/layouts/test_layout";
export default {
  name: "Dashboard",
  components: {
    baselayout: base_layout,
    testlayout: test_layout,
  },
  data: function () {
    return {
      dashboard_id: this.$route.params.id,
      dashboard: "",
      current_layout: "baselayout",
    };
  },
  mounted: function () {
    if (this.dashboard_id != "new") {
      this.axios
        .get("api/v1/my/dashboard/" + this.dashboard_id)
        .then((response) => {
          this.dashboard = response.data[0];
          this.current_layout = response.data[0].layout_name;
        })
        .catch((err) => {
          console.log(err);
        });
    }
    
  },
};
</script>

<style></style>
