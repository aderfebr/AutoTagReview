import { createApp } from 'vue'
import App from './App.vue'
import VueParticles from 'vue-particles'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { createRouter,createWebHashHistory } from 'vue-router'
import 'font-awesome/css/font-awesome.min.css'

const router = createRouter({
    history: createWebHashHistory(),
    routes:[
        { path: '/', component: ()=> import('./components/Home.vue') },
        { path: '/data', component: ()=> import('./components/Data.vue') },
        { path: '/compare', component: ()=> import('./components/Compare.vue') },
    ]
})

const app=createApp(App)
app.use(VueParticles)
app.use(router)
app.use(VueAxios,axios)
app.mount('#app')
