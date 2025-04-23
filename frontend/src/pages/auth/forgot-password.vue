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
import { useAuthStore } from '@/stores/auth'
import { emailValidator } from '@/utils/validation'
import { toTypedSchema } from '@vee-validate/zod'
import { useAsyncState } from '@vueuse/core'
import { useForm } from 'vee-validate'

const router = useRouter()

const authStore = useAuthStore()

const form = useForm({
  validationSchema: toTypedSchema(emailValidator),
})

const { isLoading, execute, error } = useAsyncState(authStore.sendEmailResetPassword, null, {
  immediate: false,
  onError: (error) => {
    Promise.reject(error)
  },
})

const onSubmit = form.handleSubmit(async (values) => {
  await execute(0, values)
  if(error.value) return
  toast({
    title: 'Thành công',
    description: 'Đã gửi email đặt lại mật khẩu, vui lòng kiểm tra email của bạn',
  })
  router.push('/auth/reset-password')
})
</script>

<template>
  <form class="sm:min-w-[25rem]" @submit.prevent="onSubmit">
    <Card class="mx-auto max-w-sm">
      <CardHeader>
        <CardTitle class="text-2xl text-center">
          Quên mật khẩu
        </CardTitle>
        <CardDescription class="text-center">
          Nhập email của bạn để nhận liên kết đặt lại mật khẩu
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid gap-4">
          <div class="grid gap-2">
            <InputValidator id="email" type="email" label="Email" placeholder="example@gmai.com" name="email" />
          </div>
          <Button
            type="submit"
            :is-loading="isLoading"
          >
            Gửi email
          </Button>
        </div>
        <div class="mt-4 text-center text-sm">
          <RouterLink to="/auth/login" class="underline">
            Quay lại trang đăng nhập
          </RouterLink>
        </div>
      </CardContent>
    </Card>
  </form>
</template>
