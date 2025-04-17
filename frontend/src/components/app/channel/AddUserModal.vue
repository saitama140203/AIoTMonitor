<script setup lang="ts">
import { FormControl, FormField, FormItem, FormMessage } from '@/components/ui/form'
import { useAdminStore } from '@/stores/admin'
import { UserRole } from '@/types'
import { createUserValidator } from '@/utils/validation'
import { toTypedSchema } from '@vee-validate/zod'
import { useAsyncState } from '@vueuse/core'
import { useForm } from 'vee-validate'

const { open } = defineProps({
  open: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['update:open', 'add'])
const adminStore = useAdminStore()
const listFilterRole = ref([
  { value: UserRole.ADMIN, label: 'Admin' },
  { value: UserRole.OPERATOR, label: 'Operator' },
  { value: UserRole.TEAM_LEAD, label: 'Team lead' },
])

const { handleSubmit, resetForm } = useForm({
  validationSchema: toTypedSchema(createUserValidator),
})
const { isLoading, execute, error } = useAsyncState(adminStore.createUser, null, {
  immediate: false,
  onError: (error) => {
    Promise.reject(error)
  },
})

const onSubmit = handleSubmit(async (values) => {
  const data = await execute(0, { ...values, role: values.role as UserRole })
  if (error.value) {
    return
  }
  emit('add', data)
  emit('update:open', false)
  resetForm()
})
</script>

<template>
  <Dialog :open="open" @update:open="(value:boolean) => emit('update:open', value)">
    <DialogContent class="sm:max-w-[425px] p-4">
      <DialogHeader>
        <DialogTitle>Create User</DialogTitle>
        <DialogDescription>
          Hello
        </DialogDescription>
      </DialogHeader>
      <form class="grid items-center gap-4" @submit.prevent="onSubmit">
        <InputValidator id="username" label="Username" placeholder="Enter username" name="username" />
        <InputValidator id="password" type="password" placeholder="Password" label="Password" name="password" />
        <InputValidator id="confirmPassword" label="Confirm Password" placeholder="Enter confirm password" type="password" name="confirmPassword" />
        <InputValidator id="email" type="email" placeholder="Email" label="Email" name="email" />
        <InputValidator id="fullName" placeholder="Full name" label="Full name" name="fullName" />
        <FormField v-slot="{ componentField }" name="role">
          <FormItem>
            <Label>Role</Label>
            <Select v-bind="componentField">
              <FormControl>
                <SelectTrigger>
                  <SelectValue placeholder="Select a Role" />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                <SelectGroup>
                  <SelectItem
                    v-for="role in listFilterRole"
                    :key="role.value"
                    :value="role.value"
                  >
                    {{ role.label }}
                  </SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
            <FormMessage />
          </FormItem>
        </FormField>
        <Button
          type="submit"
          :is-loading="isLoading"
        >
          Create
        </Button>
      </form>
    </DialogContent>
  </Dialog>
</template>
