<template>
  <div class="welcome-container">
    <h1>Welcome to Your Financial Control Application</h1>
    <p>This application helps you manage your finances effectively.</p>
    <p>Track your transactions, view reports, and gain insights into your financial health.</p>
    <router-link to="/dashboard" class="btn">Go to Dashboard</router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'TheWelcome',
});
</script>

<style scoped>
.welcome-container {
  text-align: center;
  margin: 20px;
}

.btn {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 5px;
}

.btn:hover {
  background-color: #367c6b;
}
</style>