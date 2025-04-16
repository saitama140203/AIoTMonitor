import type { BodyCreateUser } from '@/types'
import { $post } from './axios'

export function createOperator(body: BodyCreateUser) {
  const data = { ...body }
  data.full_name = body.fullName
  return $post('/auth/create-operator', data)
}
export function createSupervisor(body: BodyCreateUser) {
  const data = { ...body }
  data.full_name = body.fullName
  return $post('/auth/create-supervisor', data)
}
export function createTeamLead(body: BodyCreateUser) {
  const data = { ...body }
  data.full_name = body.fullName
  return $post('/auth/create-team-lead', data)
}
