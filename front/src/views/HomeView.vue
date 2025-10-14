<template>
  <v-container fluid class="pa-6">
    <v-row>
      <v-col>
        <h1 class="text-h4 font-weight-bold text-grey-darken-3">Bem-vindo, Luan! 👋</h1>
        <p class="text-medium-emphasis">Aqui está o seu resumo financeiro de hoje.</p>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>
    
    <v-row>
      <v-col cols="12" md="8">
        <v-fade-transition appear>
          <div>
            <v-card elevation="2" rounded="lg" class="mb-6">
              <v-card-title class="text-h6 font-weight-bold">Ações Rápidas</v-card-title>
              <v-card-text class="d-flex ga-4">
                <v-btn color="success" size="large" class="flex-grow-1" prepend-icon="mdi-plus-circle-outline">
                  Nova Receita
                </v-btn>
                <v-btn color="error" size="large" class="flex-grow-1" prepend-icon="mdi-minus-circle-outline">
                  Nova Despesa
                </v-btn>
              </v-card-text>
            </v-card>
            
            <v-card elevation="2" rounded="lg">
              <v-card-title class="text-h6 font-weight-bold">Resumo das Carteiras</v-card-title>
              <v-list class="py-0">
                <v-list-item v-for="(wallet, i) in wallets" :key="wallet.id">
                  <template v-slot:prepend>
                    <v-avatar :color="walletColors[i % walletColors.length] + '-lighten-4'" class="mr-4">
                      <v-icon :color="walletColors[i % walletColors.length]">{{ wallet.icon }}</v-icon>
                    </v-avatar>
                  </template>

                  <v-list-item-title class="font-weight-bold">{{ wallet.name }}</v-list-item-title>
                  <v-list-item-subtitle>{{ formatCurrency(wallet.balance) }}</v-list-item-subtitle>

                  <template v-slot:append>
                    <div class="d-flex flex-column align-end" style="width: 120px;">
                      <span class="text-caption font-weight-bold">{{ ((wallet.balance / totalBalance) * 100).toFixed(0) }}%</span>
                      <v-progress-linear
                        :model-value="((wallet.balance / totalBalance) * 100)"
                        :color="walletColors[i % walletColors.length]"
                        height="6"
                        rounded
                        class="mt-1"
                      ></v-progress-linear>
                    </div>
                  </template>
                </v-list-item>
              </v-list>
              <v-card-actions>
                <v-btn block color="primary" variant="text" to="/wallets">Gerenciar Carteiras</v-btn>
              </v-card-actions>
            </v-card>
          </div>
        </v-fade-transition>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-fade-transition appear>
          <v-card elevation="2" rounded="lg">
            <v-card-title class="text-h6 font-weight-bold">Últimas Atividades</v-card-title>
            <v-divider></v-divider>
            <v-list lines="two">
              <v-list-item v-for="t in recentTransactions" :key="t.id">
                <template v-slot:prepend>
                  <v-avatar :color="t.type === 'receita' ? 'success-lighten-4' : 'error-lighten-4'" size="40">
                    <v-icon :color="t.type === 'receita' ? 'success' : 'error'">{{ t.icon }}</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="font-weight-medium">{{ t.description }}</v-list-item-title>
                <v-list-item-subtitle>{{ t.category }}</v-list-item-subtitle>
                <template v-slot:append>
                  <span class="font-weight-bold" :class="t.type === 'receita' ? 'text-success' : 'text-grey-darken-3'">
                    {{ formatCurrency(t.amount) }}
                  </span>
                </template>
              </v-list-item>
            </v-list>
             <v-card-actions>
                <v-btn block color="primary" variant="text" to="/transactions">Ver Todas</v-btn>
              </v-card-actions>
          </v-card>
        </v-fade-transition>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// --- DADOS MOCKADOS ---

// Mock para as carteiras
const wallets = ref([
  { id: 1, name: 'Carteira Principal', balance: 7450.50, icon: 'mdi-wallet' },
  { id: 2, name: 'Poupança', balance: 15200.00, icon: 'mdi-piggy-bank' },
  { id: 3, name: 'Investimentos', balance: 22800.75, icon: 'mdi-trending-up' },
]);

// Paleta de cores para os gráficos das carteiras
const walletColors = ref(['primary', 'teal', 'deep-purple']);

// Mock para as transações recentes
const recentTransactions = ref([
  { id: 1, description: 'Salário', category: 'Renda', amount: 7200.00, type: 'receita', icon: 'mdi-cash' },
  { id: 2, description: 'Aluguel', category: 'Moradia', amount: -1800.00, type: 'despesa', icon: 'mdi-home' },
  { id: 3, description: 'Supermercado', category: 'Alimentação', amount: -450.75, type: 'despesa', icon: 'mdi-cart' },
  { id: 4, description: 'Freelance', category: 'Renda Extra', amount: 850.00, type: 'receita', icon: 'mdi-laptop' },
  { id: 5, description: 'Cinema', category: 'Lazer', amount: -85.50, type: 'despesa', icon: 'mdi-movie' },
]);

// --- LÓGICA DA VIEW ---

// Calcula o saldo total somando todas as carteiras
const totalBalance = computed(() => {
  return wallets.value.reduce((sum, wallet) => sum + wallet.balance, 0);
});

// Função para formatar os valores em moeda brasileira
const formatCurrency = (value: number) => {
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};
</script>