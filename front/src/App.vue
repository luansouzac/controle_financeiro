<template>
  <v-app>
    <v-layout>
      <Navbar />

      <v-main style="background-color: #f7f8fa;">
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