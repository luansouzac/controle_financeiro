<template>
  <v-app>
    <v-layout>
      <Navbar />

      <v-main style="background-color: #F7F8FA;">
        <router-view />
      </v-main>
    </v-layout>
  </v-app>
</template>

<script setup lang="ts">
  import Navbar from '@/components/Navbar.vue';
</script>

<style>
@import './assets/main.css';
</style>