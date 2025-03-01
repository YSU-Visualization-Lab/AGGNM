import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// 引入element-ui
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
// 引入全局样式
import '@/assets/global.less';
// 引入axios
import axios from '@/api/ajax.js'

Vue.config.productionTip = false
Vue.use(ElementUI) // 使用element-ui
Vue.prototype.$axios = axios // 配置axios全局使用

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
