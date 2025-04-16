export interface BodyCreateUser {
  username: string
  email: string
  password: string
  fullName: string
}
export enum UserRole {
  OPERATOR = 'operator',
  SUPERVISOR = 'supervisor',
  TEAM_LEAD = 'team_lead',
  ADMIN = 'admin',
}
export type PayloadCreateUser = BodyCreateUser & {
  role: UserRole
}

export interface User {
  id: string
  username: string
  email: string
  fullName: string
  role: UserRole
  createdAt: string
  updatedAt: string
}
export interface BodyUpdatePassword {
  current_password: string
  new_password: string
  confirmNewPassword: string
}
