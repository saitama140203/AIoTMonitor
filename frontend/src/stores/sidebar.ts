import { defineStore } from 'pinia'

export const useSidebarStore = defineStore('sidebar', () => {
  const isOpen = ref(false)
  const toggle = () => {
    isOpen.value = !isOpen.value
  }
  const open = () => {
    isOpen.value = true
  }
  const close = () => {
    isOpen.value = false
  }
  return { isOpen, toggle, open, close }
})
