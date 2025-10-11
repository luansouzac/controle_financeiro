<template>
  <div class="financial-dashboard">
    <h1>Financial Dashboard</h1>
    <div class="summary">
      <h2>Overview</h2>
      <p>Total Balance: {{ totalBalance }}</p>
      <p>Total Income: {{ totalIncome }}</p>
      <p>Total Expenses: {{ totalExpenses }}</p>
    </div>
    <transaction-list :transactions="transactions" />
    <transaction-form @add-transaction="addTransaction" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import TransactionList from './TransactionList.vue';
import TransactionForm from './TransactionForm.vue';

export default defineComponent({
  name: 'FinancialDashboard',
  components: {
    TransactionList,
    TransactionForm,
  },
  setup() {
    const transactions = ref<any[]>([]);
    
    const totalBalance = computed(() => {
      return totalIncome.value - totalExpenses.value;
    });

    const totalIncome = computed(() => {
      return transactions.value
        .filter(transaction => transaction.type === 'income')
        .reduce((acc, transaction) => acc + transaction.amount, 0);
    });

    const totalExpenses = computed(() => {
      return transactions.value
        .filter(transaction => transaction.type === 'expense')
        .reduce((acc, transaction) => acc + transaction.amount, 0);
    });

    const addTransaction = (transaction: { amount: number; type: string }) => {
      transactions.value.push(transaction);
    };

    return {
      transactions,
      totalBalance,
      totalIncome,
      totalExpenses,
      addTransaction,
    };
  },
});
</script>

<style scoped>
.financial-dashboard {
  padding: 20px;
}

.summary {
  margin-bottom: 20px;
}
</style>