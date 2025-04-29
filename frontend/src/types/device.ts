export interface BodyCreateDevice {
  name: string
  username: string
  ip: string
  port: number
  password: string
  platform: string
}
export interface Device {
  id: number
  name: string
  username: string
  ip: string
  port: number
  hashed_password: string
  platform: string
  status: string
  lastseen: string
  created_by: number
  group_id: number | null
}
