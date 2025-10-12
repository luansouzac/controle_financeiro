<!-- TheWelcome.vue -->
<template>
  <v-sheet
    elevation="2"
    class="pa-6 rounded-lg fill-height d-flex flex-column justify-center align-center"
  >
    <v-typography variant="h4" class="mb-4 text-center">
      Welcome to Your Financial Control Application
    </v-typography>
    <v-typography variant="body1" class="mb-6 text-center">
      This application helps you manage your finances effectively. Track your transactions, view
      reports, and gain insights into your spending habits.
    </v-typography>
    <v-btn color="primary" large to="/dashboard"> Go to Dashboard </v-btn>
  </v-sheet>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'TheWelcome',
})
</script>

<style scoped>
.fill-height {
  min-height: 100%;
}
</style>
