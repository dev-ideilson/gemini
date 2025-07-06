import AppLayout from '@/layout/AppLayout.vue';
import { useAuthStore } from '@/stores/AuthStore';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    {
        path: '/',
        component: AppLayout,
        children: [
            {
                path: '/',
                name: 'dashboard',
                component: () => import('@/views/Dashboard.vue')
            }
        ]
    },

    {
        path: '/auth/login',
        name: 'login',
        component: () => import('@/views/pages/auth/Login.vue'),
        meta: {
            title: 'Login',
            unprotected: true
        }
    },
    {
        path: '/auth/access',
        name: 'accessDenied',
        component: () => import('@/views/pages/auth/Access.vue')
    },
    {
        path: '/auth/error',
        name: 'error',
        component: () => import('@/views/pages/auth/Error.vue')
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach(async (to, from, next) => {
    const auth = useAuthStore();

    if (to.meta.title) {
        document.title = `${to.meta.title}`;
    }

    if (!to.meta.unprotected) {
        if (!auth.isAuthenticated) {
            return next('/auth/login');
        } else if (to.meta.admin && !(auth.user?.is_superuser || auth.user?.is_staff)) {
            return next({ name: 'denied' });
        }
    }

    next();
});

export default router;
