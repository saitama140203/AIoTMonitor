import type { BodyCreateDevice } from '@/types'
import * as deviceAPI from '@/api/device'
import { defineStore } from 'pinia'

export const useDeviceStore = defineStore('device', () => {
  async function createDevice(deviceData: BodyCreateDevice) {
    const response = await deviceAPI.createDevice(deviceData)
    return response.data
  }
  async function getDeviceList(config: any) {
    const response = await deviceAPI.getDeviceList(config)
    return response
  }
  return {
    createDevice,
    getDeviceList,
  }
})
