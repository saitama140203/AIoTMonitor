import type { EmailData, LoginData, RegisterData, ResetPasswordData } from '@/types'
import { apiLogin } from '@/api/auth'
import { defineStore } from 'pinia'
import { useUserStore } from './user'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('aiot_accesstoken') || '')
  const userStore = useUserStore()
  const isAuthenticated = computed(() => !!accessToken.value)
  const router = useRouter()
  const returnUrl = ref('')

  async function login(credentials: LoginData) {
    const data = await apiLogin(credentials)
    localStorage.setItem('aiot_accesstoken', data.access_token)
    localStorage.setItem('aiot_user', JSON.stringify(data))
    userStore.setUser(data)
    router.push(returnUrl.value || '/')
  }

  function logout() {
    localStorage.removeItem('aiot_accesstoken')
    userStore.removeUser()
    router.push('/auth/login')
    accessToken.value = ''
  }

  function setReturnUrl(url: string) {
    returnUrl.value = url
  }
  return {
    isAuthenticated,
    login,
    logout,
    returnUrl,
    accessToken,
    setReturnUrl,
  }
})
