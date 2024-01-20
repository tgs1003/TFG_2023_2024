import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "@/plugins/vuetify";
import Vuex from "vuex";
import setupInterceptors from "./services/setupInterceptors";
import Vuelidate from "vuelidate";
import i18n from "./i18n";

Vue.use(Vuelidate);
Vue.config.productionTip = false;
Vue.use(Vuex);
setupInterceptors(store);

new Vue({
  i18n,
  vuetify,
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
