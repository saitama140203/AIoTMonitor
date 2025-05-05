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
import { useUserStore } from '@/stores/user'
import { type Device, type DeviceGroup, UserRole } from '@/types'
import { useAsyncState } from '@vueuse/core'
import { MoreHorizontal } from 'lucide-vue-next'

const deviceStore = useDeviceStore()
const userStore = useUserStore()
const isCreateGroupModalVisible = ref(false)
const configQuery = ref({
  page: 1,
  limit: 10,
  username: '',
  status: 'all',
})
const { execute, state: listGroups, isLoading } = useAsyncState<{ total: number, data: DeviceGroup[] }>(() => {
  const config = {
    skip: (configQuery.value.page - 1) * configQuery.value.limit,
    limit: configQuery.value.limit,
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

function openCreateDeviceModal() {
  isCreateGroupModalVisible.value = true
}
async function handleCreateDevice(data: any) {
  await deviceStore.createGroup(data)
  toast({
    title: 'Device created successfully',
    description: 'The device has been created successfully.',
  })
  isCreateGroupModalVisible.value = false
  execute()
}
</script>

<template>
  <!-- Welcome -->
  <div class="flex flex-col gap-4 p-4 h-[calc(100vh-64px)]">
    <div class="flex justify-end">
      <Button @click="openCreateDeviceModal">
        Create Group
      </Button>
    </div>
    <template
      v-if="!isLoading && listGroups.data.length > 0"
    >
      <div class="relative rounded-lg overflow-hidden shadow-md w-full bg-card overflow-y-auto">
        <div class="grid grid-cols-3 gap-4 p-4 border-b font-semibold sticky top-0 bg-card z-10">
          <div>
            Name
          </div>
          <div>
            Status
          </div>
          <div>
            Created At
          </div>
        </div>
        <div
          v-for="device in listGroups.data"
          :key="device.id"
          class="grid grid-cols-3 gap-4 p-4 items-center hover:bg-secondary"
        >
          <!-- Avatar and Name -->
          <div class="flex items-center gap-4 truncate">
            {{ device.name }}
          </div>
          <div class="truncate">
            {{ device.is_actived ? 'Active' : 'Inactive' }}
          </div>
          <div class="truncate">
            {{ device.created_at.split('T')[0] }}
          </div>

        </div>

        <Pagination
          v-slot="{ page }"
          v-model:page="configQuery.page"
          :items-per-page="configQuery.limit"
          :total="listGroups.total"
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
    <span v-else-if="!isLoading && listGroups.data.length === 0" class="text-center text-muted-foreground">
      No groups found
    </span>
  </div>
  <CreateGroupModal
    v-model:open="isCreateGroupModalVisible"
    @create="handleCreateDevice"
  />
</template>
