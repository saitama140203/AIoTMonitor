<template>
  <div class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen w-full">
    <!-- Main scrollable content -->
    <div
      class="main-content max-w-7xl mx-auto my-0 px-3 py-8 h-[92vh] md:h-[calc(100vh-40px)]
            rounded-2xl shadow-lg overflow-y-auto flex flex-col gap-8"
    >
      <!-- Command Quick List -->
    <div class="bg-white shadow rounded-xl p-5">
    <h2 class="text-lg font-semibold mb-3 text-indigo-700 flex items-center gap-2">
      <span class="i-lucide-terminal-square" /> Whitelist
    </h2>
    <div v-if="!commands?.length" class="text-gray-400 flex items-center gap-2">
      <span class="i-lucide-info" /> Không có lệnh nào
    </div>
    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
      <div
        v-for="command in commands"
        :key="command.id"
        class="rounded-2xl border border-indigo-100 bg-indigo-50 shadow p-4 flex flex-col gap-1 items-start min-h-[64px]"
        style="user-select: none;"
      >
        <span class="font-mono text-indigo-800 text-base break-all">{{ command.commands_text }}</span>
        <span v-if="command.description" class="text-xs text-gray-500 mt-1">{{ command.description }}</span>
      </div>
    </div>
  </div>

      <!-- Header -->
      <div class="flex items-center gap-4">
        <div class="bg-indigo-600 text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold shadow">
          {{ profile?.name?.charAt(0)?.toUpperCase() || 'P' }}
        </div>
        <div>
          <h1 class="text-2xl font-bold text-gray-800 mb-1 flex items-center gap-2">
            {{ profile?.name || 'Profile' }}
            <span v-if="profile?.group_name" class="bg-indigo-100 text-indigo-600 text-xs px-2 py-0.5 rounded font-normal ml-2">
              {{ profile?.group_name }}
            </span>
          </h1>
          <p v-if="profile?.created_at" class="text-xs text-gray-400">
            Tạo lúc: {{ formatDate(profile?.created_at) }}
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Device Table -->
        <div>
          <div class="bg-white shadow-md rounded-xl p-5">
            <h2 class="text-lg font-semibold mb-3 text-indigo-700 flex items-center gap-2">
              <span class="i-lucide-server" /> Thiết bị
            </h2>
            <div v-if="!devices?.length" class="text-gray-400 text-center p-6 flex flex-col items-center">
              <span class="i-lucide-box h-8 w-8 mb-2 text-gray-300" /> Không có thiết bị nào
            </div>
            <table v-else class="w-full text-sm border-separate border-spacing-y-2">
              <thead>
                <tr class="bg-indigo-50 text-indigo-700 rounded">
                  <th class="py-2 px-2 rounded-l">Tên</th>
                  <th class="py-2 px-2">IP</th>
                  <th class="py-2 px-2">Trạng thái</th>
                  <th class="py-2 px-2 rounded-r"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="device in devices" :key="device.id"
                  :class="connectedDevice && device.id === connectedDevice.id ? 'bg-indigo-50/90 shadow rounded-xl' : 'hover:bg-indigo-50/50 transition'">
                  <td class="py-2 px-2 font-medium">{{ device.name }}</td>
                  <td class="py-2 px-2 text-gray-600">{{ device.ip }}:{{ device.port }}</td>
                  <td class="py-2 px-2">
                    <span :class="device.status==='active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                          class="px-2 py-1 rounded text-xs font-semibold">
                      {{ device.status === 'active' ? 'Hoạt động' : 'Không hoạt động' }}
                    </span>
                  </td>
                  <td class="py-2 px-2">
                    <button class="px-3 py-1 bg-indigo-600 text-white rounded shadow hover:bg-indigo-700 text-xs transition"
                      @click="onConnectDevice(device)"
                      :disabled="device.status !== 'active' || (connectedDevice && device.id === connectedDevice.id)">
                      {{ connectedDevice && device.id === connectedDevice.id ? "Đang kết nối" : "Kết nối" }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Terminal -->
        <div>
          <div class="bg-black/95 shadow-lg rounded-xl h-96 p-0 flex flex-col relative overflow-hidden border-2 border-indigo-200">
            <div v-if="connectedDevice" class="flex items-center justify-between px-4 py-2 border-b border-indigo-100 bg-indigo-50/60">
              <span class="text-indigo-700">Terminal: <b>{{ connectedDevice.name }}</b>
                <span class="text-xs text-gray-500">({{ connectedDevice.ip }})</span>
              </span>
              <button @click="disconnectDevice" class="text-xs bg-gray-200 px-2 py-1 rounded hover:bg-red-100 hover:text-red-700 transition">
                Đóng
              </button>
            </div>
            <Terminal ref="terminalRef" class="h-full" v-if="connectedDevice" />
            <div v-else class="flex items-center justify-center h-full text-gray-500 font-medium text-lg">
              <span class="i-lucide-terminal mr-2" />Chọn thiết bị để kết nối SSH
            </div>
          </div>
        </div>
      </div>

      <!-- Operator List -->
      <div class="bg-white shadow-md rounded-xl p-5">
        <h2 class="text-lg font-semibold mb-2 text-indigo-700 flex items-center gap-2">
          <span class="i-lucide-user" /> Người vận hành
        </h2>
        <div v-if="!operators?.length" class="text-gray-400">Không có người vận hành nào</div>
        <ul v-else class="space-y-2">
          <li v-for="op in operators" :key="op.id" class="flex items-center gap-2 border-b last:border-b-0 py-1">
            <span class="i-lucide-user-circle text-indigo-300" />
            <b class="text-indigo-700">{{ op.full_name }}</b>
            <span class="text-gray-500 text-xs">({{ op.email }})</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import Terminal from '@/components/Terminal.vue'
import { getProfileResources } from '@/api/profile'
import axios from 'axios'

interface Profile { id: number; name: string; created_at: string; group_id: number; group_name: string }
interface Device { id: number; name: string; ip: string; port: number; status: string; platform: string; lastseen: string }
interface Command { id: number; commands_text: string; description: string; created_by: string | null }
interface Operator { id: number; email: string; full_name: string }

const route = useRoute()
const profileId = ref(Number(route.params.profileId) || 1)

const profile = ref<Profile | null>(null)
const devices = ref<Device[]>([])
const commands = ref<Command[]>([])
const operators = ref<Operator[]>([])
const connectedDevice = ref<Device | null>(null)
const terminalRef = ref<any>(null)

async function loadProfileData() {
  try {
    const response = await getProfileResources(profileId.value, { skip: 0, limit: 1000 })
    profile.value = response.profile
    devices.value = response.devices?.items ?? []
    commands.value = response.commands?.items ?? []
    operators.value = response.operators?.items ?? []
  } catch (e) {
    profile.value = null
    devices.value = []
    commands.value = []
    operators.value = []
  }
}

async function onConnectDevice(device: Device) {
  if (connectedDevice.value && connectedDevice.value.id === device.id) {
    alert('Đã kết nối với thiết bị này.')
    return
  }
  if (connectedDevice.value && connectedDevice.value.id !== device.id) {
    const ok = confirm('Bạn muốn chuyển kết nối sang thiết bị khác? Kết nối cũ sẽ bị ngắt.')
    if (!ok) return
    terminalRef.value?.disconnect()
    connectedDevice.value = null
    await nextTick()
  }
  connectedDevice.value = device
  await nextTick()

  const user = JSON.parse(localStorage.getItem('aiot_user') || '{}')
  const operatorId = user?.user_id || 1

  // Gọi API để lấy session_id từ bảng sessions
  const response = await axios.get('http://localhost:8000/api/v1/supervisor/sessions', {
    params: {
      device_id: device.id,
      operator_id: operatorId
    }
  })

  const sessionId = response.data.session_id
  terminalRef.value?.connect({
    host: device.ip,
    port: device.port,
    username: 'root',
    password: 'secret123',
    profile_id: profileId.value,
    session_id: sessionId

  })
}

function disconnectDevice() {
  terminalRef.value?.disconnect()
  connectedDevice.value = null
}

function sendQuickCommand(cmd: string) {
  if (!connectedDevice.value) {
    alert('Bạn cần kết nối thiết bị trước!')
    return
  }
  if (!cmd) {
    alert('Lệnh không hợp lệ!')
    return
  }
  terminalRef.value?.sendCommand(cmd)
}

function formatDate(dateString?: string) {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('vi-VN', {
      year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit'
    }).format(date)
  } catch { return dateString }
}

onMounted(() => { loadProfileData() })
</script>

<style scoped>
/* Scrollbar đẹp cho main-content */
.main-content::-webkit-scrollbar {
  width: 10px;
}
.main-content::-webkit-scrollbar-thumb {
  background: #e0e7ff;
  border-radius: 8px;
}
</style>
