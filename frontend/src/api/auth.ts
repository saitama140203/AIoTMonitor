import type { EmailData, LoginData, RegisterData, ResetPasswordData } from '@/types'
import { $post } from './axios'

export function apiLogin(body: LoginData) {
  const data = new FormData()
  data.append('username', body.username)
  data.append('password', body.password)
  return $post('/auth/login', data)
}
