<route>
  {
      meta: {
          title: "Sign Up",
          layout: "auth",
      }
  }
</route>

<script setup lang="ts">
import { toast } from '@/components/ui/toast'
import { useAuthStore } from '@/stores/auth'
import { signupValidator } from '@/utils/validation'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'

const router = useRouter()
const authStore = useAuthStore()

const form = useForm({
  validationSchema: toTypedSchema(signupValidator),
})

const onSubmit = form.handleSubmit(async (values) => {
  await authStore.register(values)
  toast({
    title: 'Success',
    description: 'Account created successfully',
  })
  router.push('/auth/login')
})
</script>

<template>
  <form class="rounded-lg border bg-card text-card-foreground shadow-sm mx-auto max-w-sm sm:min-w-[25rem] h-max" @submit.prevent="onSubmit">
    <CardHeader>
      <CardTitle class="text-2xl text-center">
        Đăng ký
      </CardTitle>
      <CardDescription class="text-center">
        Nhập thông tin bên dưới để tạo tài khoản
      </CardDescription>
    </CardHeader>
    <CardContent>
      <div class="grid gap-4">
        <InputValidator id="name" label="Họ và tên" placeholder="Athony Huynh" type="text" name="name" />
        <InputValidator
          id="email"
          type="email"
          label="Email"
          placeholder="m@example.com"
          required
          name="email"
        />
        <InputValidator id="password" label="Mật khẩu" placeholder="Mật khẩu" type="password" name="password" />
        <InputValidator id="confirmPassword" label="Xác nhận mật khẩu" placeholder="Nhập lại mật khẩu" type="password" name="confirmPassword" />

        <Button type="submit" class="w-full">
          Đăng ký
        </Button>
      </div>
      <div class="mt-4 text-center text-sm">
        Bạn đã có tài khoản?
        <RouterLink to="/auth/login" class="ml-1 text-balance underline">
          Đăng nhập ngay
        </RouterLink>
      </div>
    </CardContent>
  </form>
</template>
