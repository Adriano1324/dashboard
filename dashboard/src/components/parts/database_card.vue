<template>
  <div>
    <b-card
      :header="data.typ"
      header-tag="header"
      title="Title"
      class="database_card"
      v-if="!deleted"
    >
      <b-list-group>
        <b-list-group-item>DATABASE: {{ data.database }}</b-list-group-item>
        <b-list-group-item>USER: {{ data.user }}</b-list-group-item>
        <b-list-group-item>SERVER: {{ data.server }}</b-list-group-item>
        <b-list-group-item :variant="return_variant()"
          >STATUS: {{ data.status }}</b-list-group-item
        >
      </b-list-group>
      <b-button variant="danger" class="mt-3" @click="delete_database"
        >DELETE CONNECTION</b-button
      >
      <b-button class="mt-3 ml-1" @click="modal_show(data._id.$oid)"
        >Edit database</b-button
      >
    </b-card>

    <b-modal :id="data._id.$oid" hide-footer title="Edit">
      <div class="field">
        <label class="label">Typ</label>
        <b-form-input
          type="text"
          class="input"
          v-model="edit_db.typ"
        />
      </div>
      <div class="field">
        <label class="label">user</label>
        <b-form-input
          type="text"
          class="input"
          v-model="edit_db.user"
        />
      </div>
      <div class="field">
        <label class="label">password</label>
        <b-form-input
          type="text"
          class="input"
          v-model="edit_db.password"
        />
      </div>
      <div class="field">
        <label class="label">server</label>
        <b-form-input
          type="text"
          class="input"
          v-model="edit_db.server"
        />
      </div>
      <div class="field">
        <label class="label">database</label>
        <b-form-input
          type="text"
          class="input"
          v-model="edit_db.database"
        />
      </div>
      <b-button size="sm" class="m-2 button" @click="modal_hide(data._id.$oid)"
        >Cancel</b-button>
        <b-button size="sm" class="m-2 button" @click="update_database"
        >Update</b-button
      >
    </b-modal>
  </div>
</template>

<script>
export default {
  name: "database_card",
  data: function() {
    return {
      deleted: false,
      edit_db:{
        typ: this.data.typ,
        user:this.data.user,
        password:this.data.password,
        server:this.data.server,
        database:this.data.database
      }
    };
  },
  props: ["data"],
  methods: {
    delete_database: function() {
      this.axios
        .delete("api/v1/delete/database/" + this.data._id.$oid)
        .then(() => {
          this.deleted = true;
        });
    },
    return_variant: function() {
      if (this.data.status == "success") {
        return "success";
      } else {
        return "danger";
      }
    },
    update_database: function(){
      this.axios.patch('api/v1/update/database/'+ this.data._id.$oid, this.edit_db)
      .then(() => {
        this.modal_hide(this.data._id.$oid)
      })
      .catch(err => {
        console.error(err)
      })
      
    }
  },
};
</script>

<style>
.database_card {
  width: 400px;
  margin-top: 25px;
  margin: auto;
}
</style>
