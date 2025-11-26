import { defineStore } from 'pinia';
import api from '@/services/api';
import { ref } from 'vue';
import router from '@/router';

export interface User {
  id: number;
  nome: string;
  email: string;
  cpf: string;
  criado_em: string;
  image: string | null;
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref(sessionStorage.getItem('authToken') || null);
  const user = ref<User | null>(null);

  const avatarDataUrl = ref<string | null>(null);
  async function fetchAvatar() {
    if (avatarDataUrl.value && avatarDataUrl.value.startsWith('blob:')) {
      URL.revokeObjectURL(avatarDataUrl.value);
    }
    avatarDataUrl.value = null;

    if (user.value?.image) {
      try {
        const response = await api.get('/user/get_image', {
          responseType: 'blob',
        });
        avatarDataUrl.value = URL.createObjectURL(response.data);
      } catch (error) {
        console.error("Erro ao carregar a imagem de perfil:", error);
        avatarDataUrl.value = null;
      }
    }
  }

  async function fetchUser() {
    if (!token.value) return;
    try {
      const response = await api.get('/user');
      user.value = response.data;
      await fetchAvatar();

    } catch (error) {
      logout();
    }
  }

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

  function logout() {
    token.value = null;
    user.value = null;
    sessionStorage.removeItem('authToken');

    if (avatarDataUrl.value && avatarDataUrl.value.startsWith('blob:')) {
      URL.revokeObjectURL(avatarDataUrl.value);
    }
    avatarDataUrl.value = null;
    router.push('/login');
  }

   async function updateUser(data: { nome?: string, email?: string, senha?: string }) {
    try {
      const response = await api.put('/user', data);
      user.value = response.data; 
    } catch (error) {
      console.error("Erro ao atualizar o perfil:", error);
      throw error; 
    }
  }


  return { token, user, avatarDataUrl, login, fetchUser, logout, updateUser };
});