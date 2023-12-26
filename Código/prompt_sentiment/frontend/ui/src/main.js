import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from '@/plugins/vuetify' // path to vuetify export
import Vuex from 'vuex'
import setupInterceptors from './services/setupInterceptors'
import Vuelidate from 'vuelidate'
Vue.use(Vuelidate)

Vue.config.productionTip = false
Vue.use(Vuex)
setupInterceptors(store);


new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
