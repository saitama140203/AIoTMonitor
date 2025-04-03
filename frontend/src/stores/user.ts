import { fetchUserData } from '@/api/user'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)

  function setUser(newUser: any) {
    user.value = newUser
  }
  function removeUser() {
    user.value = null
  }
  async function getUserData() {
    const data = await fetchUserData()
    setUser(data)
  }
  const isAuthenticated = computed(() => !!user.value)
  return {
    user,
    setUser,
    isAuthenticated,
    removeUser,
    getUserData
  }
})
