import type { PayloadCreateUser } from '@/types'
import { createOperator, createSupervisor, createTeamLead } from '@/api/admin'
import { UserRole } from '@/types'
import { defineStore } from 'pinia'

export const useAdminStore = defineStore('admin', () => {
  async function createUser(payload: PayloadCreateUser) {
    if (!payload) {
      return Promise.reject(new Error('Invalid payload'))
    }
    switch (payload.role) {
      case UserRole.OPERATOR:
        return createOperator(payload)
      case UserRole.SUPERVISOR:
        return createSupervisor(payload)
      case UserRole.TEAM_LEAD:
        return createTeamLead(payload)
    }
  }
  return {
    createUser,
  }
})
