<script setup>

const data = ref({
  groupA: [
    {
      id: 1,
      icon: 'IconHome',
      title: 'Home',
      url: '/home',
    },
    {
      id: 2,
      icon: 'IconLibrary',
      title: 'Your Playlist',
      url: '/playlist',
      content: 'Login to view your playlist',
      requiredAuthen: true,
    },
  ],
  groupB: [

    {
      id: 4,
      icon: 'IconMusic',
      title: 'Create Song',
      url: '/song/create',
      content: 'Login to create and share song',
      requiredAuthen: true,
    },
    {
      id: 5,
      icon: 'IconFavorite',
      title: 'Favorite',
      url: '/favorite',
      content: 'Login to view your favorite songs',
      requiredAuthen: true,
    },
    {
      id: 3,
      icon: 'IconAdd',
      title: 'Create Playlist',
      url: '/playlist/create',
      content: 'Login to create and share playlists',
      requiredAuthen: true,
      type: 'button',

    },
  ],
})
</script>

<template>
  <div class="flex flex-col duration-200 w-[15rem] bg-transparent ease-linear">
    <div class="flex gap-2 pl-6 py-6 cursor-pointer" @click="$router.push('/home')">
      <Icon name="IconLogo" class="w-9 text-foreground" />
      <span class="text-secondary-foreground text-3xl font-mono">JamCirle</span>
    </div>
    <ScrollArea class="w-full" style="height: calc(100% - 6rem)">
      <div
        class="flex flex-1 flex-col overflow-auto group-data-[collapsible=icon]:overflow-hidden gap-0"
      >
        <AppSideBarGroup class="mb-8">
          <template v-for="item in data.groupA" :key="item.id">
            <AppSideBarItem v-bind="item" />
          </template>
        </AppSideBarGroup>

        <AppSideBarGroup>
          <template v-for="item in data.groupB" :key="item.id">
            <AppSideBarItem v-bind="item" />
          </template>
        </AppSideBarGroup>

        <span class="pt-2 px-6">
          <Separator />
        </span>
        <AppSideBarGroup class="pt-4">
          <template v-for="item in data.groupC" :key="item.id">
            <AppSideBarItem v-bind="item" />
          </template>
        </AppSideBarGroup>
      </div>
    </ScrollArea>
  </div>
</template>
