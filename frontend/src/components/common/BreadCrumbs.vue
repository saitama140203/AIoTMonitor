<script setup lang="ts">
interface Props {
  items: Array<{
    text: string
    to?: string
    disabled?: boolean
  }>
}
const props = defineProps<Props>()
</script>

<template>
  <ol class="flex flex-wrap items-center gap-1.5 break-words text-md text-muted-foreground sm:gap-2.5">
    <template
      v-for="(item, index) in props.items"
      :key="index"
    >
      <li
        v-if="item.to && !item.disabled"
        class="inline-flex items-center gap-1.5"
      >
        <RouterLink :to="item.to" class="transition-colors hover:text-foreground">
          {{ item.text }}
        </RouterLink>
      </li>
      <li
        v-else-if="item.disabled"
        class="inline-flex items-center gap-1.5"
      >
        <span class="font-normal text-foreground">{{ item.text }}</span>
      </li>
      <Icon v-if="index < items.length - 1" name="IconChevronRight" class="w-3 h-3" />
    </template>
  </ol>
</template>
