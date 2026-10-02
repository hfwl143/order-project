<template>
  <section class="page-shell">
    <div class="page-heading">
      <div>
        <p class="eyebrow">OPEN MARKET / 订单市场</p>
        <h1>接单大厅</h1>
        <p class="page-lede">发现正在寻找技能搭档的需求，合适就接下来。</p>
      </div>
      <el-button class="primary-action" type="primary" @click="openCreate">
        <span aria-hidden="true">＋</span> 发布订单
      </el-button>
    </div>

    <div class="market-toolbar">
      <div class="filter-group" aria-label="按技能分类筛选">
        <button
          v-for="item in categories"
          :key="item.value"
          class="filter-button"
          :class="{ active: selectedTag === item.value }"
          @click="selectTag(item.value)"
        >
          {{ item.label }}
        </button>
      </div>
      <span class="result-count">{{ orders.length }} 个待接订单</span>
    </div>

    <div v-if="loadingOrders" class="list-placeholder">正在加载订单…</div>
    <div v-else-if="orders.length" class="order-list">
      <article v-for="order in orders" :key="order.id" class="order-row">
        <div class="order-main">
          <div class="order-meta">
            <span class="category-mark">{{ order.tag }}</span>
            <span class="meta-separator">·</span>
            <span>订单 #{{ order.id }}</span>
            <span v-if="order.deadline" class="deadline">截止 {{ order.deadline }}</span>
          </div>
          <h2>{{ order.title }}</h2>
          <p class="order-description">{{ order.description }}</p>
          <div v-if="order.contact" class="contact-line">
            微信：{{ order.contact.wechat || '未填写' }}
            <span>·</span>
            电话：{{ order.contact.phone || '未填写' }}
          </div>
        </div>
        <div class="order-side">
          <span class="status-pill status-open">{{ order.order_status }}</span>
          <el-button
            v-if="!order.is_mine && order.order_status === '未接单'"
            type="primary"
            @click="take(order)"
          >接下订单</el-button>
          <span v-else-if="order.is_mine" class="muted-note">这是你发布的订单</span>
        </div>
      </article>
    </div>
    <div v-else class="empty-state">
      <span class="empty-index">0{{ categories.findIndex(item => item.value === selectedTag) + 1 }}</span>
      <h2>暂时没有匹配订单</h2>
      <p>试试其他分类，或者发布一个你需要的订单。</p>
      <el-button @click="openCreate">发布订单</el-button>
    </div>

    <el-dialog v-model="createVisible" title="发布新订单" width="min(560px, calc(100vw - 32px))">
      <el-form label-position="top" @submit.prevent="submitOrder">
        <el-form-item label="订单标题" required>
          <el-input v-model="draft.title" maxlength="100" placeholder="例如：为活动制作一张海报" />
        </el-form-item>
        <el-form-item label="需求描述" required>
          <el-input v-model="draft.description" type="textarea" :rows="4" placeholder="写清交付内容、要求或合作方式" />
        </el-form-item>
        <div class="form-pair">
          <el-form-item label="技能分类" required>
            <el-select v-model="draft.tag" class="full-width">
              <el-option v-for="item in categories.slice(1)" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="截止时间（可选）">
            <el-input v-model="draft.deadline" type="datetime-local" />
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="createVisible = false">取消</el-button>
        <el-button type="primary" :disabled="!canSubmit" @click="submitOrder">发布订单</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { createOrder, getOrders, takeOrder } from '../api/task'
import { showToast } from '../toast'

const categories = [
  { label: '全部', value: '' },
  { label: '编程', value: '编程' },
  { label: 'PS 设计', value: 'PS设计' },
  { label: '绘图', value: '绘图' },
  { label: '文案', value: '文案' },
]
const orders = ref([])
const selectedTag = ref('')
const loadingOrders = ref(false)
const createVisible = ref(false)
const draft = ref({ title: '', description: '', tag: '编程', deadline: '' })
const canSubmit = computed(() => draft.value.title.trim() && draft.value.description.trim())

async function loadOrders() {
  loadingOrders.value = true
  try {
    const response = await getOrders(selectedTag.value)
    orders.value = response.data
  } catch {
    orders.value = []
  } finally {
    loadingOrders.value = false
  }
}

function selectTag(tag) {
  selectedTag.value = tag
  loadOrders()
}

function openCreate() {
  draft.value = { title: '', description: '', tag: '编程', deadline: '' }
  createVisible.value = true
}

async function submitOrder() {
  if (!canSubmit.value) {
    showToast('请填写订单标题和需求描述')
    return
  }
  const payload = {
    title: draft.value.title.trim(),
    description: draft.value.description.trim(),
    tag: draft.value.tag,
    deadline: draft.value.deadline || null,
  }
  try {
    await createOrder(payload)
    createVisible.value = false
    showToast('订单已发布', 'success')
    await loadOrders()
  } catch {}
}

async function take(order) {
  try {
    await takeOrder(order.id)
    showToast('接单成功', 'success')
    await loadOrders()
  } catch {}
}

onMounted(loadOrders)
</script>
