<template>
  <svg
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
  >
    <!-- 编程：代码括号 -->
    <template v-if="tag === '编程'">
      <path d="m16 18 6-6-6-6" />
      <path d="m8 6-6 6 6 6" />
    </template>
    <!-- PS设计：钢笔 -->
    <template v-else-if="tag === 'PS设计'">
      <path d="M12 20h9" />
      <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" />
    </template>
    <!-- 绘图：调色盘 -->
    <template v-else-if="tag === '绘图'">
      <path
        d="M12 22a10 10 0 1 1 10-10c0 2.76-2.24 5-5 5h-1.5a1.5 1.5 0 0 0-1.06 2.56A1.5 1.5 0 0 1 13.29 22H12Z"
      />
      <circle cx="7.5" cy="10.5" r="1" />
      <circle cx="12" cy="7.5" r="1" />
      <circle cx="16.5" cy="10.5" r="1" />
    </template>
    <!-- 文案：文档 -->
    <template v-else-if="tag === '文案'">
      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2Z" />
      <path d="M14 2v6h6" />
      <path d="M9 13h6" />
      <path d="M9 17h6" />
    </template>
    <!-- 兜底：标签 -->
    <template v-else>
      <path d="M20.59 13.41 12 22l-9-9V3h10l7.59 7.59a2 2 0 0 1 0 2.82Z" />
      <circle cx="7.5" cy="7.5" r="1.2" />
    </template>
  </svg>
</template>

<script setup>
/**
 * 分类图标
 * @prop {string} tag - 订单标签：编程 / PS设计 / 绘图 / 文案
 */
defineProps({
  tag: {
    type: String,
    default: '',
  },
})
</script>
