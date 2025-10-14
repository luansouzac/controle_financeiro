<template>
  <v-container fluid class="pa-6">
    <v-row align="center">
      <v-col>
        <h1 class="text-h4 font-weight-bold text-grey-darken-3">Minhas Receitas</h1>
        <p class="text-medium-emphasis">Acompanhe a evolução e a origem dos seus ganhos.</p>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>
    
    <v-row>
      <v-col cols="12" md="8">
        <v-fade-transition appear>
          <div>
            <v-card elevation="2" rounded="lg" class="mb-6">
              <v-card-title class="text-h6 font-weight-bold">Progressão de Receitas (Últimos 6 Meses)</v-card-title>
              <v-card-text>
                <Line :data="lineChartData" :options="lineChartOptions" height="250" />
              </v-card-text>
            </v-card>
            
            <v-card elevation="2" rounded="lg">
              <v-card-title class="text-h6 font-weight-bold">Detalhes das Receitas do Mês</v-card-title>
              <v-list lines="two">
                <v-list-item v-for="t in incomeTransactions" :key="t.id">
                  <template v-slot:prepend>
                    <v-avatar color="success-lighten-4" class="mr-4">
                      <v-icon color="success">{{ t.icon }}</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="font-weight-bold">{{ t.description }}</v-list-item-title>
                  <v-list-item-subtitle>{{ t.category }} - {{ t.date }}</v-list-item-subtitle>
                  <template v-slot:append>
                    <span class="font-weight-bold text-success text-h6">{{ formatCurrency(t.amount) }}</span>
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
            <v-card variant="tonal" color="success" class="mb-6">
              <v-card-text>
                <p class="text-caption">Receita Este Mês</p>
                <h2 class="text-h4 font-weight-bold">{{ formatCurrency(currentMonthIncome) }}</h2>
                <div class="d-flex align-center mt-2">
                  <v-icon :color="comparisonColor" size="small">{{ comparisonIcon }}</v-icon>
                  <span class="text-body-2 ml-1" :class="`text-${comparisonColor}`">
                    <strong>{{ comparisonPercentage.toFixed(1) }}%</strong> {{ comparisonText }} que o mês passado
                  </span>
                </div>
              </v-card-text>
            </v-card>
            
            <v-card elevation="2" rounded="lg">
              <v-card-title class="text-h6 font-weight-bold">Receitas por Categoria</v-card-title>
              <v-list>
                <v-list-item v-for="(cat, i) in incomeByCategory" :key="cat.name">
                  <v-list-item-title class="font-weight-medium">{{ cat.name }}</v-list-item-title>
                  <template v-slot:append>
                    <span class="font-weight-bold">{{ formatCurrency(cat.total) }}</span>
                  </template>
                  <v-progress-linear
                    :model-value="(cat.total / currentMonthIncome) * 100"
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

const currentMonthIncome = ref(8050.00);
const previousMonthIncome = ref(7500.00);
const CHART_COLORS = ['#2E7D32', '#66BB6A', '#AED581', '#DCE775'];

// Mock para o gráfico de progressão (últimos 6 meses)
const incomeProgression = ref({
  labels: ['Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro'],
  data: [7200, 7350, 7800, 7500, 8100, 8050],
});

// Mock para a lista de receitas por categoria
const incomeByCategory = ref([
  { name: 'Salário', total: 7200.00 },
  { name: 'Freelance', total: 850.00 },
]);

// Mock para a lista de transações de receita do mês
const incomeTransactions = ref([
  { id: 1, description: 'Salário Mensal', category: 'Salário', amount: 7200.00, date: '05 de out', icon: 'mdi-cash' },
  { id: 2, description: 'Projeto Website', category: 'Freelance', amount: 850.00, date: '12 de out', icon: 'mdi-laptop-account' },
]);

// --- LÓGICA DA VIEW ---

// Lógica para comparação com o mês anterior
const comparisonPercentage = computed(() => {
  if (previousMonthIncome.value === 0) return 100;
  return Math.abs(((currentMonthIncome.value - previousMonthIncome.value) / previousMonthIncome.value) * 100);
});
const isGrowth = computed(() => currentMonthIncome.value >= previousMonthIncome.value);
const comparisonText = computed(() => isGrowth.value ? 'a mais' : 'a menos');
const comparisonColor = computed(() => isGrowth.value ? 'success' : 'warning');
const comparisonIcon = computed(() => isGrowth.value ? 'mdi-trending-up' : 'mdi-trending-down');

// Configuração dos dados para o gráfico de linha
const lineChartData = computed(() => ({
  labels: incomeProgression.value.labels,
  datasets: [
    {
      label: 'Receita Mensal',
      data: incomeProgression.value.data,
      borderColor: '#2E7D32', // Verde escuro
      backgroundColor: 'rgba(102, 187, 106, 0.2)', // Verde claro com transparência
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
        label: (context) => {
          // 1. Verificamos se o valor existe e não é nulo
          if (context.parsed.y !== null && context.parsed.y !== undefined) {
            // 2. Se for um número válido, chamamos a formatação
            return formatCurrency(context.parsed.y);
          }
          // 3. Se for nulo, retornamos uma string vazia para não mostrar nada
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