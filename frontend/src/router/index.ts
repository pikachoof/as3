import { createRouter, createWebHistory } from 'vue-router'

import AppointmentsView from '@/views/AppointmentsView.vue'
import CaregiversView from '@/views/CaregiversView.vue'
import FamiliesView from '@/views/FamiliesView.vue'
import HomeView from '@/views/HomeView.vue'
import JobBoardView from '@/views/JobBoardView.vue'
import MessagesView from '@/views/MessagesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/caregivers',
      name: 'caregivers',
      component: CaregiversView,
    },
    {
      path: '/families',
      name: 'families',
      component: FamiliesView,
    },
    {
      path: '/jobs',
      name: 'jobs',
      component: JobBoardView,
    },
    {
      path: '/appointments',
      name: 'appointments',
      component: AppointmentsView,
    },
    {
      path: '/messages',
      name: 'messages',
      component: MessagesView,
    },
  ],
})

export default router
