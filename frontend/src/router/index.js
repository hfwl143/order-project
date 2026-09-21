import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
    { path: '/', component: Home },
    { path: '/about', component: () => import('../views/About.vue') },
    {
        path: '/tasks',
        name: 'tasks',
        component: () => import('../views/Tasks.vue'),
        meta: { requiresAuth: true },   // 用 meta 标记需要登录
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('../views/Login.vue'),  // 补上 login 路由
    },
]

// 1. 先创建 router
const router = createRouter({
    history: createWebHistory(),
    routes,
})

// 2. 再注册守卫
router.beforeEach((to) => {
    const token = localStorage.getItem('token')

    // 需要登录但没 token → 去登录页
    if (to.meta.requiresAuth && !token) {
        return { path: '/login', query: { redirect: to.fullPath } }
    }

    // 已登录还想去登录页 → 回任务页
    if (to.path === '/login' && token) {
        return { path: '/tasks' }
    }

    // 其他情况放行（返回 undefined 或 true）
})

export default router