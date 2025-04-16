import { $post } from './axios'

export function uploadImage(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return $post('/common/upload-file', formData)
}
