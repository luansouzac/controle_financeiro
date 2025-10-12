<template>
  <div class="home">
    <TheWelcome />
    <FinancialDashboard />
    <TransactionList />
    <TransactionForm />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import TheWelcome from '../components/TheWelcome.vue';
import FinancialDashboard from '../components/FinancialDashboard.vue';
import TransactionList from '../components/TransactionList.vue';
import TransactionForm from '../components/TransactionForm.vue';

export default defineComponent({
  name: 'HomeView',
  components: {
    TheWelcome,
    FinancialDashboard,
    TransactionList,
    TransactionForm,
  },
});
</script>

<style scoped>
.home {
  padding: 20px;
}
</style>