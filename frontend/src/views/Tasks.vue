<template>
  <div class="tasks">
    <h1 class="page-title">📝 我的待办</h1>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <el-button
        v-for="f in filters"
        :key="String(f.value)"
        :type="currentFilter === f.value ? 'primary' : 'default'"
        @click="switchFilter(f.value)"
      >
        {{ f.label }}
      </el-button>
    </div>

    <!-- 添加任务栏 -->
    <div class="add-bar">
      <el-input
        v-model="newTitle"
        placeholder="任务标题，回车添加"
        @keyup.enter="addTask"
        clearable
      />
      <el-date-picker
        v-model="newDue"
        type="date"
        placeholder="截止日期（可选）"
        format="YYYY-MM-DD"
        value-format="YYYY-MM-DD"
        style="width: 160px"
      />
      <el-input
        v-model="newDesc"
        placeholder="描述（可选）"
        @keyup.enter="addTask"
        clearable
      />
      <el-button type="primary" @click="addTask">添加</el-button>
    </div>

    <!-- 任务列表 -->
    <TransitionGroup name="task-list" tag="ul">
      <li v-for="task in tasks" :key="task.id" :class="{ done: task.completed }">
        <div class="row">
          <el-checkbox
            :model-value="task.completed"
            @change="toggleTask(task)"
          />
          <span class="title" @click="startEdit(task)">
            {{ task.title }}
            <el-tag v-if="task.due_date" type="warning" size="small" effect="plain">
              📅 {{ task.due_date }}
            </el-tag>
          </span>
          <el-button type="danger" text @click="removeTask(task)">删除</el-button>
        </div>
        <!-- 编辑区 -->
        <div v-if="editingId === task.id" class="edit-box">
          <el-input v-model="editForm.title" placeholder="标题" />
          <el-input
            v-model="editForm.description"
            type="textarea"
            placeholder="描述（可选）"
            :rows="3"
          />
          <el-date-picker
            v-model="editForm.due_date"
            type="date"
            placeholder="截止日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
          <div class="edit-actions">
            <el-button type="primary" @click="saveEdit(task)">保存</el-button>
            <el-button @click="cancelEdit">取消</el-button>
          </div>
        </div>
      </li>
    </TransitionGroup>

    <!-- 空状态 -->
    <div v-if="tasks.length === 0" class="empty-state">
      <div class="empty-icon">📋</div>
      <div class="empty-title">暂无任务</div>
      <div class="empty-desc">在上方输入框添加你的第一个任务吧～</div>
    </div>
    <div class="header">
      <h1>我的待办</h1>
      <button class="logout" @click="logout">退出</button>
    </div>
  </div>
</template>

<script setup>
// 引入响应式 ref 和生命周期钩子 onMounted
import { ref, onMounted } from 'vue'
// 引入后端接口：查询、创建、更新、删除任务的 API 函数
import { getTasks, createTask, updateTask, deleteTask } from '../api/task'
import { showToast, showLoading, hideLoading } from '../toast'

// 通用请求包装：自动 loading + 失败弹 toast
async function request(fn, { loading = true, successMsg = '' } = {}) {
  if (loading) showLoading()
  try {
    const res = await fn()
    if (successMsg) showToast(successMsg, 'success')
    return res
  } catch (err) {
    showToast(err.friendlyMessage || '操作失败')
    throw err            // 继续抛出，方便调用方做特殊处理（可选）
  } finally {
    if (loading) hideLoading()
  }
}





// 响应式状态：任务列表数组，初始为空
const tasks = ref([])
// 响应式状态：新增任务的标题输入值
const newTitle = ref('')
// 响应式状态：新增任务的截止日期输入值
const newDue = ref('')
// 响应式状态：当前选中的筛选值，默认 all
const currentFilter = ref('all')
// 响应式状态：新增任务的描述输入值
const newDesc = ref('')

// 筛选选项配置：名称与对应筛选值（value 可为字符串或布尔值）
const filters = [
  // 全部任务：筛选值为 'all'
  { label: '全部', value: 'all' },
  // 未完成任务：筛选值为 false
  { label: '未完成', value: false },
  // 已完成任务：筛选值为 true
  { label: '已完成', value: true },
]

// ===== 编辑相关 =====
// 响应式状态：当前正在编辑的任务 id，null 表示未在编辑
const editingId = ref(null)
// 响应式状态：编辑表单对象，包含标题 / 描述 / 截止日期三个字段
const editForm = ref({ title: '', description: '', due_date: '' })

// 点标题 → 进入编辑，把现有数据填进表单
function startEdit(task) {
  // 记录正在编辑的任务 id
  editingId.value = task.id
  // 用任务现有数据填充编辑表单
  editForm.value = {
    // 填标题字段
    title: task.title,
    // 填描述字段，无描述时用空字符串兜底
    description: task.description || '',
    // 填截止日期字段，无日期时用空字符串兜底
    due_date: task.due_date || '',
  }
}

