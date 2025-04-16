<template>
  <div class="flex px-2 flex-col">
    <div class="flex items-center flex-col justify-center mb-2 text-md font-semibold text-foreground ">
      <slot name="header" />
    </div>
    <div class="flex flex-col gap-1">
      <slot />
    </div>
  </div>
</template>
