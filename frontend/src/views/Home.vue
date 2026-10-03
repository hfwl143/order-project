<template>
  <section class="page-shell">
    <!-- Hero 区 -->
    <div class="market-hero">
      <p class="eyebrow">OPEN MARKET / 订单市场</p>
      <h1>接单大厅</h1>
      <p>发现正在寻找技能搭档的需求，合适就接下来。</p>
      <div class="hero-actions">
        <el-input
          v-model="keyword"
          class="hero-search"
          placeholder="搜索订单标题或描述关键词…"
          clearable
        >
          <template #prefix>
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
          </template>
        </el-input>
        <el-button class="hero-publish" @click="openCreate">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          发布订单
        </el-button>
      </div>
    </div>

    <!-- 统计条 -->
    <div v-if="!loadingOrders" class="stat-strip">
      <div class="stat-card">
        <span class="stat-icon coral">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <line x1="8" y1="6" x2="21" y2="6" />
            <line x1="8" y1="12" x2="21" y2="12" />
            <line x1="8" y1="18" x2="21" y2="18" />
            <line x1="3" y1="6" x2="3.01" y2="6" />
            <line x1="3" y1="12" x2="3.01" y2="12" />
            <line x1="3" y1="18" x2="3.01" y2="18" />
          </svg>
        </span>
        <span>
          <span class="stat-value">{{ stats.total }}</span><br />
          <span class="stat-label">待接订单</span>
        </span>
      </div>
      <div class="stat-card">
        <span class="stat-icon gold">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="13" r="8" />
            <path d="M12 9v4l2 2" />
            <path d="M5 3 2 6" />
            <path d="m22 6-3-3" />
          </svg>
        </span>
        <span>
          <span class="stat-value">{{ stats.urgent }}</span><br />
          <span class="stat-label">即将截止</span>
        </span>
      </div>
      <div class="stat-card">
        <span class="stat-icon teal">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        </span>
        <span>
          <span class="stat-value">{{ stats.mine }}</span><br />
          <span class="stat-label">我发布的</span>
        </span>
      </div>
      <div class="stat-card">
        <span class="stat-icon gray">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="3" y="4" width="18" height="18" rx="2" />
            <line x1="16" y1="2" x2="16" y2="6" />
            <line x1="8" y1="2" x2="8" y2="6" />
            <line x1="3" y1="10" x2="21" y2="10" />
          </svg>
        </span>
        <span>
          <span class="stat-value">{{ stats.deadline }}</span><br />
          <span class="stat-label">设了截止期</span>
        </span>
      </div>
    </div>

    <!-- 分类筛选 -->
    <div class="market-toolbar">
      <div class="filter-group" aria-label="按技能分类筛选">
        <button
          v-for="item in categories"
          :key="item.value"
          class="filter-button"
          :class="{ active: selectedTag === item.value }"
          @click="selectTag(item.value)"
        >
          <TagIcon v-if="item.value" :tag="item.value" />
          {{ item.label }}
        </button>
      </div>
      <span class="result-count">{{ filteredOrders.length }} 个匹配订单</span>
    </div>

    <!-- 骨架屏 -->
    <div v-if="loadingOrders" class="order-grid" aria-label="正在加载订单">
      <div v-for="n in 6" :key="n" class="skeleton-card">
        <div class="skeleton-row">
          <div class="skeleton-bar skeleton-pill" style="width: 84px"></div>
          <div class="skeleton-bar skeleton-pill" style="width: 56px"></div>
        </div>
        <div class="skeleton-bar skeleton-title" style="width: 72%"></div>
        <div class="skeleton-bar skeleton-line" style="width: 100%"></div>
        <div class="skeleton-bar skeleton-line" style="width: 88%"></div>
        <div class="skeleton-bar skeleton-line" style="width: 56%"></div>
      </div>
    </div>

    <!-- 订单卡片 -->
    <div v-else-if="filteredOrders.length" class="order-grid">
      <article
        v-for="order in filteredOrders"
        :key="order.id"
        class="order-card"
        :class="tagClass(order.tag)"
      >
        <div class="card-top">
          <span class="tag-chip" :class="tagClass(order.tag)">
            <TagIcon :tag="order.tag" />
            {{ order.tag }}
          </span>
          <span class="status-pill status-open">{{ order.order_status }}</span>
        </div>

        <h2>{{ order.title }}</h2>
        <p class="order-description">{{ order.description }}</p>

        <div class="card-meta">
          <span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <line x1="4" y1="9" x2="20" y2="9" />
              <line x1="4" y1="15" x2="20" y2="15" />
              <line x1="10" y1="3" x2="8" y2="21" />
              <line x1="16" y1="3" x2="14" y2="21" />
            </svg>
            订单 #{{ order.id }}
          </span>
          <span>发布于 {{ relativeTime(order.create_time) }}</span>
          <span v-if="dl(order)" class="deadline" :class="dl(order).level">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <rect x="3" y="4" width="18" height="18" rx="2" />
              <line x1="16" y1="2" x2="16" y2="6" />
              <line x1="8" y1="2" x2="8" y2="6" />
              <line x1="3" y1="10" x2="21" y2="10" />
            </svg>
            {{ dl(order).text }} · {{ dl(order).hint }}
          </span>
        </div>

        <div class="card-foot">
          <span v-if="order.is_mine" class="muted-note">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
            这是你发布的订单
          </span>
          <span v-else></span>
          <el-button v-if="order.contact" class="ghost-action" @click="openContact(order)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
            联系 TA
          </el-button>
          <el-button
            v-if="!order.is_mine && order.order_status === '未接单'"
            class="primary-action"
            type="primary"
            @click="take(order)"
          >
            接下订单
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <line x1="5" y1="12" x2="19" y2="12" />
              <polyline points="12 5 19 12 12 19" />
            </svg>
          </el-button>
        </div>
      </article>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <span class="empty-icon">
        <svg v-if="keyword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
          stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
          <line x1="8" y1="11" x2="14" y2="11" />
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
          stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <polyline points="22 12 16 12 14 15 10 15 8 12 2 12" />
          <path
            d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"
          />
        </svg>
      </span>
      <h2>{{ keyword ? '没有找到相关订单' : '暂时没有匹配订单' }}</h2>
      <p>
        {{ keyword
          ? '换个关键词试试，或者清空搜索浏览全部订单。'
          : '试试其他分类，或者发布一个你需要的订单。' }}
      </p>
      <el-button v-if="keyword" @click="keyword = ''">清空搜索</el-button>
      <el-button v-else class="primary-action" type="primary" @click="openCreate">发布订单</el-button>
    </div>

    <!-- 发布订单弹窗 -->
    <el-dialog v-model="createVisible" title="发布新订单" width="min(560px, calc(100vw - 32px))">
      <el-form label-position="top" @submit.prevent="submitOrder">
        <el-form-item label="订单标题" required>
          <el-input v-model="draft.title" maxlength="100" placeholder="例如：为活动制作一张海报" />
        </el-form-item>
        <el-form-item label="需求描述" required>
          <el-input
            v-model="draft.description"
            type="textarea"
            :rows="4"
            maxlength="1000"
            show-word-limit
            placeholder="写清交付内容、要求或合作方式"
          />
        </el-form-item>
        <div class="form-pair">
          <el-form-item label="技能分类" required>
            <el-select v-model="draft.tag" class="full-width">
              <el-option
                v-for="item in categories.slice(1)"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="截止时间（可选）">
            <el-input v-model="draft.deadline" type="datetime-local" />
          </el-form-item>
        </div>
        <div v-if="!hasContact" class="inline-contact-tip">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="16" x2="12" y2="12" />
            <line x1="12" y1="8" x2="12.01" y2="8" />
          </svg>
          <span>你还没填写微信或手机号，成交后接单者可能联系不到你。</span>
          <button type="button" class="tip-action" @click="goFillContact">去填写</button>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="createVisible = false">取消</el-button>
        <el-button type="primary" :disabled="!canSubmit" @click="submitOrder">发布订单</el-button>
      </template>
    </el-dialog>

    <!-- 联系对方弹窗 -->
    <ContactDialog
      v-model="contactVisible"
      :contact="activeContact"
      :role-label="contactRole"
    />
  </section>
