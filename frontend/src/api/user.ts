import { $get } from '@/api/axios'

export async function fetchUserData() {
  return $get('/users/me')
}
