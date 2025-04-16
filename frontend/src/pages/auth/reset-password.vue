<route>
    {
        meta: {
        layout: "auth",
        title: "Reset Password",
        }
    }
</route>

<script setup lang="ts">
import { toast } from '@/components/ui/toast'
import { useAuthStore } from '@/stores/auth'
import { resetPasswordValidator } from '@/utils/validation'
import { toTypedSchema } from '@vee-validate/zod'
import { useAsyncState } from '@vueuse/core'
import { useForm } from 'vee-validate'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = useForm({
  validationSchema: toTypedSchema(resetPasswordValidator),
  initialValues: {
    token: (route.query.token ?? '') as string,
    password: '',
    confirmPassword: '',
  },
})
const { isLoading, execute, error } = useAsyncState(authStore.resetPassword, null, {
  immediate: false,
  onError: (error) => {
    Promise.reject(error)
  },
})
const onSubmit = form.handleSubmit(async (values) => {
  await await execute(0, values)
  if (error.value)
    return
  toast({
    title: 'Thành công',
    description: 'Mật khẩu đã được đặt lại thành công',
  })
  router.push('/auth/login')
})
</script>

<template>
  <form class="rounded-lg border bg-card text-card-foreground shadow-sm mx-auto max-w-sm h-max sm:min-w-[25rem]" @submit.prevent="onSubmit">
    <CardHeader>
      <CardTitle class="text-2xl text-center">
        Đặt lại mật khẩu
      </CardTitle>
      <CardDescription class="text-center">
        Nhập mật khẩu mới của bạn và xác nhận mật khẩu
      </CardDescription>
    </CardHeader>
    <CardContent>
      <div class="grid gap-4">
        <InputValidator
          id="token"
          type="text"
          label="Token đặt lại mật khẩu"
          placeholder="Nhập token"
          required
          name="token"
          autocomplete="off"
        />
        <InputValidator id="password" label="Mật khẩu" placeholder="Mật khẩu" type="password" name="password" />
        <InputValidator id="confirmPassword" label="Xác nhận mật khẩu" placeholder="Nhập lại mật khẩu" type="password" name="confirmPassword" />

        <Button type="submit" class="w-full" :is-loading="isLoading">
          Đặt lại mật khẩu
        </Button>
      </div>
      <div class="mt-4 text-center text-sm">
        <RouterLink to="/auth/login" class="underline">
          Quay lại trang đăng nhập
        </RouterLink>
      </div>
    </CardContent>
  </form>
</template>
