export interface LoginData {
  email: string
  password: string
}
export interface RegisterData {
  email: string
  password: string
  confirmPassword: string
}
export interface EmailData {
  email: string
}

export interface ResetPasswordData {
  password: string
  confirmPassword: string
  token: string
}
