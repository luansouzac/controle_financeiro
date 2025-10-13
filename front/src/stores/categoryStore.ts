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

  async function createCategory(data: { nome: string, descricao: string }) {
    try {
      await api.post('/categorias_transacao', data);
      await fetchCategories();
    } catch (error) {
      console.error("Erro ao criar categoria:", error);
      throw error;
    }
  }

  async function updateCategory(id: number, data: { nome?: string, descricao?: string }) {
    try {
      await api.put(`/categorias_transacao/${id}`, data);
      await fetchCategories();
    } catch (error) {
      console.error("Erro ao atualizar categoria:", error);
      throw error;
    }
  }

  async function deleteCategory(id: number) {
    try {
      await api.delete(`/categorias_transacao/${id}`);
      await fetchCategories(); 
    } catch (error) {
      console.error("Erro ao deletar categoria:", error);
      throw error;
    }
  }

  return {
    categories,
    loading,
    fetchCategories,
    createCategory, 
    updateCategory, 
    deleteCategory, 
  };
});