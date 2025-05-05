<script setup lang="ts">
import type { Command } from '@/types'
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
import { useCommandStore } from '@/stores/command'
import { useAsyncState } from '@vueuse/core'

interface CommandData extends Command {
  is_selected: boolean
}
const commandStore = useCommandStore()
const isCreateCommandModalVisible = ref(false)
const createDeviceModal = ref<any>(null)
const configQuery = ref({
  page: 1,
  limit: 10,
  username: '',
  status: 'all',
})

const { execute, state: commands, isLoading } = useAsyncState<{ total: number, commands: CommandData[] }>(async () => {
  const config = {
    skip: (configQuery.value.page - 1) * configQuery.value.limit,
    limit: configQuery.value.limit,
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

watch(() => configQuery.value.page, () => {
  execute()
})

function openCreateCommandModal() {
  isCreateCommandModalVisible.value = true
}

async function handleCreateCommand(data: any) {
  console.log('Creating command:', data)
  await commandStore.createCommand(data)
  toast({
    title: 'Device created successfully',
    description: 'The device has been created successfully.',
  })
  isCreateCommandModalVisible.value = false
  execute()
  createDeviceModal.value?.close()
}
</script>

<template>
  <!-- Welcome -->
  <div class="flex flex-col gap-4 p-4 h-[calc(100vh-64px)]">
    <div class="flex justify-end">
      <Button @click="openCreateCommandModal">
        Create new Command
      </Button>
    </div>
    <template
      v-if="!isLoading && commands.commands.length > 0"
    >
      <div class="relative rounded-lg overflow-hidden shadow-md w-full bg-card overflow-y-auto">
        <div class="grid grid-cols-2 gap-4 p-4 border-b font-semibold sticky top-0 bg-card z-10">
          <div>
            Text
          </div>
          <div>
            Description
          </div>
        </div>
        <div
          v-for="command in commands.commands"
          :key="command.id"
          class="grid grid-cols-2 gap-4 p-4 items-center hover:bg-secondary"
        >
          <div>
            {{ command.commands_text }}
          </div>
          <div>
            {{ command.description }}
          </div>
        </div>

        <Pagination
          v-slot="{ page }"
          v-model:page="configQuery.page"
          :items-per-page="configQuery.limit"
          :total="commands.total"
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
    <span v-else-if="!isLoading && commands.commands.length === 0" class="text-center text-muted-foreground">
      No devices found
    </span>
  </div>
  <CreateCommandModal
    v-model:open="isCreateCommandModalVisible"
    @create="handleCreateCommand"
  />

  <!-- <AddDeviceToGroupModal
    v-model:open="isAddDeviceToGroupModalVisible"
    :groups="listGroups.data"
    @confirm="handleAddDeviceToGroup"
  /> -->
</template>
