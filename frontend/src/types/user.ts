export interface BodyCreateUser {
  username: string
  email: string
  password: string
  fullName: string
  full_name?: string
  role?: UserRole
}
export enum UserRole {
  OPERATOR = 'operator',
  SUPERVISOR = 'supervisor',
  TEAM_LEAD = 'team_lead',
  ADMIN = 'admin',
}
export interface User {
  id: string
  username: string
  email: string
  roles: UserRole[]
  full_name: string
  createdAt: string
  updatedAt: string
}
export interface BodyUpdatePassword {
  current_password: string
  new_password: string
  confirmNewPassword: string
}
