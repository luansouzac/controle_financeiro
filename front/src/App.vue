<template>
  <v-app>
    <v-layout>
      <Navbar v-if="shouldShowNavbar" />

      <v-main>
        <router-view />
      </v-main>
    </v-layout>
  </v-app>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from './components/Navbar.vue';

const route = useRoute();

const shouldShowNavbar = computed(() => {
  return route.name !== 'Login' && route.name !== 'Register';
});
</script>

<style>
@import './assets/main.css';
</style>