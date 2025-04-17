import type { BodyCreateUser } from '@/types'
import { $get, $post, $put } from './axios'

export function createUser(body: BodyCreateUser) {
  const data = { ...body }
  data.full_name = body.fullName
  return $post('/auth/users', data)
}

export function getListUsers(config: { role?: string, limit?: number, skip?: number }) {
  return $get('/users/', {
    params: {
      role: config.role,
      limit: config.limit,
      skip: config.skip,
    },
  })
}
export function resetPassword(email: string) {
  return $put('/auth/reset-password', { email })
}
