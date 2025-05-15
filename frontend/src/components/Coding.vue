<template>
    <div class="code-panel">
      <div class="header">
        <h3>代码编辑区</h3>
      </div>
      <textarea class="code-editor" v-model="code"></textarea>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CodePanel',
    data() {
      return {
        code: '// 在这里编写你的代码...'
      }
    }
  }
  </script>
  
  <style scoped>
  .code-panel {
    width: 100%;
    height: 100%;
    background: #1e1e1e;
    color: #d4d4d4;
    display: flex;
    flex-direction: column;
  }
  
  .header {
    padding: 10px;
    background: #252526;
    border-bottom: 1px solid #333;
  }
  
  .code-editor {
    flex: 1;
    padding: 15px;
    background: #1e1e1e;
    border: none;
    resize: none;
    font-family: 'Consolas', monospace;
    font-size: 14px;
    color: #d4d4d4;
  }
  
  .code-editor:focus {
    outline: none;
  }
  </style>