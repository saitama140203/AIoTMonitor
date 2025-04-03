<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'
import { Loader2 } from 'lucide-vue-next'
import { Primitive, type PrimitiveProps } from 'radix-vue'
import { type ButtonVariants, buttonVariants } from '.'

interface Props extends PrimitiveProps {
  variant?: ButtonVariants['variant']
  size?: ButtonVariants['size']
  class?: HTMLAttributes['class']
  isLoading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  as: 'button',
})
</script>

<template>
  <Primitive
    :as="as"
    :as-child="asChild"
    :disabled="props.isLoading"
    :class="cn(buttonVariants({ variant, size }), props.class)"
  >
    <template v-if="props.isLoading">
      <Loader2 class="w-4 h-4 animate-spin" />
    </template>
    <template v-else>
      <slot />
    </template>
  </Primitive>
</template>
