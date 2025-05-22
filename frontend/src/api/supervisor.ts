
import { $get, $post } from './axios'

export function getActiveSessions(config: any) {
    return $get('/supervisor/active', { params: config })
}

export function getSessionHistory(config: any) {
    return $get('/supervisor/history', { params: config })
}

export function killSession(sessionId: number) {
    return $post(`/supervisor/${sessionId}/terminate`, {})
}
