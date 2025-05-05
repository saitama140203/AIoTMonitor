import { $get, $post } from './axios'

export function createCommand(data: any) {
  return $post('/commands/create_command', data)
}

export function getCommandList(cofig: any) {
  return $get('/commandsget_all_commands', { params: cofig })
}

export function addCommandToProfile(data: any) {
  return $post('/commands/command-profiles/', data)
}
