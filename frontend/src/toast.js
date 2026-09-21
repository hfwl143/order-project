// src/toast.js
import { ref } from 'vue'

export const toastMsg = ref('')
export const toastType = ref('error')   // 'error' | 'success'
export const loadingCount = ref(0)      // 计数器，支持并发请求
const toastTimer = ref(null)

export function showToast(msg, type = 'error', duration = 2500) {
    toastMsg.value = msg
    toastType.value = type
    clearTimeout(toastTimer.value)
    toastTimer.value = setTimeout(() => { toastMsg.value = '' }, duration)
}

export function showLoading() { loadingCount.value++ }
export function hideLoading() { if (loadingCount.value > 0) loadingCount.value-- }
