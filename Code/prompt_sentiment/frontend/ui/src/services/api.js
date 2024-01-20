import axios from "axios";

const instance = axios.create( {
    baseURL: process.env.VUE_APP_API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

export default instance;