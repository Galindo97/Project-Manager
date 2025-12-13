import { writable } from 'svelte/store';

export interface AuthState {
  user: null | { id: number; username: string; email?: string };
  token: string | null;
  isAuthenticated: boolean;
}

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false
};

export const authStore = writable<AuthState>(initialState);

// Opcional: helpers para login/logout
export function login(user: AuthState['user'], token: string) {
  authStore.set({ user, token, isAuthenticated: true });
}

export function logout() {
  authStore.set(initialState);
}