</template>

<script setup>
import { computed, h, onMounted, ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import { createOrder, getOrders, takeOrder } from '../api/task'
import { showToast } from '../toast'
import { deadlineInfo, relativeTime } from '../utils/format'
import { hasContact, openProfileDialog } from '../utils/profile'
import TagIcon from '../components/TagIcon.vue'
import ContactDialog from '../components/ContactDialog.vue'

const categories = [
  { label: '全部', value: '' },
  { label: '编程', value: '编程' },
  { label: 'PS 设计', value: 'PS设计' },
  { label: '绘图', value: '绘图' },
  { label: '文案', value: '文案' },
]
const orders = ref([])
const selectedTag = ref('')
const keyword = ref('')
const loadingOrders = ref(false)
const createVisible = ref(false)
const draft = ref({ title: '', description: '', tag: '编程', deadline: '' })
const canSubmit = computed(() => draft.value.title.trim() && draft.value.description.trim())

/** 按关键词在前端过滤（后端暂只支持标签筛选） */
const filteredOrders = computed(() => {
  const word = keyword.value.trim().toLowerCase()
  if (!word) return orders.value
  return orders.value.filter((order) =>
    [order.title, order.description, order.tag].some((field) =>
      String(field || '').toLowerCase().includes(word),
    ),
  )
})

const stats = computed(() => ({
  total: orders.value.length,
  urgent: orders.value.filter((order) => {
    const info = deadlineInfo(order.deadline)
    return info && (info.level === 'urgent' || info.level === 'overdue')
  }).length,
  mine: orders.value.filter((order) => order.is_mine).length,
  deadline: orders.value.filter((order) => Boolean(order.deadline)).length,
}))

/**
 * 标签 → 样式类名
 * @param {string} tag - 后端标签值
 * @returns {string} tag-code / tag-ps / tag-draw / tag-copy
 */
function tagClass(tag) {
  const map = {
    编程: 'tag-code',
    PS设计: 'tag-ps',
    绘图: 'tag-draw',
    文案: 'tag-copy',
  }
  return map[tag] || ''
}

/**
 * 截止时间展示信息
 * @param {{ deadline: string|null }} order - 订单对象
 * @returns {{ text: string, hint: string, level: string }|null}
 */
function dl(order) {
  return deadlineInfo(order.deadline)
}

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
  if (selectedTag.value === tag) return
  selectedTag.value = tag
  loadOrders()
}

