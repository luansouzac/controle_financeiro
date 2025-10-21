<template>
  <v-navigation-drawer expand-on-hover permanent rail color="#0A2A4D" theme="dark">
    <v-list>
      <v-list-item
        prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
        subtitle="sandra_a88@gmail.com"
        title="Sandra Adams"
        to="/profile"
      ></v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item v-for="route in routes" 
      :key="route.name" :prepend-icon="route.icon" :title="route.name" :value="route.name" :to="route.path"></v-list-item>
      <v-list-item prepend-icon="mdi-home-outline" title="Home" value="home" to="/"></v-list-item>
      <v-list-item
        prepend-icon="mdi-swap-horizontal"
        title="Transações"
        value="transactions"
        to="/transactions"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-chart-pie-outline"
        title="Relatórios"
        value="reports"
        to="/reports"
      ></v-list-item>
    </v-list>

    <v-divider></v-divider>
    <v-list density="compact" nav>
      <v-list-item
        prepend-icon="mdi-tag-multiple-outline"
        title="Categorias"
        value="categories"
        to="/categories"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-wallet-outline"
        title="Carteiras"
        value="wallets"
        to="/wallets"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-arrow-up-bold-circle-outline"
        title="Receitas"
        value="incomes"
        to="/incomes"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-arrow-down-bold-circle-outline"
        title="Despesas"
        value="expenses"
        to="/expenses"
      ></v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item
        prepend-icon="mdi-cog-outline"
        title="Configurações"
        value="settings"
        to="/settings"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-information-outline"
        title="Sobre"
        value="about"
        to="/about"
      ></v-list-item>
    </v-list>

    <v-divider></v-divider>

    <template v-slot:append>
      <v-divider></v-divider>
      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-logout"
          title="Sair"
          value="logout"
          @click="authStore.logout()"
        ></v-list-item>
      </v-list>
    </template>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import routes from '@/router'
const authStore = useAuthStore()
</script>
