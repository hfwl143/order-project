<template>
  <main class="login-page">
    <section class="login-intro">
      <router-link to="/login" class="brand-lockup">
        <span class="brand-symbol">接</span>
        <span>接单集</span>
      </router-link>
      <div class="intro-copy">
        <p class="eyebrow">SKILLS MEET OPPORTUNITY</p>
        <h1>让每一份<br />本事都有回响。</h1>
        <p>发布需求，找到合适的合作伙伴；展示技能，把机会接到手里。</p>
        <div class="intro-badges">
          <span v-for="tag in tags" :key="tag">
            <TagIcon :tag="tag" />
            {{ tag === 'PS设计' ? 'PS 设计' : tag }}
          </span>
        </div>
      </div>
      <div class="intro-foot"><span>01</span><span>发布 · 协作 · 完成</span></div>
    </section>

    <section class="login-form-side">
      <div class="login-form-wrap">
        <p class="eyebrow">{{ isRegister ? 'CREATE ACCOUNT' : 'WELCOME BACK' }}</p>
        <h2>{{ isRegister ? '创建账号' : '欢迎回来' }}</h2>
        <p class="form-lede">{{ isRegister ? '注册后即可发布需求或接取订单。' : '登录后继续浏览订单与管理合作。' }}</p>

        <el-form label-position="top" @submit.prevent="submit">
          <el-form-item label="用户名">
            <el-input
              v-model="username"
              autocomplete="username"
              placeholder="输入用户名"
              maxlength="50"
              size="large"
            >
              <template #prefix>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input
              v-model="password"
              type="password"
              :autocomplete="isRegister ? 'new-password' : 'current-password'"
              placeholder="至少 6 位"
              show-password
              size="large"
              @keyup.enter="submit"
            >
              <template #prefix>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <rect x="3" y="11" width="18" height="11" rx="2" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
              </template>
            </el-input>
          </el-form-item>
          <el-button class="login-submit" type="primary" :loading="submitting" @click="submit">
            {{ isRegister ? '注册并登录' : '登 录' }}
          </el-button>
        </el-form>

        <p class="login-switch">
          {{ isRegister ? '已经有账号？' : '还没有账号？' }}
          <button type="button" @click="toggleMode">{{ isRegister ? '返回登录' : '立即注册' }}</button>
        </p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { login, register } from '../api/task'
import { showToast } from '../toast'
import TagIcon from '../components/TagIcon.vue'

const tags = ['编程', 'PS设计', '绘图', '文案']
const router = useRouter()
const route = useRoute()
const isRegister = ref(false)
const submitting = ref(false)
const username = ref('')
const password = ref('')

function toggleMode() {
  isRegister.value = !isRegister.value
}

async function submit() {
  const account = username.value.trim()
  if (!account || !password.value) {
    showToast('请填写用户名和密码')
    return
  }
  if (isRegister.value && password.value.length < 6) {
    showToast('密码至少需要 6 位')
    return
  }

  submitting.value = true
  try {
    const response = isRegister.value
      ? await register({ username: account, password: password.value })
      : await login(account, password.value)
    localStorage.setItem('token', response.data.access_token)
    const destination = typeof route.query.redirect === 'string' && route.query.redirect.startsWith('/')
      ? route.query.redirect
      : '/'
    await router.replace(destination)
  } catch {
  } finally {
    submitting.value = false
  }
}
</script>
