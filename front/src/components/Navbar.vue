<template>
  <v-navigation-drawer expand-on-hover permanent rail color="#0A2A4D" theme="dark">
    <v-list>
      <v-list-item
        :prepend-avatar="authStore.avatarDataUrl || 'https://i.pravatar.cc/150?u=placeholder'"
        :subtitle="authStore.user?.email"
        :title="authStore.user?.nome"
        to="/settings"
      ></v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item
        v-for="route in navigationRoutes"
        :key="route.name"
        :prepend-icon="route.icon"
        :title="route.name"
        :value="route.name"
        :to="route.path"
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
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { routes } from '@/router'

const authStore = useAuthStore()

const routeConfig = {
  Home: { icon: 'mdi-home-outline' },
  Transações: { icon: 'mdi-swap-horizontal' },
  Relatórios: { icon: 'mdi-chart-pie-outline' },
  Categorias: { icon: 'mdi-tag-multiple-outline' },
  Carteiras: { icon: 'mdi-wallet-outline' },
  Receitas: { icon: 'mdi-arrow-up-bold-circle-outline' },
  Despesas: { icon: 'mdi-arrow-down-bold-circle-outline' },
  Configurações: { icon: 'mdi-cog-outline' },
  Sobre: { icon: 'mdi-information-outline' },
}

const navigationRoutes = computed(() => {
  const publicPages = ['Login', 'Register']

  return routes
    .filter((route) => !publicPages.includes(route.name as string))
    .map((route) => ({
      name: route.name,
      path: route.path,
      icon: routeConfig[route.name as keyof typeof routeConfig]?.icon || 'mdi-circle-outline',
    }))
})
</script>
