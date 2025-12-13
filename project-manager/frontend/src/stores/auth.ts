import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { authAPI } from '$lib/api';

interface User {
    id: number;
    username: string;
    email: string;
}

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
}

function createAuthStore() {
    const { subscribe, set, update } = writable<AuthState>({
        user: null,
        isAuthenticated: browser ? authAPI.isAuthenticated() : false,
        isLoading: false
    });

    return {
        subscribe,
        
        async login(email: string, password: string) {
            update(state => ({ ...state, isLoading: true }));
            try {
                await authAPI.login(email, password);
                const user = await authAPI.getCurrentUser();
                set({ user, isAuthenticated: true, isLoading: false });
                return true;
            } catch (error) {
                set({ user: null, isAuthenticated: false, isLoading: false });
                throw error;
            }
        },

        async register(username: string, email: string, password: string) {
            update(state => ({ ...state, isLoading: true }));
            try {
                await authAPI.register(username, email, password);
                await authAPI.login(username, password);
                const user = await authAPI.getCurrentUser();
                set({ user, isAuthenticated: true, isLoading: false });
                return true;
            } catch (error) {
                set({ user: null, isAuthenticated: false, isLoading: false });
                throw error;
            }
        },

        async loadUser() {
            if (!authAPI.isAuthenticated()) {
                set({ user: null, isAuthenticated: false, isLoading: false });
                return;
            }

            update(state => ({ ...state, isLoading: true }));
            try {
                const user = await authAPI.getCurrentUser();
                set({ user, isAuthenticated: true, isLoading: false });
            } catch (error) {
                authAPI.logout();
                set({ user: null, isAuthenticated: false, isLoading: false });
            }
        },

        logout() {
            authAPI.logout();
            set({ user: null, isAuthenticated: false, isLoading: false });
        }
    };
}

export const authStore = createAuthStore();
