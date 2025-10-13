import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/services/api';
import { useWalletStore } from './walletStore';
import { type Category } from './categoryStore'; 
import { type Wallet } from './walletStore';   
export interface Transaction {
  id: number;
  descricao: string;
  valor: number;
  tipo: 'Receita' | 'Despesa';
  criado_em: string;
  carteira: Wallet;  
  categoria: Category; 
}

export const useTransactionStore = defineStore('transactions', () => {
  const transactions = ref<Transaction[]>([]);
  const loading = ref(false);

  async function fetchTransactions() {
    loading.value = true;
    try {
      const response = await api.get('/user/transacoes');
      transactions.value = response.data;
    } catch (error) {
      console.error("Erro ao buscar transações:", error);
    } finally {
      loading.value = false;
    }
  }

  async function createTransaction(data: { id_carteira: number, id_categoria: number, tipo: boolean, valor: string, descricao: string }) {
    try {
      await api.post('/user/transacoes', data);
      await fetchTransactions(); 
      
      const walletStore = useWalletStore();
      await walletStore.fetchWallets();

    } catch (error) {
      console.error("Erro ao criar transação:", error);
      throw error;
    }
  }

  async function deleteTransaction(id: number) {
    try {
      await api.delete(`/user/transacoes/${id}`);
      await fetchTransactions();

      const walletStore = useWalletStore();
      await walletStore.fetchWallets();
      
    } catch (error) {
      console.error("Erro ao deletar transação:", error);
      throw error;
    }
  }

  return { transactions, loading, fetchTransactions, createTransaction, deleteTransaction };
});