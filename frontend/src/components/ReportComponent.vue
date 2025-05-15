<template>
  <div class="A4">
    <div class="report">
      <img alt="hospital logo" src="../assets/logo.png" class="logo">
      <div class="header">
        <h3 style="color: #000000; font-weight: normal;">麻醉术后访视记录单</h3>
      </div>
      <div class="content">
        <el-row>
          <el-col :span="4"><div class="grid-content">科室：<span>{{ patient.department }}</span></div></el-col>
          <el-col :span="4"><div class="grid-content">床号：<span>{{ patient.bedNumber }}</span></div></el-col>
          <el-col :span="4"><div class="grid-content">姓名：<span>{{ patient.name }}</span></div></el-col>
          <el-col :span="4"><div class="grid-content">年龄：<span>{{ patient.age }}</span></div></el-col>
          <el-col :span="4"><div class="grid-content">性别：<span>{{ patient.gender }}</span></div></el-col>
          <el-col :span="4"><div class="grid-content">住院号：<span>{{ patient.hospitalNumber }}</span></div></el-col>
        </el-row>
        <p>主要诊断：<span>{{ patient.diagnosis }}</span></p>
        <p>实施手术名称：<span>{{ patient.surgery }}</span></p>

        <p>
          麻醉方式：&nbsp;&nbsp;
          <input type="radio" id="general-anesthesia" name="anesthesia" value="全麻" v-model="patient.anesthesia">全麻 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <input type="radio" id="epidural-anesthesia" name="anesthesia" value="椎管内麻醉或区域麻醉" v-model="patient.anesthesia">椎管内麻醉或区域麻醉 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <input type="radio" id="analgesia" name="anesthesia" value="分娩镇痛" v-model="patient.anesthesia">分娩镇痛 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <input type="radio" id="local-anesthesia" name="anesthesia" value="局麻监护" v-model="patient.anesthesia">局麻监护 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </p>

        <p>
          <strong>生命体征：</strong> &nbsp;&nbsp;&nbsp;
          T：<input type="text" v-model="patient.temperature" placeholder="" style="width: 50px; margin-right: 0px;"> ℃ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          RR：<input type="text" v-model="patient.respiratoryRate" placeholder="" style="width: 50px; margin-right: 0px;"> 次/分 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          PR：<input type="text" v-model="patient.pulseRate" placeholder="" style="width: 50px; margin-right: 0px;"> 次/分 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          BP：<input type="text" v-model="patient.bloodPressure" placeholder="" style="width: 50px; margin-right: 0px"> mm/Hg &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </p>

        <p>
          <strong>患者情况：</strong> &nbsp;&nbsp;
          <span style="color: red;">意识状态：</span> &nbsp;&nbsp;
          <input type="checkbox" id="alert" name="consciousness" value="清醒" v-model="patient.consciousness">清醒 &nbsp;&nbsp;
          <input type="checkbox" id="drowsy" name="consciousness" value="嗜睡" v-model="patient.consciousness">嗜睡 &nbsp;&nbsp;
          <input type="checkbox" id="confused" name="consciousness" value="意识模糊" v-model="patient.consciousness">意识模糊 &nbsp;&nbsp;
          <input type="checkbox" id="coma" name="consciousness" value="昏睡状态" v-model="patient.consciousness">昏睡状态 &nbsp;&nbsp;
          <input type="checkbox" id="light-coma" name="consciousness" value="浅昏迷" v-model="patient.consciousness">浅昏迷 &nbsp;&nbsp;
          <input type="checkbox" id="deep-coma" name="consciousness" value="深昏迷" v-model="patient.consciousness">深昏迷 &nbsp;&nbsp;
          <input type="checkbox" id="delirium" name="consciousness" value="谵妄" v-model="patient.consciousness">谵妄 &nbsp;&nbsp;
          <input type="checkbox" id="sedated" name="consciousness" value="镇静状态" v-model="patient.consciousness">镇静状态
        </p>
        <p>
          <span style="color: red;">头晕：</span>
          <input type="radio" id="dizziness-no" name="dizziness" value="0" v-model="patient.dizziness">无
          <input type="radio" id="dizziness-yes" name="dizziness" value="1" v-model="patient.dizziness">有
          <input type="radio" id="dizziness-unassessable" name="dizziness" value="2" v-model="patient.dizziness">无法评估
          &nbsp;
          <span style="color: red;">心血管体征状态：</span>
          <input type="radio" id="cardio-stable" name="cardiovascular" value="平稳" v-model="patient.cardiovascular">平稳
          <input type="radio" id="cardio-med-support" name="cardiovascular" value="需药物支持" v-model="patient.cardiovascular">需药物支持
          &nbsp;
          <span style="color: red;">呼吸状态：</span>
          <input type="radio" id="respiratory-stable" name="respiration" value="平稳" v-model="patient.respiration">平稳
          <input type="radio" id="respiratory-mild" name="respiration" value="轻度抑制" v-model="patient.respiration">轻度抑制
          <input type="radio" id="respiratory-support" name="respiration" value="需辅助呼吸" v-model="patient.respiration">需辅助呼吸
          <input type="radio" id="respiratory-unassessable" name="respiration" value="未拔管" v-model="patient.respiration">未拔管
        </p>
        <p>
          <span style="color: red;">咽喉痛：</span>
          <input type="radio" id="throat-pain-no" name="throatPain" value="0" v-model="patient.throatPain">否
          <input type="radio" id="throat-pain-yes" name="throatPain" value="1" v-model="patient.throatPain">是
          <input type="radio" id="throat-pain-unassessable" name="throatPain" value="2" v-model="patient.throatPain">无法评估
          &nbsp;&nbsp;
          <span style="color: red;">头疼：</span>
          <input type="radio" id="headache-no" name="headache" value="0" v-model="patient.headache">否
          <input type="radio" id="headache-yes" name="headache" value="1" v-model="patient.headache">是
          <input type="radio" id="headache-unassessable" name="headache" value="2" v-model="patient.headache">无法评估
          &nbsp;&nbsp;
          <span style="color: red;">认知障碍：</span>
          <input type="radio" id="cognitive-impairment-no" name="cognitiveImpairment" value="否" v-model="patient.cognitiveImpairment">否
          <input type="radio" id="cognitive-impairment-yes" name="cognitiveImpairment" value="是" v-model="patient.cognitiveImpairment">是
          <input type="radio" id="cognitive-impairment-unassessable" name="cognitiveImpairment" value="无法评估" v-model="patient.cognitiveImpairment">无法评估
        </p>
        <p>
          <span style="color: red;">视物模糊：</span>
          <input type="radio" id="blurry-vision-no" name="blurryVision" value="0" v-model="patient.blurryVision">否
          <input type="radio" id="blurry-vision-yes" name="blurryVision" value="1" v-model="patient.blurryVision">是
          <input type="radio" id="blurry-vision-unassessable" name="blurryVision" value="2" v-model="patient.blurryVision">无法评估
          &nbsp;&nbsp;
          <span style="color: red;">术中知晓：</span>
          <input type="radio" id="intraoperative-awareness-no" name="intraoperativeAwareness" value="0" v-model="patient.intraoperativeAwareness">否
          <input type="radio" id="intraoperative-awareness-yes" name="intraoperativeAwareness" value="1" v-model="patient.intraoperativeAwareness">是
          <input type="radio" id="intraoperative-awareness-unassessable" name="intraoperativeAwareness" value="2" v-model="patient.intraoperativeAwareness">无法评估
          &nbsp;&nbsp;
          <span style="color: red;">尿蒸馏：</span>
          <input type="radio" id="urinary-distillation-no" name="urinaryDistillation" value="否" v-model="patient.urinaryDistillation">否
          <input type="radio" id="urinary-distillation-yes" name="urinaryDistillation" value="是" v-model="patient.urinaryDistillation">是
          <input type="radio" id="urinary-distillation-unassessable" name="urinaryDistillation" value="未拔出导尿管" v-model="patient.urinaryDistillation">未拔出导尿管
        </p>
        
        <p>
          <strong style="color: red;">其他并发症：</strong>
          <input type="radio" id="complication-delirium-no" name="complicationStatus" value="无" v-model="patient.complications">无
          <input type="radio" id="complication-delirium-yes" name="complicationStatus" value="有" v-model="patient.complications">有
        </p>
        <p>
          <input type="checkbox" id="vascular-bruise" name="vascularIssues" value="动、静脉穿刺部位血肿" v-model="patient.vascularIssues">动、静脉穿刺部位血肿
          <input type="checkbox" id="vascular-catheter-fall" name="vascularIssues" value="动、静脉置管脱落" v-model="patient.vascularIssues">动、静脉置管脱落
          <input type="checkbox" id="vascular-upper-gi-bleeding" name="vascularIssues" value="上消化道出血" v-model="patient.vascularIssues">上消化道出血
          <input type="checkbox" id="vascular-upper-respiratory-bleeding" name="vascularIssues" value="上呼吸道出血" v-model="patient.vascularIssues">上呼吸道出血
        </p>
        <p>
          <input type="checkbox" id="severe-neurological-complications" name="neuroComplications" value="椎管内麻醉后严重神经并发症" v-model="patient.neuroComplications">椎管内麻醉后严重神经并发症
          <input type="checkbox" id="hoarseness-after-extubation" name="neuroComplications" value="全麻气管插管拔管后声音嘶哑" v-model="patient.neuroComplications">全麻气管插管拔管后声音嘶哑
          <input type="checkbox" id="new-coma" name="neuroComplications" value="麻醉后新发昏迷" v-model="patient.neuroComplications">麻醉后新发昏迷
        </p>
        <p>
          <input type="checkbox" id="unexpected-awareness" name="awarenessIssues" value="麻醉中发生未预期的意识障碍" v-model="patient.awarenessIssues">麻醉中发生未预期的意识障碍
          <input type="checkbox" id="death-within-24h" name="awarenessIssues" value="麻醉开始后24小时内死亡" v-model="patient.awarenessIssues">麻醉开始后24小时内死亡
          <input type="checkbox" id="cardiac-arrest-within-24h" name="awarenessIssues" value="麻醉开始后24小时内心跳骤停" v-model="patient.awarenessIssues">麻醉开始后24小时内心跳骤停
          <input type="checkbox" id="special-case" name="awarenessIssues" value="特殊情况" v-model="patient.awarenessIssues">特殊情况
        </p>

        <p>
          <strong>术后镇痛：</strong>
          <input type="radio" id="postop-pain-no" name="postopPain" value="无" v-model="patient.postopPain">无
          <input type="radio" id="postop-pain-yes" name="postopPain" value="有" v-model="patient.postopPain">有
        </p>

        <br>
        
        <p><strong>术后疼痛评估：</strong></p>
        <!-- &nbsp; x10 -->
        <p>
          <span style="color: red;">VAS评分（静息）：</span>
          <select id="vas-rest" name="vasRest" v-model="patient.vasRest" style="width: 70px; height: 22px; margin-right: 72px;">
            <option value="" disabled selected>请选择</option>
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
            <option value="6">6</option>
            <option value="7">7</option>
            <option value="8">8</option>
            <option value="9">9</option>
            <option value="10">10</option>
          </select>
          <span style="color: red;">VAS评分（活动）：</span>
          <select id="vas-activity" name="vasActivity" v-model="patient.vasActivity" style="width: 70px; height: 22px; margin-right: 72px;">
            <option value="" disabled selected>请选择</option>
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
            <option value="6">6</option>
            <option value="7">7</option>
            <option value="8">8</option>
            <option value="9">9</option>
            <option value="10">10</option>
          </select>
          <span style="color: red;">患者满意度：</span>
          <select id="satisfaction" name="satisfaction" v-model="patient.satisfaction" style="width: 70px; height: 22px; margin-right: 0px;">
            <option value="" disabled selected>请选择</option>
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
            <option value="6">6</option>
            <option value="7">7</option>
            <option value="8">8</option>
            <option value="9">9</option>
            <option value="10">10</option>
          </select>
        </p>

        <p style="color: red;">
          <span style="color: red;">恶心：</span>
          <input type="text" v-model="patient.nausea" placeholder="请输入内容" style="width: 200px; margin-right: 5px;">
          <span style="color: red;">呕吐：</span>
          <input type="text" v-model="patient.vomiting" placeholder="请输入内容" style="width: 200px; margin-right: 5px;">
          <span style="color: red;">瘙痒：</span>
          <input type="text" v-model="patient.itching" placeholder="请输入内容" style="width: 200px; margin-right: 0px;">
        </p>
            
        <p>
          <strong style="color: red;">其他情况及处理：</strong>
          <input type="radio" id="situation-no" name="otherCondition" value="无" v-model="patient.otherCondition">无
          <input type="radio" id="situation-yes" name="otherCondition" value="有" v-model="patient.otherCondition">有
        </p>
        <p>
          <textarea id="situation-details" 
                    placeholder="请输入其他情况或处理" 
                    v-model="patient.otherConditionDetails" 
                    style="width: 100%; 
                          height: 34px;
                          padding: 8px; 
                          box-sizing: border-box; 
                          resize: vertical; 
                          max-height: 200px; 
                          min-height: 34px;"></textarea>
        </p>

        <p>
          <span>麻醉医生签名：</span>
          <input type="text" v-model="anesthesiologistSignature" placeholder="请输入签名" style="width: 100px; margin-right: 50px;">
          <span>随访者：</span>
          <input type="text" v-model="follower" placeholder="请输入随访者" style="width: 100px; margin-right: 50px;">
          <span style="color: red;">随访日期：</span>
          <el-date-picker
            v-model="followUpDateTime"
            type="datetime"
            placeholder="选择日期时间"
            size="mini"
            align="right"
            :picker-options="pickerOptions">
          </el-date-picker>
        </p>
        <p style="text-align: center">
          <el-button @click="back2main">结束随访</el-button>
          <el-button @click="go2deepseek">跳转至DeepSeek</el-button>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../api';

