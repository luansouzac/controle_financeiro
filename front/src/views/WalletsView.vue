<template>
  <v-container fluid class="pa-6">
    <v-row align="center">
      <v-col>
        <h1 class="text-h4 font-weight-bold text-grey-darken-3">Minhas Carteiras</h1>
        <p class="text-medium-emphasis">Gerencie suas contas e fontes de recursos.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn
          color="#0A2A4D"
          prepend-icon="mdi-plus-circle-outline"
          size="large"
          @click="openCreateDialog"
        >
          Adicionar Carteira
        </v-btn>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>

    <div v-if="walletStore.loading" class="text-center pa-12">
      <v-progress-circular indeterminate color="#0A2A4D" size="64"></v-progress-circular>
      <p class="mt-4 text-medium-emphasis">Buscando suas carteiras...</p>
    </div>

    <div v-else>
      <v-row v-if="walletStore.wallets.length > 0">
        <v-col
          v-for="wallet in walletStore.wallets"
          :key="wallet.id"
          cols="12"
          sm="6"
          md="4"
        >
          <v-card class="fill-height d-flex flex-column" elevation="2" rounded="lg">
            <v-card-title class="font-weight-bold d-flex align-center">
              <v-icon left class="mr-2">mdi-wallet</v-icon>
              {{ wallet.nome }}
            </v-card-title>
            <v-card-subtitle>{{ wallet.descricao }}</v-card-subtitle>

            <v-card-text class="flex-grow-1">
              <p class="text-h5 font-weight-bold" :class="getBalanceColor(wallet.saldo)">
                {{ formatCurrency(wallet.saldo) }}
              </p>
              <p class="text-caption text-grey">Saldo Atual</p>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn icon="mdi-pencil" variant="text" @click="openEditDialog(wallet)"></v-btn>
              <v-btn icon="mdi-delete" variant="text" color="error" @click="openDeleteDialog(wallet)"></v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <v-row v-else class="text-center pa-12">
        <v-col>
          <v-icon size="64" color="grey-lighten-1">mdi-wallet-plus-outline</v-icon>
          <h2 class="text-h6 mt-4 text-grey-darken-1">Nenhuma carteira encontrada</h2>
          <p class="text-medium-emphasis">Comece adicionando sua primeira conta ou carteira.</p>
          <v-btn color="#0A2A4D" class="mt-4" @click="openCreateDialog">
            Criar minha primeira carteira
          </v-btn>
        </v-col>
      </v-row>
    </div>

    <v-dialog v-model="dialog" persistent max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ isEditing ? 'Editar Carteira' : 'Nova Carteira' }}</span>
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveWallet">
            <v-text-field
              v-model="editedWallet.nome"
              label="Nome da Carteira"
              variant="outlined"
              :rules="[v => !!v || 'Nome é obrigatório']"
              required
            ></v-text-field>
            <v-textarea
              v-model="editedWallet.descricao"
              label="Descrição (Opcional)"
              variant="outlined"
              rows="3"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialogs">Cancelar</v-btn>
          <v-btn color="primary" @click="saveWallet" :loading="saving">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" persistent max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Confirmar Exclusão</v-card-title>
        <v-card-text>
          Tem certeza que deseja excluir a carteira <strong>"{{ walletToDelete?.nome }}"</strong>?
          Todas as transações associadas também serão removidas. Esta ação não pode ser desfeita.
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
import { useWalletStore, type Wallet } from '@/stores/walletStore';

const walletStore = useWalletStore();

const dialog = ref(false);
const deleteDialog = ref(false);

const saving = ref(false);
const deleting = ref(false);

const editedId = ref<number | null>(null);
const editedWallet = ref({
  nome: '',
  descricao: '',
});
const walletToDelete = ref<Wallet | null>(null);

const isEditing = computed(() => editedId.value !== null);

onMounted(() => {
  walletStore.fetchWallets();
});

const formatCurrency = (value: string) => {
  const numberValue = parseFloat(value);
  if (isNaN(numberValue)) return "R$ 0,00";
  return numberValue.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};

const getBalanceColor = (value: string) => {
  const numberValue = parseFloat(value);
  if (isNaN(numberValue) || numberValue === 0) return 'text-grey-darken-1';
  return numberValue > 0 ? 'text-green' : 'text-red';
};

const openCreateDialog = () => {
  editedId.value = null;
  editedWallet.value = { nome: '', descricao: '' };
  dialog.value = true;
};

const openEditDialog = (wallet: Wallet) => {
  editedId.value = wallet.id;
  editedWallet.value = { nome: wallet.nome, descricao: wallet.descricao };
  dialog.value = true;
};

const openDeleteDialog = (wallet: Wallet) => {
  walletToDelete.value = wallet;
  deleteDialog.value = true;
};

const closeDialogs = () => {
  dialog.value = false;
  deleteDialog.value = false;
};

async function saveWallet() {
  if (!editedWallet.value.nome) return; 
  
  saving.value = true;
  try {
    if (isEditing.value && editedId.value) {
      await walletStore.updateWallet(editedId.value, editedWallet.value);
    } else {
      await walletStore.createWallet(editedWallet.value);
    }
    closeDialogs();
  } catch (error) {
    console.error("Falha ao salvar a carteira", error);
  } finally {
    saving.value = false;
  }
}

async function confirmDelete() {
  if (!walletToDelete.value) return;

  deleting.value = true;
  try {
    await walletStore.deleteWallet(walletToDelete.value.id);
    closeDialogs();
  } catch (error) {
    console.error("Falha ao deletar a carteira", error);
  } finally {
    deleting.value = false;
  }
}
</script>