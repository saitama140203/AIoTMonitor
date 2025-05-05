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
  async function getGroupList(config: any) {
    const response = await deviceAPI.getGroupList(config)
    return response
  }
  async function createGroup(name: string) {
    const response = await deviceAPI.createGroup(name)
    return response
  }
  async function addDeviceToGroup(device_ids: number[], group_id: number) {
    const response = await deviceAPI.addDeviceToGroup(device_ids, group_id)
    return response
  }
  return {
    createDevice,
    getDeviceList,
    getGroupList,
    createGroup,
    addDeviceToGroup,
  }
})
