import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Auth/Login";
import Registro from "../views/Auth/Registro";
import Inicio from "../views/Inicio";
import AdminHome from "../views/Admin/AdminHome";
import History from "../views/Sentiment/History";
import Analysis from "../views/Sentiment/Analysis";
import Details from "../views/Sentiment/Details";
import About from "../views/About";
import store from "@/store";
import api from "../services/api";

Vue.use(VueRouter);

const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/details",
    name: "Details",
    component: Details,
    meta: {
      requiresAuth: true,
    },
    props: true,
  },
  {
    path: "/admin-home",
    name: "AdminHome",
    component: AdminHome,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    path: "/history",
    name: "History",
    component: History,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/analysis",
    name: "Analysis",
    component: Analysis,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/registro",
    name: "Registro",
    component: Registro,
  },
  {
    path: "/",
    name: "Inicio",
    component: Inicio,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/about",
    name: "About",
    component: About,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/http*",
    beforeEnter: (to) => {
      window.open(to.fullPath.substring(1), "_blank");
    },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});
router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!store.state.token || localStorage.getItem("user") === "null") {
      next({
        path: "/login",
        params: { redirect: to.fullPath },
      });
    } else {
      if (to.matched.some((record) => record.meta.requiresAdmin)) {
        api.get("/auth/status").then((resp) => {
          var user = resp.data;
          if (user.rol != "Admin") {
            next({
              path: "/",
              params: { redirect: to.fullPath },
            });
          }
          else {
            next();
          }
        });
      }
      else {
        next();
      }
    }
  } else {
    next();
  }
});
export default router;
