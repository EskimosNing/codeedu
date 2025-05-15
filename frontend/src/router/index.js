import VueRouter from "vue-router";
import Vue from "vue";
import Main from "../components/Main.vue"
import Try from "../components/try.vue"
import Chatbot from "../components/Chatbot.vue"
import Login from "../components/Login.vue";
import Coding from "../components/Coding.vue";
import Try1 from "../components/try1.vue"

import Report from "../components/ReportComponent.vue"
import Camera from "../components/camera.vue"
import Test from "../components/test.vue"
import Standby from "../components/standby.vue"

Vue.use(VueRouter)

const router = new VueRouter({
    routes:[
        {path:'/',redirect:'/main'},
        {path:'/main', component: Main},
        {path:'/try', component: Try},
        {path:'/chatbot', component:Chatbot},
        {path:'/login', component: Login},
        {path:'/coding', component: Coding},
        {path:'/try1', component: Try1},

        {path:'/report', component: Report},
        {path:'/camera', component: Camera},
        {path:'/test', component:Test},
        {path:'/standby', component: Standby},
    ]
})

export default router