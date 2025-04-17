<script setup lang="ts">
import { HoatDongPhong, type Kenh, type Phong, TrangThai } from '@/types'

const { open, kenh } = defineProps({
  open: {
    type: Boolean,
    required: true,
  },
  kenh: {
    type: Object as () => Kenh,
    required: false,
  },
})

const emit = defineEmits(['update:open', 'create', 'update'])

const channelName = ref('')
watch(() => open, (value) => {
  if (value && kenh) {
    channelName.value = kenh.tenKenh
  }
  else {
    channelName.value = ''
  }
}, { immediate: true })
function handleCreate() {
  if (!channelName.value.trim())
    return
  if (kenh) {
    emit('update', {
      kenh,
      tenKenh: channelName.value,
    })
  }
  else {
    emit('create', channelName.value)
  }
  emit('update:open', false)
  channelName.value = ''
}
const isCreatable = computed(() => {
  return channelName.value.trim() !== ''
})
</script>

<template>
  <Dialog :open="open" @update:open="(value:boolean) => emit('update:open', value)">
    <DialogContent class="sm:max-w-[425px] p-4">
      <DialogHeader>
        <DialogTitle>{{ kenh ? 'Cập nhật kênh' : 'Tạo kênh mới' }}</DialogTitle>
        <DialogDescription>
          Nhập tên kênh và nhấn "{{ kenh ? 'Cập nhật' : 'Tạo' }}" khi bạn sẵn sàng.
        </DialogDescription>
      </DialogHeader>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="channel-name" class="text-left"> Tên kênh </Label>
        <Input
          id="channel-name"
          v-model="channelName"
          placeholder="Nhập tên kênh"
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
          {{ kenh ? 'Cập nhật' : 'Tạo' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
