<template>
  <div class="chat-container">
    <div class="chat-box">
      <div class="sector" v-for="(msg, index) in currentDialogue" :key="index">
        <div v-if="msg.role === 'assistant'" class="agent">
          <el-image style="width: 23px; height: 23px;" :src="require('../assets/TeachingCode.png')">
          </el-image>
          <h4>&nbsp;Coding Education System</h4>
        </div>
        <div v-if="msg.role === 'assistant' && !(msg.thought === '')" v-html="parseMarkdown(msg.thought)"
          class="thought">
        </div>
        <div class="message" :class="msg.role">
          <!-- 助手消息渲染Markdown -->
          <!-- <div v-if="msg.role === 'assistant'" v-html="parseMarkdown(msg.content)"></div> -->
          <!-- 修改助手消息的渲染逻辑 -->
          <div v-if="msg.role === 'assistant'">
            <template v-for="(block, i) in processAssistantContent(msg.content)">
              <div :key="i">
                <pre v-if="block.type === 'code'"><code v-html="block.content"></code></pre>
                <div v-else v-html="parseMarkdown(block.content)"></div>
              </div>
            </template>
          </div>
          <!-- 用户消息保持原样 -->
          <template v-else>
            <pre v-if="isCode(msg.content)"><code>{{ extractCode(msg.content) }}</code></pre>
            <strong v-else>{{ msg.content }}</strong>
          </template>
        </div>
        <div class="files">
          <div class="file" v-for="(file, i) in msg.files" :key="i">
            <file-download :fileName="file.filename"
              :fileUrl="`http://192.168.192.144:5000/${file.download_url}`"></file-download>
          </div>
        </div>
      </div>
    </div>
    <!-- 发消息部分 -->
    <div class="input-area">
      <div class="input-wrapper" :class="{ focused: isInputFocused }">
        <textarea ref="inputField" v-model="userMessage" placeholder="给多智能体编程教学系统发送消息" @focus="isInputFocused = true"
          @blur="isInputFocused = false" @keydown.enter.exact.prevent="handleSubmit"></textarea>
        <button class="submit-btn" :disabled="!userMessage.trim()" @click="handleSubmit">
          <span v-show="!isLoading" class="arrow">▶</span>
          <div v-show="isLoading" class="loader"></div>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../api";
import FileDownload from "./FileDownload.vue"
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import hljs from 'highlight.js';
import 'highlight.js/styles/monokai.css';

marked.setOptions({
  highlight: function (code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value;
    }
    return hljs.highlightAuto(code).value;
  },
  langPrefix: 'hljs language-', // 加上 hljs 类名以配合 highlight.js 的样式
});

