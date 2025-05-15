<template>
    <div class="container">
        <div class="main">
            <div class="main-aside" v-if="!isCollapsed">
                
                <history/>
            </div>
            <div class="main-main">
                <chatbot/>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .container{
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .main{
        flex: 1;
        width: 100%;
        display: flex;
        flex-direction: row;
    }
    .main-aside{
        flex: 0 0 17%;
        height: 100%;
        background-color: #202327;
    }
    .main-main{
        flex: 1;
        height: 100%;
        background-color: #2a2a2e;
    }
    .el-icon-user-solid{
        font-size: 25px;
    }
    #patient-icon{
        color: black;
    }
    #patient-icon:hover {
        color: #66b1ff;
    }
</style>

<script>
import Chatbot from "./Chatbot.vue"
import Info from "./Info.vue"
import Test from "./test.vue"
import History from "./History.vue"
export default {
    components:{
        Chatbot,
        Info,
        Test,
        History
    },
  data() {
    return {
      isCollapsed: false // 控制侧边栏是否收缩
    };
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed; // 切换收缩状态
    }
  }
};
</script>