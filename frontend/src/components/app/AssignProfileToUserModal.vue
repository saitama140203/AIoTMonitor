<script setup lang="ts">
import type { User } from '@/types'
import { Combobox, ComboboxAnchor, ComboboxEmpty, ComboboxGroup, ComboboxInput, ComboboxItem, ComboboxItemIndicator, ComboboxList, ComboboxTrigger } from '@/components/ui/combobox'
import { Check, ChevronsUpDown, Search } from 'lucide-vue-next'

const { open } = defineProps({
  open: {
    type: Boolean,
    required: true,
  },
  operators: {
    type: Array as () => User[],
    default: () => [],
    required: true,
  },
})
const emit = defineEmits(['update:open', 'assign'])

const value = ref<User>()
function handleCreate() {
  if (!value.value)
    return
  emit('assign', value.value)
  emit('update:open', false)
  value.value = undefined
}
const isCreatable = computed(() => {
  return !!value.value
})
</script>

<template>
  <Dialog :open="open" @update:open="(value:boolean) => emit('update:open', value)">
    <DialogContent class="sm:max-w-[425px] p-4">
      <DialogHeader>
        <DialogTitle>Assign Profile To Operator</DialogTitle>
        <DialogDescription>
          Enter the name of the group you want to create.
        </DialogDescription>
      </DialogHeader>
      <div class="grid grid-cols-5 items-center gap-4">
        <Label for="room-name" class="text-left">Name</Label>
        <Combobox v-model="value" by="label">
          <ComboboxAnchor as-child>
            <ComboboxTrigger as-child>
              <Button variant="outline" class="justify-between">
                {{ value?.full_name ? `${value.full_name} - ${value.username}` : 'Select operator' }}

                <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
              </Button>
            </ComboboxTrigger>
          </ComboboxAnchor>

          <ComboboxList>
            <div class="relative w-full max-w-sm items-center">
              <ComboboxInput class="pl-9 focus-visible:ring-0 border-0 border-b rounded-none h-10" placeholder="Select operator..." />
              <span class="absolute start-0 inset-y-0 flex items-center justify-center px-3">
                <Search class="size-4 text-muted-foreground" />
              </span>
            </div>

            <ComboboxEmpty>
              No operator found.
            </ComboboxEmpty>

            <ComboboxGroup>
              <ComboboxItem
                v-for="user in operators"
                :key="user.id"
                :value="user"
              >
                {{ user.full_name }} - {{ user.username }}

                <ComboboxItemIndicator>
                  <Check />
                </ComboboxItemIndicator>
              </ComboboxItem>
            </ComboboxGroup>
          </ComboboxList>
        </Combobox>
      </div>
      <DialogFooter>
        <Button
          type="submit"
          :disabled="!isCreatable"
          @click="handleCreate"
        >
          Assign
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
