<template>
  <v-container fluid class="pa-6">
    <v-row>
      <v-col>
        <h1 class="text-h4 font-weight-bold text-grey-darken-3">Configurações</h1>
        <p class="text-medium-emphasis">Gerencie seu perfil, aparência e dados da conta.</p>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>

    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-fade-transition appear>
          <div>
            <v-card elevation="2" rounded="lg" class="mb-8">
              <v-card-title class="text-h6 font-weight-bold">Meu Perfil</v-card-title>
              <v-divider></v-divider>
              <v-form @submit.prevent="handleSaveChanges">
                <v-card-text>
                  <v-row align="center">
                    <v-col cols="12" sm="4" class="d-flex justify-center align-center">
                      <input
                        type="file"
                        ref="fileInput"
                        hidden
                        accept="image/png, image/jpeg, image/gif"
                        @change="onFileSelected"
                      />
                      <div class="position-relative">
                        <v-avatar size="120">
                          <v-img :src="avatarSrc" alt="Foto do Usuário" cover></v-img>
                          <v-overlay
                            v-model="uploading"
                            contained
                            class="align-center justify-center"
                          >
                            <v-progress-circular indeterminate color="white"></v-progress-circular>
                          </v-overlay>
                        </v-avatar>
                        <v-btn
                          icon="mdi-pencil"
                          size="small"
                          class="position-absolute"
                          style="bottom: 0; right: 0"
                          :disabled="uploading"
                          @click="onAvatarClick"
                        ></v-btn>
                      </div>
                    </v-col>
                    <v-col cols="12" sm="8">
                      <v-text-field
                        v-model="profile.nome"
                        label="Nome Completo"
                        prepend-inner-icon="mdi-account-outline"
                        variant="outlined"
                        class="mb-4"
                      ></v-text-field>
                      <v-text-field
                        v-model="profile.email"
                        label="Email"
                        type="email"
                        prepend-inner-icon="mdi-email-outline"
                        variant="outlined"
                        class="mb-4"
                      ></v-text-field>
                      <v-text-field
                        v-model="profile.cpf"
                        label="CPF"
                        prepend-inner-icon="mdi-card-account-details-outline"
                        variant="outlined"
                        readonly
                        disabled
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-card-text>
                <v-card-actions class="pa-4">
                  <v-btn variant="outlined" @click="passwordDialog = true">Alterar Senha</v-btn>
                  <v-spacer></v-spacer>
                  <v-btn size="large" color="primary" type="submit" :loading="saving"
                    >Salvar Alterações</v-btn
                  >
                </v-card-actions>
              </v-form>
            </v-card>

            <v-card elevation="2" rounded="lg" class="mb-8">
              <v-card-title class="text-h6 font-weight-bold">Aparência</v-card-title>
              <v-list class="py-0">
                <v-list-item>
                  <v-list-item-title>Modo Escuro</v-list-item-title>
                  <template v-slot:append>
                    <v-switch
                      v-model="isDarkMode"
                      @change="toggleTheme"
                      color="primary"
                      inset
                      hide-details
                    ></v-switch>
                  </template>
                </v-list-item>
              </v-list>
            </v-card>
          </div>
        </v-fade-transition>
      </v-col>
    </v-row>

    <v-dialog v-model="passwordDialog" persistent max-width="450px">
      <v-card>
        <v-card-title class="text-h5">Alterar Senha</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="handleUpdatePassword">
            <v-text-field
              v-model="passwordData.current"
              label="Senha Atual"
              type="password"
              prepend-inner-icon="mdi-lock-outline"
              variant="outlined"
              class="mb-4"
              hint="Funcionalidade a implementar no backend"
              persistent-hint
            ></v-text-field>
            <v-text-field
              v-model="passwordData.new"
              label="Nova Senha"
              type="password"
              prepend-inner-icon="mdi-lock-plus-outline"
              variant="outlined"
              class="mb-4"
            ></v-text-field>
            <v-text-field
              v-model="passwordData.confirm"
              label="Confirmar Nova Senha"
              type="password"
              prepend-inner-icon="mdi-lock-check-outline"
              variant="outlined"
              :rules="[(v) => v === passwordData.new || 'As senhas não coincidem']"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="passwordDialog = false">Cancelar</v-btn>
          <v-btn color="primary" @click="handleUpdatePassword" :loading="passwordSaving"
            >Salvar Nova Senha</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" persistent max-width="450px">
      <v-card>
        <v-card-title class="text-h5 bg-error">Confirmar Exclusão de Conta</v-card-title>
        <v-card-text class="pt-4">
          Você tem certeza absoluta? Esta ação não pode ser desfeita. Para confirmar, digite
          <strong>deletar</strong> no campo abaixo.
          <v-text-field
            v-model="deleteConfirmationText"
            label="Confirmar"
            class="mt-4"
          ></v-text-field>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="3000">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from 'vuetify'
