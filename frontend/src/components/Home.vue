<template>
    <div class="homeContainer">
        <div class="introduction">
            <img
            :src="require('../assets/TeachingCode.png')"
            class="logo"
          >
          <span class="logotext">编程教育多智能体系统</span>
        </div>
        <div class="guide">
            我可以教你写代码，学习算法和数据结构，做代码习题，快来和我对话吧~
        </div>
        <div class="input-wrapper" :class="{ focused: isInputFocused }">
            <textarea
                ref="inputField"
                v-model="userInput"
                placeholder="给多智能体编程教学系统发送消息"
                @focus="isInputFocused = true"
                @blur="isInputFocused = false"
                @keydown.enter.exact.prevent="handleSubmit"
            ></textarea>
            <button 
                class="submit-btn"
                :disabled="!userInput.trim()"
                @click="handleSubmit"
            >
                <span v-show="!isLoading" class="arrow">▶</span>
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
    transform: translateY(-7%);
}
.introduction {
    display: flex;
    margin-bottom: 12px
}
.guide{
    color: white;
    font-weight: bold;
    margin-bottom: 30px;
}
.logo {
    width: 80px;
    height: 60px;
}
.logotext {
    color: white;
    margin-left: 15px;
    font-size: 30px;
    font-weight: bold;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
.input-wrapper {
    display: flex;
    flex-direction: column;
    position: relative;
    /* margin: 2rem 0; */
    border-radius: 20px;
    background-color: #404045;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transition: box-shadow 0.3s ease;
    border: 2px solid transparent;
    width: 750px;
    min-height: 150px;
}
/* .input-wrapper.focused {
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
  border-color: #74b9ff;
} */
textarea {
  width: 100%px;
  height: 60%;
  padding: 12px 20px 0px 20px;
  border: none;
  resize: none;
  font-size: 17px;
  font-weight: bolder;
  color: white;
  line-height: 1.7;
  background: transparent;
}

textarea:focus {
  outline: none;
}
.submit-btn {
  position: absolute;
  right: 1rem;
  top: 80%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #4d6bfe;
  color: #f8faff;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #4f6eca;
  transform: translateY(-50%) scale(1.05);
}

.submit-btn:disabled {
  background: #71717a;
  color: #2a2a2e;
  cursor: not-allowed;
}
.arrow {
    position: relative;
    left: 2px;
    font-size: 16px;
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
        this.$emit('child-event',{
            message: this.userInput,
        })
    }
  }
}
</script>