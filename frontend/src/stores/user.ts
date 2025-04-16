import type { BodyUpdatePassword } from '@/types'
import { changePassword } from '@/api/user'
import { useAuthStore } from '@/stores/auth'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const authStore = useAuthStore()

  function setUser(newUser: any) {
    user.value = newUser
  }
  function removeUser() {
    user.value = null
  }
  async function getUserData() {
    const data = localStorage.getItem('aiot_user')
    if (data) {
      setUser(JSON.parse(data))
    }
  }

  async function updatePasswword(payload: BodyUpdatePassword) {
    await changePassword(payload)
    authStore.logout()
  }

  const isAuthenticated = computed(() => !!user.value)

  return {
    user,
    setUser,
    removeUser,
    getUserData,
    updatePasswword,
    isAuthenticated,
  }
})
