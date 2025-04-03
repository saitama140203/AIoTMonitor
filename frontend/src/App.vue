<script setup lang="ts">
import { useThemeStore } from '@/stores/theme'

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
</template>
