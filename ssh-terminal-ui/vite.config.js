import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    // Không cần proxy vì ta sẽ connect trực tiếp tới 8000
  }
})
