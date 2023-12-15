import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from "../views/Auth/Login";
import Registro from "../views/Auth/Registro";
import Inicio from "../views/Inicio"
import AdminHome from "../views/Admin/AdminHome";
import Sentiment from "../views/Sentiment/Sentiment";
import store from '@/store'
import api from '../services/api'
Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin-home',
    name: 'AdminHome',
    component: AdminHome,
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/registro',
    name: 'Registro',
    component: Registro
  },
  {
    path: '/',
    name: 'Inicio',
    component: Inicio,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/sentiment',
    name: 'Sentiment',
    component: Sentiment,
    meta: {
      requiresAuth: true
    }
  }
  
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.state.token || localStorage.getItem('user') === 'null') {
      next({
        path: '/login',
        params: { redirect: to.fullPath },
      })
    } else {
      if (to.matched.some(record => record.meta.requiresAdmin)) {    
        api.get('/auth/status').then((resp)=>
        {
          var user = resp.data
          if (user.rol != 'Admin')
          {
            next({
              path: '/',
              params: { redirect: to.fullPath },
            })
          }
          else {
            next()
            }
        }
        )
      }
      else {
        next()
      }
}}
else{
  next()
}
})

export default router