// 取消编辑：清空编辑中的任务 id，隐藏编辑区
function cancelEdit() {
  editingId.value = null
}

// 保存
// 异步保存函数：更新当前编辑的任务
async function saveEdit(task) {
  // 取编辑表单的当前值
  const form = editForm.value
  // 标题不能为空：去除首尾空格后为空则直接返回，不保存
  if (!form.title.trim()) return
  // 组装提交给接口的数据对象
  const data = {
    // 提交标题：去除首尾空格
    title: form.title.trim(),
    // 提交描述：原样传递
    description: form.description,
    // 提交截止日期：空字符串转成 null，符合接口要求
    due_date: form.due_date || null,
  }
  try{
    // 调用接口更新任务，等待返回更新后的数据
    const res = await request(() => updateTask(task.id, data), { successMsg: '保存成功' })
    // 在任务列表中查找该任务的下标
    const index = tasks.value.findIndex(t => t.id === task.id)
    // 用接口返回的最新数据替换列表中的旧数据
    tasks.value[index] = res.data
    // 保存成功退出编辑模式
    editingId.value = null
  }catch{}
}

// ===== 列表 / 增删改 =====
// 异步切换筛选函数：根据筛选值重新加载任务列表
async function switchFilter(value) {
  // 更新当前筛选值，驱动按钮高亮
  currentFilter.value = value
  // 调用接口拉取数据：筛选值为 all 时不传参（查询全部），否则传筛选值
  const res = await getTasks(value === 'all' ? undefined : value)
  // 用接口返回的数据覆盖任务列表
  tasks.value = res.data
}

// 异步加载任务函数：无筛选条件地拉取全部任务
async function loadTasks() {
  // 调用接口获取全部任务列表
  const res = await request(() => getTasks())
  // 用接口返回的数据覆盖任务列表
  tasks.value = res.data
}

// 异步添加任务函数
async function addTask() {
  // 取输入标题并去除首尾空格
  const title = newTitle.value.trim()
  // 标题为空则直接返回，不调用接口
  if (!title) return
  // 组装新增任务的数据对象
  const data = {
    // 新增标题
    title,
    // 新增描述
    description: newDesc.value,
  }
  // 若选择了截止日期则追加到数据对象中
  if (newDue.value) data.due_date = newDue.value
  try
  {
    // 调用接口创建任务，等待返回新任务数据
    const res = await request(() => createTask(data), { successMsg: '添加成功' })
    // 将新任务插入到列表头部（最新在最上）
    tasks.value.unshift(res.data)
    // 清空标题输入框
    newTitle.value = ''
    // 清空描述输入框
    newDesc.value = ''
    // 清空截止日期输入框
    newDue.value = ''
  }catch {}
}

// 异步切换任务完成状态函数
async function toggleTask(task) {
  try{
    // 调用接口：传入任务 id 与取反后的完成状态
    const res = await request(()=>updateTask(task.id),{ completed: !task.completed })
    // 在任务列表中查找该任务的下标
    const index = tasks.value.findIndex(t => t.id === task.id)
    // 用接口返回的最新数据替换列表中的旧数据
    tasks.value[index] = res.data
  }catch{}
}

// 异步删除任务函数
async function removeTask(task) {
  try{
    // 调用接口删除该任务
    await request(() => deleteTask(task.id), { successMsg: '已删除' })
    // 从本地列表中过滤掉已删除的任务
    tasks.value = tasks.value.filter(t => t.id !== task.id)
  }catch{}
}

function logout() {
  localStorage.removeItem('token')
  location.href = '/login'
}


// 组件挂载完成后自动加载任务列表
onMounted(loadTasks)
</script>

<style scoped>
.tasks {
  max-width: 640px;
  margin: 40px auto;
  padding: 24px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.page-title {
  margin: 0 0 24px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.filter-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.add-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.add-bar .el-input {
  flex: 1;
  min-width: 180px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  padding: 16px;
  margin-bottom: 12px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

li:hover {
  background: #f5f7fa;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.row {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.title {
  flex: 1;
  cursor: pointer;
  font-size: 15px;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: color 0.2s;
}

.title:hover {
  color: #409eff;
}

.done .title {
  text-decoration: line-through;
  color: #909399;
  opacity: 0.7;
}

.done {
  background: #f9f9f9;
  opacity: 0.8;
}

.edit-box {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #eee;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.edit-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 8px;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.8;
}

.empty-title {
  font-size: 18px;
  font-weight: 500;
  color: #606266;
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 14px;
  color: #909399;
}

/* 列表动画 */
.task-list-enter-active,
.task-list-leave-active {
  transition: all 0.4s ease;
}

.task-list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.task-list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.task-list-move {
  transition: transform 0.3s ease;
}

/* 完成任务动效 */
li.done .title {
  position: relative;
}

li.done .title::after {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  width: 100%;
  height: 1px;
  background: #909399;
  animation: strikethrough 0.3s ease forwards;
}

@keyframes strikethrough {
  from {
    width: 0;
  }
  to {
    width: 100%;
  }
}
</style>