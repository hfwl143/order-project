<template>
  <div class="app-shell">
    <header v-if="route.path !== '/login'" class="app-header">
      <router-link class="brand-lockup" to="/">
        <span class="brand-symbol">接</span>
        <span>接单集</span>
      </router-link>
      <nav class="primary-nav" aria-label="主导航">
        <router-link to="/">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="10" />
            <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" />
          </svg>
          订单大厅
        </router-link>
        <router-link to="/mine">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M8 6h13" />
            <path d="M8 12h13" />
            <path d="M8 18h13" />
            <path d="M3 6h.01" />
            <path d="M3 12h.01" />
            <path d="M3 18h.01" />
          </svg>
          我的订单
        </router-link>
      </nav>
      <div class="account-group">
        <button class="profile-action" @click="openProfileDialog">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          <span class="profile-name">{{ profileState.username || '我的资料' }}</span>
          <span v-if="!hasContact" class="profile-dot" title="还未填写联系方式"></span>
        </button>
        <button class="account-action" @click="logout">
          退出登录
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
        </button>
      </div>
    </header>

    <router-view />

    <ProfileDialog />

    <div v-if="loadingCount > 0" class="global-loading" aria-label="正在加载" />
    <transition name="toast-pop">
      <div v-if="toastMsg" class="global-toast" :class="toastType" role="status">
        <svg v-if="toastType === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
          <polyline points="22 4 12 14.01 9 11.01" />
        </svg>
        <svg v-else-if="toastType === 'info'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="16" x2="12" y2="12" />
          <line x1="12" y1="8" x2="12.01" y2="8" />
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="10" />
          <line x1="15" y1="9" x2="9" y2="15" />
          <line x1="9" y1="9" x2="15" y2="15" />
        </svg>
        {{ toastMsg }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { toastMsg, toastType, loadingCount } from './toast'
import ProfileDialog from './components/ProfileDialog.vue'
import { fetchProfile, hasContact, openProfileDialog, profileState } from './utils/profile'

const route = useRoute()
const router = useRouter()

// 已登录进入应用时加载联系方式（刷新页面后同样生效）
watch(
  () => route.path,
  (path) => {
    if (path !== '/login') fetchProfile()
  },
  { immediate: true },
)

function logout() {
  localStorage.removeItem('token')
  profileState.loaded = false
  profileState.username = ''
  profileState.wechat = ''
  profileState.phone = ''
  router.replace('/login')
}
</script>
