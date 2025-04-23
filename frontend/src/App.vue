<script setup lang="ts">
import { useConfirmStore } from '@/stores/confirm'
import { useThemeStore } from '@/stores/theme'

const confirmStore = useConfirmStore()
const isDarkMode = ref(localStorage.getItem('dark') === 'true')
watch(
  isDarkMode,
  (value) => {
    document.body.classList.toggle('dark', value)
  },
  { immediate: true },
)
useThemeStore()
</script>

<template>
  <router-view v-slot="{ Component }">
    <transition name="slide">
      <ErrorBoundary>
        <component :is="Component" />
      </ErrorBoundary>
    </transition>
  </router-view>
  <Toaster />
  <ConfirmationModal
    v-if="confirmStore.visible"
  />
</template>
