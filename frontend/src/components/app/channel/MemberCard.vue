<script setup lang="ts">
import type { User } from '@/types'
import { useConfirmStore } from '@/stores/confirm'
import { CheckboxIndicator, CheckboxRoot } from 'reka-ui'

interface UserData extends User {
  isSelected: boolean
}
interface Props {
  user: UserData
  type: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update:selected', value: boolean): void
  (e: 'remove', value: UserData): void
  (e: 'handleRequest', value: UserData, accept: boolean): void
}>()
const confirmStore = useConfirmStore()
const id_selected = defineModel({
  type: Boolean,
})
async function handleRemove() {
  const confirm = await confirmStore.showConfirmDialog({
    title: 'Xóa thành viên',
    message: `Bạn có chắc chắn muốn xóa ${props.user.fullName} khỏi kênh không?`,
  })
  if (!confirm)
    return
  emit('remove', props.user)
}
async function handleAccept(accept: boolean) {
  if (!accept) {
    const confirm = await confirmStore.showConfirmDialog({
      title: 'Từ chối yêu cầu',
      message: `Bạn có chắc chắn muốn từ chối ${props.user.fullName} vào kênh không?`,
    })
    if (!confirm)
      return
    emit('handleRequest', props.user, accept)
  }
  else {
    emit('handleRequest', props.user, accept)
  }
}
</script>

<template>
  <div class="grid grid-cols-7 gap-4 items-center p-4 border-b border-border hover:bg-secondary hover:text-secondary-foreground transition-colors duration-300 cursor-pointer rounded-md">
    <CheckboxRoot
      v-model="id_selected"
      class="hover:bg-green3 flex h-[25px] w-[25px] appearance-none items-center justify-center rounded-[4px] bg-background border border-border shadow-blackA7 shadow-[0_1px_4px_-2px] outline-none"
    >
      <CheckboxIndicator class="h-full w-full rounded flex items-center justify-center">
        <Icon
          name="IconCheck"
          class="h-4 w-4 text-grass11"
        />
      </CheckboxIndicator>
    </CheckboxRoot>
    <div class="col-span-4 flex items-center gap-4">
      <img v-lazy="`https://ui-avatars.com/api/?name=${user.fullName}&background=random&size=300&bold=true`" alt="" class="w-10 h-10 rounded-full object-cover">
      <div class="flex flex-col gap-1">
        <h2 class="text-lg font-semibold truncate-one-line">
          {{ user.fullName }}
        </h2>
        <div class="text-sm text-muted-foreground truncate-one-line">
          {{ user.email }}
        </div>
      </div>
    </div>
    <div class="flex items-center justify-end gap-2 col-span-2">
      <Button
        v-if="type === 'member'"
        type="button"
        variant="destructive"
        @click="handleRemove"
      >
        Xóa khỏi kênh
      </Button>
      <template
        v-else
      >
        <Button
          type="button"
          variant="destructive"
          @click="handleAccept(false)"
        >
          Từ chối
        </Button>
        <Button
          type="button"
          variant="outline"
          @click="handleAccept(true)"
        >
          Chấp nhận
        </Button>
      </template>
    </div>
  </div>
</template>
