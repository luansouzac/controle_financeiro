<template>
  <v-container fluid class="pa-6">
    <v-row align="center">
      <v-col>
        <h1 class="text-h4 font-weight-bold text-grey-darken-3">Minhas Categorias</h1>
        <p class="text-medium-emphasis">Organize suas receitas e despesas.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn
          color="#0A2A4D"
          prepend-icon="mdi-plus-circle-outline"
          size="large"
          @click="openCreateDialog"
        >
          Adicionar Categoria
        </v-btn>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>

    <div v-if="categoryStore.loading" class="text-center pa-12">
      <v-progress-circular indeterminate color="#0A2A4D" size="64"></v-progress-circular>
      <p class="mt-4 text-medium-emphasis">Buscando suas categorias...</p>
    </div>

    <div v-else>
      <v-card v-if="categoryStore.categories.length > 0" elevation="2" rounded="lg">
        <v-list lines="two">
          <template v-for="(category, index) in categoryStore.categories" :key="category.id">
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar color="grey-lighten-4">
                  <v-icon color="grey-darken-1">mdi-tag-outline</v-icon>
                </v-avatar>
              </template>

              <v-list-item-title class="font-weight-bold">{{ category.nome }}</v-list-item-title>
              <v-list-item-subtitle>{{ category.descricao }}</v-list-item-subtitle>

              <template v-slot:append>
                <v-btn icon="mdi-pencil-outline" variant="text" @click="openEditDialog(category)"></v-btn>
                <v-btn icon="mdi-delete-outline" variant="text" color="error" @click="openDeleteDialog(category)"></v-btn>
              </template>
            </v-list-item>
            <v-divider v-if="index < categoryStore.categories.length - 1"></v-divider>
          </template>
        </v-list>
      </v-card>

      <v-row v-else class="text-center pa-12">
        <v-col>
          <v-icon size="64" color="grey-lighten-1">mdi-tag-plus-outline</v-icon>
          <h2 class="text-h6 mt-4 text-grey-darken-1">Nenhuma categoria encontrada</h2>
          <p class="text-medium-emphasis">Crie categorias para organizar suas transações.</p>
        </v-col>
      </v-row>
    </div>

    <v-dialog v-model="dialog" persistent max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ isEditing ? 'Editar Categoria' : 'Nova Categoria' }}</span>
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveCategory">
            <v-text-field
              v-model="editedCategory.nome"
              label="Nome da Categoria"
              variant="outlined"
              :rules="[v => !!v || 'Nome é obrigatório']"
              required
            ></v-text-field>
            <v-textarea
              v-model="editedCategory.descricao"
              label="Descrição (Opcional)"
              variant="outlined"
              rows="3"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialogs">Cancelar</v-btn>
          <v-btn color="primary" @click="saveCategory" :loading="saving">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" persistent max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Confirmar Exclusão</v-card-title>
        <v-card-text>
          Tem certeza que deseja excluir a categoria <strong>"{{ categoryToDelete?.nome }}"</strong>?
          Esta ação não pode ser desfeita.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialogs">Cancelar</v-btn>
          <v-btn color="error" @click="confirmDelete" :loading="deleting">Confirmar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useCategoryStore, type Category } from '@/stores/categoryStore';

const categoryStore = useCategoryStore();

const dialog = ref(false);
const deleteDialog = ref(false);
const saving = ref(false);
const deleting = ref(false);

const editedId = ref<number | null>(null);
const editedCategory = ref({
  nome: '',
  descricao: '',
});
const categoryToDelete = ref<Category | null>(null);

const isEditing = computed(() => editedId.value !== null);

onMounted(() => {
  categoryStore.fetchCategories();
});

const openCreateDialog = () => {
  editedId.value = null;
  editedCategory.value = { nome: '', descricao: '' };
  dialog.value = true;
};

const openEditDialog = (category: Category) => {
  editedId.value = category.id;
  editedCategory.value = { nome: category.nome, descricao: category.descricao };
  dialog.value = true;
};

const openDeleteDialog = (category: Category) => {
  categoryToDelete.value = category;
  deleteDialog.value = true;
};

const closeDialogs = () => {
  dialog.value = false;
  deleteDialog.value = false;
};

async function saveCategory() {
  if (!editedCategory.value.nome) return;
  
  saving.value = true;
  try {
    if (isEditing.value && editedId.value) {
      await categoryStore.updateCategory(editedId.value, editedCategory.value);
    } else {
      await categoryStore.createCategory(editedCategory.value);
    }
    closeDialogs();
  } catch (error) {
    console.error("Falha ao salvar a categoria", error);
  } finally {
    saving.value = false;
  }
}

async function confirmDelete() {
  if (!categoryToDelete.value) return;

  deleting.value = true;
  try {
    await categoryStore.deleteCategory(categoryToDelete.value.id);
    closeDialogs();
  } catch (error) {
    console.error("Falha ao deletar a categoria", error);
  } finally {
    deleting.value = false;
  }
}
</script> 