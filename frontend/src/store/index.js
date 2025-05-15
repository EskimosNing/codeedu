// store/index.js
import Vue from 'vue';
import Vuex from 'vuex';

// 告诉Vue使用Vuex插件
Vue.use(Vuex);

// 创建一个新的store实例
const store = new Vuex.Store({
  state: {
    reportGeneration: false,
  },
  mutations: {
      update (state, temp){
        state.reportGeneration = temp;
      },
    // 根状态的改变方法
  },
  actions: {
    // 异步操作和复杂的同步操作
  },
  getters: {
    // 计算属性
  },
  modules: {
    // 模块化管理状态
  }
});

export default store;