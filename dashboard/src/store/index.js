import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)


const types = {
  LOGIN: 'LOGIN',
  LOGOUT: 'LOGOUT',

}

const state = {
  logged: localStorage.getItem('token'),
}

const getters = {
  isLogged: state => state.logged,
}

const mutations = {
  [types.LOGIN](state) {
    state.logged = 1;
  },
  [types.LOGOUT](state) {
    state.logged = 0;
  },


}




const actions = {
  login({ commit }, data) {
    const p = new Promise(function (resolve, reject) {
      const formData = new FormData();
      console.log(data)
      formData.append('username', data.username);
      formData.append('password', data.password);
      return Vue.axios
        .post('api/v1/token', formData)
        .then((response) => {
          localStorage.setItem('token', response.data.access_token);
          localStorage.setItem('refresh_token', response.data.refresh_token);
          commit(types.LOGIN)
          resolve()
        })
        .catch(error => {
          reject(error)
        })
    })
    return p
  },
  logout({ commit }) {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')

    commit(types.LOGOUT)
  }
}
export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations

})
