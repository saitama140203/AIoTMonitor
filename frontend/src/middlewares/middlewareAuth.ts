import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

export async function middlewareAuth(to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) {
  const authStore = useAuthStore()
  const userStore = useUserStore()
  const accessToken = localStorage.getItem('aiot_accesstoken')

  if (!accessToken) {
    userStore.removeUser()
    const isAuthOrErrorLayout = ['auth', 'error'].includes(to.meta.layout as string)
    if (isAuthOrErrorLayout)
      return next()
    authStore.setReturnUrl(to.fullPath)
    return next('/auth/login')
  }

  if (accessToken && !userStore.isAuthenticated) {
    try {
      await userStore.getUserData()
    }
    catch (error) {
      console.error('Error fetching user data:', error)
    }
  }
  return next()
}
