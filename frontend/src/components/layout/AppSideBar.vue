<script setup>
const data = ref({
  groupA: [
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
    },
    {
      id: 3,
      icon: 'IconDevice',
      title: 'Device',
      url: '/devices',
    },
  ],
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
        <template v-for="item in data.groupA" :key="item.id">
          <AppSideBarItem v-bind="item" />
        </template>
      </div>
    </ScrollArea>
  </div>
</template>