import api from '@/services/api'

const authStore = useAuthStore()
const theme = useTheme()

const saving = ref(false)
const deleting = ref(false)
const passwordSaving = ref(false)
const deleteDialog = ref(false)
const passwordDialog = ref(false)
const deleteConfirmationText = ref('')
const snackbar = ref({ show: false, message: '', color: 'success' })
const uploading = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const profile = ref({ nome: '', email: '', cpf: '' })
const passwordData = ref({ current: '', new: '', confirm: '' })

const avatarSrc = computed(
  () => authStore.avatarDataUrl || 'https://www.pngarts.com/pt/explore/tag/imagem-de-perfil-padrao',
)

watch(
  () => authStore.user,
  (newUser) => {
    if (newUser) {
      profile.value.nome = newUser.nome
      profile.value.email = newUser.email
      profile.value.cpf = newUser.cpf
    }
  },
  { immediate: true },
)

onMounted(() => {
  if (!authStore.user) authStore.fetchUser()
})

function showSnackbar(message: string, color: 'success' | 'error' | 'info' = 'success') {
  snackbar.value.message = message
  snackbar.value.color = color
  snackbar.value.show = true
}

async function handleSaveChanges() {
  saving.value = true
  try {
    await authStore.updateUser({ nome: profile.value.nome, email: profile.value.email })
    showSnackbar('Perfil atualizado com sucesso!')
  } catch (error) {
    showSnackbar('Erro ao atualizar o perfil.', 'error')
  } finally {
    saving.value = false
  }
}

async function handleUpdatePassword() {
  if (passwordData.value.new !== passwordData.value.confirm || !passwordData.value.new) {
    showSnackbar('A nova senha e a confirmação não coincidem.', 'error')
    return
  }
  passwordSaving.value = true
  try {
    await authStore.updateUser({ senha: passwordData.value.new })
    showSnackbar('Senha alterada com sucesso!')
    passwordDialog.value = false
    passwordData.value = { current: '', new: '', confirm: '' }
  } catch (error) {
    showSnackbar('Erro ao alterar a senha.', 'error')
  } finally {
    passwordSaving.value = false
  }
}

function onAvatarClick() {
  fileInput.value?.click()
}

async function onFileSelected(event: Event) {
  const target = event.target as HTMLInputElement

  if (target.files && target.files.length > 0) {
    const file = target.files[0]

    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
    if (!allowedTypes.includes(file.type)) {
      showSnackbar('Formato de arquivo inválido. Use JPG, PNG ou GIF.', 'error')
      return
    }

    await uploadProfilePicture(file)
    target.value = ''
  } else {
    console.log('Nenhum arquivo foi selecionado.')
  }
}

async function uploadProfilePicture(file: File) {
  uploading.value = true

  const formData = new FormData()
  formData.append('image', file)

  try {
    await api.post('/user/profile_image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    showSnackbar('Foto de perfil atualizada!')
    await authStore.fetchUser()
  } catch (error: any) {
    showSnackbar(error.response?.data?.erro || 'Falha ao enviar a imagem.', 'error')
  } finally {
    uploading.value = false
  }
}

const isDarkMode = ref(theme.global.name.value === 'dark')
const toggleTheme = () => (theme.global.name.value = isDarkMode.value ? 'dark' : 'light')
</script>
