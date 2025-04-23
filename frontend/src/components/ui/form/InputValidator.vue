<script setup lang="ts">
import { FormControl, FormField, FormItem, FormMessage } from '@/components/ui/form'

interface InputProps {
  id?: string
  type?: string
  placeholder?: string
  label?: string
  name?: string
}
const props = withDefaults(defineProps<InputProps>(), {
  id: 'text',
  type: 'text',
  label: 'Text',
  name: 'text',
})
const isShowPassword = ref(false)
function toggleShowIcon() {
  isShowPassword.value = !isShowPassword.value
}
const typeInputComputed = computed(() => {
  return props.type === 'password' && isShowPassword.value ? 'text' : props.type
})
</script>

<template>
  <FormField v-slot="{ componentField }" :name="props.name" :validate-on-blur="false">
    <div class="space-y-2">
      <Label :for="props.id">{{ props.label }}</Label>
      <FormItem class="relative">
        <FormControl>
          <Input
            :id="props.id"
            :type="typeInputComputed"
            :placeholder="props.placeholder"
            v-bind="componentField"
            class="pr-9"
            autocomplete="off"
          />
          <div
            v-if="props.type === 'password'"
            class="w-10 h-10 absolute right-0 -top-2 cursor-pointer flex items-center justify-center"
            @click="toggleShowIcon"
          >
            <Icon v-if="!isShowPassword" name="IconEyeOff" class="w-6 h-6" />
            <Icon v-else name="IconEyeOn" class="w-6 h-6" />
          </div>
          <FormMessage class="error-message" />
        </FormControl>
      </FormItem>
    </div>
  </FormField>
</template>

<style scoped>
.error-message {
  margin-top: 4px !important;
}
</style>
