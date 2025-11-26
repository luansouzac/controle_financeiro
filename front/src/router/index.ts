import { createRouter, createWebHistory } from 'vue-router'
import TransactionsView from '../views/TransactionsView.vue'
import ReportsView from '../views/ReportsView.vue'
import AboutView from '../views/AboutView.vue'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/Register.vue'
import WalletsView from '@/views/WalletsView.vue'
import CategoyView from '@/views/CategoyView.vue'
import IncomeView from '@/views/IncomeView.vue'
import SettingsView from '@/views/SettingsView.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/transactions',
    name: 'Transações',
    component: TransactionsView,
  },
  // {
  //   path: '/reports',
  //   name: 'Reports',
  //   component: ReportsView,
  // },
  {
    path: '/wallets',
    name: 'Carteiras',
    component: WalletsView,
  },
  {
    path: '/categories',
    name: 'Categorias',
    component: CategoyView,
  },
  {
    path: '/incomes',
    name: 'Receitas',
    component: IncomeView,
    props: (route: any) => ({
      tipo: 'receita',
      key: 'incomes',
    }),
  },
  {
    path: '/expenses',
    name: 'Despesas',
    component: IncomeView,
    props: (route: any) => ({
      tipo: 'despesa',
      key: 'expenses',
    }),
  },
  {
    path: '/about',
    name: 'Sobre',
    component: AboutView,
  },
  {
    path: '/settings',
    name: 'Configurações',
    component: SettingsView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const publicPages = ['Login', 'Register']

  const authRequired = !publicPages.includes(to.name as string)

  const token = sessionStorage.getItem('authToken')

  if (authRequired && !token) {
    return next({ name: 'Login' })
  }

  next()
})

export default router
export { routes }
