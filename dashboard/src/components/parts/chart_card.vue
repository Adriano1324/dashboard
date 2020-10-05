<template>
  <div>
    <b-card
      :header="data.name"
      header-tag="header"
      class="database_card"
    >
      <b-list-group>
          <b-list-group-item :href="'/chart/'+data._id.$oid">Watch chart</b-list-group-item>
      </b-list-group>

    </b-card>
  </div>
</template>

<script>
export default {
  name: "chart_card",
  props: ["data"],
};
</script>

<style></style>
