<template>
    <el-container class="main-container">
        <!-- 侧边栏区域 -->
        <el-aside :width="asideWidth" class="aside-container">
            <!-- 折叠按钮 -->
            <div class="aside-header" :class="{ collapsed: isCollapse }">
                <div class="logo-wrapper">
                    <img :src="isCollapse ? require('../assets/Simple_IMCL_logo.png') : require('../assets/IMCL_logo_grey.png')"
                        class="logo" :class="{ 'small-logo': isCollapse }">
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
                <history :Dialogues="dialogueHistory" :currentDialogue="selectedDialogue"
                    @child-event="handleSelectedDialogue">
                </history>
            </div>
        </el-aside>

        <!-- 主内容区域 - 修改 -->
        <el-main class="main-content">
            <div class="content-wrapper" :class="{ 'split-view': isSplitView }">
                <!-- 左侧聊天区域 -->
                <div class="chat-section">
                    <div class="toggle-split-btn" @click="toggleSplit">
                        <i :class="isSplitView ? 'el-icon-close' : 'el-icon-right'"></i>
                    </div>
                    <chatbot v-if="selectedDialogue" />
                    <home v-else />
                </div>

                <!-- 右侧代码区域 -->
                <div v-if="isSplitView" class="coding-section">
                    <coding />
                </div>
            </div>
        </el-main>
    </el-container>
</template>

<script>
import Chatbot from './Chatbot.vue'
import History from "./History.vue"
import Home from "./Home.vue"
import Coding from "./Coding.vue" // 新增

export default {
    components: {
        History,
        Chatbot,
        Home,
        Coding // 新增
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
            isSplitView: false // 新增
        }
    },
    mounted() {
        this.dialogueHistory = [[{ "role": "user", "content": "Who are you Who are you Who are you?Who are you" }, { "role": "assistant", "content": "I'm a coding teaching agent." }], [{ "role": "user", "content": "I'm a student from polyu" }, { "role": "assistant", "content": "What do you want to learn." }]]
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
        },
        // 新增
        toggleSplit() {
            this.isSplitView = !this.isSplitView
        }
    }
}
</script>

<style scoped>

/* 新增样式 */
.content-wrapper {
  height: 100%;
  transition: all 0.3s;
}

.content-wrapper.split-view {
  display: flex;
  gap: 20px;
}

.chat-section {
  flex: 1;
  position: relative;
  height: 100%;
}

.coding-section {
  flex: 1;
  height: 100%;
  background: #1e1e1e;
  border-radius: 8px;
}

.toggle-split-btn {
  position: absolute;
  right: -25px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 100;
  background: #5c5cde;
  color: white;
  padding: 8px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
}

.toggle-split-btn:hover {
  background: #4e4ec7;
}
/* 新增样式 */


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
    flex-direction: column;
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
    margin-bottom: 10px;
    /* 为按钮腾出空间 */
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