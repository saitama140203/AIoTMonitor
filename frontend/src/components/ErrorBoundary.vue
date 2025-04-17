<script setup>
import { toast } from '@/components/ui/toast'

onMounted(() => {
  window.addEventListener('unhandledrejection', (event) => {
    event.promise.catch((error) => {
      const errorMessage = error?.response?.data?.detail || 'Something went wrong.'
      if (errorMessage) {
        toast({
          title: 'Lỗi',
          description: errorMessage,
          variant: 'destructive',
          duration: 5000,
        })
        return
      }

      toast({
        title: 'Uh oh! Something went wrong.',
        description: 'There was a problem with your request.',
        variant: 'destructive',
        duration: 5000,
      })
    })
  })
})

onUnmounted(() => {
  window.removeEventListener('unhandledrejection', () => {})
})
</script>

<template>
  <slot />
</template>
