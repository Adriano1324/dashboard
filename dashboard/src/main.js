import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { axios } from './axios'
import VueAxios from 'vue-axios'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(VueAxios, axios)

require("./assets/main.scss")

Vue.config.productionTip = false

Vue.mixin({
  methods:{
    modal_hide: function(id){
      this.$bvModal.hide(id);
    },
    modal_show: function(id){
      this.$bvModal.show(id);
    }
  }
}
)


new Vue({

  router,
  store,
  render: h => h(App)
}).$mount('#app')
