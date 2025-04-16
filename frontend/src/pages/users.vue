<script setup lang="ts">
const isAddUserModalOpen = ref(false)
function openAddUserModal() {
  isAddUserModalOpen.value = true
}
</script>

<template>
  <div>
    <h1>Users management</h1>
    <Button @click="openAddUserModal">
      Create User
    </Button>
  </div>
  <AddUserModal
    v-model:open="isAddUserModalOpen"
    @add="handleAddUser"
  />
</template>
