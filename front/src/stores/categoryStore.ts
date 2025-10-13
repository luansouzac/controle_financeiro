import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/services/api';

export interface Category {
  id: number;
  nome: string;
  descricao: string;
}

export const useCategoryStore = defineStore('categories', () => {
  const categories = ref<Category[]>([]);
  const loading = ref(false); 

  async function fetchCategories() {
    loading.value = true; 
    try {
      const response = await api.get('/categorias_transacao');
      categories.value = response.data;
    } catch (error) {
      console.error("Erro ao buscar categorias:", error);
    } finally {
      loading.value = false; 
    }
  }

  return { categories, loading, fetchCategories };
});