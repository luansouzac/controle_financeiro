<template>
  <v-container class="py-6">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-fade-transition appear>
          <div>
            <div class="text-center mb-12">
              <v-icon size="64" color="primary">mdi-rocket-launch-outline</v-icon>
              <h1 class="text-h3 font-weight-bold text-grey-darken-3 mt-4">Nossa Missão</h1>
              <p class="text-h6 text-medium-emphasis mt-2">
                Simplificar o controle financeiro, transformando dados complexos em decisões claras e inteligentes para a sua vida.
              </p>
            </div>

            <v-card elevation="2" rounded="lg" class="mb-8">
              <v-card-title class="text-h5 font-weight-bold">Recursos Principais</v-card-title>
              <v-divider></v-divider>
              <v-list lines="two" class="py-0">
                <v-list-item v-for="feature in features" :key="feature.title">
                  <template v-slot:prepend>
                    <v-avatar color="primary-lighten-4" class="mr-4">
                      <v-icon color="primary">{{ feature.icon }}</v-icon>
                    </v-avatar>
                  </template>
                  <div>
                    <v-list-item-title class="font-weight-bold">{{ feature.title }}</v-list-item-title>
                    <v-list-item-subtitle>{{ feature.subtitle }}</v-list-item-subtitle>
                  </div>
                </v-list-item>
              </v-list>
            </v-card>

            <v-card elevation="2" rounded="lg" class="mb-8">
              <v-card-title class="text-h5 font-weight-bold">Criado Por</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <div class="d-flex align-center">
                  <v-avatar size="80" class="mr-6">
                    <v-img src="https://avatars.githubusercontent.com/u/161772370?s=400&u=e9b0af46530d9492086368beafef2320c162d6c6&v=4" alt="Luan Silva"></v-img>
                  </v-avatar>
                  <div>
                    <h3 class="text-h6 font-weight-bold">Luan Souza</h3>
                    <p class="text-body-1 text-medium-emphasis">Desenvolvedor Full Stack</p>
                    <p class="mt-2">
                      "Acredito que a tecnologia tem o poder de nos dar clareza e controle sobre nossas vidas. Este projeto nasceu da minha paixão por finanças e do desejo de criar uma ferramenta que eu mesmo gostaria de usar todos os dias."
                    </p>
                  </div>
                </div>
              </v-card-text>
              <v-card-text>
                <div class="d-flex align-center">
                  <v-avatar size="80" class="mr-6">
                    <v-img src="https://avatars.githubusercontent.com/u/74503817?v=4" alt="Luan Silva"></v-img>
                  </v-avatar>
                  <div>
                    <h3 class="text-h6 font-weight-bold">Francisco Carlos</h3>
                    <p class="text-body-1 text-medium-emphasis">Desenvolvedor Full Stack</p>
                    <p class="mt-2">
                      "Acredito que a tecnologia tem o poder de nos dar clareza e controle sobre nossas vidas. Este projeto nasceu da minha paixão por finanças e do desejo de criar uma ferramenta que eu mesmo gostaria de usar todos os dias."
                    </p>
                  </div>
                </div>
              </v-card-text>
            </v-card>

            <v-card elevation="2" rounded="lg" class="mb-8">
              <v-card-title class="text-h5 font-weight-bold">Feito Com</v-card-title>
              <v-divider></v-divider>
              <v-card-text class="d-flex flex-wrap ga-2">
                <v-chip prepend-icon="mdi-vuejs" color="green" variant="tonal">Vue.js 3</v-chip>
                <v-chip prepend-icon="mdi-vuetify" color="blue" variant="tonal">Vuetify</v-chip>
                <v-chip prepend-icon="mdi-language-typescript" color="blue-darken-2" variant="tonal">TypeScript</v-chip>
                <v-chip prepend-icon="mdi-pine-tree" color="yellow-darken-3" variant="tonal">Pinia</v-chip>
                <v-chip prepend-icon="mdi-language-python" color="indigo" variant="tonal">Python & Flask</v-chip>
              </v-card-text>
            </v-card>

            <v-card elevation="2" rounded="lg">
              <v-card-title class="text-h5 font-weight-bold">Entre em Contato</v-card-title>
              <v-card-text class="text-body-1 text-medium-emphasis">
                Seu feedback é muito importante! Encontrou um bug ou tem uma sugestão? Adoraria ouvir de você.
              </v-card-text>
              <v-card-actions class="pa-4">
                <v-btn href="https://github.com" target="_blank" prepend-icon="mdi-github" variant="outlined">GitHub</v-btn>
                <v-btn href="https://linkedin.com" target="_blank" prepend-icon="mdi-linkedin" variant="outlined" class="ml-2">LinkedIn</v-btn>
                <v-spacer></v-spacer>
                <v-btn href="mailto:contato@email.com" color="primary" prepend-icon="mdi-email-outline">Enviar Email</v-btn>
              </v-card-actions>
            </v-card>

          </div>
        </v-fade-transition>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const features = ref([
  { title: 'Dashboard Inteligente', subtitle: 'Visão geral e tendências com gráficos minimalistas.', icon: 'mdi-chart-donut-variant' },
  { title: 'Gestão de Transações', subtitle: 'Adicione suas receitas e despesas de forma rápida e intuitiva.', icon: 'mdi-swap-horizontal' },
  { title: 'Carteiras Múltiplas', subtitle: 'Organize suas contas, cartões e investimentos em um só lugar.', icon: 'mdi-wallet' },
  { title: 'Categorias Personalizáveis', subtitle: 'Adapte o sistema à sua realidade financeira.', icon: 'mdi-tag-multiple' },
]);
</script>