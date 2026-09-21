<template>
  <!-- 你的路由出口 -->
  <router-view />

  <!-- 全局 loading -->
  <div v-if="loadingCount > 0" class="global-loading">加载中…</div>

  <!-- 全局 toast -->
  <transition name="fade">
    <div v-if="toastMsg" class="global-toast" :class="toastType">
      {{ toastMsg }}
    </div>
  </transition>
</template>

<script setup>
import { toastMsg, toastType, loadingCount } from './toast'
</script>

<style>
.global-loading {
  position: fixed; top: 0; left: 0; right: 0;
  background: #409eff; color: #fff;
  text-align: center; padding: 4px; font-size: 13px; z-index: 999;
}
.global-toast {
  position: fixed; top: 60px; left: 50%; transform: translateX(-50%);
  padding: 10px 20px; border-radius: 6px; z-index: 1000;
  font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,.15);
}
.global-toast.error   { background: #fef0f0; color: #c00; border: 1px solid #fbc4c4; }
.global-toast.success { background: #f0f9eb; color: #67c23a; border: 1px solid #b3e19d; }
.fade-enter-active, .fade-leave-active { transition: opacity .3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
