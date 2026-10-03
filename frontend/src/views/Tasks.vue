<template>
  <section class="page-shell">
    <div class="page-heading">
      <div>
        <p class="eyebrow">YOUR WORK / 订单管理</p>
        <h1>我的订单</h1>
        <p class="page-lede">跟进你发起的需求，以及正在合作的订单。</p>
      </div>
      <router-link class="text-link" to="/">
        浏览订单大厅
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"
          stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <line x1="5" y1="12" x2="19" y2="12" />
          <polyline points="12 5 19 12 12 19" />
        </svg>
      </router-link>
    </div>

    <div class="mine-toolbar">
      <div class="role-switch" role="tablist" aria-label="订单身份">
        <button
          v-for="tab in tabsWithCount"
          :key="tab.value"
          class="role-tab"
          :class="{ active: role === tab.value }"
          role="tab"
          :aria-selected="role === tab.value"
          @click="role = tab.value"
        >
          {{ tab.label }}
          <span class="tab-count">{{ tab.count }}</span>
        </button>
      </div>
      <span class="result-count">{{ orders.length }} 个订单</span>
    </div>

    <!-- 统计条 -->
    <div v-if="!loadingOrders" class="stat-strip">
      <div class="stat-card">
        <span class="stat-icon coral">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="2" y="7" width="20" height="14" rx="2" />
            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
        </svg>
        </span>
        <span>
          <span class="stat-value">{{ stats.total }}</span><br />
          <span class="stat-label">全部订单</span>
        </span>
      </div>
      <div class="stat-card">
        <span class="stat-icon teal">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12 6 12 12 16 14" />
          </svg>
        </span>
        <span>
          <span class="stat-value">{{ stats.open }}</span><br />
          <span class="stat-label">{{ role === 'published' ? '等待接单' : '可接取状态' }}</span>
        </span>
      </div>
      <div class="stat-card">
        <span class="stat-icon gold">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
        </span>
        <span>
          <span class="stat-value">{{ stats.taken }}</span><br />
          <span class="stat-label">合作进行中</span>
        </span>
      </div>
      <div class="stat-card">
        <span class="stat-icon gray">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
            <path d="M13.73 21a2 2 0 0 1-3.46 0" />
          </svg>
        </span>
        <span>
          <span class="stat-value" :class="{ 'count-alert': stats.pending > 0 }">{{ stats.pending }}</span><br />
          <span class="stat-label">放弃申请待处理</span>
        </span>
      </div>
    </div>

    <!-- 骨架屏 -->
    <div v-if="loadingOrders" class="order-grid single" aria-label="正在加载订单">
      <div v-for="n in 3" :key="n" class="skeleton-card">
        <div class="skeleton-row">
          <div class="skeleton-bar skeleton-pill" style="width: 84px"></div>
          <div class="skeleton-bar skeleton-pill" style="width: 56px"></div>
        </div>
        <div class="skeleton-bar skeleton-title" style="width: 60%"></div>
        <div class="skeleton-bar skeleton-line" style="width: 100%"></div>
        <div class="skeleton-bar skeleton-line" style="width: 78%"></div>
      </div>
    </div>

    <!-- 订单列表 -->
    <div v-else-if="orders.length" class="order-grid single">
      <article
        v-for="order in orders"
        :key="order.id"
        class="order-card"
        :class="tagClass(order.tag)"
      >
        <div class="card-top">
          <span class="tag-chip" :class="tagClass(order.tag)">
            <TagIcon :tag="order.tag" />
            {{ order.tag }}
          </span>
          <span class="status-pill" :class="statusClass(order.order_status)">
            {{ order.order_status }}
          </span>
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

        <div class="mine-details">
          <span class="role-badge">{{ role === 'published' ? '我是发布者' : '我是接单者' }}</span>
          <span v-if="order.taker_id">接单者 #{{ order.taker_id }}</span>
          <span v-if="order.contact" class="contact-ready">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
            联系方式已解锁
          </span>
        </div>

        <p v-if="order.abandon_requested" class="request-note">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
            <line x1="12" y1="9" x2="12" y2="13" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
          {{ role === 'published' ? '接单者申请放弃，等待你处理。' : '放弃申请已提交，等待发布者处理。' }}
        </p>

        <div class="card-foot">
          <div class="card-actions">
            <el-button v-if="order.contact" class="ghost-action" @click="openContact(order)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
                stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
              联系{{ role === 'published' ? '接单者' : '发布者' }}
            </el-button>
            <template v-if="role === 'published' && order.abandon_requested">
              <el-button type="primary" @click="decide(order, 'agree')">同意放弃</el-button>
              <el-button @click="decide(order, 'reject')">拒绝申请</el-button>
            </template>
            <template v-else-if="role === 'published' && order.order_status === '未接单'">
              <el-button type="primary" plain @click="openEdit(order)">编辑订单</el-button>
              <el-button type="danger" plain @click="close(order)">关闭订单</el-button>
            </template>
            <el-button
              v-else-if="role === 'taken' && order.order_status === '已接单' && !order.abandon_requested"
              type="danger"
              plain
              @click="abandon(order)"
            >
              申请放弃
            </el-button>
          </div>
          <span v-if="!hasActions(order)" class="muted-note">当前没有需要处理的操作</span>
        </div>
      </article>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <span class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
          stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <template v-if="role === 'published'">
            <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2Z" />
            <path d="M14 2v6h6" />
            <path d="M12 18v-6" />
            <path d="M9 15h6" />
          </template>
          <template v-else>
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </template>
        </svg>
      </span>
      <h2>{{ role === 'published' ? '还没有发布订单' : '还没有接取订单' }}</h2>
      <p>
        {{ role === 'published'
          ? '把需要协作的事情发布出来，让有技能的伙伴看到你。'
          : '去订单大厅看看，或许正有适合你的合作机会。' }}
      </p>
      <router-link class="empty-link" to="/">
        前往订单大厅
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"
          stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <line x1="5" y1="12" x2="19" y2="12" />
          <polyline points="12 5 19 12 12 19" />
        </svg>
      </router-link>
    </div>

    <!-- 编辑订单弹窗 -->
    <el-dialog v-model="editVisible" title="编辑订单" width="min(560px, calc(100vw - 32px))">
      <el-form label-position="top" @submit.prevent="saveEdit">
        <el-form-item label="订单标题" required>
          <el-input v-model="editDraft.title" maxlength="100" />
        </el-form-item>
        <el-form-item label="需求描述" required>
          <el-input
            v-model="editDraft.description"
            type="textarea"
            :rows="4"
            maxlength="1000"
            show-word-limit
          />
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
        <el-button
          type="primary"
          :disabled="!editDraft.title.trim() || !editDraft.description.trim()"
          @click="saveEdit"
        >
          保存修改
        </el-button>
      </template>
    </el-dialog>

    <!-- 联系对方弹窗 -->
    <ContactDialog
      v-model="contactVisible"
      :contact="activeContact"
      :role-label="role === 'published' ? '接单者' : '发布者'"
    />
  </section>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { ElMessageBox } from 'element-plus'
