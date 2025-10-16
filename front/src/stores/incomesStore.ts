import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/services/api';

export interface IncomesData {
	criado_em: string,
	descricao: string,
	id: number,
	id_carteira: number,
	id_categoria: number,
	tipo: boolean,
	valor: number
}

export const useIncomesStore = defineStore('incomes', () => {
  const incomesData = ref<IncomesData[]>([]);
  const loading = ref(false);

  async function fetchIncomes(tipo?: 'receita' | 'despesa', carteira_id?: number, data_inicio?: string, data_fim?: string) {
    loading.value = true;
    incomesData.value = [];
    
    try {
      const params: any = {};
      
      if (tipo) {
        params.tipo = tipo;
      }
      if (carteira_id) {
        params.carteira_id = carteira_id;
      }
      if (data_inicio) {
        params.data_inicio = data_inicio;
      }
      if (data_fim) {
        params.data_fim = data_fim;
      }

      const response = await api.get('/user/transacoes', {
        params
      });
      incomesData.value = response.data;
    } catch (error) {
      console.error("Erro ao buscar transações:", error);
    } finally {
      loading.value = false;
    }
  }

  return { incomesData, loading, fetchIncomes };
});