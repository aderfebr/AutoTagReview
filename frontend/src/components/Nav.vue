<template>
  <ul>
    <li :id="$route.path === '/' ? 'selected' : ''">
      <router-link to="/"><i class="fa fa-home"/>&ensp;首页</router-link>
    </li>
    <li :id="$route.path === '/data' ? 'selected' : ''">
      <router-link to="/data"><i class="fa fa-archive" />&ensp;数据展示</router-link>
    </li>
    <li :id="$route.path === '/compare' ? 'selected' : ''">
      <router-link to="/compare"><i class="fa fa-code" />&ensp;算法比较</router-link>
    </li>
    <li :id="$route.path === '/device' ? 'selected' : ''">
      <router-link to="/device"><i class="fa fa-tag"/>&ensp;标签生成</router-link>
    </li>
    <li :id="$route.path === '/security' ? 'selected' : ''">
      <router-link to="/security"><i class="fa fa-search"/>&ensp;相关推荐</router-link>
    </li>
  </ul>
</template>

<script setup>
import { useRoute } from 'vue-router'

const $route = useRoute()
</script>


<style scoped>
ul {
  list-style: none;
}

li {
  margin: 15px 0;
  padding: 10px 20px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

li:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

li#selected {
  background-color: rgba(0, 0, 0, 0.2);
  border-left: 4px solid #ff5f5f;
}

a {
  color: white;
  text-decoration: none;
  font-size: 20px;
  display: flex;
  align-items: center;
}

i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
}
</style>