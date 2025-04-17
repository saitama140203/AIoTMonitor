import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import { toast } from '@/components/ui/toast'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

export async function middlewareLayout(to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) {
  const userStore = useUserStore()
  const authStore = useAuthStore()
  const isAuthenticated = userStore.isAuthenticated
  const layout = to.meta.layout as string

  if (isAuthenticated && layout === 'auth') {
    if (authStore.returnUrl) {
      const returnUrl = authStore.returnUrl
      authStore.clearReturnUrl()
      return next(returnUrl)
    }
    return next('/')
  }

  if (!isAuthenticated && !['error', 'auth'].includes(layout)) {
    authStore.clearUserData()
  }

  if (!isAuthenticated && to.meta.authorized) {
    toast({
      title: 'Lỗi',
      description: 'Bạn cần đăng nhập để truy cập vào trang này, bạn đã được chuyển hướng đến trang chủ',
      variant: 'destructive',
      duration: 5000,
    })
    next('/')
  }

  return next()
}
