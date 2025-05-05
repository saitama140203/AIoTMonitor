import * as api from '@/api/command'
import { defineStore } from 'pinia'

export const useCommandStore = defineStore('command', () => {
  function createCommand(data: any) {
    return api.createCommand(data)
  }
  function getCommandList(config: any) {
    return api.getCommandList(config)
  }
  return {
    createCommand,
    getCommandList,
  }
})
