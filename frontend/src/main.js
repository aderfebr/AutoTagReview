import { createApp } from 'vue'
import App from './App.vue'
import VueParticles from 'vue-particles'
import { createRouter,createWebHashHistory } from 'vue-router'
import 'font-awesome/css/font-awesome.min.css'

const router = createRouter({
    history: createWebHashHistory(),
    routes:[
        { path: '/', component: ()=> import('./components/Home.vue') },
        { path: '/data/product', component: ()=> import('./components/Product.vue') },
        { path: '/data/review', component: ()=> import('./components/Review.vue') },
        { path: '/classification/compare', component: ()=> import('./components/Compare.vue') },
        { path: '/classification/profile', component: ()=> import('./components/Profile.vue') },
        { path: '/classification/recommend', component: ()=> import('./components/Recommend.vue') },
        { path: '/tag/single', component: ()=> import('./components/Single.vue') },
        { path: '/tag/batch', component: ()=> import('./components/Batch.vue') },
        { path: '/tag/file', component: ()=> import('./components/File.vue') },
        { path: '/tag/history', component: ()=> import('./components/Taghistory.vue') },
        { path: '/tag/visualization', component: ()=> import('./components/Visualization.vue') },
    ]
})

const app=createApp(App)
app.use(VueParticles)
app.use(router)
app.mount('#app')
