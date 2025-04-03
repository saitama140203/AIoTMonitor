<script setup lang="ts">
import type { ColorsType } from '@/types/theme-type'
import { Button } from '@/components/ui/button'
import { useThemeStore } from '@/stores/theme'
import { ref } from 'vue'

const themeStore = useThemeStore()
function setColor(color: ColorsType) {
  themeStore.setColor(color)
}
const colors = ref<ColorsType[]>(['rose', 'blue', 'green', 'orange', 'zinc'],
)
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="outline">
        {{ themeStore.color }}
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <template v-for="(color, index) in colors" :key="index">
        <DropdownMenuItem @click="setColor(color)">
          {{ color }}
        </DropdownMenuItem>
      </template>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
