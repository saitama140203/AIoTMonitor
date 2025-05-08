<script setup lang="ts">
import {
  Pagination,
  PaginationEllipsis,
  PaginationFirst,
  PaginationLast,
  PaginationList,
  PaginationListItem,
  PaginationNext,
  PaginationPrev,
} from '@/components/ui/pagination'
import { toast } from '@/components/ui/toast'
import { useDeviceStore } from '@/stores/device'
import { useProfileStore } from '@/stores/profile'
import { type Command, type Device, type DeviceGroup, type User, UserRole } from '@/types'
import { useAsyncState } from '@vueuse/core'

interface Profile {
  id: string
  name: string
  group_id: number
  created_at: string
}
const deviceStore = useDeviceStore()
const profileStore = useProfileStore()
const isCreateProfileModalVisible = ref(false)
const configQuery = ref({
  page: 1,
  limit: 10,
})

const { state: listGroups } = useAsyncState<{ total: number, data: DeviceGroup[] }>(() => {
  const config = {
    skip: 0,
    limit: 1000,
  }
  return deviceStore.getGroupList(config)
}, {
  total: 0,
  data: [],
}, {
  onError: (error) => {
    Promise.reject(error)
  },
})

const { execute, state: listProfiles, isLoading } = useAsyncState<{ total: number, data: Profile[] }>(() => {
  const config = {
    skip: (configQuery.value.page - 1) * configQuery.value.limit,
    limit: configQuery.value.limit,
  }
  return profileStore.getProfileList(config)
}, {
  total: 0,
  data: [],
}, {
  onError: (error) => {
    Promise.reject(error)
  },
})
watch(() => configQuery.value.page, () => {
  execute()
})
function openCreateDeviceModal() {
  isCreateProfileModalVisible.value = true
}
async function handleCreateProfile(data: any) {
  await profileStore.createProfile(data)
  toast({
    title: 'Profile created',
    description: 'The profile has been created successfully.',
  })
  isCreateProfileModalVisible.value = false
  execute()
}
</script>

<template>
  <!-- Welcome -->
  <div class="flex flex-col gap-4 p-4 h-[calc(100vh-64px)]">
    <div class="flex justify-end">
      <Button @click="openCreateDeviceModal">
        Create Profile
      </Button>
    </div>
    <template
      v-if="!isLoading && listProfiles.data.length > 0"
    >
      <div class="relative rounded-lg overflow-hidden shadow-md w-full bg-card overflow-y-auto">
        <div class="grid grid-cols-4 gap-4 p-4 border-b font-semibold sticky top-0 bg-card z-10">
          <div>
            Name
          </div>
          <div>
            Group Device
          </div>
          <div>
            Created At
          </div>
          <div>
            Action
          </div>
        </div>
        <div
          v-for="profile in listProfiles.data"
          :key="profile.id"
          class="grid grid-cols-4 gap-4 p-4 items-center hover:bg-secondary"
        >
          <!-- Avatar and Name -->
          <div class="flex items-center gap-4 truncate">
            {{ profile.name }}
          </div>
          <div class="truncate">
            {{ listGroups.data.find(group => group.id === profile.group_id)?.name || 'No group' }}
          </div>
          <div class="truncate">
            {{ profile.created_at.split('T')[0] }}
          </div>
          <div class="flex items-center gap-2">
            <RouterLink
              :to="`/profiles/${profile.id}`"
              class="text-blue-500 hover:text-blue-700"
            >
              Detail
            </RouterLink>
          </div>
        </div>

        <Pagination
          v-slot="{ page }"
          v-model:page="configQuery.page"
          :items-per-page="configQuery.limit"
          :total="listProfiles.total"
          :sibling-count="1"
          :default-page="configQuery.page"
          show-edges
          class="mt-4 pb-10"
        >
          <PaginationList v-slot="{ items }" class="flex items-center gap-1 justify-center">
            <PaginationFirst />
            <PaginationPrev />

            <template v-for="(item, index) in items">
              <PaginationListItem v-if="item.type === 'page'" :key="index" :value="item.value" as-child>
                <Button class="w-10 h-10 p-0" :variant="item.value === page ? 'default' : 'outline'">
                  {{ item.value }}
                </Button>
              </PaginationListItem>
              <PaginationEllipsis v-else :key="item.type" :index="index" />
            </template>

            <PaginationNext />
            <PaginationLast />
          </PaginationList>
        </Pagination>
      </div>
    </template>
    <span v-else-if="!isLoading && listProfiles.data.length === 0" class="text-center text-muted-foreground">
      No groups found
    </span>
  </div>
  <CreateProfileModal
    v-model:open="isCreateProfileModalVisible"
    :groups="listGroups.data"
    @create="handleCreateProfile"
  />
</template>
