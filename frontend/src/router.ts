import { middlewareAuth, middlewareLayout } from '@/middlewares'
import generatedRoutes from '~pages'
import { setupLayouts } from 'virtual:generated-layouts'
import { createRouter, createWebHistory } from 'vue-router'
import { UserRole } from './types'
import ActiveSessions from '@/components/supervisor/ActiveSessions.vue'
import ViewHistory from '@/components/supervisor/HistoryView.vue'
import SupervisorDashboard from '@/layouts/default.vue'

const manualRoutes = [
  {
    path: '/supervisor',
    component: SupervisorDashboard,
    children: [
      {
        path: '',
        redirect: 'sessions',
      },
      {
        path: 'sessions',
        name: 'SupervisorActiveSessions',
        component: ActiveSessions,
        meta: {
          title: 'Active Sessions',
          requiresAuth: true,
          allowedRoles: [UserRole.SUPERVISOR]
        }
      },
      {
        path: 'history',
        name: 'SupervisorViewHistory',
        component: ViewHistory,
        meta: {
          title: 'Session History',
          requiresAuth: true,
          allowedRoles: [UserRole.SUPERVISOR]
        }
      }
    ],
    meta: {
      title: 'Supervisor',
      requiresAuth: true,
      allowedRoles: [UserRole.SUPERVISOR]
    }
  }
]

const routes = setupLayouts(generatedRoutes).concat(manualRoutes)

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  if (to.matched.length === 0) {
    return next('/notfound')
  }
  return next()
})
router.beforeEach(middlewareAuth)
router.beforeEach(middlewareLayout)

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = `AIoT Monitor - ${to.meta.title}`
  }
  next()
})

export default router
