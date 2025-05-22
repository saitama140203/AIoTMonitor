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
          <th class="px-4 py-2 border">Detail</th>
          <th class="px-4 py-2 border text-center">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="session in sessions"
          :key="session.id"
          class="hover:bg-gray-50"
        >
          <td class="px-4 py-2 border">{{ session.operatorName }}</td>
          <td class="px-4 py-2 border">{{ session.device }}</td>
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
          <td class="px-4 py-2 border">{{ session.detail }}</td>
          <td class="px-4 py-2 border text-center">
            <button
              @click="killSession(session.id)"
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
import { ref, onMounted } from 'vue'

interface Session {
  id: number
  operatorName: string
  device: string
  status: string
  detail: string
}

const sessions = ref<Session[]>([])
const loading = ref(true)

// Thông báo
const message = ref('')
const isSuccess = ref(true)

const showMessage = (msg: string, success = true) => {
  message.value = msg
  isSuccess.value = success

  // 3 giây sau tự ẩn
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

const fetchSessions = async () => {
  loading.value = true
  try {
    const res = await fetch('/api/v1/supervisor/active')
    const data = await res.json()
    sessions.value = data
  } catch (error) {
    showMessage('Failed to load sessions.', false)
  } finally {
    loading.value = false
  }
}

const killSession = async (sessionId: number) => {
  if (!confirm('Are you sure you want to kill this session?')) return

  try {
    const res = await fetch(`/api/v1/supervisor/${sessionId}/terminate`, {
      method: 'DELETE'
    })
    if (!res.ok) throw new Error()

    showMessage('Session terminated successfully!', true)
    sessions.value = sessions.value.filter((s) => s.id !== sessionId)
  } catch (error) {
    showMessage('Failed to terminate session.', false)
  }
}

onMounted(fetchSessions)
</script>
