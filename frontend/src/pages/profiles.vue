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
import { useAdminStore } from '@/stores/admin'
import { useCommandStore } from '@/stores/command'
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
interface CommandData extends Command {
  is_selected: boolean
}
const deviceStore = useDeviceStore()
const commandStore = useCommandStore()
const profileStore = useProfileStore()
const adminStore = useAdminStore()

const selectedProfile = ref('')
const isCreateProfileModalVisible = ref(false)
const isCreateCommandModalVisible = ref(false)
const isAssignProfileToUserModalVisible = ref(false)
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

const { state: commands } = useAsyncState<{ total: number, commands: CommandData[] }>(async () => {
  const config = {
    skip: 0,
    limit: 5000,
  }
  const response = await commandStore.getCommandList(config)
  response.commands.forEach((device: any) => {
    device.is_selected = false
  })
  return response
}, {
  total: 0,
  commands: [] as CommandData[],
}, {
  onError: (error) => {
    Promise.reject(error)
  },
})
const { state: operators } = useAsyncState(async () => {
  const config = {
    skip: 0,
    limit: 1000,
  }
  const response = await adminStore.getListUsers(config)
  return response.filter((user: any) => user.roles.some((role: any) => role.name === UserRole.OPERATOR))
}, [], {
  onError: (error) => {
    Promise.reject(error)
  },
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
function openCreateCommandModal(profileId: string) {
  selectedProfile.value = profileId
  isCreateCommandModalVisible.value = true
}
function openAssignModal(profileId: string) {
  selectedProfile.value = profileId
  isAssignProfileToUserModalVisible.value = true
}
async function handleAddCommandToProfile(data: any) {
  if (data.length === 0) {
    toast({
      title: 'No command selected',
      description: 'Please select at least one command.',
      variant: 'destructive',
    })
    return
  }
  await profileStore.addCommandToProfile({
    command_ids: data,
    profile_id: selectedProfile.value,
  })
  selectedProfile.value = ''
  toast({
    title: 'Command added to profile',
    description: 'The command has been added to the profile successfully.',
  })
}
async function handleAssignProfileToUser(operator: User) {
  await profileStore.assignProfile({
    operator_id: operator.id,
    profile_id: selectedProfile.value,
  })
  toast({
    title: 'Profile assigned to user',
    description: 'The profile has been assigned to the user successfully.',
  })
  selectedProfile.value = ''
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
            <Button
              variant="secondary"
              @click.stop="openAssignModal(profile.id)"
            >
              Assign to User
            </Button>
            <Button
              @click.stop="openCreateCommandModal(profile.id)"
            >
              Update Commands
            </Button>
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
  <AddCommandToProfileModal
    v-model:open="isCreateCommandModalVisible"
    v-model="commands.commands"
    @confirm="handleAddCommandToProfile"
  />
  <AssignProfileToUserModal
    v-model:open="isAssignProfileToUserModalVisible"
    :profile-id="selectedProfile"
    :operators="operators"
    @assign="handleAssignProfileToUser"
  />
</template>
