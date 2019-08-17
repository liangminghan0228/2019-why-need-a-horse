/* eslint-disable no-extra-boolean-cast */
import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueRouter from 'vue-router'
import routers from './router/router'
import store from './vuex/store'
import echarts from 'echarts'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import * as Cookies from 'js-cookie'

axios.defaults.headers.post['Content-Type'] = 'application/x-www-fromurlencodeed'
Vue.use(VueRouter)
Vue.use(VueAxios, axios)
Vue.use(ElementUI)

const router = new VueRouter({
  mode: 'history',
  routes: routers
})
Vue.config.productionTip = false
Vue.prototype.$echarts = echarts

router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
    if (to.fullPath === '/') {
      if (Boolean(Cookies.get('student'))) {
        next({
          path: '/beforestudying',
          query: {redirect: to.fullPath}
        })
      } else {
        next({
          path: '/login',
          query: {redirect: to.fullPath}
        })
      }
    } else if (Boolean(Cookies.get('student')) || sessionStorage.getItem('student') !== null) {
      next()
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
      })
    }
  } else if (to.meta.needLogin) {
    if (to.fullPath === '/') {
      if (Boolean(Cookies.get('teacher'))) {
        next({
          path: '/teacherclasses',
          query: {redirect: to.fullPath}
        })
      } else {
        next({
          path: '/login',
          query: {redirect: to.fullPath}
        })
      }
    } else if (Boolean(Cookies.get('teacher')) || sessionStorage.getItem('teacher') !== null) {
      next()
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
      })
    }
  } else {
    next()
  }
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
