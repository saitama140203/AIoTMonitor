<script setup lang="ts">
defineProps<{
  placeholder: string
}>()
const searchValue = defineModel({
  type: String,
  default: '',
})
</script>

<template>
  <div class="relative w-full max-w-sm items-center">
    <Input id="search" v-model="searchValue" type="text" :placeholder="placeholder || 'Search...'" class="px-10" />
    <span class="absolute start-0 inset-y-0 flex items-center justify-center px-2">
      <Icon name="IconSearch" class="w-5 text-muted-foreground" />
    </span>
    <span
      v-if="searchValue"
      class="absolute end-0 inset-y-0 flex items-center justify-center px-2 cursor-pointer" @click="searchValue = ''"
    >
      <Icon name="IconClose" class="w-6 text-muted-foreground" />
    </span>
  </div>
</template>
