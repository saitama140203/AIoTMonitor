<template>
  <div class="session-history">
    <div class="header">
      <h3>Session History</h3>
      <div class="controls">
        <input
          v-model="searchQuery"
          placeholder="Search by device or operator..."
          class="search-input"
        />
        <select v-model="itemsPerPage" class="page-select">
          <option value="10">10 items/page</option>
          <option value="25">25 items/page</option>
          <option value="50">50 items/page</option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table class="history-table">
        <thead>
          <tr>
            <th @click="sortBy('ended_at')">
              Time
              <span v-if="sortColumn === 'ended_at'">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('device_id')">
              Device
              <span v-if="sortColumn === 'device_id'">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('operator_name')">
              Operator
              <span v-if="sortColumn === 'operator_name'">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th>Duration</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="session in paginatedSessions" :key="session.id">
            <td>{{ formatDate(session.ended_at) }}</td>
            <td>{{ session.device_id }}</td>
            <td>{{ session.operator_name }}</td>
            <td>{{ formatDuration(session.duration_seconds) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination">
      <button 
        @click="prevPage" 
        :disabled="currentPage === 1"
        class="pagination-button"
      >
        Previous
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button 
        @click="nextPage" 
        :disabled="currentPage === totalPages"
        class="pagination-button"
      >
        Next
      </button>
    </div>

    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { getSessionHistory } from '@/api/supervisor'

interface SessionHistory {
  id: number
  operator_name: string
  device_id: string
  ended_at: string
  duration_seconds: number
}

// Reactive data
const sessions = ref<SessionHistory[]>([])
const loading = ref(false)
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(10)
const sortColumn = ref('ended_at')
const sortOrder = ref('desc')

// Computed properties
const filteredSessions = computed(() => {
  return (sessions.value || []).filter(session => {
    const matchesSearch = 
      session.device_id?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      session.operator_name?.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesSearch
  })
})

const sortedSessions = computed(() => {
  return [...filteredSessions.value].sort((a, b) => {
    const valA = a[sortColumn.value as keyof SessionHistory]
    const valB = b[sortColumn.value as keyof SessionHistory]
    
    if (valA < valB) return sortOrder.value === 'asc' ? -1 : 1
    if (valA > valB) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
})

const totalPages = computed(() => {
  return Math.ceil(sortedSessions.value.length / itemsPerPage.value)
})

const paginatedSessions = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return sortedSessions.value.slice(start, end)
})

// Methods
const fetchSessionHistory = async () => {
  try {
    loading.value = true
    const response = await getSessionHistory({ 
      sort_by: sortColumn.value,
      sort_order: sortOrder.value
    })
    sessions.value = response.data
  } catch (error) {
    console.error('Failed to fetch session history:', error)
  } finally {
    loading.value = false
  }
}

const sortBy = (column: string) => {
  if (sortColumn.value === column) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = column
    sortOrder.value = 'asc'
  }
  fetchSessionHistory()
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

const formatDuration = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}m ${secs}s`
}

// Watchers
watch(itemsPerPage, () => {
  currentPage.value = 1
})

// Lifecycle hooks
onMounted(() => {
  fetchSessionHistory()
})
</script>

<style scoped>
.session-history {
  position: relative;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.controls {
  display: flex;
  gap: 10px;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 250px;
}

.page-select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.table-container {
  overflow-x: auto;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
}

.history-table th, 
.history-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.history-table th {
  background-color: #f5f5f5;
  cursor: pointer;
  user-select: none;
}

.history-table th:hover {
  background-color: #eee;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
}

.pagination-button {
  padding: 8px 16px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>