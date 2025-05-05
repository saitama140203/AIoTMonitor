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
const emit = defineEmits(['update:open', 'create'])
const profile = ref({
  name: '',
  group_id: '',
})

function handleCreate() {
  emit('create', profile.value)
  emit('update:open', false)
}
const isCreatable = computed(() => {
  return profile.value.name !== '' && profile.value.group_id !== ''
})
</script>

<template>
  <Dialog :open="open" @update:open="(value:boolean) => emit('update:open', value)">
    <DialogContent class="sm:max-w-[425px] p-4">
      <DialogHeader>
        <DialogTitle>Create Profile</DialogTitle>
        <DialogDescription>
          Enter the name of the profile you want to create.
        </DialogDescription>
      </DialogHeader>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="name" class="text-left">Name</Label>
        <Input
          id="name"
          v-model="profile.name"
          placeholder="Enter profile name"
          class="col-span-4"
          autocomplete="off"
        />
      </div>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="room-name" class="text-left">Group</Label>
        <div class="w-full col-span-4">
          <Select v-model="profile.group_id" class="col-span-4">
            <SelectTrigger class="w-full">
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
      </div>
      <DialogFooter>
        <Button
          type="submit"
          :disabled="!isCreatable"
          @click="handleCreate"
        >
          Create
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