import {
  closeOrder,
  decideAbandon,
  getMyOrders,
  requestAbandon,
  updateOrder,
} from '../api/task'
import { showToast } from '../toast'
import { deadlineInfo, relativeTime, toInputDateTime } from '../utils/format'
import TagIcon from '../components/TagIcon.vue'
import ContactDialog from '../components/ContactDialog.vue'

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

const stats = computed(() => ({
  total: orders.value.length,
  open: orders.value.filter((item) => item.order_status === '未接单').length,
  taken: orders.value.filter((item) => item.order_status === '已接单').length,
  pending: orders.value.filter((item) => item.abandon_requested).length,
}))

const tabsWithCount = computed(() =>
  tabs.map((tab) => ({
    ...tab,
    count: tab.value === role.value ? orders.value.length : '',
  })),
)

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
 * 状态 → 样式类名
 * @param {string} status - 未接单 / 已接单 / 已关闭
 * @returns {string} status-open / status-taken / status-closed
 */
function statusClass(status) {
  if (status === '已接单') return 'status-taken'
  if (status === '已关闭') return 'status-closed'
  return 'status-open'
}

/**
 * 截止时间展示信息
 * @param {{ deadline: string|null }} order - 订单对象
 * @returns {{ text: string, hint: string, level: string }|null}
 */
