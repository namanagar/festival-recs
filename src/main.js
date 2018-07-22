import Vue from 'vue'
import App from './App.vue'
var VueFire = require("vuefire");
Vue.use(VueFire);

new Vue({
  el: '#app',
  render: h => h(App)
})
