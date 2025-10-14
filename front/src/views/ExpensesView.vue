<template>
  <v-container fluid class="pa-6">
    <v-row align="center">
      <v-col>
        <h1 class="text-h4 font-weight-bold text-grey-darken-3">Minhas Despesas</h1>
        <p class="text-medium-emphasis">Analise para onde seu dinheiro está indo.</p>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>
    
    <v-row>
      <v-col cols="12" md="8">
        <v-fade-transition appear>
          <div>
            <v-card elevation="2" rounded="lg" class="mb-6">
              <v-card-title class="text-h6 font-weight-bold">Progressão de Despesas (Últimos 6 Meses)</v-card-title>
              <v-card-text>
                <Line :data="lineChartData" :options="lineChartOptions" height="250" />
              </v-card-text>
            </v-card>
            
            <v-card elevation="2" rounded="lg">
              <v-card-title class="text-h6 font-weight-bold">Detalhes das Despesas do Mês</v-card-title>
              <v-list lines="two">
                <v-list-item v-for="t in expenseTransactions" :key="t.id">
                  <template v-slot:prepend>
                    <v-avatar color="error-lighten-4" class="mr-4">
                      <v-icon color="error">{{ t.icon }}</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="font-weight-bold">{{ t.description }}</v-list-item-title>
                  <v-list-item-subtitle>{{ t.category }} - {{ t.date }}</v-list-item-subtitle>
                  <template v-slot:append>
                    <span class="font-weight-bold text-grey-darken-2 text-h6">{{ formatCurrency(t.amount) }}</span>
                  </template>
                </v-list-item>
              </v-list>
            </v-card>
          </div>
        </v-fade-transition>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-fade-transition appear>
          <div>
            <v-card variant="tonal" color="error" class="mb-6">
              <v-card-text>
                <p class="text-caption">Despesa Este Mês</p>
                <h2 class="text-h4 font-weight-bold">{{ formatCurrency(currentMonthExpenses) }}</h2>
                <div class="d-flex align-center mt-2">
                  <v-icon :color="comparisonColor" size="small">{{ comparisonIcon }}</v-icon>
                  <span class="text-body-2 ml-1" :class="`text-${comparisonColor}`">
                    <strong>{{ comparisonPercentage.toFixed(1) }}%</strong> {{ comparisonText }} que o mês passado
                  </span>
                </div>
              </v-card-text>
            </v-card>
            
            <v-card elevation="2" rounded="lg">
              <v-card-title class="text-h6 font-weight-bold">Despesas por Categoria</v-card-title>
              <v-list>
                <v-list-item v-for="(cat, i) in expensesByCategory" :key="cat.name">
                  <v-list-item-title class="font-weight-medium">{{ cat.name }}</v-list-item-title>
                  <template v-slot:append>
                    <span class="font-weight-bold">{{ formatCurrency(cat.total) }}</span>
                  </template>
                  <v-progress-linear
                    :model-value="(cat.total / currentMonthExpenses) * 100"
                    :color="CHART_COLORS[i % CHART_COLORS.length]"
                    height="6"
                    rounded
                    class="mt-1"
                  ></v-progress-linear>
                </v-list-item>
              </v-list>
            </v-card>
          </div>
        </v-fade-transition>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, PointElement, LineElement, CategoryScale, LinearScale, Filler } from 'chart.js';
import type { ChartOptions } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, PointElement, LineElement, CategoryScale, LinearScale, Filler);

// --- DADOS MOCKADOS ---

const currentMonthExpenses = ref(4350.50);
const previousMonthExpenses = ref(4100.00); // Gastou mais este mês
const CHART_COLORS = ['#D32F2F', '#E57373', '#FFAB91', '#FF7043'];

// Mock para o gráfico de progressão (últimos 6 meses)
const expenseProgression = ref({
  labels: ['Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro'],
  data: [3800, 4200, 3950, 4100, 4500, 4350.50],
});

// Mock para a lista de despesas por categoria
const expensesByCategory = ref([
  { name: 'Moradia', total: 1800.00 },
  { name: 'Alimentação', total: 1150.50 },
  { name: 'Transporte', total: 650.00 },
  { name: 'Lazer', total: 450.00 },
  { name: 'Outros', total: 300.00 },
]);

// Mock para a lista de transações de despesa do mês
const expenseTransactions = ref([
  { id: 1, description: 'Aluguel', category: 'Moradia', amount: 1800.00, date: '05 de out', icon: 'mdi-home' },
  { id: 2, description: 'Supermercado', category: 'Alimentação', amount: 450.75, date: '10 de out', icon: 'mdi-cart' },
  { id: 3, description: 'Gasolina', category: 'Transporte', amount: 200.00, date: '12 de out', icon: 'mdi-gas-station' },
  { id: 4, description: 'Fatura do Cartão', category: 'Outros', amount: 1500.25, date: '14 de out', icon: 'mdi-credit-card' },
]);

// --- LÓGICA DA VIEW ---

// Lógica para comparação com o mês anterior
const comparisonPercentage = computed(() => {
  if (previousMonthExpenses.value === 0) return 100;
  return Math.abs(((currentMonthExpenses.value - previousMonthExpenses.value) / previousMonthExpenses.value) * 100);
});
// Para despesas, um aumento é negativo (warning/error), uma diminuição é positiva (success)
const isIncrease = computed(() => currentMonthExpenses.value > previousMonthExpenses.value);
const comparisonText = computed(() => isIncrease.value ? 'a mais' : 'a menos');
const comparisonColor = computed(() => isIncrease.value ? 'warning' : 'success');
const comparisonIcon = computed(() => isIncrease.value ? 'mdi-trending-up' : 'mdi-trending-down');

// Configuração dos dados para o gráfico de linha
const lineChartData = computed(() => ({
  labels: expenseProgression.value.labels,
  datasets: [
    {
      label: 'Despesa Mensal',
      data: expenseProgression.value.data,
      borderColor: '#D32F2F', // Vermelho escuro
      backgroundColor: 'rgba(229, 115, 115, 0.2)', // Vermelho claro com transparência
      tension: 0.4,
      fill: true,
    },
  ],
}));

// Configuração das opções de estilo do gráfico
const lineChartOptions = computed((): ChartOptions<'line'> => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        // ✅ CORREÇÃO APLICADA AQUI
        label: (context) => {
          // 1. Verifica se o valor 'y' do ponto existe e não é nulo
          if (context.parsed.y !== null) {
            // 2. Se for um número válido, formata como moeda
            return formatCurrency(context.parsed.y);
          }
          // 3. Se for nulo, retorna uma string vazia para não exibir nada
          return '';
        },
      },
    },
  },
  scales: {
    y: {
      beginAtZero: false,
      grid: { color: '#EEEEEE' },
      ticks: { callback: (value) => `R$ ${value}` },
    },
    x: { grid: { display: false } },
  },
}));

// Função para formatar valores em moeda
const formatCurrency = (value: number) => {
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};
</script>