import type { BodyCreateUser } from '@/types'
import * as apiAdmin from '@/api/admin'
import { defineStore } from 'pinia'

export const useAdminStore = defineStore('admin', () => {
  async function createUser(payload: BodyCreateUser) {
    if (!payload) {
      return Promise.reject(new Error('Invalid payload'))
    }
    return apiAdmin.createUser(payload)
  }
  async function getListUsers(config: { role?: string, limit?: number, skip?: number }) {
    if (!config) {
      return Promise.reject(new Error('Invalid config'))
    }
    return apiAdmin.getListUsers(config)
  }
  async function resetPassword(email: string) {
    if (!email) {
      return Promise.reject(new Error('Invalid email'))
    }
    return apiAdmin.resetPassword(email)
  }
  return {
    createUser,
    getListUsers,
    resetPassword,
  }
})
