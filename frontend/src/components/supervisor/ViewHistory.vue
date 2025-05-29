<template>
  <div class="session-history">
    <div class="header">
      <h3>View History</h3>
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
            <th @click="sortBy('device_name')">
              Device
              <span v-if="sortColumn === 'device_name'">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('operator_name')">
              Operator
              <span v-if="sortColumn === 'operator_name'">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('durationSeconds')">
              Duration
              <span v-if="sortColumn === 'durationSeconds'">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('end_status')">
              Status
              <span v-if="sortColumn === 'end_status'">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <!-- Session ID column đã ẩn -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="session in paginatedSessions" :key="session.session_id">
            <td>{{ formatDate(session.ended_at) }}</td>
            <td>{{ session.device_name }}</td>
            <td>{{ session.operator_name }}</td>
            <td>{{ formatDuration(session.durationSeconds) }}</td>
            <td>{{ session.end_status }}</td>
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
import { ref, computed, onMounted, watch } from "vue";

interface SessionHistory {
  session_id: number;
  device_name: string;
  operator_name: string;
  end_status: string;
  ended_at: string;      // thời điểm kết thúc
  start_time: string;    // thời điểm bắt đầu 
  durationSeconds: number; // thời gian (giây) tính từ ended_at - start_time
}

const sessions = ref<SessionHistory[]>([]);
const loading = ref(false);
const searchQuery = ref("");
const currentPage = ref(1);
const itemsPerPage = ref(10);
const sortColumn = ref("ended_at");
const sortOrder = ref<"asc" | "desc">("desc");

// Hàm tính durationSeconds khi nhận dữ liệu mới
const processSessions = (data: any[]) => {
  return data.map((item) => {
    const ended = new Date(item.ended_at).getTime();
    const started = new Date(item.connected_time).getTime();
    const durationSeconds = Math.max(0, Math.floor((ended - started) / 1000));

    return {
      ...item,
      durationSeconds,
    };
  });
};

const filteredSessions = computed(() => {
  return sessions.value.filter((session) => {
    const deviceMatch = session.device_name
      ?.toLowerCase()
      .includes(searchQuery.value.toLowerCase());
    const operatorMatch = session.operator_name
      ?.toLowerCase()
      .includes(searchQuery.value.toLowerCase());
    return deviceMatch || operatorMatch;
  });
});

const sortedSessions = computed(() => {
  return [...filteredSessions.value].sort((a, b) => {
    let valA: any = a[sortColumn.value as keyof SessionHistory];
    let valB: any = b[sortColumn.value as keyof SessionHistory];

    // Nếu sort theo durationSeconds thì so sánh số nguyên
    if (sortColumn.value === "durationSeconds") {
      if (valA < valB) return sortOrder.value === "asc" ? -1 : 1;
      if (valA > valB) return sortOrder.value === "asc" ? 1 : -1;
      return 0;
    }

    // So sánh string hoặc date string
    if (valA < valB) return sortOrder.value === "asc" ? -1 : 1;
    if (valA > valB) return sortOrder.value === "asc" ? 1 : -1;
    return 0;
  });
});

const totalPages = computed(() => {
  return Math.ceil(sortedSessions.value.length / itemsPerPage.value);
});

const paginatedSessions = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return sortedSessions.value.slice(start, end);
});

const token = localStorage.getItem("aiot_accesstoken") || "";

const fetchSessionHistory = async () => {
  try {
    loading.value = true;
    const response = await fetch(
      "http://localhost:8000/api/v1/supervisor/sessions/history",
      {
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/json",
        },
      }
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    sessions.value = processSessions(data);
  } catch (error) {
    console.error("Failed to fetch session history:", error);
  } finally {
    loading.value = false;
  }
};

const sortBy = (column: string) => {
  if (sortColumn.value === column) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
  } else {
    sortColumn.value = column;
    sortOrder.value = "asc";
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString();
};

// format durationSeconds thành string dạng "1h 5m 30s"
const formatDuration = (seconds: number) => {
  if (seconds <= 0) return "0s";

  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;

  let result = "";
  if (h > 0) result += `${h}h `;
  if (m > 0) result += `${m}m `;
  if (s > 0) result += `${s}s`;
  return result.trim();
};

watch([itemsPerPage, searchQuery], () => {
  currentPage.value = 1;
});

onMounted(() => {
  fetchSessionHistory();
});
</script>

<style scoped>
/* style không đổi */
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
  width: 300px;
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
  inset: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
}

.loading-spinner {
  border: 6px solid #eee;
  border-top: 6px solid #007bff;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
