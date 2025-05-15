<template>
  <div class="info-whole">
    <div class="info-container">
      <img alt="patient photo" src="../assets/patient.jpg" class="patient-photo">
      <div class="info-section">
        <div class="info-title">姓名：</div>
        <div class="info-content">
          <span>{{ patient.name }}</span>
        </div>
      </div>
      <div class="info-section">
        <div class="info-title">年龄：</div>
        <div class="info-content">
          <span>{{ patient.age }}</span>
        </div>
      </div>
      <div class="info-section">
        <div class="info-title">性别：</div>
        <div class="info-content">
          <span>{{ patient.gender }}</span>
        </div>
      </div>
      <div class="info-section">
        <div class="info-title">科室：</div>
        <div class="info-content">
          <span>{{ patient.department }}</span>
        </div>
      </div>
      <div class="info-section">
        <div class="info-title">床号：</div>
        <div class="info-content">
          <span>{{ patient.bedNumber }}</span>
        </div>
      </div>
      <div class="info-section">
        <div class="info-title">住院号：</div>
        <div class="info-content">
          <span>{{ patient.hospitalNumber }}</span>
        </div>
      </div>
      <div class="info-section">
        <div class="info-title">主要诊断：</div>
        <div class="info-content">
          <span>{{ patient.diagnosis }}</span>
        </div>
      </div>
      <div class="info-section">
        <div class="info-title">实施手术名称：</div>
        <div class="info-content">
          <span>{{ patient.surgery }}</span>
        </div>
      </div>
      <div class="info-section">
        <div class="info-title">麻醉方式：</div>
        <div class="info-content">
          <span>{{ patient.anesthesia }}</span>
        </div>
      </div>
      <div class="info-section">
        <div class="info-title">生命体征：</div>
        <div class="info-content">
          <div> <span>T：</span> <span>{{ patient.temperature }}</span> °C </div>
          <div> <span>RR：</span> <span>{{ patient.respiratoryRate }}</span> 次/分 </div>
          <div> <span>PR：</span> <span>{{ patient.pulseRate }}</span> 次/分 </div>
          <div> <span>BP：</span> <span>{{ patient.bloodPressure }}</span> mm/Hg </div>
        </div>
      </div>
    </div>
    <div class="button-container">
      <!-- <el-button @click="generate">生成报告</el-button> -->
      <el-button @click="go2camera">面部分析</el-button>
      <el-button :disabled="!this.$store.state.reportGeneration" @click="generate">生成报告</el-button>
    </div>
  </div>
</template>

<script>
import axios from "../api"
export default {
  data() {
    return {
      patient: {
        name: "王清英",
        age: "59岁",
        gender: "女",
        department: "神经外科病区",
        bedNumber: "4",
        hospitalNumber: "P2216317",
        diagnosis: "动脉瘤",
        surgery: "经动脉瘤栓塞全脑动脉造影术",
        anesthesia: "全麻",
        temperature: "36.5",
        respiratoryRate: "20",
        pulseRate: "78",
        bloodPressure: "126/70",
      },
    };
  },
  methods:{
      go2camera(){
        this.$router.push('/camera')
      },
      generate(){
        //   axios.get('reportGeneration')
        //   .then(response => {
        //     console.log(response)
        //     if(response.status == 200 && response.data.reportGeneration == true){
        //       this.$router.push('/report');
        //   }
        //   else{
        //     alert('模型还未收集到全部信息！');
        //   }
        // })
        this.$router.push('/report')
        // axios.get('/reportGeneration')
        // .then(response => {
        //   if(response.status == 200){
        //     this.$router.push('/report');
        //   }
        //   else{
        //     alert("网络出现问题！")
        //   }
        // })
      }
  }
};
</script>

<style scoped>
.info-whole {
  width: 100%;
  height: 100%;
  background: rgb(255, 255, 255);
}
.info-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height:calc(100vh - 150px);
  overflow-y: auto;
}
.info-container::-webkit-scrollbar {
  width: 8px; /* 设置宽度 */
}
.info-container::-webkit-scrollbar-thumb {
  background-color: transparent; /* 使滚动条透明 */
}
.patient-photo {
  width: auto;
  max-width: 100%;
  height: 150px;
  object-fit: contain;
  margin: 15px;
}
.info-section {
  display: flex;
  width: 100%;
  margin-bottom: 15px;
  }
.info-title {
  width: 40%;
  padding-left: 15px;
  text-align: left;
  font-size: 14px;
  font-weight: bold;
}
.info-content {
  flex: 1;
  width: 60%;
  padding-right: 15px;
  text-align: left;
  font-size: 14px;
}
input[type="text"] {
  border: none;
  background: transparent;
  color: #000000;
}
.button-container{
  justify-content: center;
  margin-top: 35px;
}
</style>
