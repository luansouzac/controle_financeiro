<template>
  <v-container fluid class="pa-4">
    <!-- Saudações -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-typography variant="h4" class="font-weight-bold mb-1">Olá, Sandra!</v-typography>
        <v-typography variant="body2" class="text--secondary"
          >Aqui está seu resumo financeiro de Outubro.</v-typography
        >
      </v-col>
    </v-row>

    <!-- Cards de resumo -->
    <v-row class="mb-6" dense>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text class="d-flex align-center justify-space-between">
            <v-icon large color="primary">mdi-wallet</v-icon>
            <div>
              <div class="text-caption text--secondary">Saldo Total</div>
              <div class="font-weight-bold text-h6">R$ 12.450,75</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text class="d-flex align-center justify-space-between">
            <v-icon large color="green">mdi-arrow-up</v-icon>
            <div>
              <div class="text-caption text--secondary">Receitas do Mês</div>
              <div class="font-weight-bold text-h6 green--text">R$ 7.200,00</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text class="d-flex align-center justify-space-between">
            <v-icon large color="red">mdi-arrow-down</v-icon>
            <div>
              <div class="text-caption text--secondary">Despesas do Mês</div>
              <div class="font-weight-bold text-h6 red--text">R$ 4.350,50</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text class="d-flex align-center justify-space-between">
            <v-icon large color="teal">mdi-scale-balance</v-icon>
            <div>
              <div class="text-caption text--secondary">Balanço do Mês</div>
              <div class="font-weight-bold text-h6 teal--text">R$ 2.849,50</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Gráficos -->
    <v-row dense>
      <v-col cols="12" md="8">
        <v-card height="300px" class="d-flex align-center justify-center">
          <v-typography variant="body2" class="text--secondary"
            >Placeholder para Gráfico de Barras</v-typography
          >
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card height="300px" class="pa-4">
          <v-typography variant="subtitle1" class="mb-2">Gastos por Categoria</v-typography>
          <v-row dense>
            <v-col
              cols="12"
              v-for="(item, index) in gastos"
              :key="index"
              class="d-flex justify-space-between align-center"
            >
              <v-chip :color="item.color" small class="ma-0">{{ item.name }}</v-chip>
              <span class="font-weight-bold">{{ item.valor }}</span>
            </v-col>
          </v-row>
          <v-spacer></v-spacer>
          <v-typography variant="body2" class="text--secondary text-center mt-2">
            Placeholder para Gráfico de Rosca
          </v-typography>
        </v-card>
      </v-col>
    </v-row>

    <!-- Últimas transações -->
    <v-row class="mt-6">
      <v-col cols="12">
        <v-card>
          <v-card-title>Últimas Transações</v-card-title>
          <v-divider></v-divider>
          <v-list>
            <v-list-item v-for="(t, i) in transacoes" :key="i">
              <v-list-item-avatar>
                <v-icon :color="t.type === 'expense' ? 'red' : 'green'">{{ t.icon }}</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>{{ t.nome }}</v-list-item-title>
                <v-list-item-subtitle>{{ t.categoria }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <span :class="t.type === 'expense' ? 'red--text' : 'green--text'">{{
                  t.valor
                }}</span>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'DashboardView',
  data() {
    return {
      gastos: [
        { name: 'Moradia', valor: 'R$ 1.800,00', color: 'blue darken-3' },
        { name: 'Alimentação', valor: 'R$ 1.100,50', color: 'green' },
        { name: 'Transporte', valor: 'R$ 650,00', color: 'yellow darken-2' },
        { name: 'Lazer', valor: 'R$ 450,00', color: 'purple' },
        { name: 'Outros', valor: 'R$ 350,00', color: 'grey' },
      ],
      transacoes: [
        {
          nome: 'Supermercado Pão de Açúcar',
          categoria: 'Alimentação',
          valor: '- R$ 345,50',
          type: 'expense',
          icon: 'mdi-cart',
        },
        {
          nome: 'Salário Mensal',
          categoria: 'Renda',
          valor: '+ R$ 7.200,00',
          type: 'income',
          icon: 'mdi-cash',
        },
      ],
    }
  },
})
</script>

<style scoped>
/* Estilizações adicionais podem ser feitas aqui */
</style>
