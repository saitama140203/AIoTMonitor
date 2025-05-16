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
export function getProfileDetail(id: number) {
  return $get(`/profiles/get_profile_by_id/${id}`)
}
export function getUnassignedProfileList(id: number) {
  return $get(`/profiles/profiles/${id}/unassigned_operators`)
}
export function getUnassignedCommnands(id: number) {
  return $get(`/profiles/profiles/${id}/unassigned_commands`)
}

export function getProfile(config: any) {
  return $get(`/profiles/profiles/me`, {params: config})
}

export function getProfileResources(
  profileId: number,
  pagination: { skip: number; limit: number }
) {
  // Đảm bảo endpoint này khớp với API backend
  return $get(`/profiles/profiles/${profileId}/resources`, {
    params: pagination
  })
}
