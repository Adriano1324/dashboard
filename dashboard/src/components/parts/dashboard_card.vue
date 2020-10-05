<template>
  <div>
      <b-card
      :header="data.name"
      header-tag="header"
      class="database_card"
    >
      <b-list-group>
          {{ data.layout_name }}
          <b-list-group-item :href="'/dashboard/watch/'+data._id.$oid">Watch dashboard</b-list-group-item>
          <b-list-group-item :href="'/dashboard/edit/'+data._id.$oid">Edit dashboard</b-list-group-item>
      </b-list-group>
    </b-card>
  </div>
</template>

<script>
export default {
    name:'dashboard_card',
    props:['data']
}
</script>

<style>

</style>