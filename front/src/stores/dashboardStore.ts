import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/services/api';

export interface DashboardData {
  total_receitas: string;
  total_despesas: string;
  saldo_do_mes: string;
}

export const useDashboardStore = defineStore('dashboard', () => {
  const dashboardData = ref<DashboardData>({
    total_receitas: "0.00",
    total_despesas: "0.00",
    saldo_do_mes: "0.00",
  });
  const loading = ref(false);

  async function fetchDashboardData(mes?: number, ano?: number) {
    loading.value = true;
    try {
      const response = await api.get('/user/dashboard', {
        params: { mes, ano }
      });
      dashboardData.value = response.data;
    } catch (error) {
      console.error("Erro ao buscar dados do dashboard:", error);
    } finally {
      loading.value = false;
    }
  }

  return { dashboardData, loading, fetchDashboardData };
});