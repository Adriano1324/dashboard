import axios from 'axios'
import router from './router/index'
import store from './store';
axios.defaults.baseURL = 'http://127.0.0.1:8000/'

axios.defaults.headers.post['accept'] = 'application/json';


axios.interceptors.request.use(req => {
    if (localStorage.getItem('token')) {
        req.headers['Authorization'] = 'Bearer ' + localStorage.getItem('token')
        return req
    }
    else {
        return req
    }
}, error => {
    return Promise.reject(error);
}
);


let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    })

    failedQueue = [];
}

axios.interceptors.response.use(function (response) {
    return response;
}, function (error) {

    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
        if(error.response.config.url == "api/v1/token/refresh"){
            store.dispatch('logout')
            processQueue(error, null);
            router.push('/')
        }

        if (isRefreshing) {

            return new Promise(function (resolve, reject) {
                failedQueue.push({ resolve, reject })
            }).then(token => {
                originalRequest.headers['Authorization'] = 'Bearer ' + token;
                return axios(originalRequest);
            }).catch(err => {
                return Promise.reject(err);
            })
        }

        originalRequest._retry = true;
        isRefreshing = true;
        const refreshToken = localStorage.getItem('refresh_token');
        return new Promise(function (resolve, reject) {
            axios.post('api/v1/token/refresh', {}, {
                headers: {
                    'refresh-token': refreshToken
                }
            })
                .then( response => {
                    localStorage.setItem('token', response.data.access_token);
                    localStorage.setItem('refresh_token', response.data.refresh_token);
                    originalRequest.headers['Authorization'] = 'Bearer ' + response.data.access_token;
                    processQueue(null, response.data.access_token);
                    resolve(axios(originalRequest));
                })
                .catch(err => {
                    store.dispatch('logout')
                    processQueue(err, null);
                    reject(err);
                    router.push('/')
                })
                .finally(() => { isRefreshing = false })
        })
    }

    return Promise.reject(error);
});

export { axios }