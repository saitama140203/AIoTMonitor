<route>
  {
    meta: {
      title: 'Users',
    }
  }
</route>

<script setup lang="ts">
import { toast } from '@/components/ui/toast'
import { useAdminStore } from '@/stores/admin'
import { useConfirmStore } from '@/stores/confirm'
import { useUserStore } from '@/stores/user'
import { UserRole } from '@/types'
import { useAsyncState } from '@vueuse/core'
import { MoreHorizontal } from 'lucide-vue-next'

const userStore = useUserStore()
const adminStore = useAdminStore()
const confirmStore = useConfirmStore()

const isAddUserModalOpen = ref(false)
const configQuery = ref({
  page: 1,
  limit: 100,
  search: '',
  role: 'all',
})
const listFilterRole = ref([
  { value: 'all', label: 'All' },
  { value: UserRole.ADMIN, label: 'Admin' },
  { value: UserRole.OPERATOR, label: 'Operator' },
  { value: UserRole.TEAM_LEAD, label: 'Team lead' },
])

const { isLoading, execute, state } = useAsyncState(() => {
  const config = {
    skip: (configQuery.value.page - 1) * configQuery.value.limit,
    limit: configQuery.value.limit,
    search: configQuery.value.search,
    role: configQuery.value.role === 'all' ? undefined : configQuery.value.role,
  }
  return adminStore.getListUsers(config)
}, [], {
  onError: (error) => {
    Promise.reject(error)
  },
})

function openAddUserModal() {
  isAddUserModalOpen.value = true
}
function handleAddUser() {
  toast({
    title: 'User created successfully',
    description: 'The user has been created successfully.',
  })
}
watch(configQuery, () => {
  execute()
}, { deep: true })
async function confirmResetPassword(user: any) {
  const confirm = await confirmStore.showConfirmDialog({
    title: 'Reset Password',
    message: `Are you sure you want to reset the password for ${user.username}?`,
    confirmText: 'Yes, reset it!',
    cancelText: 'No, cancel!',
  })
  if (confirm) {
    // User confirmed the action
    try {
      const data = await adminStore.resetPassword(user.email)
      toast({
        title: 'Password Reset Successfully',
        description: `"${data.temp_password}" is the new password for ${user.username}.`,
      })
    }
    catch (error: any) {
      const errorMessage = error?.response?.data?.detail || 'Something went wrong.'
      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      })
    }
  }
}
</script>

<template>
  <div class="flex flex-col gap-4 p-4 h-[calc(100vh-64px)]">
    <div class="flex justify-between">
      <div class="flex gap-2 w-[400px]">
        <div class="w-72">
          <InputSearch
            v-model="configQuery.search"
            placeholder="Search users..."
          />
        </div>
        <div class="w-52">
          <Select v-model="configQuery.role">
            <SelectTrigger>
              <SelectValue placeholder="Select a Role" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem
                  v-for="(role, index) in listFilterRole"
                  :key="index"
                  :value="role.value"
                >
                  {{ role.label }}
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
      </div>
      <Button @click="openAddUserModal">
        Create User
      </Button>
    </div>
    <div v-if="state.length > 0" class="relative rounded-lg overflow-hidden shadow-md w-full bg-card overflow-y-auto">
      <div class="grid lg:grid-cols-7 grid-cols-5 gap-4 p-4 border-b font-semibold sticky top-0 bg-card z-10">
        <div>
          Username
        </div>
        <div class="lg:col-span-2">
          Email
        </div>
        <div class="lg:col-span-2">
          Full name
        </div>
        <div>Role</div>
        <div>Status</div>
      </div>
      <div
        v-for="user in state"
        :key="user.id"
        class="grid lg:grid-cols-7 grid-cols-5 gap-4 p-4 items-center hover:bg-secondary"
      >
        <!-- Avatar and Name -->
        <div class="flex items-center gap-4 truncate">
          {{ user.username }}
        </div>
        <div class="lg:col-span-2 truncate">
          {{ user.email }}
        </div>
        <div class="lg:col-span-2">
          {{ user.full_name }}
        </div>
        <div>{{ user.role }}</div>
        <div class="flex justify-between items-center gap-2">
          <span
            class="px-2 py-1 rounded text-sm truncate"
            :class="[user.is_active ? 'bg-success' : 'bg-destructive']"
          >
            {{ user.is_active ? 'Active' : 'Inactive' }}
          </span>
          <DropdownMenu v-if="user.role !== 'admin' && userStore?.user?.role === 'admin'">
            <DropdownMenuTrigger
              class="cursor-pointer"
              as-child
            >
              <Button variant="outline" class="w-8 h-8 p-0">
                <span class="sr-only">Open menu</span>
                <MoreHorizontal class="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent class="">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem class="cursor-pointer" @click="confirmResetPassword(user)">
                Reset Password
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
      <PaginationTable
        total="10"
        :current-page="configQuery.page"
        :items-per-page="configQuery.limit"
        :is-loading="isLoading"
      />
    </div>
  </div>
  <AddUserModal
    v-model:open="isAddUserModalOpen"
    @add="handleAddUser"
  />
</template>
