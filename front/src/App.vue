<template>
  <v-app>
    <NavbarDrawer />
    <v-main>
      <v-container fluid>
        <v-card style="height: 250px">
          <TheWelcome />
        </v-card>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import NavbarDrawer from './components/Navbar.vue'
import TheWelcome from './components/TheWelcome.vue'
export default {
  name: 'App',
  components: {
    NavbarDrawer,
    TheWelcome,
  },
}
</script>

<style>
@import './assets/main.css';
</style>
