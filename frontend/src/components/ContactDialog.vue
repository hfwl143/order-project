<template>
  <el-dialog
    :model-value="modelValue"
    title="联系对方"
    width="min(440px, calc(100vw - 32px))"
    align-center
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <p class="contact-intro">
      订单已成交，以下是<span class="contact-role">{{ roleLabel }}</span>的联系方式（仅你们双方可见），
      请礼貌联系，注意保护个人隐私与财产安全。
    </p>

    <div class="contact-item">
      <span class="contact-kind">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
        </svg>
        微信
      </span>
      <template v-if="contact?.wechat">
        <span class="contact-value" @click="copy(contact.wechat, '微信号')">{{ contact.wechat }}</span>
        <button class="copy-chip" type="button" @click="copy(contact.wechat, '微信号')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
          </svg>
          复制
        </button>
      </template>
      <span v-else class="contact-empty">对方暂未填写</span>
    </div>

    <div class="contact-item">
      <span class="contact-kind">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path
            d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"
          />
        </svg>
        手机
      </span>
      <template v-if="contact?.phone">
        <a class="contact-value link" :href="`tel:${contact.phone}`">{{ contact.phone }}</a>
        <button class="copy-chip" type="button" @click="copy(contact.phone, '手机号')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
          </svg>
          复制
        </button>
      </template>
      <span v-else class="contact-empty">对方暂未填写</span>
    </div>

    <p v-if="!contact?.wechat && !contact?.phone" class="contact-missing-note">
      对方两种联系方式都未填写。请稍后再来查看，或通过订单状态保持协作同步。
    </p>

    <template #footer>
      <el-button type="primary" @click="$emit('update:modelValue', false)">我知道了</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { showToast } from '../toast'

defineProps({
  modelValue: { type: Boolean, default: false },
  contact: { type: Object, default: null },
  roleLabel: { type: String, default: '对方' },
})

defineEmits(['update:modelValue'])

/**
 * 复制文本（clipboard API + 旧浏览器兜底）
 * @param {string} text
 * @param {string} label - 提示文案中的字段名
 */
async function copy(text, label) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text)
    } else {
      const textarea = document.createElement('textarea')
      textarea.value = text
      textarea.style.position = 'fixed'
      textarea.style.opacity = '0'
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
    }
    showToast(`${label}已复制`, 'success')
  } catch {
    showToast('复制失败，请长按或手动选择文本复制')
  }
}
</script>