export default {
  name: 'ChatBot',
  components: {
    FileDownload
  },
  // isDisabled: !reportGeneration,
  props: {
    currentDialogue: {
      type: Array,
    }
  },
  data() {
    return {
      userMessage: '',
      //此处获取初始问题，后续应该由后端实现
      messages: [],
      nextMessageId: 0, // 用于生成唯一的消息ID，现在暂时设置为1，后续需要设置为0
      key: 'questions',
      mediaRecorder: null,
      audioChunks: [],
      isRecording: false,
      stream: null,
      currentUtterance: null,
      isInputFocused: false,
      isLoading: false
    };
  },
  // 需要初始化
  mounted() {
    // axios.get('/reportGeneration')
    //     .then(response => {
    //       if(response.status == 200){
    //         this.getBotResponse(this.userMessage)
    //       }
    //       else{
    //         alert("网络出现问题！")
    //       }
    //     })
  },
  methods: {
    // 新增方法：将助手消息内容分割为代码块和普通文本
    processAssistantContent(content) {
      const blocks = [];
      // 使用正则分割代码块和非代码内容
      const parts = content.split(/(```[\s\S]*?```)/g);
      parts.forEach(part => {
        if (part.startsWith('```')) {
          const codeContent = part.slice(3, -3).trim();
          blocks.push({
            type: 'code',
            content: DOMPurify.sanitize(
              hljs.highlightAuto(codeContent).value
            )
          });
        } else if (part.trim()) {
          blocks.push({
            type: 'text',
            content: this.parseMarkdown(part)
          });
        }
      });
      return blocks;
    },
    parseMarkdown(content) {
      // 安全渲染Markdown
      return DOMPurify.sanitize(marked.parse(content));
    },
    // 检测是否为代码内容
    isCode(content) {
      return /(`{1,3}[^`]+`{1,3})/.test(content);
    },
    // 提取代码部分（移除反引号）
    extractCode(content) {
      const matches = content.match(/`{1,3}([^`]+)`{1,3}/);
      return matches ? matches[1] : content;
    },
    handleSubmit() {
      this.$emit('child-event', {
        message: this.userMessage,
      })
      this.userMessage = ""
    },
    sendMessage() {
    },
    getBotResponse(userMessage) {

    },
    chooseResponse(response) {
      this.userMessage = response;
      this.sendMessage();
    },
    scrollToBottom() {
      const chatBox = this.$el.querySelector('.chat-box');
      chatBox.scrollTop = chatBox.scrollHeight;
    },
    async toggleRecording() {

    }
  }
};
</script>

<style scoped>
.chat-container {
  width: 100%;
  height: 100%;
  /* display: flex;          
  flex-direction: column; */
}

/* 当前还存在问题，当出现一长串英文字母的时候会影响到界面 */
.chat-box {
  /* 该处需要关注，之前设置为-130px */
  margin-top: 2%;
  height: calc(98vh - 180px);
  width: 100%;
  display: flex;
  flex-direction: column;
  /* 将聊天框设置在正中间 */
  align-items: center;
  overflow-y: auto;
  /* border-bottom: 1px solid #eee; */
}

.chat-box::-webkit-scrollbar {
  width: 8px;
  /* 设置宽度 */
}

.chat-box::-webkit-scrollbar-thumb {
  background-color: transparent;
  /* 使滚动条透明 */
}

.sector {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.agent {
  /*这里是绝对值，需要注意*/
  height: 23px;
  margin-left: 18%;
  margin-top: 40px;
  color: #4c6afc;
  display: flex;
  flex-direction: row;
  align-items: center;
  /* 垂直居中 */
  justify-content: flex-start;
  /* 水平左对齐 */
}

.thought {
  border-left: 3px solid #4e4e56;
  padding-left: 10px;
  white-space: pre-wrap;
  font-size: 16px;
  margin-top: 10px;
  color: #a6a6a6;
  text-align: left;
  align-self: flex-start;
  margin-left: 18%;
  max-width: 62%;
  word-wrap: break-word;
}

.message {
  /* max-width: 60%;          设置宽度 */
  /*border: 1px solid #ccc; /* 可选: 添加边框以便观察 */
  border-radius: 12px;
  white-space: pre-wrap;
  font-size: 19px;
  word-wrap: break-word;
}

.message.user {
  margin-top: 40px;
  padding: 10px;
  /* 可选: 添加内边距 */
  background-color: #414158;
  text-align: left;
  color: #fcfbfe;
  align-self: flex-end;
  margin-right: 20%;
  max-width: 60%;
}

/* 用户消息的代码块样式 */
.message.user pre {
  background-color: #2d2d42;
  padding: 16px;
  border-radius: 8px;
  margin: 12px 0;
  white-space: pre-wrap;
  /* 允许代码换行 */
}

.message.user code {
  font-family: 'Consolas', monospace;
  font-size: 15px;
  color: #e6e6e6;
}

/* 保持用户普通消息的粗体样式 */
.message.user strong {
  font-weight: bold;
  color: #fcfbfe;
}

.message.assistant {
  margin-top: 10px;
  color: white;
  font-weight: bold;
  text-align: left;
  align-self: flex-start;
  margin-left: 18%;
  max-width: 62%;
}

.message.assistant pre {
  background-color: #2d2d42;
  padding: 16px;
  border-radius: 8px;
  margin: 12px 0;
  white-space: pre-wrap;
}

.message.assistant code {
  font-family: 'Courier New', monospace;
  font-size: 15px;
  color: #e6e6e6;
}

.questions {
  margin-left: 10%;
  margin-top: 5px;
  text-align: left;
}

.question {
  display: inline-block;
  margin-top: 10px;
  margin-right: 10px;
  /* border: 1px solid #ccc; 可选: 添加边框以便观察 */
  border-radius: 12px;
  padding: 8px 15px 8px 15px;
  /* 可选: 添加内边距，上右下左 */
  background-color: #f7f7f7;
  text-align: center;
  user-select: none;
  /* 防止文本被选中 */
  cursor: pointer;
}

.question:hover {
  background-color: #919292;
  /* 鼠标悬停时的颜色变化 */
  color: white;
}

.showimage {
  max-width: 60%;
  /* 设置宽度 */
  height: 160px;
  /*border: 1px solid #ccc; /* 可选: 添加边框以便观察 */
  border-radius: 12px;
  padding: 10px;
  /* 可选: 添加内边距 */
  margin-top: 10px;
  background-color: #f7f7f7;
  text-align: left;
  align-self: flex-start;
  margin-left: 10%;
}

.input-area {
  /* 此处可能要注意 */
  height: 150px;
  display: flex;
  justify-content: center;
  /* 水平居中 */
  align-items: center;
  /*垂直居中 */
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  position: relative;
  /* margin: 2rem 0; */
  border-radius: 20px;
  background-color: #404045;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  border: 2px solid transparent;
  width: 750px;
  min-height: 120px;
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

.input-area input {
  font-weight: bold;
  width: 70%;
  height: 70%;
  padding: 5px 20px;
  border: 1px solid #ddd;
  border-radius: 20px;
}

.sbutton {
  margin-left: 10px;
  padding: 5px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.el-icon-microphone {
  font-size: 20px;
}

.el-icon-microphone.recording {
  animation: pulse 1s infinite;
}

.el-button {
  /* padding: 10px 20px;
  font-size: 16px;
  cursor: pointer; */
  /*transition: transform 0.3s;  添加平滑过渡 */
  border-radius: 50%;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  /*垂直居中*/
  justify-content: center;
  /*水平居中*/
  margin-right: 5px;
  /* border: 1.5px #d1d1d1 solid; */
  color: #5c5cde;
  /* background-color: black; */
}

.el-button.recording {
  background-color: #5c5cde;
  color: white;
}

.files {
  margin-top: 20px;
}

.file {
  margin-left: 18%;
  display: flex;
  flex-direction: row;
  align-items: center;
  /* 垂直居中 */
  justify-content: flex-start;
  /* 水平左对齐 */
}

@keyframes pulse {
  0% {
    font-size: 20px;
  }

  50% {
    font-size: 23px;
    /* 放大 */
  }

  100% {
    font-size: 20px;
  }
}
</style>