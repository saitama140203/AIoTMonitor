<script setup lang="ts">
import type { BodyCreateDevice } from '@/types'

const { open } = defineProps({
  open: {
    type: Boolean,
    required: true,
  },
})
const emit = defineEmits(['update:open', 'create'])
defineExpose({
  close,
})
const device = ref<BodyCreateDevice>({
  name: '',
  username: '',
  ip: '',
  port: 0,
  password: '',
  platform: '',
})
function close() {
  emit('update:open', false)
  device.value = {
    name: '',
    username: '',
    ip: '',
    port: 0,
    password: '',
    platform: '',
  }
}
const isCreatable = computed(() => {
  return !!(device.value?.name && device.value?.ip && device.value.platform && device.value.password)
})
</script>

<template>
  <Dialog :open="open" @update:open="(value:boolean) => emit('update:open', value)">
    <DialogContent class="sm:max-w-[425px] p-4">
      <DialogHeader>
        <DialogTitle>Create new device</DialogTitle>
      </DialogHeader>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="device-name" class="text-left">Name</Label>
        <Input
          id="device-name"
          v-model="device.name"
          placeholder="Enter device name"
          class="col-span-4"
          autocomplete="off"
        />
      </div>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="device-platform" class="text-left">Platform</Label>
        <div class="w-full col-span-4">
          <Select
            v-model="device.platform"
          >
            <SelectTrigger>
              <SelectValue
                placeholder="Select a platform"
              />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem
                  value="linux"
                >
                  Linux
                </SelectItem>
                <SelectItem
                  value="windows"
                >
                  Windows
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
      </div>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="device-ip" class="text-left">IP v4 Address</Label>
        <Input
          id="device-ip"
          v-model="device.ip"
          placeholder="Enter device IP address"
          class="col-span-4"
          autocomplete="off"
        />
      </div>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="device-port" class="text-left">Port</Label>
        <Input
          id="device-port"
          v-model="device.port"
          placeholder="Enter device port"
          class="col-span-4"
          autocomplete="off"
        />
      </div>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="device-username" class="text-left">Username</Label>
        <Input
          id="device-username"
          v-model="device.username"
          placeholder="Enter device username"
          class="col-span-4"
          autocomplete="off"
        />
      </div>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="device-pw" class="text-left">Password</Label>
        <Input
          id="device-pw"
          v-model="device.password"
          placeholder="Enter device password"
          class="col-span-4"
          autocomplete="off"
        />
      </div>
      <DialogFooter>
        <Button
          type="submit"
          :disabled="!isCreatable"
          @click="$emit('create', device)"
        >
          Create
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
