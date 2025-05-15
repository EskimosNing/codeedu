<template>
  <div class="w-full max-w-md mx-auto p-4 border rounded-md shadow-md">
    <div class="flex flex-col">
      <textarea
        v-model="message"
        class="resize-none overflow-y-auto p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        :style="{ height: initialHeight + 'px', maxHeight: maxHeight + 'px' }"
        @input="autoResize"
        ref="textarea"
      ></textarea>
      <button
        class="mt-2 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
        @click="submit"
      >
        提交
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const message = ref('')
const initialHeight = 100
const maxHeight = 300
const textarea = ref(null)

const autoResize = () => {
  const el = textarea.value
  if (!el) return
  el.style.height = initialHeight + 'px'
  const newHeight = Math.min(el.scrollHeight, maxHeight)
  el.style.height = newHeight + 'px'
}

const submit = () => {
  alert('提交的内容: ' + message.value)
}
</script>

<style scoped>
/* 可选：为滚动条美化 */
textarea::-webkit-scrollbar {
  width: 6px;
}
textarea::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}
</style>
