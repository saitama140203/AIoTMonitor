import { $get, $post } from './axios'

export function createProfile(data: any) {
  return $post('/profiles/create_profile', data)
}
export function getProfileList(config: any) {
  return $get('/profiles/get_all_profiles', { params: config })
}
export function assignProfile(data: any) {
  return $post('/profiles/assign_profile', data)
}
