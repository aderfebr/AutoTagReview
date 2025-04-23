<template>
  <div class="nav-container">
    <ul class="main-menu">
      <li :class="{ 'active-menu': $route.path === '/' }">
        <router-link to="/" class="menu-head">
          <i class="fa fa-home"/>&ensp;首页
        </router-link>
      </li>
      <li 
        :class="{ 
          'expanded': expandedMenu === 'data',
          'active-menu': $route.path.startsWith('/data')
        }" 
        class="has-submenu"
      >
        <div class="menu-head" @click="toggleMenu('data')">
          <i class="fa fa-archive" />&ensp;数据展示
          <i class="fa fa-angle-down arrow" />
        </div>
        <ul class="submenu">
          <li :class="{ 'active-submenu': $route.path === '/data/product' }">
            <router-link to="/data/product">产品数据</router-link>
          </li>
          <li :class="{ 'active-submenu': $route.path === '/data/review' }">
            <router-link to="/data/review">评论数据</router-link>
          </li>
        </ul>
      </li>
      <li 
        :class="{ 
          'expanded': expandedMenu === 'label',
          'active-menu': $route.path.startsWith('/label')
        }" 
        class="has-submenu"
      >
        <div class="menu-head" @click="toggleMenu('label')">
          <i class="fa fa-search"/>&ensp;问题分类
          <i class="fa fa-angle-down arrow" />
        </div>
        <ul class="submenu">
          <li :class="{ 'active-submenu': $route.path === '/label/compare' }">
            <router-link to="/label/compare">算法比较</router-link>
          </li>
          <li :class="{ 'active-submenu': $route.path === '/label/history' }">
            <router-link to="/label/history">历史记录</router-link>
          </li>
        </ul>
      </li>
      <li 
        :class="{ 
          'expanded': expandedMenu === 'tag',
          'active-menu': $route.path.startsWith('/tag')
        }" 
        class="has-submenu"
      >
        <div class="menu-head" @click="toggleMenu('tag')">
          <i class="fa fa-tag" />&ensp;标签生成
          <i class="fa fa-angle-down arrow" />
        </div>
        <ul class="submenu">
          <li :class="{ 'active-submenu': $route.path === '/tag/single' }">
            <router-link to="/tag/single">单条分析</router-link>
          </li>
          <li :class="{ 'active-submenu': $route.path === '/tag/batch' }">
            <router-link to="/tag/batch">批量分析</router-link>
          </li>
          <li :class="{ 'active-submenu': $route.path === '/tag/file' }">
            <router-link to="/tag/file">文件分析</router-link>
          </li>
          <li :class="{ 'active-submenu': $route.path === '/tag/history' }">
            <router-link to="/tag/history">历史记录</router-link>
          </li>
          <li :class="{ 'active-submenu': $route.path === '/tag/visualization' }">
            <router-link to="/tag/visualization">数据可视化</router-link>
          </li>
          <li :class="{ 'active-submenu': $route.path === '/tag/recommendation' }">
            <router-link to="/tag/recommendation">相关推荐</router-link>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const expandedMenu = ref(null)

const toggleMenu = (menu) => {
  expandedMenu.value = expandedMenu.value === menu ? null : menu
}
</script>

<style scoped>
.main-menu {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
}

.main-menu > li {
  position: relative;
  width: 100%;
}

.main-menu > li > .menu-head {
  color: #2c3e50;
  text-decoration: none;
  font-size: 18px;
  display: flex;
  align-items: center;
  padding: 12px 20px;
  transition: all 0.3s ease;
  width: 100%;
  box-sizing: border-box;
  cursor: pointer;
  position: relative;
}

.main-menu > li > .menu-head:hover {
  color: #1a73e8;
  background-color: #e1f5fe;
}

.main-menu > li > a.menu-head {
  text-decoration: none;
  display: flex;
  align-items: center;
  padding: 12px 20px;
}

.has-submenu .arrow {
  margin-left: auto;
  transition: transform 0.3s ease;
}

.has-submenu.expanded .arrow {
  transform: rotate(180deg);
}

.submenu {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.has-submenu.expanded .submenu {
  max-height: 300px;
}

.submenu li a {
  color: #0277bd;
  text-decoration: none;
  font-size: 16px;
  display: block;
  padding: 10px 20px 10px 50px;
  transition: all 0.2s ease;
  position: relative;
}

.submenu li a:hover {
  color: #01579b;
  background-color: #e1f5fe;
}

.submenu li .router-link-active {
  color: #01579b;
  font-weight: 500;
  background-color: #e1f5fe;
}

/* Active menu styles */
.main-menu > li.active-menu > .menu-head {
  border-left: 4px solid #1a73e8;
  padding-left: 16px; /* Adjust padding to account for border */
  background-color: #e1f5fe;
  color: #1a73e8;
}

.main-menu > li.active-menu > .menu-head > i {
  color: #1a73e8;
}

.submenu li.active-submenu a {
  border-left: 4px solid #1a73e8;
  padding-left: 46px; /* 50px - 4px border */
  background-color: #e1f5fe;
  color: #01579b;
  font-weight: 500;
}

i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
  color: #0288d1;
}

.main-menu > li > .menu-head:hover > i,
.has-submenu.expanded > .menu-head > i {
  color: #01579b;
}
</style>