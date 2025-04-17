<script setup lang="ts">
import EditableInput from '@/components/common/EditableInput.vue'
import UserDropdown from '@/components/common/UserDropdown.vue'
import Button from '@/components/ui/button/Button.vue'
import { useSidebarStore } from '@/stores/sidebar'
import { useUserStore } from '@/stores/user'

const sidebarStore = useSidebarStore()
function toggleSidebar() {
  sidebarStore.toggle()
}
const userStore = useUserStore()
function handleSaveTitle(title: string) {
  console.log('Title saved:', title)
}
</script>

<template>
  <div class="app-header">
    <div class="app-header-part">
      <RouterLink
        to="/rooms"
        class="gap-2 ml-6 cursor-pointer flex items-center hover:bg-muted rounded-lg py-2 px-4"
      >
        <Icon name="IconArrowRight" class="w-6 h-6 rotate-180" />
      </RouterLink>
      <div class="flex items-center mr-4">
        <EditableInput
          v-slot="{ data }"
          class="text-lg font-medium"
          value="Untitled"
          @save="handleSaveTitle"
        >
          <div class="flex flex-col cursor-pointer">
            <span class="border-transparent hover:border-slate-500 text-base">
              {{ data }}
            </span>
            <span class="text-xs text-gray-500"> Click để chỉnh sửa </span>
          </div>
        </EditableInput>
      </div>
    </div>
    <div class="app-header-part">
      <Button
        variant="secondary"
        class="text-sm rounded-full"
      >
        <Icon name="IconTheme" class="w-5 h-5" />
        Chủ đề chung
      </Button>
      <Button
        variant="secondary"
        class="text-sm rounded-full"
      >
        <Icon name="IconEyeOn" class="w-5 h-5" />
        Xem trước
      </Button>

      <Separator orientation="vertical" class="h-6" />
      <Button
        variant="secondary"
        class="text-sm rounded-full"
      >
        Hủy bỏ
      </Button>
      <Button
        class="text-sm rounded-full"
      >
        Lưu
      </Button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.app-header {
  @apply flex items-center justify-between w-full h-full gap-1 p-2 lg:pr-8 bg-card shadow-lg;
}
.app-header-part {
    @apply flex items-center gap-2;
}
</style>
