<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { UserRole } from '@/types'

const userStore = useUserStore()
const listNav = ref([
  {
    id: 1,
    icon: 'IconDashboard',
    title: 'Dashboard',
    url: '/',
  },
  {
    id: 2,
    icon: 'IconUserGroup',
    title: 'Users',
    url: '/users',
    roles: [UserRole.ADMIN, UserRole.TEAM_LEAD],
  },
  {
    id: 3,
    icon: 'IconDevice',
    title: 'Devices',
    url: '/devices',
    roles: [UserRole.TEAM_LEAD],
  },
  {
    id: 4,
    icon: 'IconGroup',
    title: 'Groups Devices',
    url: '/groups',
    roles: [UserRole.TEAM_LEAD],
  },
  {
    id: 5,
    icon: 'IconCommand',
    title: 'Commands',
    url: '/commands',
    roles: [UserRole.TEAM_LEAD],

  },
  {
    id: 6,
    icon: 'IconProfile',
    title: 'Profiles',
    url: '/profiles',
    roles: [UserRole.TEAM_LEAD],
  },
  {
    id: 7,
    icon: 'IconProfile',
    title: ' List Profiles',
    url: '/profiles_operator',
    roles: [UserRole.OPERATOR],
  },
])
const listNavFilter = computed(() => {
  return listNav.value.filter((item) => {
    if (item.roles) {
      return userStore?.user?.roles?.some((role: UserRole) => item.roles.includes(role))
    }
    return true
  })
})
</script>

<template>
  <div class="flex flex-col duration-200 w-[15rem] bg-transparent ease-linear">
    <div class="flex gap-2 pl-6 py-6 cursor-pointer" @click="$router.push('/home')">
      <Icon name="IconLogo" class="w-9 text-foreground" />
      <span class="text-secondary-foreground text-3xl font-mono">AIOT</span>
    </div>
    <ScrollArea class="w-full" style="height: calc(100% - 6rem)">
      <div
        class="flex flex-1 flex-col overflow-auto group-data-[collapsible=icon]:overflow-hidden gap-2"
      >
        <template v-for="item in listNavFilter" :key="item.id">
          <AppSideBarItem v-bind="item" />
        </template>
      </div>
    </ScrollArea>
  </div>
</template>
