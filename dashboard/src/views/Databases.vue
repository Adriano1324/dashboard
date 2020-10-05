<template>
  <div>
    <div>
      <b-list-group horizontal>
        <b-list-group-item>succes: {{ succes }}</b-list-group-item>
        <b-list-group-item>invalid credentials: {{ credentials }}</b-list-group-item>
        <b-list-group-item>invalid connections: {{ adress }}</b-list-group-item>
        <b-list-group-item>
          <b-button @click="modal_show('new_database_modal')" variant='light'>Add new database connection</b-button>
        </b-list-group-item>
      </b-list-group>
    </div>

    <b-modal id="new_database_modal" hide-footer title="Register form">
      <form>
        <div class="field">
          <label class="label">typ</label>
          <b-form-select v-model="data.typ" :options="options"></b-form-select>
        </div>
        <div class="field">
          <label class="label">user</label>
          <b-form-input type="text" v-model="data.user" class="input" />
        </div>
        <div class="field">
          <label class="label">password</label>
          <b-form-input type="password" v-model="data.password" class="password" />
        </div>
        <div class="field">
          <label class="label">server</label>
          <b-form-input type="text" class="input" v-model="data.server" />
        </div>
        <div class="field">
          <label class="label">database</label>
          <b-form-input type="text" class="input" v-model="data.database" />
        </div>
      </form>

      <b-button class="m-2 button is-success" @click="add_connection">add connection</b-button>
      <b-button class="m-2 button" @click="modal_hide('new_database_modal')">Cancel</b-button>
    </b-modal>
    <b-row>
      <b-col cols=10 offset=1>
        <b-card-group  class="justify-content-center">
          <databasecard v-for="database of databases" :data="database" :key="database._id.id"></databasecard>
        </b-card-group>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import database_card from "../components/parts/database_card";
export default {
  name: "Databases",
  data: function() {
    return {
      options: [
        { value: "postgres", text: "postgres sql database" },
        { value: "mysql", text: "mysql database" }
      ],
      data: {
        typ: "",
        user: "",
        password: "",
        server: "",
        database: ""
      },
      databases: "",
      succes: 0,
      credentials: 0,
      adress: 0
    };
  },
  components: {
    databasecard: database_card
  },
  mounted: function() {
    this.get_databases();
  },
  methods: {
    add_connection: function() {
      this.axios
        .post("/api/v1/add/database", this.data)
        .then(response => {
          console.log(response.data);
          this.modal_hide("new_database_modal");
          this.succes = 0
          this.credentials = 0
          this.adress = 0
          this.get_databases()
        })
        .catch(err => {
          console.log(err);
        });
    },
    get_databases: function() {
      this.axios.get("api/v1/my/databases").then(response => {
        this.databases = response.data;
        for (const ob of response.data) {
          if (ob.status == "success") {
            this.succes += 1;
          }
          if (ob.status == "wrong credentials") {
            this.credentials += 1;
          }
          if (ob.status == "wrong server address") {
            this.adress += 1;
          }
        }
      });
    }
  }
};
</script>

<style>
</style>