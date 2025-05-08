<script setup lang="ts">
import { toast } from '@/components/ui/toast'
import { useAdminStore } from '@/stores/admin'

import { useProfileStore } from '@/stores/profile'
import { type Command, type Device, type DeviceGroup, type User, UserRole } from '@/types'
import { useAsyncState } from '@vueuse/core'

interface ProfileDetail {
  name: string
  operators: string[]
  commands: string[]
}

interface CommandData extends Command {
  is_selected: boolean
}
const profileStore = useProfileStore()
const route = useRoute()
const { id } = route.params as { id: string }

const isCreateCommandModalVisible = ref(false)
const isAssignProfileToUserModalVisible = ref(false)
const { state, execute } = useAsyncState<ProfileDetail>(async () => {
  const response = await profileStore.getProfileDetail(id as unknown as number)
  return response.data
}, {
  name: '',
  operators: [],
  commands: [],
}, {
  onError: (error) => {
    Promise.reject(error)
  },
})

const { state: commands, execute: fetchUnassignedCommnands } = useAsyncState<CommandData[]>(async () => {
  const response = await profileStore.getUnassignedCommnands(id as unknown as number)
  response.data.forEach((command: any) => {
    command.is_selected = false
  })
  return response.data
}, [])
const { state: operators, execute:  fetchUnassignedProfileList} = useAsyncState(async () => {
  const response = await profileStore.getUnassignedProfileList(id as unknown as number)
  return response.data
}, [])
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
    profile_id: id,
  })
  execute()
  fetchUnassignedCommnands()
  toast({
    title: 'Command added to profile',
    description: 'The command has been added to the profile successfully.',
  })
}
async function handleAssignProfileToUser(operator: User) {
  await profileStore.assignProfile({
    operator_id: operator.id,
    profile_id: id,
  })
  toast({
    title: 'Profile assigned to user',
    description: 'The profile has been assigned to the user successfully.',
  })
  
  execute()
  fetchUnassignedProfileList()
}

function openCreateCommandModal() {
  isCreateCommandModalVisible.value = true
}
function openAssignModal() {
  isAssignProfileToUserModalVisible.value = true
}
</script>

<template>
  <div
    class="flex flex-col gap-4 p-4 h-[calc(100vh-64px)] overflow-y-auto"
  >
    <div class="container mx-auto mt-4 bg-card rounded-lg p-4 shadow-md">
      <div class="flex gap-2 justify-end">
        <Button
          variant="outline"
          @click.stop="openAssignModal()"
        >
          Assign to User
        </Button>
        <Button
          @click.stop="openCreateCommandModal()"
        >
          Update Commands
        </Button>
      </div>
      <template v-if="state">
        <div class="flex flex-col gap-2">
          <h2 class="text-lg font-semibold">
            Profile Name: {{ state.name }}
          </h2>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div class="flex flex-col gap-2">
            <table class="table-auto border-collapse border border-gray-300 w-full">
              <thead>
              <tr>
                <th class="border border-gray-300 px-4 py-2 text-left">Operators (Username)</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(operator, index) in state.operators" :key="index">
                <td class="border border-gray-300 px-4 py-2">{{ operator }}</td>
              </tr>
              </tbody>
            </table>
          </div>
          <div class="flex flex-col gap-2">
            <table class="table-auto border-collapse border border-gray-300 w-full">
              <thead>
              <tr>
                <th class="border border-gray-300 px-4 py-2 text-left">Commands</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="(command, index) in state.commands" :key="index">
                <td class="border border-gray-300 px-4 py-2">{{ command }}</td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </div>

    <AddCommandToProfileModal
      v-model:open="isCreateCommandModalVisible"
      v-model="commands"
      @confirm="handleAddCommandToProfile"
    />
    <AssignProfileToUserModal
      v-model:open="isAssignProfileToUserModalVisible"
      :operators="operators"
      @assign="handleAssignProfileToUser"
    />
  </div>
</template>
