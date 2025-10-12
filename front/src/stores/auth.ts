import { defineStore } from 'pinia';
import api from '@/services/api';
import { ref } from 'vue';
import router from '@/router';

export const useAuthStore = defineStore('auth', () => {
  const token = ref(sessionStorage.getItem('authToken') || null);
  const user = ref(null);

  async function login(credentials: { email: string, senha: string }) {
    try {
      const response = await api.post('/login', credentials);
      token.value = response.data.access_token;

      if (token.value) {
        sessionStorage.setItem('authToken', token.value);
      }

      await fetchUser();
      router.push('/');
    } catch (error) {
      console.error("Erro no login:", error);
    }
  }

  async function fetchUser() {
    if (!token.value) return;
    try {
      const response = await api.get('/user');
      user.value = response.data;
    } catch (error) {
      logout();
    }
  }

  function logout() {
    token.value = null;
    user.value = null;
    sessionStorage.removeItem('authToken');
    router.push('/login');
  }

  return { token, user, login, fetchUser, logout };
});