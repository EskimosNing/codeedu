<template>
    <div class="historyContainer">
        <div
          v-for="(dialogue, index) in Dialogues"
          :key="index"
          class="list-item"
          :class="{ 'active': selectedDialogue === dialogue }"
          @click="selectDialogue(dialogue)"
        >
            <span class="text">{{dialogue[0]['content']}}</span>
        </div>
    </div>
</template>

<script>
export default{
    props: {
        Dialogues: {
            type: Array,
            required: true
        },
        currentDialogue: {
            type: Array,
        }
    },
    data() {
    return {
        selectedDialogue: null // 控制侧边栏是否收缩
    };
  },
    mounted() {
        this.selectedDialogue = this.currentDialogue
    },
    methods: {
        selectDialogue(dialogue){
            this.selectedDialogue = dialogue
            this.$emit('child-event',{
                message: dialogue,
            })
        }
    }
}
</script>

<style scoped>
.list-item {
    transition: all 0.3s;
    margin-left: 15px;
    padding: 9px 13px;
    margin-bottom: 1px;
    font-weight: bold;
    color: #ecf0f1;
    cursor: pointer;
    border-radius: 10px;
    width: 230px;        /* 固定宽度（略小于侧边栏宽度）*/
    box-sizing: border-box; /* 防止尺寸溢出 */
    
    /* 文本溢出处理 */
    overflow: hidden;    /* 隐藏溢出内容 */
    white-space: nowrap; /* 禁止换行 */
    
    /* 文本对齐优化 */
    display: flex;
    align-items: flex-start; /* 居左 */
}

.text {
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
}

.list-item:hover {
    background-color: #343434;
}

.list-item.active {
  background: #494949;
}
</style>
