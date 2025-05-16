<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getProfile } from '@/api/profile'

interface Profile {
  id: number
  name: string
  description?: string
}

const myProfiles = ref<Profile[]>([])
const isLoading = ref(false)
const errorMsg = ref<string | null>(null)
const searchTerm = ref('')
const router = useRouter()

const filteredProfiles = computed(() => {
  if (!searchTerm.value) return myProfiles.value
  return myProfiles.value.filter(p =>
    p.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

async function loadProfiles() {
  isLoading.value = true
  errorMsg.value = null
  try {
    const response = await getProfile({})
    myProfiles.value = response.data || []
  } catch (err: any) {
    console.error(err)
    errorMsg.value = err.message || 'Không thể tải Profile'
  } finally {
    isLoading.value = false
  }
}

function goToDetails(profileId: number) {
  if (profileId !== undefined && profileId !== null && !isNaN(Number(profileId))) {
    console.log('Gọi API với profileId:', profileId, 'typeof:', typeof profileId)
    router.push(`/profile-resources/${profileId}`)
  } else {
    errorMsg.value = 'ID profile không hợp lệ'
  }
}


onMounted(loadProfiles)
</script>

<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Profiles của bạn</h1>

    <!-- Search box -->
    <div class="mb-4">
      <input
        v-model="searchTerm"
        type="text"
        placeholder="Tìm kiếm profile..."
        class="w-full p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300"
      />
    </div>

    <!-- Error / Loading / Empty -->
    <p v-if="errorMsg" class="text-red-500 mb-4">{{ errorMsg }}</p>
    <div v-else-if="isLoading" class="flex justify-center py-10">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
    </div>
    <p v-else-if="filteredProfiles.length === 0" class="text-gray-500 py-6 text-center">
      Không tìm thấy profile nào.
    </p>

    <!-- Grid of cards -->
    <div v-else class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="profile in filteredProfiles"
        :key="profile.id"
        class="bg-white shadow-md rounded-lg hover:shadow-lg transition-shadow overflow-hidden"
      >
        <div class="p-4 flex flex-col h-full">
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-xl font-semibold truncate">{{ profile.name }}</h2>
            <button
              @click="goToDetails(profile.id)"
              class="text-blue-600 hover:text-blue-800 focus:outline-none"
            >
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg"
                   fill="none" viewBox="0 0 24 24"
                   stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round"
                      stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
          <p v-if="profile.description"
             class="text-gray-600 text-sm mb-3">{{ profile.description }}</p>
          <span class="mt-auto inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">
            ID: {{ profile.id }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
