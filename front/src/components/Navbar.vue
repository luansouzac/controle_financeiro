<template>
  <v-navigation-drawer
    expand-on-hover
    permanent
    rail
    color="#0A2A4D"
    theme="dark"
  >
    <v-list>
      <v-list-item
        prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
        subtitle="sandra_a88@gmail.com"
        title="Sandra Adams"
      ></v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item
        prepend-icon="mdi-view-dashboard-outline"
        title="Início"
        value="dashboard"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-swap-horizontal"
        title="Transações"
        value="transactions"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-wallet-outline"
        title="Carteiras"
        value="wallets"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-credit-card-outline"
        title="Cartões"
        value="cards"
      ></v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item
        prepend-icon="mdi-arrow-up-bold-circle-outline"
        title="Receitas"
        value="income"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-arrow-down-bold-circle-outline"
        title="Despesas"
        value="expenses"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-chart-pie-outline"
        title="Relatórios"
        value="reports"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-target"
        title="Orçamentos"
        value="budgets"
      ></v-list-item>
    </v-list>
    
    <v-divider></v-divider>
    
    <v-list density="compact" nav>
      <v-list-item
        prepend-icon="mdi-account-circle-outline"
        title="Meu Perfil"
        value="profile"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-cog-outline"
        title="Configurações"
        value="settings"
      ></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
</script>