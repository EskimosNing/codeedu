<template>
    <div class="homeContainer">
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
    </div>
</template>

<style scoped>
.homeContainer{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
}
.input-wrapper {
  position: relative;
  /* margin: 2rem 0; */
  border-radius: 20px;
  background-color: #404045;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: box-shadow 0.3s ease;
  border: 2px solid transparent;
  width: 750px;
  
}
.input-wrapper.focused {
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
  border-color: #74b9ff;
}
textarea {
  width: 100%;
  height: 100%;
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
</style>

<script>
export default {
  data() {
    return {
      userInput : "",
      isInputFocused : false,
      isLoading: false,
    }
  },
  methods: {
    handleSubmit(){

    }
  }
}
</script>