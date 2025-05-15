import VueRouter from "vue-router";
import Vue from "vue";
import Chatbot from "../components/Chatbot.vue"
import Test from "../components/test.vue"
import Try from "../components/try.vue"
import Main from "../components/Main.vue"
import Report from "../components/ReportComponent.vue"
import Standby from "../components/standby.vue"
import Camera from "../components/camera.vue"
import Aside from "../components/History.vue"

Vue.use(VueRouter)

const router = new VueRouter({
    routes:[
        {path:'/',redirect:'/main'},
        {path:'/chatbot', component:Chatbot},
        {path:'/test', component:Test},
        {path:'/try', component: Try},
        {path:'/main', component: Main},
        {path:'/report', component: Report},
        {path:'/standby', component: Standby},
        {path:'/camera', component: Camera},
    ]
})

export default router