import { httpAuth } from '@/service/requests/auth';
import { defineStore } from 'pinia';
import { computed, reactive } from 'vue';

export const useAuthStore = defineStore('auth', () => {
    const state = reactive({
        user: localStorage.getItem('user'),
        token: {
            access: localStorage.getItem('tk_access') || null,
            refresh: localStorage.getItem('tk_refresh') || null
        },
        isAuthenticated: false
    });

    function setUser(user) {
        if (user) {
            state.user = user;
            localStorage.setItem('user', JSON.stringify(user));
        }
    }

    function setToken(access, refresh) {
        if (access && access) {
            state.token.access = access;
            state.token.refresh = refresh;
            localStorage.setItem('tk_access', access);
            localStorage.setItem('tk_refresh', refresh);
        }
    }

    function clearAuth() {
        state.user = null;
        state.token.access = null;
        state.token.refresh = null;
        localStorage.removeItem('user');
        localStorage.removeItem('tk_access');
        localStorage.removeItem('tk_refresh');
        setIsAuthenticated(false);
        // window.location.href = '/auth/login';
    }

    function setAuth(data) {
        setToken(data.access, data.refresh);
        setUser(data.user);
        setIsAuthenticated(true);
    }

    function setIsAuthenticated(asBoolean) {
        state.isAuthenticated = asBoolean;
    }

    function validate_token() {
        (async () => {
            try {
                if (state.token.access) {
                    setIsAuthenticated(true);
                    const response = await httpAuth.auth_me();
                    setUser(response.data);
                }
            } catch (error) {
                clearAuth();
            }
        })();
    }

    const isAuthenticated = computed(() => {
        return state.isAuthenticated;
    });

    return {
        user: computed(() => state.user),
        token: computed(() => state.token),
        isAuthenticated,
        setAuth,
        validate_token,
        clearAuth
    };
});
