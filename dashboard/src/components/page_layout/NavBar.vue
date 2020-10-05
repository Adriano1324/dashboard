<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark" style="min-height:64px">
      <router-link to="/">
        <b-navbar-brand>Dashboard</b-navbar-brand>
      </router-link>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav v-if="isLogged" class="mr-auto">
          <b-nav-item href="/databases">Databases</b-nav-item>
          <b-nav-item href="/charts">Charts</b-nav-item>
          <b-nav-item href="/dashboards">Dashboards</b-nav-item>
        </b-navbar-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav v-if="!isLogged" class="ml-auto">
          <b-button class="m-1" @click="modal_show('register_modal')">register</b-button>
          <b-button class="m-1" @click="modal_show('login_modal')" >login</b-button>
        </b-navbar-nav>

        <b-navbar-nav v-else class="ml-auto">
          <router-link to="/my-profile">
            <b-avatar class="m-1" :src="user.photo_url"></b-avatar>
          </router-link>
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>{{user.username}}</template>
            <b-dropdown-item href="#">Profile</b-dropdown-item>
            <b-dropdown-item href="/" @click="logout">Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <b-modal id="login_modal" hide-footer title="Login">
      <form>
        <div class="field">
          <label class="label">username</label>
          <b-form-input
            type="text"
            class="input"
            v-bind:class="{'is-danger': login_error }"
            v-model="data.username"
          />
        </div>
        <div class="field">
          <label class="label">password</label>
          <b-form-input
            type="password"
            class="input"
            v-bind:class="{'is-danger': login_error }"
            v-model="data.password"
          />
        </div>
      </form>
      <b-button size="sm" class="m-2 button is-success" @click="login">Login</b-button>
      <b-button size="sm" class="m-2 button" @click="modal_hide('login_modal')">Cancel</b-button>
    </b-modal>

    <b-modal id="register_modal" hide-footer title="Register form">
      <form>
        <div class="field">
          <label class="label">username</label>
          <b-form-input
            type="text"
            class="input"
            v-bind:class="{'is-danger': login_error }"
            v-model="register.username"
          />
        </div>
        <div class="field">
          <label class="label">password</label>
          <b-form-input
            type="password"
            class="input"
            v-bind:class="{'is-danger': login_error }"
            v-model="register.password"
          />
        </div>
        <div class="field">
          <label class="label">e-mail</label>
          <b-form-input
            type="text"
            class="input"
            v-bind:class="{'is-danger': login_error }"
            v-model="register.email"
          />
        </div>
        <div class="field">
          <label class="label">full name</label>
          <b-form-input
            type="text"
            class="input"
            v-bind:class="{'is-danger': login_error }"
            v-model="register.full_name"
          />
        </div>
        <div class="field">
          <label class="checkbox label">public</label>
          <b-form-checkbox
            type="checkbox"
            class="checkbox"
            v-bind:class="{'is-danger': login_error }"
            v-model="register.public"
          />
        </div>
      </form>

      <b-button class="m-2 button is-success" @click="register_account">register</b-button>
      <b-button class="m-2 button" @click="modal_hide('register_modal')">Cancel</b-button>
    </b-modal>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "navbar",
  data: function() {
    return {
      data: {
        username: "Adrian",
        password: "qwerty"
      },
      register: {
        username: "",
        email: "",
        full_name: "",
        password: "",
        public: false
      },
      login_error: false,
      menuIsActive: false,
      user: ""
    };
  },
  computed: mapGetters(["isLogged"]),
  mounted: function() {
    this.get_user();
  },
  methods: {
    login: function() {
      this.$store
        .dispatch("login", this.data)
        .then(() => {
          this.$bvModal.hide("login_modal");
          this.$bvModal.hide("register_modal");
          this.get_user();
        })
        .catch(err => {
          console.error(err);
          this.login_error = true;
        });
    },
    logout: function() {
      this.$store.dispatch("logout");
    },
    register_account: function() {
      this.axios
        .post("/api/v1/user/create", this.register)
        .then(response => {
          console.log(response);
        })
        .catch(err => {
          console.log(err);
        });
    },
    get_user: function() {
      if (localStorage.getItem("token") != null) {
        this.axios.get("/api/v1/user/me").then(response => {
          this.user = response.data;
        });
      }
    }
  }
};
</script>
<style>
</style>