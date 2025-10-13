<template>
  <v-container fluid class="pa-6">
    <v-row align="center">
      <v-col>
        <h1 class="text-h4 font-weight-bold text-grey-darken-3">Resumo Financeiro</h1>
        <p class="text-medium-emphasis">Sua performance financeira no mês atual.</p>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>

    <div v-if="isLoading" class="text-center pa-12">
      <v-progress-circular indeterminate color="#0A2A4D" size="64"></v-progress-circular>
      <p class="mt-4 text-medium-emphasis">Analisando seus dados...</p>
    </div>

    <div v-else>
      <v-row>
        <v-col cols="12" md="8">
          <v-fade-transition appear>
            <div>
              <v-row>
                <v-col cols="12" sm="4">
                  <v-card variant="tonal" color="success">
                    <v-card-text>
                      <p class="text-caption">Receitas do Mês</p>
                      <h3 class="text-h5 font-weight-bold">{{ formatCurrency(monthlyIncome) }}</h3>
                    </v-card-text>
                    <v-sparkline
                      :model-value="incomeTrend"
                      color="success"
                      height="50"
                      line-width="2"
                      padding="12"
                      fill
                    ></v-sparkline>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="4">
                  <v-card variant="tonal" color="error">
                    <v-card-text>
                      <p class="text-caption">Despesas do Mês</p>
                      <h3 class="text-h5 font-weight-bold">{{ formatCurrency(monthlyExpenses) }}</h3>
                    </v-card-text>
                    <v-sparkline
                      :model-value="expenseTrend"
                      color="error"
                      height="50"
                      line-width="2"
                      padding="12"
                      fill
                    ></v-sparkline>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="4">
                  <v-card variant="tonal" color="primary">
                    <v-card-text>
                      <p class="text-caption">Balanço do Mês</p>
                      <h3 class="text-h5 font-weight-bold">{{ formatCurrency(monthlyBalance) }}</h3>
                    </v-card-text>
                    <v-sparkline
                      :model-value="balanceTrend"
                      :color="monthlyBalance >= 0 ? 'primary' : 'error'"
                      height="50"
                      line-width="2"
                      padding="12"
                    ></v-sparkline>
                  </v-card>
                </v-col>
              </v-row>

              <v-card elevation="2" rounded="lg" class="mt-6">
                <v-card-title class="text-h6 font-weight-bold">Principais Despesas do Mês</v-card-title>
                <v-list v-if="expensesByCategory.length > 0">
                  <v-list-item v-for="(category, i) in expensesByCategory" :key="category.name">
                    <v-list-item-title class="font-weight-bold">{{ category.name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ formatCurrency(category.total) }}</v-list-item-subtitle>
                    <template v-slot:append>
                      <span class="text-caption text-grey-darken-1">{{ category.percentage.toFixed(0) }}%</span>
                    </template>
                    <v-progress-linear
                      :model-value="category.percentage"
                      :color="CHART_COLORS[i % CHART_COLORS.length]"
                      height="6"
                      rounded
                      class="mt-1"
                    ></v-progress-linear>
                  </v-list-item>
                </v-list>
                <div v-else class="text-center pa-8 text-medium-emphasis">
                  <v-icon size="48" color="grey-lighten-1">mdi-tag-off-outline</v-icon>
                  <p class="mt-2">Nenhuma despesa registrada este mês.</p>
                </div>
              </v-card>

            </div>
          </v-fade-transition>
        </v-col>

        <v-col cols="12" md="4">
          <v-fade-transition appear>
            <div>
              <v-card elevation="2" rounded="lg" class="mb-6">
                 <v-list-item>
                  <template v-slot:prepend><v-icon color="primary">mdi-wallet</v-icon></template>
                  <v-list-item-title class="font-weight-bold">Saldo Total</v-list-item-title>
                  <template v-slot:append>
                    <span class="text-h6 font-weight-bold" :class="totalBalance >= 0 ? 'text-grey-darken-3' : 'text-error'">
                      {{ formatCurrency(totalBalance) }}
                    </span>
                  </template>
                 </v-list-item>
              </v-card>
              
              <v-card elevation="2" rounded="lg">
                <v-card-title class="text-h6 font-weight-bold">Transações Recentes</v-card-title>
                <v-divider></v-divider>
                <v-list lines="two" v-if="recentTransactions.length > 0">
                  <v-list-item v-for="t in recentTransactions" :key="t.id">
                    <template v-slot:prepend>
                      <v-avatar :color="t.tipo === 'Receita' ? 'success-lighten-4' : 'error-lighten-4'" size="40">
                        <v-icon :color="t.tipo === 'Receita' ? 'success' : 'error'">
                          {{ t.tipo === 'Receita' ? 'mdi-arrow-up-thin' : 'mdi-arrow-down-thin' }}
                        </v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title class="font-weight-medium">{{ t.descricao }}</v-list-item-title>
                    <v-list-item-subtitle>{{ t.categoria.nome }}</v-list-item-subtitle>
                    <template v-slot:append>
                      <span class="font-weight-bold" :class="t.tipo === 'Receita' ? 'text-success' : 'text-grey-darken-3'">{{ formatCurrency(t.valor) }}</span>
                    </template>
                  </v-list-item>
                </v-list>
                <div v-else class="text-center pa-8 text-medium-emphasis">
                  <p>Nenhuma transação recente.</p>
                </div>
              </v-card>
            </div>
          </v-fade-transition>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useDashboardStore } from '@/stores/dashboardStore';
