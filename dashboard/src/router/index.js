import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Profile from '../views/Profile.vue'
import Dashboard from '../views/Dashboard.vue'
import Dashboards from '../views/Dashboards.vue'
import Databases from '../views/Databases.vue'
import Charts from '../views/Charts.vue'
import Chart_view from '../views/Chart_view.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/my-profile',
    name: 'my profile',
    component: Profile
  },
  {
    path: '/dashboards',
    name: 'dashboars view',
    component: Dashboards
  },
  {
    path: '/dashboard/:mode/:id',
    name: 'dashboar view',
    component: Dashboard
  },
  {
    path: '/databases',
    name: 'databases view',
    component: Databases
  },
  {
    path:'/charts',
    name:'charts view',
    component: Charts
  },
  {
    path: '/chart/:id',
    name: 'view chart',
    component: Chart_view
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
