<script setup lang="ts">
import { HoatDongPhong, type Kenh, type Phong, TrangThai } from '@/types'

const { open } = defineProps({
  open: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['update:open', 'create'])

const roomName = ref('')
function handleCreate() {
  if (!roomName.value.trim())
    return
  emit('create', roomName.value)
  emit('update:open', false)
  roomName.value = ''
}
const isCreatable = computed(() => {
  return roomName.value.trim() !== ''
})
</script>

<template>
  <Dialog :open="open" @update:open="(value:boolean) => emit('update:open', value)">
    <DialogContent class="sm:max-w-[425px] p-4">
      <DialogHeader>
        <DialogTitle>Tạo phòng mới</DialogTitle>
        <DialogDescription>
          Nhập tên phòng và nhấn "Tạo" khi bạn sẵn sàng.
        </DialogDescription>
      </DialogHeader>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="room-name" class="text-left"> Tên phòng </Label>
        <Input
          id="room-name"
          v-model="roomName"
          placeholder="Nhập tên phòng"
          class="col-span-4"
          autocomplete="off"
        />
      </div>
      <DialogFooter>
        <Button
          type="submit"
          :disabled="!isCreatable"
          @click="handleCreate"
        >
          Tạo
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
