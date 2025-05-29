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
        <history :Dialogues="dialogueHistory" :currentDialogue="selectedDialogueID"
          @child-event="handleSelectedDialogue">
        </history>
      </div>
    </el-aside>

    <!-- 主内容区域 -->
    <el-main class="main-content">
      <!-- coding切换按钮 -->
      <div v-if="!isSplitView" class="coding-toggle-btn" @click="toggleSplit">
        <i class="el-icon-caret-left"></i>
        <span>Coding Space</span>
      </div>

      <div class="split-container">
        <!-- 左侧聊天区域 -->
        <div class="chat-section" :style="{ width: isSplitView ? splitWidth + '%' : '100%' }">
          <div v-if="selectedDialogue">
            <chatbot ref="chatbot" :currentDialogue="selectedDialogue" @child-event="getAgentResponse">
            </chatbot>
          </div>
          <div v-else>
            <home @child-event="createNewDialogue">
            </home>
          </div>
        </div>
        <!-- 调整条 -->
        <div class="split-handle" @mousedown="startResize" v-if="isSplitView"></div>
        <!-- 右侧代码区域 -->
        <div v-if="isSplitView" class="coding-section" :style="{ width: (100 - splitWidth) + '%' }">
          <coding @close="toggleSplit" @send="getAgentResponseWithCode" />
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import Chatbot from './Chatbot.vue'
import History from "./History.vue"
import Home from "./Home.vue"
import Coding from "./Coding.vue"
import axios from "../api"
export default {
  components: {
    History,
    Chatbot,
    Home,
    Coding
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
      selectedDialogueID: null,
      abortController: null,
      isSplitView: false,
      splitWidth: 50,
      isResizing: false
    }
  },
  mounted() {
    axios.get("/conversations").then(response => {
      this.dialogueHistory = response.data
    })

  },
  methods: {
    addBackticks(str) {
      return `\`${str}\``;
    },
    toggleCollapse() {
      this.isCollapse = !this.isCollapse
      this.asideWidth = this.isCollapse ? this.collapsedWidth : this.expandedWidth
    },
    creatNewChat() {
      this.selectedDialogue = null
      this.selectedDialogueID = null
    },
    async createNewDialogue(receivedData) {
      await axios.post("/new_conversation", { user_id: "123", message: receivedData.message }).then(response => {
        this.selectedDialogueID = response.data.conversation_id
        let temp = {}
        temp.id = this.selectedDialogueID
        temp.title = response.data.title
        console.log(temp.id)
        this.dialogueHistory.unshift(temp)
      })
      this.selectedDialogue = []
      this.getAgentResponse(receivedData)
    },
    handleSelectedDialogue(receivedData) {
      this.selectedDialogueID = receivedData.message.id
      console.log(this.selectedDialogueID)
      axios.get(`/conversation/${this.selectedDialogueID}`).then(response => {
        this.selectedDialogue = response.data
      })
    },
    callscrollToBottom() {
      this.$refs.chatbot.scrollToBottom()
    },
    async getAgentResponse(receivedData) {
      let temp = { 'role': 'user', 'content': receivedData.message }
      this.selectedDialogue.push(temp)
      let ttemp = { 'role': 'assistant', 'content': '', 'thought': '', 'files': [] }
      this.selectedDialogue.push(ttemp)

      if (this.abortController) {
        this.abortController.abort()
      }
      this.abortController = new AbortController()

      const res = await fetch(
        `http://192.168.192.144:5000/chat`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: receivedData.message,
            conversation_id: this.selectedDialogueID
          }),
          signal: this.abortController.signal
        }
      );

      if (!res.ok) throw new Error('网络请求失败')

      const reader = res.body.getReader()
      const decoder = new TextDecoder('utf-8')
      let buffer = ''

      const processStream = async () => {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })
          let lines = buffer.split('\n')
          buffer = lines.pop() // 残留未完整的行

          lines.forEach(line => {
            if (!line.trim()) return
            try {
              const msg = JSON.parse(line)
              if (msg.type === 'thought') {
                this.selectedDialogue[this.selectedDialogue.length - 1]['thought'] += msg.data
              } else if (msg.type === 'result') {
                this.selectedDialogue[this.selectedDialogue.length - 1]['content'] += msg.data
              } else if (msg.type === 'file_list') {
                this.selectedDialogue[this.selectedDialogue.length - 1]['files'] = msg.files
              }
              this.callscrollToBottom()
            } catch (err) {
              console.error('JSON parse error:', line)
            }
          })
        }
      }
      await processStream()
      this.callscrollToBottom()
    },

    // 分屏切换 & 调整大小
    toggleSplit() {
      this.isSplitView = !this.isSplitView;
      if (this.isSplitView) {
        this.splitWidth = 50; // 打开时重置为默认比例
      }
    },
    startResize(e) {
      this.isResizing = true
      document.addEventListener('mousemove', this.handleResize)
      document.addEventListener('mouseup', this.stopResize)
    },
    handleResize(e) {
      if (!this.isResizing) return
      const container = this.$el.querySelector('.split-container')
      const rect = container.getBoundingClientRect()
      const newWidth = ((e.clientX - rect.left) / rect.width) * 100
      this.splitWidth = Math.max(20, Math.min(80, newWidth)) // 限制在20%-80%之间
    },
    stopResize() {
      this.isResizing = false
      document.removeEventListener('mousemove', this.handleResize)
      document.removeEventListener('mouseup', this.stopResize)
    },

    // 处理代码内容
    async getAgentResponseWithCode(code) {
      let newcode = this.addBackticks(code)
      let temp = { 'role': 'user', 'content': newcode }
      this.selectedDialogue.push(temp)
      let ttemp = { 'role': 'assistant', 'content': '', 'thought': '', 'files': [] }
      this.selectedDialogue.push(ttemp)

      if (this.abortController) {
        this.abortController.abort()
      }
      this.abortController = new AbortController()

      const blob = new Blob([code], { type: 'text/plain' })
      const file = new File([blob], 'code.py', { type: 'text/plain' })
      const formData = new FormData()
      formData.append('file', file)
      formData.append('conversation_id', this.selectedDialogueID)

      const res = await fetch(
        `http://192.168.192.144:5000/execute_code_snippet`,
        {
          method: 'POST',
          body: formData,
          signal: this.abortController.signal
        }
      );

      if (!res.ok) throw new Error('网络请求失败')

      const reader = res.body.getReader()
      const decoder = new TextDecoder('utf-8')
      let buffer = ''

      const processStream = async () => {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })
          let lines = buffer.split('\n')
          buffer = lines.pop() // 残留未完整的行

          lines.forEach(line => {
            if (!line.trim()) return
            try {
              const msg = JSON.parse(line)
              if (msg.type === 'thought') {
                this.selectedDialogue[this.selectedDialogue.length - 1]['thought'] += msg.data
              } else if (msg.type === 'result') {
                this.selectedDialogue[this.selectedDialogue.length - 1]['content'] += msg.data
              } else if (msg.type === 'file_list') {
                this.selectedDialogue[this.selectedDialogue.length - 1]['files'] = msg.files
              }
              this.callscrollToBottom()
            } catch (err) {
              console.error('JSON parse error:', line)
            }
          })
        }
      }
      await processStream()
      this.callscrollToBottom()
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
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 200px;
  padding: 10px 0;
}

.main-content {
  display: flex;
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

.split-container {
  display: flex;
  position: relative;
  height: 100%;
  width: 100%;
}

/* 调整条样式 */
.split-handle {
  width: 3px;
  background: #4a4a4a;
  cursor: col-resize;
  position: relative;
  z-index: 10;
}

.split-handle:hover,
.split-handle:active {
  background: #5c5cde;
}

.chat-section.split-view {
  width: 50%;
  position: relative;
  height: 100%;
}

.chat-section {
  width: 100%;
  position: relative;
  height: 100%;
}

.coding-section {
  width: 50%;
  overflow: auto;
  height: 100%;
  background: #202327;
  border-radius: 8px;
}

/* 新增coding切换按钮样式 */
.coding-toggle-btn {
  position: absolute;
  right: 20px;
  top: 20px;
  z-index: 100;
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background: #5c5cde;
  color: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.coding-toggle-btn:hover {
  background: #4e4ec7;
}

.coding-toggle-btn i {
  margin-right: 6px;
  font-size: 16px;
}
</style>