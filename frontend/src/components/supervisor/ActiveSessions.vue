<template>
  <div class="p-6 bg-white rounded shadow-md">
    <!-- Hiển thị thông báo -->
    <div v-if="message" :class="{'text-green-600': isSuccess, 'text-red-600': !isSuccess}" class="mb-4">
      {{ message }}
    </div>

    <h2 class="text-xl font-semibold mb-4">Active Sessions</h2>

    <div v-if="loading" class="text-gray-500">Loading sessions...</div>
    <div v-else-if="sessions.length === 0" class="text-gray-500">No active sessions found.</div>

    <table v-else class="min-w-full table-auto border border-gray-200">
      <thead class="bg-gray-100 text-left">
        <tr>
          <th class="px-4 py-2 border">Operator Name</th>
          <th class="px-4 py-2 border">Device</th>
          <th class="px-4 py-2 border">Status</th>
          <th class="px-4 py-2 border">Start Time</th>
          <th class="px-4 py-2 border">Current Command</th>
          <th class="px-4 py-2 border text-center">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="session in sessions"
          :key="session.session_id"
          class="hover:bg-gray-50"
        >
          <td class="px-4 py-2 border">{{ session.operator_name }}</td>
          <td class="px-4 py-2 border">{{ session.device_name }}</td>
          <td class="px-4 py-2 border">
            <span
              :class="{
                'text-green-600': session.status === 'active',
                'text-red-600': session.status !== 'active',
              }"
            >
              {{ session.status }}
            </span>
          </td>
          <td class="px-4 py-2 border">{{ new Date(session.start_time).toLocaleString() }}</td>
          <td class="px-4 py-2 border">{{ session.current_command || '-' }}</td>
          <td class="px-4 py-2 border text-center">
            <button
              @click="killSession(session.session_id)"
              class="px-3 py-1 bg-red-500 text-white text-sm rounded hover:bg-red-600"
            >
              Kill
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Session {
  session_id: number
  operator_name: string
  device_name: string
  status: string
  start_time: string
  current_command: string | null
}

const sessions = ref<Session[]>([])
const loading = ref(true)
const message = ref('')
const isSuccess = ref(true)

const showMessage = (msg: string, success = true) => {
  message.value = msg
  isSuccess.value = success
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

const token = localStorage.getItem('aiot_accesstoken') || ''

const fetchSessions = async () => {
  loading.value = true
  try {
    const res = await fetch('http://localhost:8000/api/v1/supervisor/sessions/active', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json'
      }
    })
    if (!res.ok) throw new Error('Failed to fetch')

    const data: Session[] = await res.json()
    sessions.value = data
  } catch (error) {
    showMessage('Failed to load sessions.', false)
  } finally {
    loading.value = false
  }
}

const user = JSON.parse(localStorage.getItem('aiot_user') || '{}')
const userId = user?.user_id

const killSession = async (sessionId: number) => {
  if (!confirm('Are you sure you want to kill this session?')) return

  try {
    const res = await fetch(`http://localhost:8000/api/v1/supervisor/sessions/${sessionId}/terminate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        terminated_by: userId
      })
    })

    if (!res.ok) throw new Error()

    showMessage('Session terminated successfully!', true)
    sessions.value = sessions.value.filter((s) => s.session_id !== sessionId)
  } catch (error) {
    showMessage('Failed to terminate session.', false)
  }
}

// --- WebSocket ---
let socket: WebSocket

const connectWebSocket = () => {
  socket = new WebSocket('ws://localhost:8000/api/v1/ssh_proxy/supervisor')

  socket.onopen = () => {
    console.log('✅ WebSocket connected')
  }

socket.onmessage = (event) => {
  try {
    const data = JSON.parse(event.data)

    if (data.type === 'current_command') {
      console.log('Supervisor received command:', data.current_command)
    }
    // Nếu chỉ cập nhật current_command
    if (data.session_id && data.current_command !== undefined) {
      const session = sessions.value.find(s => s.session_id === data.session_id)
      if (session) {
        session.current_command = data.current_command
      }
      return
    }

    // Trường hợp đầy đủ session data
    if (data.session_id) {
      const index = sessions.value.findIndex(s => s.session_id === data.session_id)
      if (index !== -1) {
        sessions.value[index] = { ...sessions.value[index], ...data }
      } else {
        sessions.value.push(data)
      }
    }

  } catch (err) {
    console.error('Invalid WebSocket data:', event.data)
  }
}

  socket.onerror = (err) => {
    console.error('WebSocket error:', err)
    showMessage('WebSocket connection error.', false)
  }

  socket.onclose = () => {
    console.warn('WebSocket closed. Reconnecting in 3s...')
    setTimeout(connectWebSocket, 3000)
  }
}

onMounted(() => {
  fetchSessions()
  connectWebSocket()
})

onUnmounted(() => {
  if (socket) {
    socket.close()
  }
})
</script>
