import VueRouter from "vue-router";
import Vue from "vue";
import Login from "../components/Login.vue";
import Main from "../components/Main.vue"
import Chatbot from "../components/Chatbot.vue"
import Coding from "../components/Coding.vue";

Vue.use(VueRouter)

const router = new VueRouter({
    routes:[
        {path: '/', redirect: '/login'},
        {path:'/login', component: Login},
        {path:'/main', component: Main},
        {path:'/chatbot', component:Chatbot},
        {path:'/coding', component: Coding},
    ]
})

export default router