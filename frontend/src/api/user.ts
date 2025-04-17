import type { BodyUpdatePassword } from '@/types'
import { $put } from '@/api/axios'

export async function changePassword(payload: BodyUpdatePassword) {
  return $put('/auth/update-password', payload)
}
