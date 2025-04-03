import type { EmailData, LoginData, RegisterData, ResetPasswordData } from '@/utils/types'
import { $post } from './axios'

export function apiLogin(data: LoginData) {
  return $post('/auth/login', data)
}

export function apiRegister(data: RegisterData) {
  return $post('/auth/register', data)
}

export function forgotPassword(data: EmailData) {
  return $post('/auth/forgot-password', data)
}

export function requestResetPassword(data: ResetPasswordData) {
  return $post(`/auth/reset-password/${data.token}`, {
    password: data.password,
    confirmPassword: data.confirmPassword,
  })
}
