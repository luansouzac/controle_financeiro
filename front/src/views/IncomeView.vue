<template>
  <v-container fluid class="pa-6">
    <v-row align="center">
      <v-col>
        <h1 class="text-h4 font-weight-bold text-grey-darken-3">{{ title }}</h1>
        <p class="text-medium-emphasis">{{ subtitle }}</p>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>
    
    <v-row>
      <v-col cols="12" md="8">
        <v-fade-transition appear>
          <div>
            <v-card elevation="2" rounded="lg" class="mb-6">
              <v-card-title class="text-h6 font-weight-bold">{{ chartTitle }}</v-card-title>
              <v-card-text>
                <Line :data="lineChartData" :options="lineChartOptions" height="250" />
              </v-card-text>
            </v-card>
            
            <v-card elevation="2" rounded="lg">
              <v-card-title class="text-h6 font-weight-bold">{{ detailsTitle }}</v-card-title>
              <v-list lines="two">
                <v-progress-linear 
                  v-if="incomesStore.loading" 
                  indeterminate 
                  color="primary" 
                  class="mb-2"
                ></v-progress-linear>
                <v-list-item v-for="t in incomeTransactions" :key="t.id">
                  <template v-slot:prepend>
                    <v-avatar :color="avatarColor" class="mr-4">
                      <v-icon :color="iconColor">{{ t.icon }}</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="font-weight-bold">{{ t.description }}</v-list-item-title>
                  <v-list-item-subtitle>{{ t.category }} - {{ t.date }}</v-list-item-subtitle>
                  <template v-slot:append>
                    <span class="font-weight-bold text-h6" :class="amountColor">{{ formatCurrency(t.amount) }}</span>
                  </template>
                </v-list-item>
                <v-list-item v-if="!incomesStore.loading && incomeTransactions.length === 0">
                  <v-list-item-title class="text-center text-grey">
                    Nenhuma transação encontrada
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-card>
          </div>
        </v-fade-transition>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-fade-transition appear>
          <div>
            <v-card variant="tonal" :color="cardColor" class="mb-6">
              <v-card-text>
                <p class="text-caption">{{ monthLabel }}</p>
                <h2 class="text-h4 font-weight-bold">
                  <v-progress-circular 
                    v-if="incomesStore.loading" 
                    indeterminate 
                    size="24" 
                    width="3"
                    class="mr-2"
                  ></v-progress-circular>
                  {{ formatCurrency(currentMonthIncome) }}
                </h2>
                <div class="d-flex align-center mt-2" v-if="!incomesStore.loading">
                  <v-icon :color="comparisonColor" size="small">{{ comparisonIcon }}</v-icon>
                  <span class="text-body-2 ml-1" :class="`text-${comparisonColor}`">
                    <strong>{{ comparisonPercentage.toFixed(1) }}%</strong> {{ comparisonText }} que o mês passado
                  </span>
                </div>
              </v-card-text>
            </v-card>
            
            <v-card elevation="2" rounded="lg">
              <v-card-title class="text-h6 font-weight-bold">{{ categoryTitle }}</v-card-title>
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
import { ref, computed, watch } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, PointElement, LineElement, CategoryScale, LinearScale, Filler } from 'chart.js';
import type { ChartOptions } from 'chart.js';
import { useIncomesStore } from '@/stores/incomesStore';

const props = defineProps<{
  tipo?: 'receita' | 'despesa'
  key?: string
}>();

const incomesStore = useIncomesStore();
const tipo = ref(props.tipo || 'receita');

const loadData = async () => {
  await incomesStore.fetchIncomes(tipo.value);
};

watch(() => props.tipo, (newTipo) => {
  if (newTipo) {
    tipo.value = newTipo;
    loadData();
  }
}, { immediate: true });

ChartJS.register(Title, Tooltip, Legend, PointElement, LineElement, CategoryScale, LinearScale, Filler);

const CHART_COLORS = computed(() => 
  tipo.value === 'receita' 
    ? ['#2E7D32', '#66BB6A', '#AED581', '#DCE775']
    : ['#D32F2F', '#E57373', '#FFAB91', '#FF7043']
);

const title = computed(() => 
  tipo.value === 'receita' ? 'Minhas Receitas' : 'Minhas Despesas'
);

const subtitle = computed(() => 
  tipo.value === 'receita' 
    ? 'Acompanhe a evolução e a origem dos seus ganhos.'
    : 'Analise para onde seu dinheiro está indo.'
);

