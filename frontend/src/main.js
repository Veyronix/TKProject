import Vue from 'vue'
import Vuelidate from 'vuelidate'
import Vuetify from 'vuetify/lib'
import '@mdi/font/css/materialdesignicons.css'
import router from './router'
import App from './App.vue'

Vue.config.productionTip = false

Vue.use(Vuetify)
Vue.use(Vuelidate)

new Vue({
  vuetify: new Vuetify({
    icons: {
      iconfont: 'mdi',
    },
  }),
  router,
  render: h => h(App),
}).$mount('#app')