export default {
  name: 'Report',
  data() {
    return {
      patient: {
        department: "", // 科室
        bedNumber: "", // 床号
        name: "", // 姓名
        age: "", // 年龄
        gender: "", // 性别
        hospitalNumber: "", // 住院号
        diagnosis: "", // 主要诊断
        surgery: "", // 实施手术名称
        anesthesia: '', // 麻醉方式

        temperature: '', // 体温
        respiratoryRate: '', // 呼吸频率
        pulseRate: '', // 脉搏
        bloodPressure: '', // 血压

        consciousness: [], // 意识状态

        dizziness: '', // 头晕
        cardiovascular: '', // 心血管体征状态
        respiration: '', // 呼吸状态
        
        throatPain: '', // 咽喉痛
        headache: '', // 头痛
        cognitiveImpairment: '', // 认知障碍

        blurryVision: '', // 视物模糊
        intraoperativeAwareness: '', // 术中知晓
        urinaryDistillation: '', // 尿蒸馏

        complications: '', // 其他并发症

        vascularIssues: [], // 血管问题
        neuroComplications: [], // 神经并发症
        awarenessIssues: [], // 意识问题

        postopPain: '', // 术后镇痛

        vasRest: '', // VAS 分数（静息）
        vasActivity: '', // VAS 分数（活动）

        nausea: '', // 恶心
        vomiting: '', // 呕吐
        itching: '', // 瘙痒
        satisfaction: '', // 患者满意度

        otherCondition: '', // 其他情况及处理
        otherConditionDetails: '' // 其他情况或处理的详细信息
      },
      anesthesiologistSignature: '', // 麻醉医生签名
      follower: '', // 随访者
      pickerOptions: {
        shortcuts: [{
          text: '今天',
          onClick(picker) {
            picker.$emit('pick', new Date());
          }
        }, {
          text: '昨天',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24);
            picker.$emit('pick', date);
          }
        }, {
          text: '一周前',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
            picker.$emit('pick', date);
          }
        }]
      },  
      followUpDateTime: '', //随访日期和时间
    };
  },

  // patient1.json 在前端
  // mounted() {
  //   this.fetchPatientData();
  // },
  // methods: {
  //   fetchPatientData() {
  //     // 在 Vue 项目中，public 文件夹通常用于存放静态资源，这些资源可以通过相对路径直接访问。这里的 /patient_report.json 是相对于项目根目录的路径。
  //     // 当 Vue 应用运行时，开发服务器会将这个路径映射到 public 文件夹下的 patient_report.json 文件。
  //     axios.get('/patient1.json')
  //       .then(response => {
  //         this.patient = response.data.patient; // 根据 JSON 结构更新 patient 数据
  //         this.anesthesiologistSignature = response.data.anesthesiologistSignature;
  //         this.follower = response.data.follower;
  //         this.followUpDateTime = response.data.followUpDateTime;
  //       })
  //       .catch(error => {
  //         console.error('获取数据失败', error);
  //       });
  //   }
  // },

  methods: {
    back2main(){
      this.$router.push('/standby');
    },
    go2deepseek() {
      window.location.href = 'http://127.0.0.1:8081/#/main';
    },
    getPatientData() {
      axios.get('/send_patient_data') // Flask 服务器运行端口
        .then(response => {
          this.patient = response.data.patient;
          this.anesthesiologistSignature = response.data.anesthesiologistSignature;
          this.follower = response.data.follower;
          this.followUpDateTime = response.data.followUpDateTime;
        })
        .catch(error => {
          console.error('获取数据失败', error);
        });
    }
  },
  mounted() {
    this.getPatientData();
  }
};
</script>

<style scoped>
.A4 {
  display: flex;
  justify-content: center; /* 水平居中 */
  /* align-items: flex-start; 垂直居中 */
  /* height: 297mm; 占满整个视口高度 */
  /* margin: 0; 去掉默认的边距 */
  background-color: #ffffff; /* 背景色 */
}

.report {
  width: 210mm; /* A4 纸宽度 */
  height: 297mm; /* A4 纸高度 */
  background-color: white; /* 纸张背景色 */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  padding: 24px; /* 内边距 */
  overflow: hidden; /* 防止内容溢出 */
  position: relative; /* 相对定位 */
  box-sizing: border-box; /* 包含内边距和边框 */
}

.content {
  text-align: left; /* 左对齐文本 */
}

.content p {
  font-size: 12px;
  color: #000000; /* 设置段落颜色 */
}

.el-row {
  margin-bottom: 0;
  /* &:last-child {
    margin-bottom: 0;
  } */
}
.el-col {
  border-radius: 0;
}
.grid-content {
  font-size: 12px;
  color: #000000;
}

.content input[type="text"]{
  height: 16px;
  font-size: 12px;
  color: #000000;
}
</style>
