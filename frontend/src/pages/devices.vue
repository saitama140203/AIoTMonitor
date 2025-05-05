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

interface DeviceData extends Device {
  is_selected: boolean
}
const deviceStore = useDeviceStore()
const isCreateDeviceModalVisible = ref(false)
const isAddDeviceToGroupModalVisible = ref(false)
const createDeviceModal = ref<any>(null)
const configQuery = ref({
  page: 1,
  limit: 10,
  username: '',
  status: 'all',
})
const { execute, state: listDevices, isLoading } = useAsyncState<{ total: number, data: DeviceData[] }>(async () => {
  const config = {
    skip: (configQuery.value.page - 1) * configQuery.value.limit,
    limit: configQuery.value.limit,
    username: configQuery.value.username,
    status: configQuery.value.status === 'all' ? undefined : configQuery.value.status,
  }
  const response = await deviceStore.getDeviceList(config)
  response.data.forEach((device: any) => {
    device.is_selected = false
  })
  return response
}, {
  total: 0,
  data: [] as DeviceData[],
}, {
  onError: (error) => {
    Promise.reject(error)
  },
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

function openCreateDeviceModal() {
  isCreateDeviceModalVisible.value = true
}

async function handleCreateDevice(data: any) {
  await deviceStore.createDevice(data)
  toast({
    title: 'Device created successfully',
    description: 'The device has been created successfully.',
  })
  isCreateDeviceModalVisible.value = false
  execute()
  createDeviceModal.value?.close()
}
function addToGroup() {
  const selectedDevices = listDevices.value.data.filter((device: DeviceData) => device.is_selected)
  if (selectedDevices.length === 0) {
    toast({
      title: 'No devices selected',
      description: 'Please select at least one device to add to the group.',
      variant: 'destructive',
    })
  }
  else {
    isAddDeviceToGroupModalVisible.value = true
  }
}
async function handleAddDeviceToGroup(data: any) {
  const selectedDevices = listDevices.value.data.reduce((arr: number[], curr: DeviceData) => {
    if (curr.is_selected) {
      arr.push(curr.id)
    }
    return arr
  }, [])
  console.log('Adding devices to group:', selectedDevices, data)
  await deviceStore.addDeviceToGroup(selectedDevices, data)
  isAddDeviceToGroupModalVisible.value = false
  toast({
    title: 'Devices added to group successfully',
    description: 'The devices have been added to the group successfully.',
  })
  execute()
}
</script>

<template>
  <!-- Welcome -->
  <div class="flex flex-col gap-4 p-4 h-[calc(100vh-64px)]">
    <div class="flex justify-end">
      <Button @click="openCreateDeviceModal">
        Create Device
      </Button>

      <Button
        class="ml-2"
        @click="addToGroup"
      >
        Add to Group
      </Button>
    </div>
    <template
      v-if="!isLoading && listDevices.data.length > 0"
    >
      <div class="relative rounded-lg overflow-hidden shadow-md w-full bg-card overflow-y-auto">
        <div class="grid grid-cols-7 gap-4 p-4 border-b font-semibold sticky top-0 bg-card z-10">
          <div>
            Group
          </div>
          <div>
            Name
          </div>
          <div>
            Username
          </div>
          <div>
            Ip address
          </div>
          <div>
            Platform
          </div>
          <div>Port</div>
          <div>Status</div>
        </div>
        <div
          v-for="device in listDevices.data"
          :key="device.id"
          class="grid grid-cols-7 gap-4 p-4 items-center hover:bg-secondary"
        >
          <!-- Avatar and Name -->
          <div class="flex gap-2 items-center">
            <input id="" v-model="device.is_selected" type="checkbox" name="" class="w-4 h-4 cursor-pointer">
            {{ listGroups.data.find((group) => group.id === device.group_id)?.name }}
          </div>
          <div class="flex items-center gap-4 truncate">
            {{ device.name }}
          </div>
          <div class="flex items-center gap-4 truncate">
            {{ device.username }}
          </div>
          <div class="truncate">
            {{ device.ip }}
          </div>
          <div>
            {{ device.platform }}
          </div>
          <div>{{ device.port }}</div>
          <div class="flex justify-between items-center gap-2">
            <span
              class="px-2 py-1 rounded text-sm truncate"
              :class="[device.status === 'active' ? 'bg-success' : 'bg-destructive']"
            >
              {{ device.status === 'active' ? 'Active' : 'Inactive' }}
            </span>
          </div>
        </div>

        <Pagination
          v-slot="{ page }"
          v-model:page="configQuery.page"
          :items-per-page="configQuery.limit"
          :total="listDevices.total"
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
    <span v-else-if="!isLoading && listDevices.data.length === 0" class="text-center text-muted-foreground">
      No devices found
    </span>
  </div>
  <CreateDeviceModal
    ref="createDeviceModal"
    v-model:open="isCreateDeviceModalVisible"
    @create="handleCreateDevice"
  />

  <AddDeviceToGroupModal
    v-model:open="isAddDeviceToGroupModalVisible"
    :groups="listGroups.data"
    @confirm="handleAddDeviceToGroup"
  />
</template>
