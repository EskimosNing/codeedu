<template>
  <div class="chat-container">
    <div class="chat-box">
      <div
        class="sector"
        v-for="msg in messages"
        :key="msg.id"
      >
        <div
          v-if="!msg.user"
          class="agent"
        >
          <el-image
            style="width: 23px; height: 23px;"
            :src="require('../assets/hos.png')">
          </el-image>
          <h4>&nbsp;Assistant</h4>
        </div>
        <div
          class="message"
          :class="{ 'user': msg.user , 'robot': !msg.user}"
        >
          <strong>{{ msg.text }}</strong>
        </div>
        <div
          v-if="key in msg"
          class="questions"
        >
            <div v-for="q in msg.questions" class="question" :key="q" @click="chooseResponse(q)">
              <strong>{{q}}</strong>
            </div>
        </div>
        <div
          class="showimage"
          v-if="'showImage' in msg"
          :class="{ 'user': msg.user , 'robot': !msg.user}"
        >
          <el-image
            :src="require('../assets/pain.jpg')">
          </el-image>
        </div>
      </div>
    </div>
    <div class="input-area">
      <el-button type="text" :class="{'recording': isRecording}" @click="toggleRecording">
        <i class="el-icon-microphone" :class="{'recording': isRecording}"></i>
      </el-button>
      <input
        type="text"
        v-model="userMessage"
        @keyup.enter="sendMessage"
        placeholder="输入消息..."
      />
      <button @click="sendMessage" class="sbutton">发送</button>
    </div>
  </div>
</template>

<script>
import axios from "../api";
export default {
  name: 'ChatBot',
  // isDisabled: !reportGeneration,
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
    };
  },
  // 需要初始化
  mounted(){
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
    sendMessage() {
      if (this.userMessage.trim()) {
        let temp = this.messages.length - 2;
        temp = Math.max(temp,0)
        for (let i = temp; i < this.messages.length; i++) {
          if (this.key in this.messages[i]){
            this.$delete(this.messages[i], this.key);
          }
        }
        this.messages.push({ id: this.nextMessageId++, user: true, text: this.userMessage});
        this.getBotResponse(this.userMessage);
        this.userMessage = '';
      }
    },
    getBotResponse(userMessage) {
      // 简单的回复逻辑，可以根据需要进行修改
      let forms = new FormData();
      forms.append("userMessage",userMessage);
      axios.post('/robotReply',forms)
        .then(response => {
          if(response.status == 200){
            //判断回复是否为空
            if(this.currentUtterance){
              speechSynthesis.cancel(this.currentUtterance);
              this.currentUtterance = null;
            }
            let temp = {};
            if(response.data.Reply != ""){
              temp["id"] = this.nextMessageId++;
              temp["user"] = false;
              temp["text"] = response.data.Reply;
              if(response.data.Questions.length > 0){
                temp["questions"] = response.data.Questions;
              }
              //添加showImage
              if(response.data.showImage.length > 0){
                temp["showImage"] = response.data.showImage;
              }
              // console.log(response.data.showImage)
              this.messages.push(temp);
            }
            if(temp["text"]!=""){
              let utterance = new SpeechSynthesisUtterance(temp["text"]);
              utterance.lang = 'zh-CN';
              this.currentUtterance = utterance;
              speechSynthesis.speak(utterance);
            }
            if("reAsk" in response.data){
              temp = {};
              temp["id"] = this.nextMessageId++;
              temp["user"] = false;
              temp["text"] = response.data.reAsk;
              if(response.data.reChoice.length > 0){
                temp["questions"] = response.data.reChoice;
              }
              this.messages.push(temp);
              //进行音频处理
              if(temp["text"]!=""){
                let utterance = new SpeechSynthesisUtterance(temp["text"]);
                utterance.lang = 'zh-CN';
                this.currentUtterance = utterance;
                speechSynthesis.speak(utterance);
              }
            }
            this.$store.commit('update', response.data.reportGeneration);
            // console.log(response.data.reportGeneration)
            this.$nextTick(() => {
              this.scrollToBottom();
            });
          }
        })
        .catch(error => {
          // 处理错误
        });
    },
    chooseResponse(response){
      this.userMessage = response;
      this.sendMessage();
    },
    scrollToBottom() {
      const chatBox = this.$el.querySelector('.chat-box');
      chatBox.scrollTop = chatBox.scrollHeight;
    },
    async toggleRecording() {
      if (this.isRecording) {
        // 停止录音
        this.audioChunks = [];
        this.mediaRecorder.stop();
        this.isRecording = false;
        this.stream.getAudioTracks().forEach(track => {
          track.stop();
        });
        this.stream = null;
        this.mediaRecorder = null;
      } else {
        // 开始录音，同时停止音频输出
        if(this.currentUtterance){
          speechSynthesis.cancel(this.currentUtterance);
          this.currentUtterance = null;
        }
        this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(this.stream);
        this.mediaRecorder.start();
        this.isRecording = true;

        this.mediaRecorder.ondataavailable = (e) => {
          this.audioChunks.push(e.data);
        };

        this.mediaRecorder.onstop = () => {
          const blob = new Blob(this.audioChunks, { type: 'audio/ogg; codecs=opus' });
          let forms = new FormData();
          forms.append('audio',blob,'audio.ogg');
          console.log("发出请求")
          // const apiInstance = axios.create({
          //       baseURL: 'http://localhost:5003', // 替换为你的局域网 IP 和端口
          //       timeout: 100000,
          //   });
          axios.post('audio2text',forms)
          .then(response => {
          if(response.status == 200){
            this.userMessage = response.data.userMessage;
            this.sendMessage();
          }
        })
          // console.log('录音完成，文件URL:', audioURL);
        };
      }
    }
  }
};
</script>

