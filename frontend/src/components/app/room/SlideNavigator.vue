<script setup lang="ts">
import { ref } from 'vue'

interface Slide {
  id: string
  type: 'slide' | 'question'
  title: string
  thumbnail?: string
}

const slides = ref<Slide[]>([
  {
    id: '1',
    type: 'slide',
    title: 'Đây là cái gì',
    thumbnail: 'https://via.placeholder.com/150/0000FF/FFFFFF?text=Slide+1',
  },
  {
    id: '2',
    type: 'slide',
    title: 'Máy bay x²',
    thumbnail: 'https://via.placeholder.com/150/222/fff?text=Slide+2',
  },
  {
    id: '3',
    type: 'question',
    title: 'Con gà có mấy c...',
  },
  {
    id: '4',
    type: 'question',
    title: 'Tui đẹp trai',
  },
  {
    id: '5',
    type: 'slide',
    title: 'Đây là cái gì',
    thumbnail: 'https://via.placeholder.com/150/0000FF/FFFFFF?text=Slide+1',
  },
  {
    id: '6',
    type: 'slide',
    title: 'Máy bay x²',
    thumbnail: 'https://via.placeholder.com/150/222/fff?text=Slide+2',
  },
  {
    id: '7',
    type: 'question',
    title: 'Con gà có mấy c.s..',
  },
])

const selectedSlideId = ref<string>('2')
</script>

<template>
  <div class="h-full space-y-2">
    <div class="w-full border-r py-2 space-y-2  overflow-y-auto">
      <div
        v-for="(slide, index) in slides" :key="slide.id"
        class="card"
        :class="{ 'card-active': selectedSlideId === slide.id }"
      >
        <div class="action">
          <Button
            variant="secondary"
            class="w-6 h-6 p-2 hover:bg-gray-300 rounded-full bg-transparent "
            title="Nhân đôi"
          >
            <Icon name="IconCopy" class="w-4 h-4" />
          </Button>
          <Button
            variant="secondary"
            class="w-6 h-6 p-2 hover:bg-gray-300 rounded-full bg-transparent "
            title="Xóa"
          >
            <Icon name="IconTrash" class="w-4 h-4" />
          </Button>
        </div>
        <div class="text-sm font-semibold text-gray-600">
          {{ index + 1 }}.
          {{ slide.type === 'slide' ? 'Slide' : 'Câu hỏi' }}
        </div>
        <div
          class="card-content" :class="[
            selectedSlideId === slide.id ? 'border-accent' : 'border-transparent',
          ]"
          @click="selectedSlideId = slide.id"
        >
          <div class="mt-1">
            <p class="text-[13px] font-medium text-black truncate">
              {{ slide.title }}
            </p>
            <div v-if="slide.thumbnail" class="mt-1">
              <img :src="slide.thumbnail" alt="thumb" class="w-full h-16 object-cover rounded-sm">
            </div>
            <div v-else class="w-full h-16 rounded-sm flex items-center justify-center text-gray-500 text-sm">
              <span class="italic">Văn bản</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Thêm nút -->
    <div class="space-y-2 pt-4 h-28 left-0 flex flex-col items-center justify-center w-full pl-4 pr-2 sticky bottom-0 bg-card">
      <Button
        class="w-full"
      >
        Thêm slide
      </Button>
      <Button
        class="w-full"
        variant="secondary"
      >
        Thêm câu hỏi
      </Button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.card {
  @apply py-1 pr-2 pl-8 cursor-pointer bg-card relative;
  .card-content {
    @apply rounded-md p-2 border-2 bg-gray-200 dark:bg-gray-200/20;
  }
  .action {
    @apply absolute flex-col top-1/2 -translate-y-3 left-1 space-y-1 hidden;
  }
  &:hover {
    .card-content {
      @apply border-accent; 
    }
    .action {
      @apply flex;
    }
  }
}
.card-active {
  @apply bg-accent/10
}
</style>