import { useTransactionStore } from '@/stores/transactionStore';
import { useWalletStore } from '@/stores/walletStore';

const dashboardStore = useDashboardStore();
const transactionStore = useTransactionStore();
const walletStore = useWalletStore();

const isLoading = computed(() => dashboardStore.loading || transactionStore.loading || walletStore.loading);

const totalBalance = computed(() => walletStore.wallets.reduce((sum, wallet) => sum + parseFloat(wallet.saldo), 0));
const monthlyIncome = computed(() => parseFloat(dashboardStore.dashboardData?.total_receitas || '0'));
const monthlyExpenses = computed(() => parseFloat(dashboardStore.dashboardData?.total_despesas || '0'));
const monthlyBalance = computed(() => parseFloat(dashboardStore.dashboardData?.saldo_do_mes || '0'));
const recentTransactions = computed(() => [...transactionStore.transactions].sort((a, b) => new Date(b.criado_em).getTime() - new Date(a.criado_em).getTime()).slice(0, 5));

const TREND_DAYS = 7;
const CHART_COLORS = ['#0A2A4D', '#2ECC71', '#FF6384', '#FFCE56', '#4BC0C0', '#9966FF'];

const getTrendData = (type: 'Receita' | 'Despesa' | 'Saldo') => {
  const trendData = Array(TREND_DAYS).fill(0);
  const today = new Date();
  const recent = transactionStore.getTransactionsFromLastDays(TREND_DAYS);

  recent.forEach(t => {
    const transactionDate = new Date(t.criado_em);
    const diffDays = Math.floor((today.getTime() - transactionDate.getTime()) / (1000 * 3600 * 24));
    const index = TREND_DAYS - 1 - diffDays;
    
    if (index >= 0) {
      if (type === 'Saldo') {
        trendData[index] += t.tipo === 'Receita' ? t.valor : -t.valor;
      } else if (t.tipo === type) {
        trendData[index] += t.valor;
      }
    }
  });
  
  if (type === 'Saldo') {
    for (let i = 1; i < trendData.length; i++) {
      trendData[i] += trendData[i - 1];
    }
  }

  return trendData.length > 1 ? trendData : [0, ...trendData];
};

const incomeTrend = computed(() => getTrendData('Receita'));
const expenseTrend = computed(() => getTrendData('Despesa'));
const balanceTrend = computed(() => getTrendData('Saldo'));

const expensesByCategory = computed(() => {
  if (monthlyExpenses.value === 0) return [];
  
  const expenses = transactionStore.transactions.filter(t => t.tipo === 'Despesa');
  const totals: { [key: string]: number } = {};
  expenses.forEach(t => {
    totals[t.categoria.nome] = (totals[t.categoria.nome] || 0) + t.valor;
  });

  return Object.entries(totals)
    .map(([name, total]) => ({
      name,
      total,
      percentage: (total / monthlyExpenses.value) * 100,
    }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 5); 
});

onMounted(() => {
  dashboardStore.fetchDashboardData();
  transactionStore.fetchTransactions();
  walletStore.fetchWallets();
});

const formatCurrency = (value: number) => {
  if (isNaN(value)) return 'R$ 0,00';
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};
</script>