<style scoped>
.chat-container {
  width: 100%;
  height: 100%;
  background: #2a2a2e;
  /* display: flex;          
  flex-direction: column; */
}
/* 当前还存在问题，当出现一长串英文字母的时候会影响到界面 */
.chat-box {
  /* 该处需要关注，之前设置为-130px */
  height:calc(100vh - 150px);
  width: 100%;
  display: flex;          
  flex-direction: column;
  /* 将聊天框设置在正中间 */
  align-items: center;
  overflow-y: auto;
  /* border-bottom: 1px solid #eee; */
}
.chat-box::-webkit-scrollbar {
  width: 8px; /* 设置宽度 */
}
.chat-box::-webkit-scrollbar-thumb {
  background-color: transparent; /* 使滚动条透明 */
}
.sector{
  width: 100%;
  display: flex;
  flex-direction: column;
}
.agent{
  /*这里是绝对值，需要注意*/
  height: 23px;
  margin-left:10%;
  margin-top: 10px;
  display: flex;
  flex-direction: row;
  align-items: center; /* 垂直居中 */
  justify-content: flex-start; /* 水平左对齐 */
}
.message {
  max-width: 60%;          /* 设置宽度 */
  /*border: 1px solid #ccc; /* 可选: 添加边框以便观察 */
  border-radius: 12px;
  padding: 10px;        /* 可选: 添加内边距 */
  white-space: pre-wrap;
}
.message.user {
  margin: 10px 0;
  background-color: #5d5cde;
  text-align: left;
  color: #fcfbfe;
  align-self: flex-end;
  margin-right:10%;
}
.message.robot {
  margin-top: 3px;
  background-color: #f7f7f7;
  text-align: left;
  align-self: flex-start;
  margin-left: 10%;
}
.questions{
  margin-left:10%;
  margin-top: 5px;
  text-align: left;
}
.question{
  display: inline-block;
  margin-top: 10px;
  margin-right: 10px;
  /* border: 1px solid #ccc; 可选: 添加边框以便观察 */
  border-radius: 12px;
  padding: 8px 15px 8px 15px;        /* 可选: 添加内边距，上右下左 */
  background-color: #f7f7f7;
  text-align: center;
  user-select: none; /* 防止文本被选中 */
  cursor: pointer;
}
.question:hover {
  background-color: #919292; /* 鼠标悬停时的颜色变化 */
  color: white;
}
.showimage{
  max-width: 60%;          /* 设置宽度 */
  height: 160px;
  /*border: 1px solid #ccc; /* 可选: 添加边框以便观察 */
  border-radius: 12px;
  padding: 10px;        /* 可选: 添加内边距 */
  margin-top: 10px;
  background-color: #f7f7f7;
  text-align: left;
  align-self: flex-start;
  margin-left: 10%;
}
.input-area {
  /* 此处可能要注意 */
  margin-top: 20px;
  height: 45px;
  display: flex;
  padding: 10px;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
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
.el-icon-microphone{
  font-size: 20px;
}
.el-icon-microphone.recording{
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
  align-items: center; /*垂直居中*/
  justify-content: center; /*水平居中*/
  margin-right:5px;
  /* border: 1.5px #d1d1d1 solid; */
  color: #5c5cde;
  /* background-color: black; */
}
.el-button.recording {
  background-color: #5c5cde;
  color: white;
}
@keyframes pulse {
  0% {
    font-size: 20px;
  }
  50% {
    font-size: 23px; /* 放大 */
  }
  100% {
    font-size: 20px;
  }
}
</style>