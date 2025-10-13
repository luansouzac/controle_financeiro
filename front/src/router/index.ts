import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import TransactionsView from '../views/TransactionsView.vue'
import ReportsView from '../views/ReportsView.vue'
import AboutView from '../views/AboutView.vue'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/Register.vue'
import WalletsView from '@/views/WalletsView.vue'

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
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
  },
  {
    path: '/transactions',
    name: 'Transactions',
    component: TransactionsView,
  },
  {
    path: '/reports',
    name: 'Reports',
    component: ReportsView,
  },
  {
    path: '/about',
    name: 'About',
    component: AboutView,
  },
  {
    path: '/wallets',
    name: 'Wallets',
    component: WalletsView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const publicPages = ['Login', 'Register'];
  
  const authRequired = !publicPages.includes(to.name as string);
  
  const token = sessionStorage.getItem('authToken');

  if (authRequired && !token) {
    return next({ name: 'Login' });
  }

  next();
});

export default router
