import * as command from '@/api/command'
import * as api from '@/api/profile'
import { defineStore } from 'pinia'

export const useProfileStore = defineStore('profile', () => {
  function createProfile(data: any) {
    return api.createProfile(data)
  }
  function getProfileList(config: any) {
    return api.getProfileList(config)
  }
  function assignProfile(data: any) {
    return api.assignProfile(data)
  }
  function addCommandToProfile(data: any) {
    return command.addCommandToProfile(data)
  }
  return {
    createProfile,
    getProfileList,
    assignProfile,
    addCommandToProfile,
  }
})
