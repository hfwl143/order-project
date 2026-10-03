// 当前登录用户的联系方式资料（轻量全局状态，供导航/发布/接单各处共享）
import { computed, reactive } from 'vue'
import { getMyProfile, updateMyProfile } from '../api/task'

export const PHONE_PATTERN = /^1[3-9]\d{9}$/
// 微信号：字母开头，6-20 位字母/数字/下划线/减号
export const WECHAT_PATTERN = /^[a-zA-Z][-_a-zA-Z0-9]{5,19}$/

export const profileState = reactive({
  username: '',
  wechat: '',
  phone: '',
  loaded: false,
  dialogVisible: false,
})

export const hasContact = computed(() => Boolean(profileState.wechat || profileState.phone))

export function openProfileDialog() {
  profileState.dialogVisible = true
}

/**
 * 拉取当前用户资料；已拉取过默认复用缓存
 * @param {boolean} force - 是否强制刷新
 */
export async function fetchProfile(force = false) {
  if (!localStorage.getItem('token')) return
  if (profileState.loaded && !force) return
  try {
    const { data } = await getMyProfile()
    profileState.username = data.username || ''
    profileState.wechat = data.wechat || ''
    profileState.phone = data.phone || ''
    profileState.loaded = true
  } catch {
    profileState.loaded = false
  }
}

/**
 * 保存联系方式
 * @param {{wechat?: string, phone?: string}} payload
 */
export async function saveProfile(payload) {
  const { data } = await updateMyProfile(payload)
  profileState.username = data.username || ''
  profileState.wechat = data.wechat || ''
  profileState.phone = data.phone || ''
  profileState.loaded = true
  return data
}
