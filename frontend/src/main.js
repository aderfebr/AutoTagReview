import { createApp } from 'vue'
import App from './App.vue'
import VueParticles from 'vue-particles'
import { createRouter,createWebHashHistory } from 'vue-router'
import 'font-awesome/css/font-awesome.min.css'

const router = createRouter({
    history: createWebHashHistory(),
    routes:[
        { path: '/', component: ()=> import('./components/Data.vue') },
        { path: '/data/product', component: ()=> import('./components/Product.vue') },
        { path: '/data/review', component: ()=> import('./components/Review.vue') },
        { path: '/tag/single', component: ()=> import('./components/Single.vue') },
        { path: '/tag/batch', component: ()=> import('./components/Batch.vue') },
        { path: '/tag/file', component: ()=> import('./components/File.vue') },
        { path: '/tag/history', component: ()=> import('./components/TagHistory.vue') },
        { path: '/tag/visualization', component: ()=> import('./components/Visualization.vue') },
    ]
})

const app=createApp(App)
app.use(VueParticles)
app.use(router)
app.mount('#app')
