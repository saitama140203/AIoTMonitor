<script setup lang="ts">
import { useConfirmStore } from '@/stores/confirm'

const confirmStore = useConfirmStore()

const text = ref('Hello world!')

async function showConfirmmation() {
  const confirm = await confirmStore.showConfirmDialog({
    title: 'Are you sure?',
    message: 'This action cannot be undone.',
    confirmText: 'Yes, delete it!',
    cancelText: 'No, cancel!',
  })
  if (confirm) {
    // User confirmed the action
    console.log('Confirmed!')
  }
  else {
    // User canceled the action
    console.log('Canceled!')
  }
}
function saveTitle(newTitle: string) {
  if (newTitle === text.value) {
    return
  }
  text.value = newTitle
  console.log('Title saved:', newTitle)
}
</script>

<template>
  <!-- Welcome -->
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
    <h1 class="text-4xl font-bold text-gray-800 dark:text-white">
      Welcome to My App
    </h1>
    <p class="mt-4 text-lg text-gray-600 dark:text-gray-400">
      This is a simple Vue.js app.
    </p>
    <ColorSelect />
    <EditableInput
      :value="text"
      @save="saveTitle"
    >
      <div class="flex flex-col cursor-pointer">
        <span class="border-transparent hover:border-slate-500 text-base">
          {{ text }}
        </span>
        <span class="text-xs text-gray-500"> Click để chỉnh sửa </span>
      </div>
    </EditableInput>
    <Popover>
      <PopoverTrigger>
        <Button variant="outline" class="mt-4">
          <span>Click me - Popover trigger</span>
        </Button>
      </PopoverTrigger>
      <PopoverContent>
        Some popover content
      </PopoverContent>
    </Popover>
    <br>
    <Button size="sm" class="w-32" @click="showConfirmmation">
      Show confirmation
    </Button>
  </div>
</template>
