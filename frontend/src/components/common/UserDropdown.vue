<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { useUserStore } from '@/stores/user'

const authStore = useAuthStore()
const userStore = useUserStore()
const themeStore = useThemeStore()
</script>

<template>
  <DropdownMenu v-if="userStore?.user">
    <DropdownMenuTrigger as-child>
      <Button variant="ghost" class="relative lg:px-6 py-6 lg:w-40">
        <div class="max-lg:hidden  grid flex-1 text-left text-sm leading-tight">
          <span class="truncate font-semibold">{{ userStore.user.username }}</span>
          <span class="truncate text-xs">{{ userStore.user.email }}</span>
        </div>
        <Icon name="IconArrowDown" class="ml-4" />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent class="w-40 rounded-lg" side="bottom" align="end" :side-offset="4">
      <DropdownMenuItem>
        <div class="flex justify-between item-centers w-full">
          <span>Dark Mode</span><Switch :model-value="themeStore.theme === 'dark'" @update:model-value="themeStore.toggleTheme()" />
        </div>
      </DropdownMenuItem>
      <DropdownMenuSeparator />
      <RouterLink to="/update-password">
        <DropdownMenuItem class="cursor-pointer">
          Update Password
        </DropdownMenuItem>
      </RouterLink>
      <DropdownMenuSeparator />
      <DropdownMenuItem @click="authStore.logout()">
        Log out
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
