<template>
  <v-container fluid class="pa-0 fill-height">
    <v-row no-gutters class="fill-height">
      <v-col
        cols="12"
        md="6"
        class="d-none d-md-flex align-center justify-center"
        style="background-color: #0A2A4D;"
      >
        <v-fade-transition appear>
          <div class="text-center">
            <v-icon
              icon="mdi-finance"
              size="64"
              color="white"
              class="mb-4"
            ></v-icon>
            <h1 class="text-h4 font-weight-bold text-white mb-2">
              Seu Controle Financeiro
            </h1>
            <p class="text-subtitle-1 text-grey-lighten-2">
              Organize suas finanças de forma inteligente.
            </p>
          </div>
        </v-fade-transition>
      </v-col>

      <v-col
        cols="12"
        md="6"
        class="d-flex align-center justify-center"
        style="background-color: #F7F8FA;"
      >
        <v-fade-transition appear>
          <v-sheet class="pa-6 pa-md-8" rounded="lg" width="100%" max-width="450">
            <h2 class="text-h5 font-weight-bold text-grey-darken-4 mb-2">
              Bem-vindo de volta!
            </h2>
            <p class="text-subtitle-1 text-grey-darken-1 mb-6">
              Acesse sua conta para continuar.
            </p>

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
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="senha"
                label="Senha"
                :type="showPassword ? 'text' : 'password'"
                prepend-inner-icon="mdi-lock-outline"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                class="mb-4"
              ></v-text-field>

              <v-btn
                :loading="loading"
                type="submit"
                block
                color="#0A2A4D"
                size="large"
                class="text-white"
              >
                Entrar
              </v-btn>
            </v-form>

            <p class="text-center mt-6 text-grey-darken-1">
              Não tem uma conta?
              <router-link to="/register" class="text-blue-darken-2 font-weight-bold">
                Cadastre-se
              </router-link>
            </p>
          </v-sheet>
        </v-fade-transition>
      </v-col>
    </v-row>
  </v-container>
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