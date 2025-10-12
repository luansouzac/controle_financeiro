<template>
  <v-sheet class="d-flex align-center justify-center" style="min-height: 100vh; background-color: #F7F8FA;">
    <v-card class="mx-auto pa-4" elevation="8" max-width="400" rounded="lg">
      <v-card-title class="text-center text-h5 font-weight-bold text-grey-darken-3">
        Crie sua conta
      </v-card-title>
      <v-card-subtitle class="text-center mb-6">
        Comece a organizar suas finanças hoje mesmo
      </v-card-subtitle>

      <v-alert
        v-if="message"
        :type="messageType"
        variant="tonal"
        class="mb-4"
        density="compact"
      >
        {{ message }}
      </v-alert>

      <v-form @submit.prevent="handleRegister">
        <v-text-field
          v-model="nome"
          label="Nome Completo"
          prepend-inner-icon="mdi-account-outline"
          variant="outlined"
          density="compact"
          required
        ></v-text-field>

        <v-text-field
          v-model="cpf"
          label="CPF"
          prepend-inner-icon="mdi-card-account-details-outline"
          variant="outlined"
          density="compact"
          required
        ></v-text-field>

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
          Cadastrar
        </v-btn>
      </v-form>

      <v-card-text class="text-center mt-4">
        Já tem uma conta?
        <router-link to="/" class="text-blue-darken-2 font-weight-bold">
          Entre aqui
        </router-link>
      </v-card-text>
    </v-card>
  </v-sheet>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const nome = ref('');
const cpf = ref('');
const email = ref('');
const senha = ref('');
const showPassword = ref(false);
const loading = ref(false);
const message = ref<string | null>(null);
const messageType = ref<'success' | 'error'>('error');

const router = useRouter();

async function handleRegister() {
  if (!nome.value || !cpf.value || !email.value || !senha.value) {
    message.value = 'Por favor, preencha todos os campos.';
    messageType.value = 'error';
    return;
  }
  
  loading.value = true;
  message.value = null;

  try {
    await api.post('/register', {
      nome: nome.value,
      cpf: cpf.value,
      email: email.value,
      senha: senha.value
    });

    message.value = 'Cadastro realizado com sucesso! Você será redirecionado.';
    messageType.value = 'success';

    setTimeout(() => {
      router.push('/');
    }, 2000);

  } catch (error: any) {
    message.value = error.response?.data?.erro || 'Ocorreu um erro ao registrar. Tente novamente.';
    messageType.value = 'error';
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