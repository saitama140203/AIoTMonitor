import type { BodyCreateDevice } from '@/types'
import { $get, $post } from './axios'

export function createDevice(data: BodyCreateDevice) {
  return $post('/devices/devices/create_device', data)
}
export function getDeviceList(config: any) {
  return $get('/devices/devices/get_devices', { params: config })
}
export function createGroup(name: string) {
  return $post('/devices/groups/create_group', { name })
}
export function addDeviceToGroup(device_ids: string[], group_id: string) {
  return $post('/devices/add-to-group', { device_ids, group_id })
}
