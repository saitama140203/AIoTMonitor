import { UserRole } from '@/types'
import { z } from 'zod'

export const emailSchema = z.string().email()

export const passwordSchema = z
  .string()
  .min(8, { message: 'Password must be at least 8 characters long' })
  .max(32, { message: 'Password must not exceed 32 characters' })
  .refine(value => /[a-z]/.test(value), { message: 'Password must include at least one letter' })
  .refine(value => /\d/.test(value), { message: 'Password must include at least one number' })

export const requiredStringSchema = z.string()

export const signupValidator = z
  .object({
    email: emailSchema,
    password: passwordSchema,
    confirmPassword: passwordSchema,
  })
  .refine(data => data.password === data.confirmPassword, {
    message: 'Password confirmation does not match',
    path: ['confirmPassword'],
  })

export const emailValidator = z.object({
  email: emailSchema,
})

export const loginValidator = z.object({
  username: requiredStringSchema,
  password: requiredStringSchema,
})

export const resetPasswordValidator = z
  .object({
    token: requiredStringSchema,
    password: passwordSchema,
    confirmPassword: passwordSchema,
  })
  .refine(data => data.password === data.confirmPassword, {
    message: 'Password confirmation does not match',
    path: ['confirmPassword'],
  })
export const createUserValidator = z.object({
  username: requiredStringSchema,
  email: emailSchema,
  password: passwordSchema,
  confirmPassword: passwordSchema,
  fullName: requiredStringSchema,
  role: z.enum(Object.values(UserRole) as [string, ...string[]]),
})
  .refine(data => data.password === data.confirmPassword, {
    message: 'Password confirmation does not match',
    path: ['confirmPassword'],
  })

export const changePasswordValidator = z
  .object({
    current_password: passwordSchema,
    new_password: passwordSchema,
    confirmNewPassword: passwordSchema,
  })
  .refine(data => data.new_password === data.confirmNewPassword, {
    message: 'Password confirmation does not match',
    path: ['confirmNewPassword'],
  })
