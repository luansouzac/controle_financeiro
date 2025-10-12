<template>
  <div class="transaction-list">
    <h2>Transaction List</h2>
    <ul>
      <li v-for="transaction in transactions" :key="transaction.id">
        {{ transaction.date }} - {{ transaction.description }}: {{ transaction.amount }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'TransactionList',
  data() {
    return {
      transactions: [
        { id: 1, date: '2023-01-01', description: 'Salary', amount: 5000 },
        { id: 2, date: '2023-01-05', description: 'Groceries', amount: -150 },
        { id: 3, date: '2023-01-10', description: 'Utilities', amount: -200 },
        // Add more transactions as needed
      ],
    };
  },
});
</script>

<style scoped>
.transaction-list {
  margin: 20px;
}

.transaction-list h2 {
  font-size: 24px;
}

.transaction-list ul {
  list-style-type: none;
  padding: 0;
}

.transaction-list li {
  padding: 8px;
  border-bottom: 1px solid #ccc;
}
</style>