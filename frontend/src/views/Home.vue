<template>
  <div>
    <h1>首页</h1>
    <button @click="checkHealth">测试后端连接</button>
    <p v-if="result">后端返回：{{ result }}</p>
    <p v-if="error" style="color: red">出错了：{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const result = ref('')
const error = ref('')

async function checkHealth() {
  try {
    error.value = ''
    const res = await axios.get('http://127.0.0.1:8000/health')
    result.value = JSON.stringify(res.data)
  } catch (e) {
    error.value = e.message
  }
}
</script>
