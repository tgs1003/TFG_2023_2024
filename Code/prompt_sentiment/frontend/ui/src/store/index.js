import Vue from "vue";
import Vuex from "vuex";
import api from "../services/api";
import TokenService from "../services/token.service";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        status: "",
        token: TokenService.getLocalAccessToken(),
        user: {},
        dark: true
    },
    mutations: {
        auth_request(state) {
            state.status = "loading";
        },
        auth_success(state, token, user) {
            state.status = "success";
            state.token = token;
            state.user = user;
        },
        auth_error(state) {
            state.status = "error";
        },
        logout(state) {
            state.status = "";
            state.token = "";
        },
    },
    actions: {
        login({ commit }, user) {
            commit("auth_request");
            return api
                .post("/auth/login", user)
                .then((response) => {
                    if (response.data.access_token) {
                        TokenService.setUser(response.data);
                        commit("auth_success", response.data.access_token, user.email);
                    }
                    return response;
                })
                .catch((err) => {
                    TokenService.removeUser();
                    console.info(err);
                    return err;
                });
        },
        register({ commit }, user) {
            commit("auth_request");
            return api
                .post("/auth/register", user)
                .then((response) => {
                    if (response.code === 200)
                        this.$router.push("/")
                    return response;
                })
                .catch((err) => {
                    TokenService.removeUser();
                    console.info(err);
                    return err;
                });

        },
        logout({ commit }) {
            return new Promise((resolve) => {
                commit("logout");
                TokenService.removeUser();
                commit("auth_success", "", "");
                resolve();
            })
        },
    },
    getters: {
        isLoggedIn: (state) => !!state.token,
        authStatus: (state) => state.status,
    },
})
