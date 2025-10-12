<template>
  <div class="transaction-form">
    <h2>Add New Transaction</h2>
    <form @submit.prevent="submitTransaction">
      <div>
        <label for="description">Description:</label>
        <input type="text" v-model="transaction.description" required />
      </div>
      <div>
        <label for="amount">Amount:</label>
        <input type="number" v-model="transaction.amount" required />
      </div>
      <div>
        <label for="date">Date:</label>
        <input type="date" v-model="transaction.date" required />
      </div>
      <button type="submit">Add Transaction</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'TransactionForm',
  setup() {
    const transaction = ref({
      description: '',
      amount: 0,
      date: ''
    });

    const submitTransaction = () => {
      // Logic to handle the transaction submission
      console.log('Transaction submitted:', transaction.value);
      // Reset the form
      transaction.value = { description: '', amount: 0, date: '' };
    };

    return {
      transaction,
      submitTransaction
    };
  }
});
</script>

<style scoped>
.transaction-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.transaction-form h2 {
  text-align: center;
}

.transaction-form div {
  margin-bottom: 15px;
}

.transaction-form label {
  display: block;
  margin-bottom: 5px;
}

.transaction-form input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.transaction-form button {
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.transaction-form button:hover {
  background-color: #218838;
}
</style>