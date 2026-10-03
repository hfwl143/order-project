<template>
  <el-dialog
    :model-value="profileState.dialogVisible"
    title="我的资料"
    width="min(460px, calc(100vw - 32px))"
    align-center
    @update:model-value="(v) => (profileState.dialogVisible = v)"
    @open="resetForm"
  >
    <p class="profile-intro">
      填写至少一种联系方式，订单成交后才会向该订单的对方展示；大厅里的其他用户看不到。
    </p>
    <el-form label-position="top" @submit.prevent="save">
      <el-form-item label="微信号（选填）">
        <el-input
          v-model="form.wechat"
          :class="{ 'input-invalid': errors.wechat }"
          maxlength="20"
          placeholder="字母开头，6-20 位字母/数字/下划线/减号"
          @input="errors.wechat = ''"
        >
          <template #prefix>
            <svg class="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
            </svg>
          </template>
        </el-input>
        <p v-if="errors.wechat" class="field-error">{{ errors.wechat }}</p>
      </el-form-item>
      <el-form-item label="手机号（选填）">
        <el-input
          v-model="form.phone"
          :class="{ 'input-invalid': errors.phone }"
          maxlength="11"
          inputmode="numeric"
          placeholder="11 位大陆手机号，成交后对方可一键拨打"
          @input="onPhoneInput"
        >
          <template #prefix>
            <svg class="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path
                d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"
              />
            </svg>
          </template>
        </el-input>
        <p v-if="errors.phone" class="field-error">{{ errors.phone }}</p>
      </el-form-item>
    </el-form>
    <p v-if="!form.wechat && !form.phone" class="profile-warn">
      两种联系方式都为空时，成交后对方将无法联系你。
    </p>
    <template #footer>
      <el-button @click="profileState.dialogVisible = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="save">保存资料</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { profileState, saveProfile, PHONE_PATTERN, WECHAT_PATTERN } from '../utils/profile'
import { showToast } from '../toast'

const form = reactive({ wechat: '', phone: '' })
const errors = reactive({ wechat: '', phone: '' })
const saving = ref(false)

function resetForm() {
  form.wechat = profileState.wechat
  form.phone = profileState.phone
  errors.wechat = ''
  errors.phone = ''
}

/** 手机号只保留数字 */
function onPhoneInput(value) {
  form.phone = value.replace(/\D/g, '').slice(0, 11)
  errors.phone = ''
}

/**
 * @returns {boolean} 表单格式是否合法
 */
function validate() {
  errors.wechat = ''
  errors.phone = ''
  const wechat = form.wechat.trim()
  const phone = form.phone.trim()
  let ok = true
  if (wechat && !WECHAT_PATTERN.test(wechat)) {
    errors.wechat = '微信号需以字母开头，为 6-20 位字母、数字、下划线或减号'
    ok = false
  }
  if (phone && !PHONE_PATTERN.test(phone)) {
    errors.phone = '请输入正确的 11 位大陆手机号'
    ok = false
  }
  return ok
}

async function save() {
  if (!validate()) return
  saving.value = true
  try {
    await saveProfile({ wechat: form.wechat.trim(), phone: form.phone.trim() })
    profileState.dialogVisible = false
    showToast('联系方式已保存', 'success')
  } catch {
    // 错误提示已由接口拦截器统一弹出
  } finally {
    saving.value = false
  }
}
</script>
