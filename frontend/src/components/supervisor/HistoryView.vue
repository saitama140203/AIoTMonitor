<template>
  <div class="p-6 bg-white rounded shadow-md">
    <h2 class="text-xl font-semibold mb-4">Command History</h2>
    <button
        @click="fetchHistory"
        class="mb-4 px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
        Refresh
    </button>
    <div v-if="loading" class="text-gray-500">Loading history...</div>
    <div v-else-if="history.length === 0" class="text-gray-500">No history available.</div>

    <table v-else class="min-w-full table-auto border border-gray-200">
      <thead class="bg-gray-100 text-left">
        <tr>
          <th class="px-4 py-2 border">Time Start</th>
          <th class="px-4 py-2 border">Duration</th>
          <th class="px-4 py-2 border">Operator</th>
          <th class="px-4 py-2 border">Device</th>
          <th class="px-4 py-2 border">Command</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="entry in paginatedHistory"
          :key="entry.session_id"
          class="hover:bg-gray-50 cursor-pointer"
          @click="toggleExpanded(entry.session_id)"
        >
          <td class="px-4 py-2 border">{{ formatDate(entry.connected_time) }}</td>
          <td class="px-4 py-2 border">{{ formatDuration(entry.connected_time, entry.ended_at) }}</td>
          <td class="px-4 py-2 border">{{ entry.operator_name }}</td>
          <td class="px-4 py-2 border">{{ entry.device_name }}</td>
          <td class="px-4 py-2 border font-mono whitespace-pre-line">
            <div v-if="expandedRowId === entry.session_id">
              <div v-for="(cmd, index) in entry.all_commands" :key="index">
                {{ cmd.text }}
              </div>
            </div>
            <div v-else>
              <span class="text-blue-500 underline">View</span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div class="mt-4 flex justify-center items-center gap-2">
      <button 
        @click="prevPage" 
        :disabled="currentPage === 1"
        class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
      >Prev</button>

      <span>Page {{ currentPage }} of {{ totalPages }}</span>

      <button 
        @click="nextPage" 
        :disabled="currentPage === totalPages"
        class="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
      >Next</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Command {
  text: string
  timestamp: string
}

interface HistoryEntry {
  session_id: number
  connected_time: string
  ended_at: string
  operator_name: string
  device_name: string
  all_commands: Command[]
}

const history = ref<HistoryEntry[]>([])
const loading = ref(true)
const token = localStorage.getItem('aiot_accesstoken') || ''

const currentPage = ref(1)
const itemsPerPage = 10

const expandedRowId = ref<number | null>(null)

const totalPages = computed(() =>
  Math.ceil(history.value.length / itemsPerPage)
)

const paginatedHistory = computed(() =>
  history.value.slice(
    (currentPage.value - 1) * itemsPerPage,
    currentPage.value * itemsPerPage
  )
)

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

const toggleExpanded = (sessionId: number) => {
  expandedRowId.value = expandedRowId.value === sessionId ? null : sessionId
}

const fetchHistory = async () => {
  loading.value = true
  try {
    const res = await fetch('http://localhost:8000/api/v1/supervisor/sessions/history', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json'
      }
    })
    if (!res.ok) throw new Error('Failed to fetch')

    const data: HistoryEntry[] = await res.json()
    history.value = data
  } catch (error) {
    console.error('Error loading history:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchHistory()
})

const formatDate = (iso: string) =>
  new Date(iso).toLocaleString()

const formatDuration = (start: string, end: string) => {
  const diff = new Date(end).getTime() - new Date(start).getTime()
  if (isNaN(diff)) return 'N/A'

  const seconds = Math.floor(diff / 1000)
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}m ${secs}s`
}
</script>
