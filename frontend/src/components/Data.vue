<template>
  <div id="main">
    <div id="left">
      <Nav></Nav>
    </div>
    
    <div id="right">
      <div id="top">
        <div class="top-content">
          <h1><i class="fa fa-archive"></i> 数据展示</h1>
          <button id="add" @click="add()">
            <i class="fa fa-plus"></i> 添加评论
          </button>
        </div>
      </div>
      
      <div class="content-section product-section">
        <div id="product-container">
          <div id="product-image">
            <img src="./1.jpg" alt="产品图片">
          </div>
          <div id="product-details">
            <h2>牧马人 M6机甲可充电无线鼠标蓝牙双模静音游戏电竞外接电脑网吧笔记本电脑台式吃鸡竞技外设 M6机甲风【无线2.4G静音版】</h2>
            <div id="product-thumbnails">
              <img src="./2.jpg" alt="产品细节1">
              <img src="./3.jpg" alt="产品细节2">
            </div>
          </div>
        </div>
      </div>
      
      <div class="content-section review-section">
        <div id="reviews-header">
          <h3><i class="fa fa-comments"></i> 商品评论</h3>
          <div class="section-divider"></div>
        </div>
        
        <div id="reviews-container">
          <div class="review-card">
            <div class="review-header">
              <span class="user-avatar" style="background-color: #FF9AA2;">A</span>
              <span class="user-name">用户A</span>
              <span class="review-date">2023-05-15</span>
            </div>
            <p class="review-text">挺好用的 外观也好看 这是第二次买了 我很喜欢 续航时间也挺久的 鼠标很轻 静音 一分价钱一分货 质量就是没得说 物流也很快 没让我失望 推荐大家</p>
            <div class="review-tags">
              <span class="tag">外观漂亮</span>
              <span class="tag">续航持久</span>
              <span class="tag">静音设计</span>
            </div>
          </div>
          
          <div class="review-divider"></div>
          
          <div class="review-card">
            <div class="review-header">
              <span class="user-avatar" style="background-color: #FFB7B2;">B</span>
              <span class="user-name">用户B</span>
              <span class="review-date">2023-05-10</span>
            </div>
            <p class="review-text">看上这款鼠标很久了，我的小鼠标也不给力。首先从颜色到款式都是很喜欢。快递也好快。但是它是充电口。希望可以用的久一点。喜欢他，爱了爱了。可是没有给我赠送鼠标垫。</p>
            <div class="review-tags">
              <span class="tag">快递迅速</span>
              <span class="tag">款式新颖</span>
            </div>
          </div>
          
          <div class="review-divider"></div>
          
          <div class="review-card">
            <div class="review-header">
              <span class="user-avatar" style="background-color: #FFDAC1;">C</span>
              <span class="user-name">用户C</span>
              <span class="review-date">2023-05-05</span>
            </div>
            <p class="review-text">
              耐用度：续航很不错，好评<br>
              响应速度：反应很快，DPI可调节<br>
              便携度：蓝牙连接，很方便<br>
              外观颜值：灯带很酷，不刺眼
            </p>
            <div class="review-tags">
              <span class="tag">响应迅速</span>
              <span class="tag">蓝牙连接</span>
              <span class="tag">灯光效果</span>
            </div>
          </div>
          
          <div class="review-divider"></div>
          
          <div class="review-card">
            <div class="review-header">
              <span class="user-avatar" style="background-color: #E2F0CB;">D</span>
              <span class="user-name">用户D</span>
              <span class="review-date">2023-05-01</span>
            </div>
            <p class="review-text">握持感非常舒服，看着也特别精致，用起来还没有声音，不会打扰到女朋友，这个价格非常良心了，非常满意的一次购物</p>
            <div class="review-tags">
              <span class="tag">握感舒适</span>
              <span class="tag">性价比高</span>
              <span class="tag">静音设计</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Nav from './Nav.vue';
</script>

<style scoped>
/* 基础设置 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  line-height: 1.6;
  color: #333;
}

#main {
  position: relative;
  height: 100vh;
  display: flex;
}

/* 左侧导航栏 */
#left {
  flex: 0 0 220px;
  background: linear-gradient(135deg,rgba(0, 139, 189, 0.7),rgba(80, 0, 192, 0.7));
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  padding: 20px 0;
  z-index: 10;
}

#right {
  flex: 1;
  background: linear-gradient(to bottom, rgba(230, 235, 245, 0.5), rgba(220, 225, 240, 0.5));
  overflow-y: auto;
  padding-bottom: 30px;
}

/* 顶部区域 */
#top {
  padding: 30px 30px;
  background: rgba(180, 240, 210, 0.15);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
  margin-bottom: 20px;
  position: relative;
  z-index: 5;
}

.top-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

#top h1 {
  font-size: 32px;
  color: #4a6fa5;
  display: flex;
  align-items: center;
  margin: 0;
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

#top h1 i {
  margin-right: 10px;
}

/* 内容区块样式 */
.content-section {
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
  margin: 0 20px 20px;
  overflow: hidden;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  transition: all 0.3s ease;
  border: 1px solid rgba(0,0,0,0.05);
  transform: translateY(-2px);
}

.product-section {
  background: rgba(180, 210, 240, 0.15);
}

.review-section {
  background: rgba(240, 180, 210, 0.15);
}

.section-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(200, 210, 220, 0.3), transparent);
  margin: 10px 30px;
}

/* 产品展示区 */
#product-container {
  display: flex;
  padding: 30px;
  gap: 30px;
}

#product-image img {
  width: 220px;
  height: 220px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0,0,0,0.1);
}

#product-details {
  flex: 1;
}

#product-details h2 {
  font-size: 20px;
  margin-bottom: 20px;
  color: #333;
  line-height: 1.4;
}

#product-thumbnails {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

#product-thumbnails img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid rgba(200, 210, 220, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
}

#product-thumbnails img:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 评论标题 */
#reviews-header {
  padding: 20px 30px 10px;
}

#reviews-header h3 {
  font-size: 18px;
  color: #4a6fa5;
  display: flex;
  align-items: center;
  margin: 0;
}

#reviews-header h3 i {
  margin-right: 10px;
}

/* 评论容器 */
#reviews-container {
  padding: 0 30px 20px;
}

.review-card {
  padding: 20px 0;
  transition: all 0.3s ease;
  border-radius: 8px;
  padding: 15px;
  margin: 0 -15px;
}

.review-card:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  margin-right: 12px;
}

.user-name {
  font-weight: 600;
  margin-right: 12px;
}

.review-date {
  color: #6c757d;
  font-size: 13px;
}

.review-divider {
  height: 1px;
  background: #ddd;
  margin: 15px 0;
}

.review-text {
  font-size: 15px;
  line-height: 1.7;
  margin-bottom: 12px;
  color: #333;
}

.review-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag {
  background-color: rgba(200, 220, 240, 0.6);
  color: #1976d2;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

/* 按钮样式 */
button {
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  display: flex;
  align-items: center;
}

button#add {
  background: linear-gradient(to right, #218838, #4cae4c);
  color: white;
  font-size: 18px;
  box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
}

button#add:hover {
  background: linear-gradient(to right, #218838, #4cae4c);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
}

button#add i {
  margin-right: 8px;
}

div::-webkit-scrollbar {
  width: 10px;
}

div::-webkit-scrollbar-thumb {
  border-radius: 10px;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);
  background: rgba(180, 180, 180, 0.6);
}

div::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.05);
  border-radius: 0;
  background: rgba(200, 200, 200, 0.3);
}
</style>