<script setup lang="ts">
import { toast } from '@/components/ui/toast'

function showtoast() {
  toast({
    title: 'Hello from the Home Page',
    description: 'This is a toast message from the Home Page',
  })
}
</script>

<template>
  <Button @click="showtoast">
    Click me
  </Button>
  <RouterLink to="/project">
    <Button>
      Go to project
    </Button>
  </RouterLink>
  <br>
  <ColorSelect />
  <br>
  <Icon name="IconBack" class="w-10 h-10 text-primary" />
  <Icon name="IconPlus" class="w-10 h-10 text-primary" />
</template>
