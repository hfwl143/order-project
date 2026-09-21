// api/task.js
import axios from 'axios'

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',  // 按你的实际地址
    timeout: 10000,
})

// 请求拦截器
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
})

// 响应拦截器的错误分支里加：
if (api.response?.status === 401) {
    localStorage.removeItem('token')
    window.location.href = '/login'   // token 过期，踢回登录页
}


// 响应拦截器：统一错误处理
api.interceptors.response.use(
    res => res,           // 成功直接放行
    err => {
        // 提取后端返回的错误信息
        let msg = '网络错误，请稍后重试'
        if (err.response) {
            msg = err.response.data?.detail || `请求失败（${err.response.status}）`
        } else if (err.code === 'ECONNABORTED') {
            msg = '请求超时'
        }
        err.friendlyMessage = msg   // 挂上可读信息，抛给调用方
        return Promise.reject(err)
    }
)

export const getTasks = (completed) => api.get('/tasks', { params: { completed } })
export const createTask = (data) => api.post('/tasks', data)
export const updateTask = (id, data) => api.put(`/tasks/${id}`, data)
export const deleteTask = (id) => api.delete(`/tasks/${id}`)

export const register = (data) => api.post('/register', data)
export const login = (username, password) => {
    const form = new URLSearchParams({ username, password })
    return api.post('/login', form)   // OAuth2 表单格式
}
