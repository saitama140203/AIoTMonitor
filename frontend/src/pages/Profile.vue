<script setup lang="ts">
import { uploadImage } from '@/api/upload'
import { useUserStore } from '@/stores/user'
import { emailSchema, nameSchema, passwordSchema } from '@/utils/validation'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import * as z from 'zod'

const userStore = useUserStore()
const isEditing = ref(false)
const avatarPreview = ref(userStore.user?.anhDaiDien || '')
const isAvatarRemoved = ref(false)
const fileImage = ref<File | null>(null)
const isLoading = ref(false)
const profileSchema = toTypedSchema(
  z
    .object({
      username: nameSchema,
      email: emailSchema,
      password: passwordSchema.optional(),
      confirmPassword: z.string().optional(),
      role: z.string().optional(),
      gender: z.string().optional(),
      dateOfBirth: z.string().optional(),
    })
    .refine(
      (data) => {
        if (data.password) {
          return data.password === data.confirmPassword
        }
        return true
      },
      {
        message: 'Passwords do not match',
        path: ['confirmPassword'],
      },
    ),
)

const form = useForm({
  validationSchema: profileSchema,
  initialValues: {
    username: userStore.user?.hoTen || '',
    email: userStore.user?.email || '',
  },
})

const handleSubmit = form.handleSubmit(async (values) => {
  try {
    isLoading.value = true
    let avatarLink = isAvatarRemoved.value ? '' : userStore.user?.anhDaiDien || ''
    if (fileImage.value) {
      const res = await uploadImage(fileImage.value)
      avatarLink = res.url
    }
    const updatedValues = {
      ...values,
      avatar: avatarLink || 'https://static-00.iconduck.com/assets.00/avatar-default-icon-2048x2048-h6w375ur.png',
    }

    // await userStore.updateUser(updatedValues)
    isEditing.value = false
    form.resetForm()
    form.setValues({
      username: userStore.user?.hoTen || '',
      email: userStore.user?.email || '',
    })
  }
  finally {
    isLoading.value = false
  }
})
function handleAvatarChange(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    fileImage.value = target.files[0]
  }
  avatarPreview.value = URL.createObjectURL(fileImage.value as File)
  isAvatarRemoved.value = false
}
function removeAvatar() {
  avatarPreview.value = ''
  isAvatarRemoved.value = true
  fileImage.value = null
}
function startEdit() {
  isEditing.value = true
}
function cancelEdit() {
  isEditing.value = false
  form.resetForm()
  avatarPreview.value = userStore.user?.anhDaiDien || ''
  isAvatarRemoved.value = false
  fileImage.value = null
}
const firstLetter = userStore.user?.hoTen
  ?.split(' ')
  .map(name => name.charAt(0))
  .join('')
  .slice(-2)
</script>

<template>
  <div class="flex flex-col items-center justify-center h-full">
    <div class="w-full flex justify-center">
      <div class="flex flex-col items-center w-11/12 md:w-3/4 lg:w-1/2">
        <h1 class="self-start text-2xl font-bold mt-4 mb-2">
          Thông tin cá nhân
        </h1>

        <form class="w-full" @submit="handleSubmit">
          <div class="relative w-24 h-24 mb-4">
            <img
              v-lazy="avatarPreview || 'https://static-00.iconduck.com/assets.00/avatar-default-icon-2048x2048-h6w375ur.png'"
              alt="Avatar"
              class="w-full h-full rounded-lg border-2 object-cover"
            >
            <div
              v-if="isEditing"
              class="absolute rounded-lg inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity cursor-pointer "
            >
              <label class="text-white text-sm font-medium cursor-pointer">
                Tải lên
                <input
                  type="file"
                  class="hidden"
                  accept="image/*"
                  @change="handleAvatarChange"
                >
              </label>
            </div>
          </div>

          <button
            v-if="isEditing && avatarPreview"
            type="button"
            class="text-red-500 text-sm mb-4"
            @click="removeAvatar"
          >
            Xóa ảnh đại diện
          </button>
          <InputValidator
            v-model="form.values.username"
            type="text"
            label="Tên người dùng"
            name="username"
            :disabled="!isEditing"
            custom="h-[3rem] mb-5 mt-1"
          />
          <InputValidator
            v-model="form.values.email"
            type="text"
            label="Địa chỉ email"
            name="email"
            disabled
            custom="h-[3rem] mb-5 mt-1"
          />
          <div class="flex justify-end">
            <div v-if="isEditing">
              <Button
                class="bg-foreground hover:bg-muted-foreground mr-2"
                @click="cancelEdit"
              >
                Hủy
              </Button>
              <Button type="submit">
                <template v-if="isLoading">
                  <div class="flex w-full p-8 justify-center gap-2 items-center">
                    <Icon name="IconLoading" />
                    Vui lòng chờ...
                  </div>
                </template>
                <template v-else>
                  Lưu
                </template>
              </Button>
            </div>
            <div v-else>
              <Button @click="startEdit">
                Chỉnh sửa
              </Button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
