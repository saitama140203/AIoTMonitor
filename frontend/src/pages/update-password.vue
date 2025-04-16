<route>
    {
        meta: {
            title: 'Change Password'
        }
    }
  </route>

<script setup lang="ts">
import { toast } from '@/components/ui/toast'
import { useUserStore } from '@/stores/user'
import { changePasswordValidator } from '@/utils/validation'
import { toTypedSchema } from '@vee-validate/zod'
import { useAsyncState } from '@vueuse/core'
import { useForm } from 'vee-validate'

const userStore = useUserStore()

const form = useForm({
  validationSchema: toTypedSchema(changePasswordValidator),
})
const { isLoading, execute, error } = useAsyncState(userStore.updatePasswword, null, {
  immediate: false,
  onError: (error) => {
    Promise.reject(error)
  },
})
const onSubmit = form.handleSubmit(async (values) => {
  await execute(0, values)
  if (error.value)
    return
  toast({
    title: 'Success',
    description: 'Password changed successfully.',
  })
  form.resetForm()
})
</script>

<template>
  <form class="rounded-lg border bg-card text-card-foreground shadow-sm mx-auto h-max w-full max-w-xl mt-4" @submit.prevent="onSubmit">
    <CardHeader>
      <CardTitle class="text-2xl text-center">
        Change Password
      </CardTitle>
      <CardDescription class="text-center">
        Please enter your new password
      </CardDescription>
    </CardHeader>
    <CardContent>
      <div class="flex gap-3 flex-col">
        <InputValidator id="password" label="Current Password" placeholder="Enter Current Password" type="password" name="current_password" />
        <InputValidator id="newPassword" label="New Password" placeholder="Enter New Password" type="password" name="new_password" />
        <InputValidator id="confirmNewPassword" label="Confirm New password" placeholder="Confirm New Password" type="password" name="confirmNewPassword" />
        <Button type="submit" :is-loading="isLoading" class="mx-auto mt-4">
          Update Password
        </Button>
      </div>
    </CardContent>
  </form>
</template>
