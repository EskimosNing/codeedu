<template>
    <div class="container" @click="gotomain">
        <div class="gif-container"> 
            <img src="../assets/gif3.gif">
        </div>
    </div>
</template>

<script>
import axios from "../api";
export default {
    data() {
        return {
        currentIndex: 0,
        gifs: [
            '../assets/gif3.gif',
            '../assets/gif2.gif'
            ]
        }
  },
    computed: {
        currentGif() {
            return this.gifs[this.currentIndex];
        }
    },
    mounted() {
        this.startGifSwitcher();
    },
  methods: {
    startGifSwitcher() {
        setInterval(() => {
            this.currentIndex = (this.currentIndex + 1) % this.gifs.length;
        }, 3000); // 每3秒切换一次
    },
    gotomain(){
        // axios.get('/reportGeneration')
        // .then(response => {
        //   if(response.status == 200){
        //     console.log("test")
        //   }
        //   else{
        //     alert("网络出现问题！")
        //   }
        // })
        this.$router.push('/main');
    }
  }
};
</script>

<style scoped>
.container{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    color: #fff;
}
.gif-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(1);
}
.gif-container img {
    display: block;
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
}
</style>