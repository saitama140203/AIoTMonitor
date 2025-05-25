<route>
    {
        meta: {
        layout: "auth",
        title: "Forgot Password",
        }
    }
</route>

<script setup lang="ts">
import { toast } from '@/components/ui/toast'
import { useAdminStore } from '@/stores/admin'
import { usernameValidator } from '@/utils/validation'
import { toTypedSchema } from '@vee-validate/zod'
import { useAsyncState } from '@vueuse/core'
import { useForm } from 'vee-validate'

const router = useRouter()
const adminStore = useAdminStore()

const form = useForm({
  validationSchema: toTypedSchema(usernameValidator),
})

const { isLoading, execute, error } = useAsyncState(adminStore.resetPassword, null, {
  immediate: false,
  onError: (error) => {
    Promise.reject(error)
  },
})

const onSubmit = form.handleSubmit(async (values) => {
  await execute(0, values.username)
  if (error.value)
    return
  toast({
    title: 'Success',
    description: 'Reset admin password successfully.',
  })
  router.push('/auth/login')
})
</script>

<template>
  <form class="sm:min-w-[25rem]" @submit.prevent="onSubmit">
    <Card class="mx-auto max-w-sm">
      <CardHeader>
        <CardTitle class="text-2xl text-center">
          Reset Admin Password
        </CardTitle>
        <CardDescription class="text-center">
          Enter to reset password.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid gap-4">
          <div class="grid gap-2">
            <InputValidator id="email"label="" placeholder="Enter admin username" name="username" value="admin"  type="hidden" />
          </div>
          <Button
            type="submit"
            :is-loading="isLoading"
          >
            Reset Password
          </Button>
        </div>
        <div class="mt-4 text-center text-sm">
          <RouterLink to="/auth/login" class="underline">
            Back to Login
          </RouterLink>
        </div>
      </CardContent>
    </Card>
  </form>
</template>
