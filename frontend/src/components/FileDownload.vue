<template>
  <div class="file-item" @click="downloadFile">
    <img :src="fileIcon" alt="file icon" class="file-icon" />
    <span class="file-name" :title="fileName">{{ fileName }}</span>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FileDownload',
  props: {
    fileName: {
      type: String,
      required: true
    },
    fileUrl: {
      type: String,
      required: true
    }
  },
  computed: {
    fileExtension() {
      const match = this.fileName.match(/\.([a-zA-Z0-9]+)$/)
      return match ? match[1].toLowerCase() : ''
    },
    fileIcon() {
      switch (this.fileExtension) {
        case 'pdf':
          return require('@/assets/pdf.png')
        case 'doc':
        case 'docx':
          return require('@/assets/word.png')
        case 'xls':
        case 'xlsx':
          return require('@/assets/excel.png')
        // case 'ppt':
        // case 'pptx':
        //   return require('@/assets/icons/ppt.png')
        default:
          return require('@/assets/file.png')
      }
    }
  },
  methods: {
    async downloadFile() {
      try {
        const response = await axios.get(this.fileUrl, {
          responseType: 'blob'
        })
        const blob = new Blob([response.data])
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = this.fileName
        link.click()
        window.URL.revokeObjectURL(url)
      } catch (err) {
        console.error('下载失败:', err)
      }
    }
  }
}
</script>

<style scoped>
.file-item {
  width: auto;
  max-width: 260px;
  display: inline-flex;
  align-items: center;
  padding: 10px 12px;
  border: 3px solid #838383;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
  background-color: transparent;
  margin-bottom: 10px;
}

.file-item:hover {
  background-color: #f5f7fa;
}

.file-icon {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  margin-right: 5px;
}

.file-name {
  font-size: 18px;
  font-weight: bold;
  color: #eaebec;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: left;
}
</style>
