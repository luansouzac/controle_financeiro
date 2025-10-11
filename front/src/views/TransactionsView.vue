<template>
  <div class="transactions-view">
    <h1>Transactions</h1>
    <TransactionForm @add-transaction="addTransaction" />
    <TransactionList :transactions="transactions" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import TransactionForm from '../components/TransactionForm.vue';
import TransactionList from '../components/TransactionList.vue';

export default defineComponent({
  name: 'TransactionsView',
  components: {
    TransactionForm,
    TransactionList,
  },
  setup() {
    const transactions = ref([]);

    const addTransaction = (transaction) => {
      transactions.value.push(transaction);
    };

    return {
      transactions,
      addTransaction,
    };
  },
});
</script>

<style scoped>
.transactions-view {
  padding: 20px;
}
</style>