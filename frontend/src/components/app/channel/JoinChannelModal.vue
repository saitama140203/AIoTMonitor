<script setup lang="ts">
import { HoatDongPhong, type Kenh, type Phong, TrangThai } from '@/types'

const { open } = defineProps({
  open: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['update:open', 'create'])

const channelId = ref('')
function handleCreate() {
  if (!channelId.value.trim())
    return
  emit('create', channelId.value)
  emit('update:open', false)
  channelId.value = ''
}
const isCreatable = computed(() => {
  return channelId.value.trim() !== ''
})
</script>

<template>
  <Dialog :open="open" @update:open="(value:boolean) => emit('update:open', value)">
    <DialogContent class="sm:max-w-[425px] p-4">
      <DialogHeader>
        <DialogTitle>Yêu cầu tham gia kênh</DialogTitle>
        <DialogDescription>
            Nhập mã kênh và nhấn "Gửi yêu cầu" khi bạn sẵn sàng.
        </DialogDescription>
      </DialogHeader>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="channel-id" class="text-left"> Mã kênh </Label>
        <Input
          id="channel-id"
          v-model="channelId"
          placeholder="Nhập mã kênh"
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
          Gửi yêu cầu
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
