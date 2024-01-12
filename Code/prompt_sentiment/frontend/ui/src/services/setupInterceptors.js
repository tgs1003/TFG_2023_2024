import axiosInstance from "./api"
import TokenService from "./token.service"

const setup = ({commit}) =>{
    axiosInstance.interceptors.request.use(
        (config) => {
            const token = TokenService.getLocalAccessToken();
            if(token){
                config.headers['Authorization']= token;
            }
            return config
        },
        (error) =>{
            return Promise.reject(error);
        }
    );
    axiosInstance.interceptors.response.use(
        (res)=>{
            return res;
        },
        async (err) =>{
            const originalConfig = err.config;

            if(originalConfig.url !== "/auth/login" && err.response){
                if(err.response.status === 401 && !originalConfig._retry){
                    originalConfig.retry = true;
                    try{
                        const rs = await axiosInstance.post("/auth/refresh",{
                            refresh_token : TokenService.getLocalRefreshToken(),
                        });
                        
                        TokenService.setUser(rs.data)
                        return axiosInstance(originalConfig);
                    } catch(_error){
                        commit('logout')
                        TokenService.removeUser();
                        commit('auth_success', '', '')
                        
                        return Promise.reject(err);
                    }
                }
            }
            return Promise.reject(err);
        }
    );
}

export default setup;