const chartTitle = computed(() => 
  tipo.value === 'receita' 
    ? 'Progressão de Receitas (Últimos 6 Meses)'
    : 'Progressão de Despesas (Últimos 6 Meses)'
);

const detailsTitle = computed(() => 
  tipo.value === 'receita' 
    ? 'Detalhes das Receitas do Mês'
    : 'Detalhes das Despesas do Mês'
);

const monthLabel = computed(() => 
  tipo.value === 'receita' ? 'Receita Este Mês' : 'Despesa Este Mês'
);

const categoryTitle = computed(() => 
  tipo.value === 'receita' ? 'Receitas por Categoria' : 'Despesas por Categoria'
);

const cardColor = computed(() => tipo.value === 'receita' ? 'success' : 'error');
const avatarColor = computed(() => tipo.value === 'receita' ? 'success-lighten-4' : 'error-lighten-4');
const iconColor = computed(() => tipo.value === 'receita' ? 'success' : 'error');
const amountColor = computed(() => tipo.value === 'receita' ? 'text-success' : 'text-grey-darken-2');

const currentMonthIncome = computed(() => {
  const now = new Date();
  const currentMonth = now.getMonth() + 1;
  const currentYear = now.getFullYear();
  
  return incomesStore.incomesData
    .filter(income => {
      const incomeDate = new Date(income.criado_em);
      return incomeDate.getMonth() + 1 === currentMonth && incomeDate.getFullYear() === currentYear;
    })
    .reduce((total, income) => total + income.valor, 0);
});

const previousMonthIncome = computed(() => {
  const now = new Date();
  const previousMonth = now.getMonth() === 0 ? 12 : now.getMonth();
  const previousYear = now.getMonth() === 0 ? now.getFullYear() - 1 : now.getFullYear();
  
  return incomesStore.incomesData
    .filter(income => {
      const incomeDate = new Date(income.criado_em);
      return incomeDate.getMonth() + 1 === previousMonth && incomeDate.getFullYear() === previousYear;
    })
    .reduce((total, income) => total + income.valor, 0);
});

const incomeProgression = ref({
  labels: ['Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro'],
  data: [7200, 7350, 7800, 7500, 8100, 8050],
});

const incomeByCategory = ref([
  { name: 'Salário', total: 7200.00 },
  { name: 'Freelance', total: 850.00 },
]);

const incomeTransactions = computed(() => {
  const now = new Date();
  const currentMonth = now.getMonth() + 1;
  const currentYear = now.getFullYear();
  
  return incomesStore.incomesData
    .filter(income => {
      const incomeDate = new Date(income.criado_em);
      return incomeDate.getMonth() + 1 === currentMonth && incomeDate.getFullYear() === currentYear;
    })
    .map(income => ({
      id: income.id,
      description: income.descricao,
      category: 'Categoria',
      amount: income.valor,
      date: new Date(income.criado_em).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' }),
      icon: 'mdi-cash'
    }))
    .reverse();
});

const comparisonPercentage = computed(() => {
  if (previousMonthIncome.value === 0) return 100;
  return Math.abs(((currentMonthIncome.value - previousMonthIncome.value) / previousMonthIncome.value) * 100);
});

const isIncrease = computed(() => currentMonthIncome.value > previousMonthIncome.value);
const comparisonText = computed(() => isIncrease.value ? 'a mais' : 'a menos');

const comparisonColor = computed(() => {
  if (tipo.value === 'receita') {
    return isIncrease.value ? 'success' : 'warning';
  } else {
    return isIncrease.value ? 'warning' : 'success';
  }
});

const comparisonIcon = computed(() => isIncrease.value ? 'mdi-trending-up' : 'mdi-trending-down');

const lineChartData = computed(() => ({
  labels: incomeProgression.value.labels,
  datasets: [
    {
      label: tipo.value === 'receita' ? 'Receita Mensal' : 'Despesa Mensal',
      data: incomeProgression.value.data,
      borderColor: tipo.value === 'receita' ? '#2E7D32' : '#D32F2F',
      backgroundColor: tipo.value === 'receita' 
        ? 'rgba(102, 187, 106, 0.2)'
        : 'rgba(229, 115, 115, 0.2)',
      tension: 0.4,
      fill: true,
    },
  ],
}));

const lineChartOptions = computed((): ChartOptions<'line'> => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context) => {
          if (context.parsed.y !== null && context.parsed.y !== undefined) {
            return formatCurrency(context.parsed.y);
          }
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

const formatCurrency = (value: number) => {
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};
</script>