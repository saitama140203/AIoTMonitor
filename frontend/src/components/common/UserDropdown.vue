<script setup>
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { useUserStore } from '@/stores/user'

const authStore = useAuthStore()
const userStore = useUserStore()
const themeStore = useThemeStore()

function handleChange(value) {
  themeStore.setTheme(value ? 'dark' : 'light')
}
</script>

<template>
  <DropdownMenu v-if="userStore?.user">
    <DropdownMenuTrigger as-child>
      <Button variant="ghost" class="relative lg:px-6 py-6 lg:w-60">
        <Avatar class="h-8 w-8 rounded-lg">
          <AvatarImage :src="userStore.user.avatar" :alt="userStore.user.name" />
          <AvatarFallback class="rounded-lg">
            CN
          </AvatarFallback>
        </Avatar>
        <div class="max-lg:hidden  grid flex-1 text-left text-sm leading-tight">
          <span class="truncate font-semibold">{{ userStore.user.name }}</span>
          <span class="truncate text-xs">{{ userStore.user.email }}</span>
        </div>
        <Icon name="IconArrowDown" class="ml-4" />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent class="w-52 rounded-lg" side="bottom" align="end" :side-offset="4">
      <DropdownMenuItem>
        <div class="flex justify-between item-centers w-full">
          <span>Dark mode</span><Switch :checked="isDarkMode" @update:checked="handleChange" />
        </div>
      </DropdownMenuItem>
      <DropdownMenuSeparator />
      <DropdownMenuItem> Profile </DropdownMenuItem>
      <DropdownMenuSeparator />
      <DropdownMenuItem @click="authStore.logout()">
        Log out
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
