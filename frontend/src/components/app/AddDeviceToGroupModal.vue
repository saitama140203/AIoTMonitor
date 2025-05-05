<script setup lang="ts">
import type { DeviceGroup } from '@/types'

const { open } = defineProps({
  open: {
    type: Boolean,
    required: true,
  },
  groups: {
    type: Array as PropType<DeviceGroup[]>,
    default: () => [],
  },
})
const emit = defineEmits(['update:open', 'confirm'])
const selectedGroup = ref('')

function handleCreate() {
  emit('confirm', selectedGroup.value)
  emit('update:open', false)
}
const isCreatable = computed(() => {
  return selectedGroup.value !== ''
})
</script>

<template>
  <Dialog :open="open" @update:open="(value:boolean) => emit('update:open', value)">
    <DialogContent class="sm:max-w-[425px] p-4">
      <DialogHeader>
        <DialogTitle>Add To Group</DialogTitle>
        <DialogDescription>
          Select the group you want to add the device to.
        </DialogDescription>
      </DialogHeader>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="room-name" class="text-left">Group</Label>
        <Select v-model="selectedGroup" class="col-span-4">
          <SelectTrigger class="w-[180px]">
            <SelectValue placeholder="Select a group" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Group</SelectLabel>
              <SelectItem
                v-for="group in groups"
                :key="group.id"
                :value="group.id"
              >
                {{ group.name }}
              </SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
      <DialogFooter>
        <Button
          type="submit"
          :disabled="!isCreatable"
          @click="handleCreate"
        >
          Confirm
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
