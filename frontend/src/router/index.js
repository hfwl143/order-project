import { createRouter, createWebHistory } from 'vue-router'
const routes = [
    { path: '/', name: 'home', component: () => import('../views/Home.vue'), meta: { requiresAuth: true } },
    {
        path: '/mine',
        name: 'mine',
        component: () => import('../views/Tasks.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('../views/Login.vue'),
    },
    { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to) => {
    const token = localStorage.getItem('token')

    if (to.meta.requiresAuth && !token) {
        return { path: '/login', query: { redirect: to.fullPath } }
    }

    if (to.path === '/login' && token) {
        const redirect = to.query.redirect
        return {
            path: typeof redirect === 'string' && redirect.startsWith('/') && !redirect.startsWith('//')
                ? redirect
                : '/',
        }
    }
})

export default router