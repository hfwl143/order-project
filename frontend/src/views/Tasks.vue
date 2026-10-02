<template>
  <section class="page-shell">
    <div class="page-heading">
      <div>
        <p class="eyebrow">YOUR WORK / 订单管理</p>
        <h1>我的订单</h1>
        <p class="page-lede">跟进你发起的需求，以及正在合作的订单。</p>
      </div>
      <router-link class="text-link" to="/">浏览订单大厅 <span aria-hidden="true">→</span></router-link>
    </div>

    <div class="mine-toolbar">
      <div class="role-switch" role="tablist" aria-label="订单身份">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          class="role-tab"
          :class="{ active: role === tab.value }"
          role="tab"
          :aria-selected="role === tab.value"
          @click="role = tab.value"
        >
          {{ tab.label }}
        </button>
      </div>
      <span class="result-count">{{ orders.length }} 个订单</span>
    </div>

    <div v-if="loadingOrders" class="list-placeholder">正在加载订单…</div>
    <div v-else-if="orders.length" class="order-list">
      <article v-for="order in orders" :key="order.id" class="order-row mine-row">
        <div class="order-main">
          <div class="order-meta">
            <span class="category-mark">{{ order.tag }}</span>
            <span class="meta-separator">·</span>
            <span>订单 #{{ order.id }}</span>
            <span v-if="order.deadline" class="deadline">截止 {{ order.deadline }}</span>
          </div>
          <h2>{{ order.title }}</h2>
          <p class="order-description">{{ order.description }}</p>
          <div class="mine-details">
            <span>身份：{{ role === 'published' ? '发布者' : '接单者' }}</span>
            <span v-if="order.taker_id">接单人 #{{ order.taker_id }}</span>
            <span v-if="order.contact">
              微信 {{ order.contact.wechat || '未填写' }} · 电话 {{ order.contact.phone || '未填写' }}
            </span>
          </div>
          <p v-if="order.abandon_requested" class="request-note">
            {{ role === 'published' ? '接单者申请放弃，等待你处理。' : '放弃申请已提交，等待发布者处理。' }}
          </p>
        </div>
        <div class="order-side">
          <span class="status-pill" :class="statusClass(order.order_status)">{{ order.order_status }}</span>
          <template v-if="role === 'published' && order.abandon_requested">
            <el-button type="primary" @click="decide(order, 'agree')">同意放弃</el-button>
            <el-button @click="decide(order, 'reject')">拒绝</el-button>
          </template>
          <template v-else-if="role === 'published' && order.order_status === '未接单'">
            <el-button @click="openEdit(order)">编辑</el-button>
            <el-button type="danger" plain @click="close(order)">关闭订单</el-button>
          </template>
          <el-button
            v-else-if="role === 'taken' && order.order_status === '已接单' && !order.abandon_requested"
            type="danger"
            plain
            @click="abandon(order)"
          >申请放弃</el-button>
        </div>
      </article>
    </div>
    <div v-else class="empty-state">
      <span class="empty-index">01</span>
      <h2>{{ role === 'published' ? '还没有发布订单' : '还没有接取订单' }}</h2>
      <p>{{ role === 'published' ? '把需要协作的事情发布出来，找到合适的人。' : '去订单大厅看看，或许有适合你的合作。' }}</p>
      <router-link class="empty-link" to="/">前往订单大厅 <span aria-hidden="true">→</span></router-link>
    </div>

    <el-dialog v-model="editVisible" title="编辑订单" width="min(560px, calc(100vw - 32px))">
      <el-form label-position="top" @submit.prevent="saveEdit">
        <el-form-item label="订单标题" required>
          <el-input v-model="editDraft.title" maxlength="100" />
        </el-form-item>
        <el-form-item label="需求描述" required>
          <el-input v-model="editDraft.description" type="textarea" :rows="4" />
        </el-form-item>
        <div class="form-pair">
          <el-form-item label="技能分类" required>
            <el-select v-model="editDraft.tag" class="full-width">
              <el-option v-for="tag in tags" :key="tag" :label="tag" :value="tag" />
            </el-select>
          </el-form-item>
          <el-form-item label="截止时间（可选）">
            <el-input v-model="editDraft.deadline" type="datetime-local" />
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" :disabled="!editDraft.title.trim() || !editDraft.description.trim()" @click="saveEdit">
          保存修改
        </el-button>
      </template>
    </el-dialog>
  </section>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import {
  closeOrder,
  decideAbandon,
  getMyOrders,
  requestAbandon,
  updateOrder,
} from '../api/task'
import { showToast } from '../toast'

const tabs = [
  { label: '我发布的', value: 'published' },
  { label: '我接取的', value: 'taken' },
]
const tags = ['编程', 'PS设计', '绘图', '文案']
const role = ref('published')
const orders = ref([])
const loadingOrders = ref(false)
const editVisible = ref(false)
const editingId = ref(null)
const editDraft = ref({ title: '', description: '', tag: '编程', deadline: '' })

async function loadOrders() {
  loadingOrders.value = true
  try {
    const response = await getMyOrders(role.value)
    orders.value = response.data
  } catch {
    orders.value = []
  } finally {
    loadingOrders.value = false
  }
}

function statusClass(status) {
  if (status === '已接单') return 'status-taken'
  if (status === '已关闭') return 'status-closed'
  return 'status-open'
}

function openEdit(order) {
  editingId.value = order.id
  editDraft.value = {
    title: order.title,
    description: order.description,
    tag: order.tag,
    deadline: order.deadline || '',
  }
  editVisible.value = true
}

async function saveEdit() {
  if (!editingId.value || !editDraft.value.title.trim() || !editDraft.value.description.trim()) return
  try {
    await updateOrder(editingId.value, {
      title: editDraft.value.title.trim(),
      description: editDraft.value.description.trim(),
      tag: editDraft.value.tag,
      deadline: editDraft.value.deadline || null,
    })
    editVisible.value = false
    showToast('订单已更新', 'success')
    await loadOrders()
  } catch {}
}

async function close(order) {
  if (!window.confirm(`确定关闭「${order.title}」吗？`)) return
  try {
    await closeOrder(order.id)
    showToast('订单已关闭', 'success')
    await loadOrders()
  } catch {}
}

async function abandon(order) {
  try {
    await requestAbandon(order.id)
    showToast('放弃申请已提交', 'success')
    await loadOrders()
  } catch {}
}

async function decide(order, decision) {
  try {
    await decideAbandon(order.id, decision)
    showToast(decision === 'agree' ? '已同意放弃，订单重新开放' : '已拒绝放弃申请', 'success')
    await loadOrders()
  } catch {}
}

watch(role, loadOrders)
onMounted(loadOrders)
</script>