function dl(order) {
  return deadlineInfo(order.deadline)
}

/**
 * 判断卡片是否有可执行操作（用于占位提示）
 * @param {object} order - 订单对象
 * @returns {boolean} 是否存在操作按钮
 */
function hasActions(order) {
  if (order.contact) return true
  if (role.value === 'published') {
    return Boolean(order.abandon_requested) || order.order_status === '未接单'
  }
  return order.order_status === '已接单' && !order.abandon_requested
}

const contactVisible = ref(false)
const activeContact = ref(null)

/**
 * 打开「联系对方」弹窗
 * @param {object} order - 含 contact 的订单
 */
function openContact(order) {
  activeContact.value = order.contact
  contactVisible.value = true
}

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

/**
 * @param {object} order
 */
function openEdit(order) {
  editingId.value = order.id
  editDraft.value = {
    title: order.title,
    description: order.description,
    tag: order.tag,
    deadline: toInputDateTime(order.deadline),
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
  try {
    await ElMessageBox.confirm(
      `关闭后「${order.title}」将不再出现在订单大厅，此操作无法撤销。`,
      '确认关闭订单？',
      {
        confirmButtonText: '确认关闭',
        cancelButtonText: '再想想',
        type: 'warning',
        confirmButtonClass: 'el-button--danger',
      },
    )
  } catch {
    return
  }
  try {
    await closeOrder(order.id)
    showToast('订单已关闭', 'success')
    await loadOrders()
  } catch {}
}

async function abandon(order) {
  try {
    await ElMessageBox.confirm(
      `提交后发布者会收到你的放弃申请，在对方同意前订单仍保持合作状态。`,
      `申请放弃「${order.title}」？`,
      {
        confirmButtonText: '提交申请',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger',
      },
    )
  } catch {
    return
  }
  try {
    await requestAbandon(order.id)
    showToast('放弃申请已提交，等待发布者处理', 'success')
    await loadOrders()
  } catch {}
}

async function decide(order, decision) {
  if (decision === 'agree') {
    try {
      await ElMessageBox.confirm(
        '同意后订单将重新开放接单，你与当前接单者的合作随即终止。',
        '同意接单者放弃？',
        {
          confirmButtonText: '同意放弃',
          cancelButtonText: '取消',
          type: 'warning',
        },
      )
    } catch {
      return
    }
  }
  try {
    await decideAbandon(order.id, decision)
    showToast(decision === 'agree' ? '已同意放弃，订单重新开放' : '已拒绝放弃申请', 'success')
    await loadOrders()
  } catch {}
}

watch(role, loadOrders)
onMounted(loadOrders)
</script>

<style scoped>
.tab-count:empty {
    display: none;
}

.tab-count {
    display: inline-grid;
    min-width: 20px;
    height: 20px;
    margin-left: 2px;
    padding: 0 6px;
    place-items: center;
    border-radius: 999px;
    background: rgba(14, 59, 54, 0.08);
    color: var(--muted);
    font-size: 11px;
    font-weight: 700;
}

.role-tab.active .tab-count {
    background: var(--brand-soft);
    color: var(--brand);
}

.count-alert {
    color: var(--brand);
}
</style>
