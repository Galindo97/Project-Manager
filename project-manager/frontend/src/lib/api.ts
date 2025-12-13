import { browser } from '$app/environment';

const API_BASE_URL = 'http://localhost:8000';

// Get token from localStorage
function getToken(): string | null {
    if (!browser) return null;
    return localStorage.getItem('access_token');
}

// Set token in localStorage
function setToken(token: string): void {
    if (!browser) return;
    localStorage.setItem('access_token', token);
}

// Remove token from localStorage
function removeToken(): void {
    if (!browser) return;
    localStorage.removeItem('access_token');
}

// API request helper
async function apiRequest(endpoint: string, options: RequestInit = {}) {
    const token = getToken();
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
    };

    // Merge existing headers
    if (options.headers) {
        Object.entries(options.headers).forEach(([key, value]) => {
            if (typeof value === 'string') {
                headers[key] = value;
            }
        });
    }

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        // Token expired or invalid
        removeToken();
        if (browser) {
            window.location.href = '/login';
        }
        throw new Error('Unauthorized');
    }

    if (!response.ok && response.status !== 204) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || 'Request failed');
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}

// Auth API
export const authAPI = {
    async register(username: string, email: string, password: string) {
        return apiRequest('/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password }),
        });
    },

    async login(email: string, password: string) {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Login failed' }));
            throw new Error(error.detail || 'Login failed');
        }

        const data = await response.json();
        setToken(data.access_token);
        return data;
    },

    async getCurrentUser() {
        return apiRequest('/users/me');
    },

    logout() {
        removeToken();
        if (browser) {
            window.location.href = '/login';
        }
    },

    isAuthenticated(): boolean {
        return !!getToken();
    }
};

// Tasks API
export const tasksAPI = {
    async getAll() {
        return apiRequest('/tasks');
    },

    async getById(id: number) {
        return apiRequest(`/tasks/${id}`);
    },

    async create(task: {
        title: string;
        description?: string;
        priority?: string;
        status?: string;
        category?: string;
        due_date?: string;
        project_id?: number;
    }) {
        return apiRequest('/tasks', {
            method: 'POST',
            body: JSON.stringify(task),
        });
    },

    async update(id: number, task: {
        title?: string;
        description?: string;
        priority?: string;
        status?: string;
        category?: string;
        due_date?: string;
        completed?: boolean;
        project_id?: number;
    }) {
        return apiRequest(`/tasks/${id}`, {
            method: 'PUT',
            body: JSON.stringify(task),
        });
    },

    async delete(id: number) {
        return apiRequest(`/tasks/${id}`, {
            method: 'DELETE',
        });
    }
};

// Projects API
export const projectsAPI = {
    async getAll() {
        return apiRequest('/projects');
    },

    async getById(id: number) {
        return apiRequest(`/projects/${id}`);
    },

    async create(project: {
        name: string;
        description?: string;
        status?: string;
    }) {
        return apiRequest('/projects', {
            method: 'POST',
            body: JSON.stringify(project),
        });
    },

    async update(id: number, project: {
        name?: string;
        description?: string;
        status?: string;
    }) {
        return apiRequest(`/projects/${id}`, {
            method: 'PUT',
            body: JSON.stringify(project),
        });
    },

    async delete(id: number) {
        return apiRequest(`/projects/${id}`, {
            method: 'DELETE',
        });
    }
};
