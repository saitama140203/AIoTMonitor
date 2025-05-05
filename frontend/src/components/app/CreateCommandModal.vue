<script setup lang="ts">
const { open } = defineProps({
  open: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['update:open', 'create'])

const command = ref({
  commands_text: '',
  description: '',
})
function handleCreate() {
  if (!command.value.commands_text.trim())
    return
  emit('create', command.value)
  emit('update:open', false)
  command.value.commands_text = ''
  command.value.description = ''
}
const isCreatable = computed(() => {
  return command.value.commands_text.trim() !== '' && command.value.description.trim() !== ''
})
</script>

<template>
  <Dialog :open="open" @update:open="(value:boolean) => emit('update:open', value)">
    <DialogContent class="sm:max-w-[425px] p-4">
      <DialogHeader>
        <DialogTitle>Create new command</DialogTitle>
        <DialogDescription>
          Enter the command text and description you want to create.
        </DialogDescription>
      </DialogHeader>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="command-text" class="text-left">Text</Label>
        <Input
          id="command-text"
          v-model="command.commands_text"
          placeholder="Enter command text"
          class="col-span-4"
          autocomplete="off"
        />
      </div>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="command-text" class="text-left">Description</Label>
        <Input
          id="command-text"
          v-model="command.description"
          placeholder="Enter command description"
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
          Create
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
