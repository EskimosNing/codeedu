<template>
  <div class="chat-container">
    <!-- 主内容区域 -->
    <div class="hero-section">
        <h1>智能助手</h1>
      </div>

      <!-- 功能提示区 -->
      <div class="prompt-grid">
        <div class="prompt-card" v-for="(prompt, index) in quickPrompts" :key="index">
          <h3>{{ prompt.title }}</h3>
          <p>{{ prompt.description }}</p>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="input-wrapper" :class="{ focused: isInputFocused }">
        <textarea
          ref="inputField"
          v-model="userInput"
          placeholder="输入您的问题或需求..."
          @focus="isInputFocused = true"
          @blur="isInputFocused = false"
          @keydown.enter.exact.prevent="handleSubmit"
        ></textarea>
        <button 
          class="submit-btn"
          :disabled="!userInput.trim()"
          @click="handleSubmit"
        >
          <span v-show="!isLoading">▶</span>
          <div v-show="isLoading" class="loader"></div>
        </button>
      </div>

      <!-- 免责声明 -->
      <p class="disclaimer">
        本系统可能会产生不准确信息，请谨慎验证
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 响应式数据
const userInput = ref('')
const isInputFocused = ref(false)
const isLoading = ref(false)

// 快捷提示示例
const quickPrompts = ref([
  {
    title: '创意写作',
    description: '帮我写一篇关于未来城市的科幻短篇'
  },
  {
    title: '数据分析',
    description: '解释以下销售数据的趋势...'
  },
  {
    title: '学习助手',
    description: '用简单的方式讲解量子力学基础'
  },
  {
    title: '编程帮助',
    description: '如何用Python实现快速排序？'
  }
])

// 提交处理
const handleSubmit = async () => {
  if (!userInput.value.trim()) return
  
  try {
    isLoading.value = true
    // 这里添加实际API调用逻辑
    console.log('提交内容:', userInput.value)
    await new Promise(resolve => setTimeout(resolve, 1000)) // 模拟延迟
  } finally {
    isLoading.value = false
    userInput.value = ''
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background: radial-gradient(ellipse at top, #f8f9fa, #e9ecef);
}

.hero-section {
  width: min(100%, 800px);
  text-align: center;
}

.logo {
  margin-bottom: 3rem;
  opacity: 0;
  animation: fadeInUp 0.6s ease-out forwards;
}

.logo h1 {
  font-size: 2.5rem;
  color: #2d3436;
  margin-top: 1rem;
}

.prompt-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin: 3rem 0;
}

.prompt-card {
  background: white;
  padding: 1.5rem;
  border-radius: 16px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #e0e0e0;
}

.prompt-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

.input-wrapper {
  position: relative;
  margin: 2rem 0;
  border-radius: 50px;
  background: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: box-shadow 0.3s ease;
  border: 2px solid transparent;
}

.input-wrapper.focused {
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
  border-color: #74b9ff;
}

textarea {
  width: 100%;
  height: 56px;
  padding: 1rem 4.5rem 1rem 2rem;
  border: none;
  border-radius: 50px;
  resize: none;
  font-size: 1rem;
  line-height: 1.5;
  background: transparent;
}

textarea:focus {
  outline: none;
}

.submit-btn {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #74b9ff;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #0984e3;
  transform: translateY(-50%) scale(1.05);
}

.submit-btn:disabled {
  background: #dfe6e9;
  cursor: not-allowed;
}

.loader {
  width: 24px;
  height: 24px;
  margin: 0 auto;
  border: 3px solid #fff;
  border-bottom-color: transparent;
  border-radius: 50%;
  animation: rotation 1s linear infinite;
}

.disclaimer {
  color: #636e72;
  font-size: 0.9rem;
  margin-top: 1.5rem;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes rotation {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .prompt-grid {
    grid-template-columns: 1fr;
  }
  
  textarea {
    height: 48px;
    padding-right: 3.5rem;
  }
}
</style>