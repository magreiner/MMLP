import '@babel/polyfill'
import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import store from './store/index.js'
import './registerServiceWorker'
import Navigation from '@/modules/navigation'
// import dataRadioList from '@/components/dataRadioList'
// import dataExplorer from '@/components/dataExplorer'
// import Trend from 'vuetrend'
// import VeeValidate from 'vee-validate'
// import VueJsonPretty from 'vue-json-pretty'

Vue.config.productionTip = false
Vue.component('app-navigation', Navigation)
// Vue.component('dataRadioList', dataRadioList)
// Vue.component('dataExplorer', dataExplorer)
// Vue.component('trend', Trend)
// Vue.component('veeValidate', VeeValidate)
// Vue.component('vue-json-pretty', VueJsonPretty)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
