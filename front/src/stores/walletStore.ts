import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/services/api';

export interface Wallet {
  id: number;
  nome: string;
  descricao: string;
  saldo: string;
  criado_em: string;
}

export const useWalletStore = defineStore('wallets', () => {
  const wallets = ref<Wallet[]>([]);
  const loading = ref(false);

  async function fetchWallets() {
    loading.value = true;
    try {
      const response = await api.get('/user/carteiras');
      wallets.value = response.data;
    } catch (error) {
      console.error("Erro ao buscar carteiras:", error);
    } finally {
      loading.value = false;
    }
  }

  async function createWallet(data: { nome: string, descricao: string }) {
    try {
      await api.post('/carteiras', data);
      await fetchWallets();
    } catch (error) {
      console.error("Erro ao criar carteira:", error);
      throw error; 
    }
  }

  async function updateWallet(id: number, data: { nome?: string, descricao?: string }) {
    try {
      await api.put(`/carteiras/${id}`, data);
      await fetchWallets(); 
    } catch (error) {
      console.error("Erro ao atualizar carteira:", error);
      throw error;
    }
  }

  async function deleteWallet(id: number) {
    try {
      await api.delete(`/carteiras/${id}`);
      await fetchWallets(); 
    } catch (error) {
      console.error("Erro ao deletar carteira:", error);
      throw error;
    }
  }

  return {
    wallets,
    loading,
    fetchWallets,
    createWallet,
    updateWallet,
    deleteWallet,
  };
});