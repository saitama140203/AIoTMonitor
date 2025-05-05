<script setup lang="ts">
import type { Command } from '@/types'

interface CommandData extends Command {
  is_selected: boolean
}
const { open } = defineProps({
  open: {
    type: Boolean,
    required: true,
  },
})
const emit = defineEmits(['update:open', 'confirm'])
const searchValue = ref('')
const commands = defineModel({
  type: Array as PropType<CommandData[]>,
  default: () => [],
})
function handleCreate() {
  emit('confirm', commands.value.filter(command => command.is_selected).map(command => command.id))
  emit('update:open', false)
  searchValue.value = ''
  commands.value.forEach((command: CommandData) => {
    command.is_selected = false
  })
}
const commandList = computed(() => {
  return commands.value.filter((command: CommandData) => {
    return command.commands_text.toLowerCase().includes(searchValue.value.toLowerCase())
  })
})
</script>

<template>
  <Dialog :open="open" @update:open="(value:boolean) => emit('update:open', value)">
    <DialogContent class="sm:max-w-6xl p-4">
      <DialogHeader>
        <DialogTitle>Add Command To Profile</DialogTitle>
        <DialogDescription>
          Select the command you want to add to the profile.
        </DialogDescription>
      </DialogHeader>
      <InputSearch
        v-model="searchValue"
        placeholder="Search command..."
      />
      <div class="relative rounded-lg overflow-hidden shadow-md w-full max-h-[460px] bg-card overflow-y-auto">
        <div class="grid grid-cols-3 gap-4 p-4 border-b font-semibold sticky top-0 bg-card z-10">
          <div />
          <div>
            Text
          </div>
          <div>
            Description
          </div>
        </div>
        <div
          v-for="command in commandList"
          :key="command.id"
          class="grid grid-cols-3 gap-4 p-4 items-center hover:bg-secondary"
        >
          <input id="" v-model="command.is_selected" type="checkbox" name="" class="w-4 h-4 cursor-pointer">
          <div>
            {{ command.commands_text }}
          </div>
          <div>
            {{ command.description }}
          </div>
        </div>
      </div>
      <DialogFooter>
        <Button
          type="submit"
          @click="handleCreate"
        >
          Confirm
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
