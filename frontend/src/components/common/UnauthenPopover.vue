<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { PopoverClose } from 'reka-ui'

const props = defineProps({
  title: String,
  content: String,
  isRequired: Boolean,
})
</script>

<template>
  <Popover>
    <PopoverTrigger v-if="props.isRequired" as-child>
      <slot>
        <Button>
          Button trigger
        </Button>
      </slot>
    </PopoverTrigger>
    <template v-else>
      <slot>
        <Button>
          Button trigger
        </Button>
      </slot>
    </template>
    <PopoverContent class="w-80 popover-custom">
      <div class="flex flex-col gap-2 bg-transparent">
        <h4 class="title text-sm font-semibold">
          {{ props.title }}
        </h4>
        <p class="font-light">
          {{ props.content }}
        </p>
        <div class="flex justify-end gap-2 bg-transparent">
          <PopoverClose class="bg-transparent">
            <Button variant="outline" class="rounded-full">
              Không phải bây giờ
            </Button>
          </PopoverClose>
          <RouterLink to="/auth/login">
            <Button class="rounded-full">
              Đăng nhập ngay
            </Button>
          </RouterLink>
        </div>
      </div>
    </PopoverContent>
  </Popover>
</template>

<style lang="scss">
.popover-custom {
  background: url('@/assets/images/Logo_Slooh_Vertical.png') center !important;
  background-size: 60px !important;
  background-repeat: no-repeat !important;
  background-position: top right !important;
  background-color: hsl(var(--background)) !important;
}
</style>
