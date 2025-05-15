import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import "element-ui/lib/theme-chalk/index.css"
import router from "./router/index.js"
import store from "./store"
import './assets/scrollbar.css'

Vue.config.productionTip = false
Vue.use(ElementUI)

new Vue({
  render: h => h(App),
  store,
  router: router,
}).$mount('#app')
