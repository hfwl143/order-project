<template>
  <div class="auth">
    <div class="card">
      <h2>{{ isRegister ? '注册' : '登录' }}</h2>
      <input v-model="username" placeholder="用户名" />
      <input v-model="password" type="password" placeholder="密码" @keyup.enter="submit" />
      <button @click="submit">{{ isRegister ? '注册并登录' : '登录' }}</button>
      <p class="switch" @click="isRegister = !isRegister">
        {{ isRegister ? '已有账号？去登录' : '没有账号？去注册' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register, login } from '../api/task'
import { showToast } from '../toast'

const router = useRouter()
const isRegister = ref(false)
const username = ref(''); const password = ref('')

async function submit() {
  if (!username.value || !password.value) return showToast('请填写完整')
  try {
    const fn = isRegister.value
      ? () => register({ username: username.value, password: password.value })
      : () => login(username.value, password.value)
    const res = await fn()
    localStorage.setItem('token', res.data.access_token)
    router.push('/tasks')
  } catch (e) {
    showToast(e.friendlyMessage || '操作失败')
  }
}
</script>
