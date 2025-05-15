<template>
    <div id="app">
      <div class="container">
        <div class="video-container">
          <video ref="video" autoplay playsinline></video>
          <div class="overlay"></div>
        </div>
        <button class="capture-button" @click="captureImage">Capture</button>
        <div v-if="result" class="result show">{{ result }}</div>
        <div v-if="error" class="error show">{{ error }}</div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "../api";
  export default {
    data() {
      return {
        videoStream: null,
        result: '',
        error: ''
      };
    },
    mounted() {
      this.accessCamera();
    },
    methods: {
      accessCamera() {
        navigator.mediaDevices.getUserMedia({ video: true })
          .then((stream) => {
            this.$refs.video.srcObject = stream;
            this.videoStream = stream;
          })
          .catch((error) => {
            console.error('Error accessing camera:', error);
            this.showError(`Error accessing camera: ${error.message}`);
          });
      },
      captureImage() {
        const canvas = document.createElement('canvas');
        canvas.width = this.$refs.video.videoWidth;
        canvas.height = this.$refs.video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(this.$refs.video, 0, 0, canvas.width, canvas.height);
  
        canvas.toBlob((blob) => {
          const formData = new FormData();
          formData.append('image', blob, 'captured_image.jpg');
  
          axios.post('/imageAnalyze',formData)
            .then((response) => {
              if (!response.status === 200) {
                throw new Error(`HTTP error! status: ${response.status}`);
              }
              return response.data;
            })
            .then((data) => {
              if (data.error) {
                this.showError(`Error: ${data.error}`);
                this.hideResult();
              } else {
                this.showResult(`Analysis result: ${data.result}`);
                this.hideError();
              }
            })
            .catch((error) => {
              this.showError(`Error: ${error.message}`);
              this.hideResult();
            });
        }, 'image/jpeg');
      },
      showResult(message) {
        this.result = message;
      },
      hideResult() {
        this.result = '';
      },
      showError(message) {
        this.error = message;
      },
      hideError() {
        this.error = '';
      }
    },
    beforeDestroy() {
      if (this.videoStream) {
        this.videoStream.getTracks().forEach((track) => track.stop());
      }
    }
  };
  </script>
  
  <style scoped>
  #app {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #f4f4f4, #e0e0e0);
  }
  
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 90%;
    max-width: 600px;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    padding: 20px;
    animation: fadeIn 0.5s ease-out;
    height: 90vh;
    justify-content: space-between;
  }
  
  .video-container {
    position: relative;
    width: 100%;
    height: 50vh;
    margin-bottom: 0;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }
  
  .video-container video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(1.1) contrast(1.05);
  }
  
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.3);
    transition: background-color 0.3s ease;
  }
  
  .video-container:hover .overlay {
    background-color: rgba(0, 0, 0, 0.4);
  }
  
  .capture-button {
    padding: 12px 25px;
    font-size: 16px;
    font-weight: 600;
    background-color: #007BFF;
    color: #fff;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
  }
  
  .capture-button:hover {
    background-color: #0056b3;
    transform: scale(1.05);
  }
  
  .capture-button:active {
    transform: scale(0.95);
  }
  
  .result,
  .error {
    margin-top: 10px;
    font-size: 16px;
    font-weight: 500;
    padding: 12px;
    border-radius: 10px;
    opacity: 0;
    transition: opacity 0.3s ease;
    width: 100%;
    word-wrap: break-word;
  }
  
  .result {
    color: #28a745;
    background-color: rgba(40, 167, 69, 0.1);
  }
  
  .error {
    color: #dc3545;
    background-color: rgba(220, 53, 69, 0.1);
  }
  
  .result.show,
  .error.show {
    opacity: 1;
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  </style>