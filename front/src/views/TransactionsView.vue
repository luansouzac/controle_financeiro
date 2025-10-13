<template>
  <v-container fluid class="pa-6">
    <v-row align="center">
      <v-col>
        <h1 class="text-h4 font-weight-bold text-grey-darken-3">Transações</h1>
        <p class="text-medium-emphasis">Visualize e adicione suas receitas e despesas.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn
          color="#0A2A4D"
          prepend-icon="mdi-plus-circle-outline"
          size="large"
          @click="openCreateDialog"
        >
          Nova Transação
        </v-btn>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>

    <div v-if="isLoading" class="text-center pa-12">
      <v-progress-circular indeterminate color="#0A2A4D" size="64"></v-progress-circular>
      <p class="mt-4 text-medium-emphasis">Carregando dados...</p>
    </div>

    <div v-else>
      <v-card v-if="transactionStore.transactions.length > 0" elevation="2" rounded="lg">
        <v-list lines="two">
          <template
            v-for="(transaction, index) in transactionStore.transactions"
            :key="transaction.id"
          >
            <v-list-item>
              <template v-slot:prepend>
                <v-avatar
                  :color="transaction.tipo === 'Receita' ? 'green-lighten-4' : 'red-lighten-4'"
                >
                  <v-icon :color="transaction.tipo === 'Receita' ? 'green' : 'red'">
                    {{ transaction.tipo === 'Receita' ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
                  </v-icon>
                </v-avatar>
              </template>

              <v-list-item-title class="font-weight-bold">{{
                transaction.descricao
              }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ transaction.categoria.nome }} em {{ transaction.carteira.nome }}
              </v-list-item-subtitle>

              <template v-slot:append>
                <div class="text-right">
                  <p
                    class="font-weight-bold"
                    :class="transaction.tipo === 'Receita' ? 'text-green' : 'text-red'"
                  >
                    {{ formatCurrency(transaction.valor) }}
                  </p>
                  <p class="text-caption text-grey">{{ formatDate(transaction.criado_em) }}</p>
                </div>
                <v-btn
                  icon="mdi-delete-outline"
                  variant="text"
                  color="grey"
                  size="small"
                  class="ml-2"
                  @click="openDeleteDialog(transaction)"
                ></v-btn>
              </template>
            </v-list-item>
            <v-divider v-if="index < transactionStore.transactions.length - 1"></v-divider>
          </template>
        </v-list>
      </v-card>

      <v-row v-else class="text-center pa-12">
        <v-col>
          <v-icon size="64" color="grey-lighten-1">mdi-swap-horizontal-bold</v-icon>
          <h2 class="text-h6 mt-4 text-grey-darken-1">Nenhuma transação registrada</h2>
          <p class="text-medium-emphasis">
            Clique no botão para adicionar sua primeira receita ou despesa.
          </p>
        </v-col>
      </v-row>
    </div>

    <v-dialog v-model="createDialog" persistent max-width="600px">
      <v-card>
        <v-card-title><span class="text-h5">Nova Transação</span></v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveTransaction">
            <v-switch
              v-model="newTransaction.isRecipe"
              :label="newTransaction.isRecipe ? 'Receita' : 'Despesa'"
              color="primary"
            ></v-switch>
            <v-text-field
              v-model="valorFormatado"
              label="Valor"
              prefix="R$"
              variant="outlined"
              required
              inputmode="numeric"
              :class="{ 'text-error': !newTransaction.isRecipe }"
              :color="newTransaction.isRecipe ? 'primary' : 'error'"
            ></v-text-field>
            <v-text-field
              v-model="newTransaction.descricao"
              label="Descrição"
              variant="outlined"
              required
            ></v-text-field>
            <v-select
              v-model="newTransaction.id_carteira"
              :items="walletStore.wallets"
              item-title="nome"
              item-value="id"
              label="Carteira"
              variant="outlined"
              required
            ></v-select>
            <v-select
              v-model="newTransaction.id_categoria"
              :items="categoryStore.categories"
              item-title="nome"
              item-value="id"
              label="Categoria"
              variant="outlined"
              required
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialogs">Cancelar</v-btn>
          <v-btn color="primary" @click="saveTransaction" :loading="saving">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" persistent max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Confirmar Exclusão</v-card-title>
        <v-card-text>
          Tem certeza que deseja excluir a transação
          <strong>"{{ transactionToDelete?.descricao }}"</strong>? Esta ação irá reverter o valor no
          saldo da carteira.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialogs">Cancelar</v-btn>
          <v-btn color="error" @click="handleConfirmDelete" :loading="deleting">Confirmar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useTransactionStore, type Transaction } from '@/stores/transactionStore'
import { useWalletStore } from '@/stores/walletStore'
import { useCategoryStore } from '@/stores/categoryStore'

const transactionStore = useTransactionStore()
const walletStore = useWalletStore()
const categoryStore = useCategoryStore()

const createDialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const transactionToDelete = ref<Transaction | null>(null)

const isLoading = computed(() => {
  return transactionStore.loading || walletStore.loading || categoryStore.loading
})

const newTransaction = ref({
  isRecipe: true,
  valor: '',
  descricao: '',
  id_carteira: null as number | null,
  id_categoria: null as number | null,
})

const valorFormatado = ref('')

watch(valorFormatado, (newValue) => {
  const digits = newValue.toString().replace(/\D/g, '')
  if (!digits) {
    newTransaction.value.valor = ''
    return
  }

  newTransaction.value.valor = (parseInt(digits, 10) / 100).toFixed(2)

  const formattedForDisplay = (parseInt(digits, 10) / 100).toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
  })

  if (formattedForDisplay !== valorFormatado.value) {
    valorFormatado.value = formattedForDisplay
  }
})

onMounted(() => {
  walletStore.fetchWallets()
  categoryStore.fetchCategories()
  transactionStore.fetchTransactions()
})

const openCreateDialog = () => {
  newTransaction.value = {
    isRecipe: true,
    valor: '',
    descricao: '',
    id_carteira: null,
    id_categoria: null,
  }
  valorFormatado.value = ''
  createDialog.value = true
}

const openDeleteDialog = (transaction: Transaction) => {
  transactionToDelete.value = transaction
  deleteDialog.value = true
}

const closeDialogs = () => {
  createDialog.value = false
  deleteDialog.value = false
}

async function saveTransaction() {
  if (
    !newTransaction.value.valor ||
    !newTransaction.value.id_carteira ||
    !newTransaction.value.id_categoria
  ) {
    alert('Por favor, preencha os campos obrigatórios.')
    return
  }
  saving.value = true
  try {
    await transactionStore.createTransaction({
      id_carteira: newTransaction.value.id_carteira,
      id_categoria: newTransaction.value.id_categoria,
      tipo: newTransaction.value.isRecipe,
      valor: newTransaction.value.valor,
      descricao: newTransaction.value.descricao,
    })
    closeDialogs()
  } catch (error) {
    console.error('Falha ao salvar a transação', error)
  } finally {
    saving.value = false
  }
}

async function handleConfirmDelete() {
  if (!transactionToDelete.value) return
  deleting.value = true
  try {
    await transactionStore.deleteTransaction(transactionToDelete.value.id)
    closeDialogs()
  } catch (error) {
    console.error('Falha ao deletar a transação', error)
  } finally {
    deleting.value = false
  }
}

const formatCurrency = (value: number) =>
  value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

const formatDate = (dateString: string) =>
  new Date(dateString).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' })
</script>
