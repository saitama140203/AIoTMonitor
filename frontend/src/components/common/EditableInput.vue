<script setup lang="ts">
const props = defineProps<{
  value: string // initial value
  clickCallback?: () => void
}>()

const emits = defineEmits<{
  (e: 'save', payload: string, isModified?: boolean): void
}>()
const data = ref(props.value)
const isEditing = ref(false)
const inputRef = ref(null)
const componentElement = ref<HTMLElement>()

function startEditing() {
  isEditing.value = true
  if (props.clickCallback && typeof props.clickCallback === 'function') {
    props.clickCallback()
  }
  nextTick(() => {
    componentElement.value?.querySelector('input')?.focus()
  })
}

function finishEditing() {
  if (!data.value.trim()) {
    data.value = 'Untitled'
  }
  isEditing.value = false
  emits('save', data.value, data.value !== props.value)
}
function handleKey(event: KeyboardEvent) {
  if (event.key === 'Enter') {
    isEditing.value = false
  }
  else if (event.key === 'Escape') {
    data.value = props.value
    isEditing.value = false
  }
}
watch(
  () => props.value,
  (value) => {
    data.value = value
  },
)
</script>

<template>
  <span ref="componentElement">
    <slot
      v-if="isEditing"
      name="input"
      :finish-editing="finishEditing"
    >
      <Input
        ref="inputRef"
        v-model="data"
        :style="{ width: `${data.length + 3}ch !important`, maxWidth: '300px', minWidth: '50px' }"
        class="inputText"
        @blur="finishEditing"
        @keydown="handleKey"
      />
    </slot>
    <span
      v-else
      @click="startEditing"
    >
      <slot
        :data="data"
        :is-editing="isEditing"
      >
        <span class="border-transparent px-1 hover:border-muted">
          {{ data }}
        </span>
      </slot>
    </span>
  </span>
</template>
