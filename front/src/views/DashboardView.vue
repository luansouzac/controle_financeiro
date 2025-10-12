<template>
  <div class="dashboard">
    <h1>Financial Dashboard</h1>
    <FinancialDashboard />
    <TransactionList />
    <TransactionForm />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import FinancialDashboard from '@/components/FinancialDashboard.vue';
import TransactionList from '@/components/TransactionList.vue';
import TransactionForm from '@/components/TransactionForm.vue';

export default defineComponent({
  name: 'DashboardView',
  components: {
    FinancialDashboard,
    TransactionList,
    TransactionForm,
  },
});
</script>

<style scoped>
.dashboard {
  padding: 20px;
}
</style>