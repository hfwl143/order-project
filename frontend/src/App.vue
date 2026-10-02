<template>
  <div class="app-shell">
    <header v-if="route.path !== '/login'" class="app-header">
      <router-link class="brand-lockup" to="/">
        <span class="brand-symbol">接</span>
        <span>接单集</span>
      </router-link>
      <nav class="primary-nav" aria-label="主导航">
        <router-link to="/">订单大厅</router-link>
        <router-link to="/mine">我的订单</router-link>
      </nav>
      <button class="account-action" @click="logout">退出登录 <span aria-hidden="true">↗</span></button>
    </header>

    <router-view />

    <div v-if="loadingCount > 0" class="global-loading" aria-label="正在加载" />
    <transition name="fade">
      <div v-if="toastMsg" class="global-toast" :class="toastType" role="status">
        {{ toastMsg }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { toastMsg, toastType, loadingCount } from './toast'

const route = useRoute()
const router = useRouter()

function logout() {
  localStorage.removeItem('token')
  router.replace('/login')
}
</script>

<style>
.global-toast {
  position: fixed;
  top: 24px;
  left: 50%;
  z-index: 1000;
  max-width: calc(100vw - 32px);
  padding: 12px 18px;
  transform: translateX(-50%);
  border: 1px solid var(--line);
  border-radius: 6px;
  background: #fff;
  box-shadow: 0 12px 32px rgba(23, 35, 33, 0.12);
  font-size: 14px;
}
.global-toast.error { color: #a33f32; border-color: #efc8c0; }
.global-toast.success { color: #155c4a; border-color: #b8d6c8; }
.global-loading {
  position: fixed;
  z-index: 999;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--brand);
  transform-origin: left;
  animation: loading-sweep 1.2s ease-in-out infinite;
}
@keyframes loading-sweep {
  0% { transform: scaleX(0.08); }
  50% { transform: scaleX(0.72); }
  100% { transform: scaleX(1); }
}
.fade-enter-active, .fade-leave-active { transition: opacity .3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
