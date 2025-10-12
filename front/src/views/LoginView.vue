<template>
  <v-sheet class="d-flex align-center justify-center" style="min-height: 100vh; background-color: #F7F8FA;">
    <v-card class="mx-auto pa-4" elevation="8" max-width="400" rounded="lg">
      <v-card-title class="text-center text-h5 font-weight-bold text-grey-darken-3">
        Bem-vindo de volta!
      </v-card-title>
      <v-card-subtitle class="text-center mb-6">
        Acesse sua conta para continuar
      </v-card-subtitle>

      <v-alert
        v-if="errorMessage"
        type="error"
        variant="tonal"
        class="mb-4"
        density="compact"
      >
        {{ errorMessage }}
      </v-alert>

      <v-form @submit.prevent="handleLogin">
        <v-text-field
          v-model="email"
          label="Email"
          type="email"
          prepend-inner-icon="mdi-email-outline"
          variant="outlined"
          density="compact"
          required
        ></v-text-field>

        <v-text-field
          v-model="senha"
          label="Senha"
          :type="showPassword ? 'text' : 'password'"
          prepend-inner-icon="mdi-lock-outline"
          :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
          @click:append-inner="showPassword = !showPassword"
          variant="outlined"
          density="compact"
          required
          class="mb-4"
        ></v-text-field>

        <v-btn
          :loading="loading"
          type="submit"
          block
          color="#0A2A4D"
          size="large"
        >
          Entrar
        </v-btn>
      </v-form>

      <v-card-text class="text-center mt-4">
        Não tem uma conta?
        <router-link to="/register" class="text-blue-darken-2 font-weight-bold">
          Cadastre-se
        </router-link>
      </v-card-text>
    </v-card>
  </v-sheet>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const email = ref('');
const senha = ref('');
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref<string | null>(null);

const authStore = useAuthStore();

async function handleLogin() {
  if (!email.value || !senha.value) {
    errorMessage.value = 'Por favor, preencha todos os campos.';
    return;
  }

  loading.value = true;
  errorMessage.value = null;

  try {
    await authStore.login({ email: email.value, senha: senha.value });
  } catch (error: any) {
    errorMessage.value = error.response?.data?.erro || 'Credenciais inválidas. Tente novamente.';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>