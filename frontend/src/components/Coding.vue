<template>
  <div class="coding-container">
    <div class="toolbar">
      <el-button-group>
        <el-button title="撤销" @click="handleUndo" class="tool-btn">
          <i class="el-icon-refresh-left"></i>
        </el-button>
        <el-button title="重做" @click="handleRedo" class="tool-btn">
          <i class="el-icon-refresh-right"></i>
        </el-button>
        <el-button title="复制" @click="handleCopy" class="tool-btn">
          <i class="el-icon-document-copy"></i>
        </el-button>
        <el-button 
          type="primary" 
          @click="$emit('send', code)"
          class="send-btn"
        >
          发送 <i class="el-icon-s-promotion"></i>
        </el-button>
      </el-button-group>
    </div>

    <!-- 使用vue-codemirror封装组件 -->
    <codemirror
      ref="cmEditor"
      v-model="code"
      :options="cmOptions"
      @ready="onEditorReady"
      class="fullscreen-editor"
    ></codemirror>
  </div>
</template>

<script>
import { codemirror } from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/darcula.css'
import 'codemirror/mode/python/python.js'
import 'codemirror/addon/selection/active-line.js'

export default {
  components: { codemirror },
  data() {
    return {
      code: '',
      cmOptions: {
        mode: 'text/x-python',
        line: true,
        theme: 'darcula',
        tabSize: 4,
        indentUnit: 4,
        firstLineNumber: 1,
        autoRefresh: true,
        smartIndent: true,
        lineNumbers: true,
        styleActiveLine: true,
        showCursorWhenSelecting: true,
        lineWrapping: true,
        extraKeys: { 'Tab': 'indentMore' },
        gutters: ['CodeMirror-linenumbers'],
      },
      editor: null
    }
  },
  methods: {
    onEditorReady(cm) {
      this.editor = cm
      // 初始化示例代码
      this.code = `# 欢迎使用代码编辑器
def hello():
    print("Hello World!")
    
if __name__ == "__main__":
    hello()`
    },
    handleUndo() {
      this.editor.execCommand('undo')
    },
    handleRedo() {
      this.editor.execCommand('redo')
    },
    handleCopy() {
      navigator.clipboard.writeText(this.code)
      this.$message.success('代码已复制')
    }
  }
}
</script>

<style scoped>
/* 全局样式覆盖 */
.coding-container {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  background: #202327;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.toolbar {
  flex-shrink: 0;
  padding: 8px 16px;
  background: #202327;
  border-bottom: 1px solid #333;
  z-index: 2;
}

.fullscreen-editor {
  flex: 1;
  min-height: 0;
}
</style>

<style>
/* 代码左对齐核心样式 */
.coding-container .CodeMirror {
  height: 100% !important;
  /* font-family: 'Fira Code', monospace; */
  font-size: 14px;
  background: #202327 !important;
  position: static !important;
}

/* 替代原有padding */
/* 强制左对齐 */
.coding-container .CodeMirror-lines {
  padding: 12px 0 !important;
  text-align: left !important;
}

/* 代码行号样式 */
.coding-container .CodeMirror-gutters {
  background: #202327 !important;
  border-right: 1px solid #333 !important;
  left: 0 !important; /* 强制左侧对齐 */
}

/* 行号样式 */
.coding-container .CodeMirror-linenumber {
  color: #666 !important;
  min-width: 40px !important; /* 固定行号宽度 */
  padding-right: 10px !important;
  text-align: right !important;
}

/* 移除左边距 */
/* 添加左右内边距 */
.coding-container .CodeMirror-scroll {
  margin-left: 0 !important; 
  padding: 0 15px !important; 
}

/* 代码区左内边距 */
/* .coding-container .CodeMirror-code {
  padding-left: 10px !important; 
} */

/* 光标和选中样式 */
.coding-container .CodeMirror-cursor {
  border-left: 2px solid #fff !important;
}

.coding-container .CodeMirror-selected {
  background: rgba(255,255,255,0.1) !important;
}

.coding-container::-webkit-scrollbar-track {
    background: transparent;  /* 关键设置 */
    border: none;            /* 去除边框 */
  }
  
  /* 滚动条整体样式 */
.coding-container::-webkit-scrollbar {
    width: 17px;  /* 仅保留滑块所需宽度 */
    height: 17px; /* 横向滚动条同理 */
    background: transparent;  /* 滚动条所在区域透明 */
  }
  
  /* 灰色滑块样式 */
.coding-container::-webkit-scrollbar-thumb {
    background: #494a4d;
    border-radius: 5px;
    border: 2px solid rgba(255,255,255,0.1); /* 微透明边框增加层次 */
    background-clip: content-box; /* 防止背景渗透到边框 */
  }
</style>