function openCreate() {
  draft.value = { title: '', description: '', tag: '编程', deadline: '' }
  createVisible.value = true
}

/** 从发布弹窗跳去填写联系方式（软提醒入口） */
function goFillContact() {
  createVisible.value = false
  openProfileDialog()
}

const contactVisible = ref(false)
const activeContact = ref(null)
const contactRole = ref('对方')

/**
 * 打开「联系对方」弹窗
 * @param {object} order - 含 contact/my_role 的订单
 */
function openContact(order) {
  activeContact.value = order.contact
  contactRole.value = order.my_role === 'publisher' ? '接单者' : '发布者'
  contactVisible.value = true
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
    showToast('订单已发布，等待有缘人接单', 'success')
    await loadOrders()
  } catch {}
}

async function take(order) {
  const missingContact = !hasContact.value
  try {
    await ElMessageBox.confirm(
      h('div', { class: 'confirm-block' }, [
        h('p', { class: 'confirm-lead' }, `确认接下「${order.title}」吗？`),
        h('p', { class: 'confirm-sub' }, '接单后，双方可在「我的订单」中查看彼此的微信/手机号。'),
        missingContact &&
          h('p', { class: 'confirm-warn' }, '你还没有填写联系方式，接单后发布者将无法联系你，建议先补充。'),
      ]),
      '确认接单',
      {
        confirmButtonText: missingContact ? '仍然接单' : '确认接单',
        cancelButtonText: missingContact ? '先去填写' : '再看看',
        distinguishCancelAndClose: true,
        type: missingContact ? 'warning' : 'success',
        roundButton: false,
      },
    )
  } catch (action) {
    // 未填联系方式时点「先去填写」→ 打开资料弹窗；点关闭/遮罩则什么都不做
    if (action === 'cancel' && missingContact) openProfileDialog()
    return
  }
  try {
    await takeOrder(order.id)
    showToast('接单成功，快去联系发布者吧', 'success')
    await loadOrders()
  } catch {}
}

onMounted(loadOrders)
</script>
