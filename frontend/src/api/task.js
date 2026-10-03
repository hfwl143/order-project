import axios from 'axios'
import { hideLoading, showLoading, showToast } from '../toast'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
    timeout: 10000,
})

api.interceptors.request.use(config => {
    showLoading()
    const token = localStorage.getItem('token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
})

api.interceptors.response.use(
    response => {
        hideLoading()
        return response
    },
    error => {
        hideLoading()
        const status = error.response?.status
        const detail = error.response?.data?.detail
        const message = Array.isArray(detail)
            ? '请求参数不正确，请检查后重试'
            : detail || (error.code === 'ECONNABORTED'
                ? '请求超时，请稍后重试'
                : status
                    ? `请求失败（${status}）`
                    : '无法连接服务器，请检查后端是否启动')

        error.friendlyMessage = message

        const hasToken = Boolean(localStorage.getItem('token'))
        const isLoginRequest = error.config?.url?.endsWith('/login')
        if (status === 401 && hasToken && !isLoginRequest) {
            localStorage.removeItem('token')
            const next = `${window.location.pathname}${window.location.search}`
            window.location.assign(`/login?redirect=${encodeURIComponent(next)}`)
        }

        showToast(message)
        return Promise.reject(error)
    }
)

export const getOrders = (tag) => api.get('/orders', { params: tag ? { tag } : {} })
export const getMyOrders = (role = 'published') => api.get('/orders/mine', { params: { role } })
export const createOrder = (data) => api.post('/orders', data)
export const updateOrder = (id, data) => api.put(`/orders/${id}`, data)
export const takeOrder = (id) => api.post(`/orders/${id}/take`)
export const requestAbandon = (id) => api.post(`/orders/${id}/abandon`)
export const decideAbandon = (id, decision) => api.post(`/orders/${id}/abandon/${decision}`)
export const closeOrder = (id) => api.post(`/orders/${id}/close`)

export const register = (data) => api.post('/register', data)
export const login = (username, password) => {
    const form = new URLSearchParams({ username, password })
    return api.post('/login', form)
}

export const getMyProfile = () => api.get('/users/me')
export const updateMyProfile = (data) => api.patch('/users/me', data)
