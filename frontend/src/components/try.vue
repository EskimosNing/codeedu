<template>
  <el-container class="main-container">
    <!-- 侧边栏区域 -->
    <el-aside 
      :width="asideWidth"
      class="aside-container"
    >
      <!-- 折叠按钮 -->
      <div class="aside-header" :class="{ collapsed:isCollapse }">
        <div class="logo-wrapper">
          <img
            :src="isCollapse ? require('../assets/Simple_IMCL_logo.png') : require('../assets/IMCL_logo_grey.png')"
            class="logo"
            :class="{ 'small-logo': isCollapse }"
          >
        </div>
        <div class="toggle-btn" @click="toggleCollapse">
          <i :class="isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'"></i>
        </div>
      </div>        

      <div class="button-container" v-if="!isCollapse">
          <el-button class="NewChatButton" @click="creatNewChat">
            <i class="el-icon-chat-line-square"></i>
            新建对话
          </el-button>
      </div>

      <div class="history-container" v-if="!isCollapse">
          <history :Dialogues="dialogueHistory" :currentDialogue="selectedDialogue" @child-event="handleSelectedDialogue">
          </history>
      </div>
    </el-aside>

    <!-- 主内容区域 -->
    <el-main class="main-content">
      <div v-if="selectedDialogue">
          <chatbot/>
      </div>
      <div v-else>
          <home>
          </home>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import Chatbot from './Chatbot.vue'
import History from "./History.vue"
import Home from "./Home.vue"
export default {
  components:{
    History,
    Chatbot,
    Home
  },
  data() {
    return {
      isCollapse: false,
      activeIndex: '1',
      expandedWidth: '270px',
      asideWidth: '270px',
      collapsedWidth: '80px',
      dialogueHistory: [],
      selectedDialogue: null,
    }
  },
  mounted(){
    this.dialogueHistory = [[{"role":"user", "content":"Who are you Who are you Who are you?Who are you"},{"role":"assistant", "content":"I'm a coding teaching agent."}],[{"role":"user", "content":"I'm a student from polyu"},{"role":"assistant", "content":"What do you want to learn."}]]
  },
  methods: {
    toggleCollapse() {
      this.isCollapse = !this.isCollapse
      this.asideWidth = this.isCollapse ? this.collapsedWidth : this.expandedWidth
    },
    creatNewChat() {
      this.selectedDialogue = null
    },
    handleSelectedDialogue(receivedData) {
      this.selectedDialogue = receivedData.message
    }
  }
}
</script>

<style scoped>
.main-container {
  height: 100vh;
}

.aside-container {
  background-color: #202327;
  transition: width 0.3s;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.aside-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  height: 85px;
  padding: 0 10px;
  margin-top: 10px;
  cursor: pointer;
  flex-shrink: 0;
  /* transition: all 0.3s; */
}

.aside-header.collapsed {
  flex-direction:column;
  align-items: center;
  justify-content: flex-start;
  height: 200px;
  padding: 10px 0;
}

/* Logo容器 */
.logo-wrapper {
  /* transition: all 0.3s; */
}

/* 展开状态的Logo */
.logo {
  width: 200px;
  height: auto;
}

/* 折叠状态的Logo */
.small-logo {
  width: 42px;
  height: auto;
  margin-bottom: 10px; /* 为按钮腾出空间 */
}

.side-menu:not(.el-menu--collapse) {
  width: expandedWidth;
}

.toggle-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
  color: #99a0aa;
  font-size: 27px;
  cursor: pointer;
  /* transition: all 0.3s; */
}

/* 折叠状态下的按钮样式 */
.toggle-btn.collapsed-btn {
  position: relative;
  margin-top: 8px;
  transform: rotate(180deg);
}

/* 激活状态边框 */
.toggle-btn.active-border {
  border: 2px solid #ffd04b;
  box-shadow: 0 0 8px rgba(255, 208, 75, 0.5);
}

.button-container {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}

.history-container {
  margin-top: 40px;
  flex: 1;
  min-height: 0;
  overflow: auto;
}

.history-container::-webkit-scrollbar-track {
  background-color: #202327;
}

.NewChatButton {
  border-radius: 12px;
  background-color: #4e6bff;
  color: #f8fafc;
  border: none;
  padding: 15px 60px;
  font-size: 18px;
  font-weight: bold;
}

.NewChatButton:hover {
  background-color: #4166d5;
}

.el-main {
  padding: 0px;
  background-color: #2a2a2e;
}

.el-menu {
  border-right: none;
}
</style>