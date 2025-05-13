<template>
  <div id="main">
    <Title></Title>
    <Nav></Nav>

    <div id="right">
      <div class="content-section dashboard-section">
        <div class="dashboard-header">
          <h2><i class="fa fa-dashboard"></i> 系统概览</h2>
        </div>

        <div class="stats-container">
          <div class="stat-card" style="--card-color: #6366F1;">
            <div class="stat-icon">
              <i class="fa fa-cubes"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">300</div>
              <div class="stat-label">产品条目</div>
            </div>
          </div>

          <div class="stat-card" style="--card-color: #10B981;">
            <div class="stat-icon">
              <i class="fa fa-comments"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">67,125</div>
              <div class="stat-label">评论条目</div>
            </div>
          </div>

          <div class="stat-card" style="--card-color: #F59E0B;">
            <div class="stat-icon">
              <i class="fa fa-tags"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">772</div>
              <div class="stat-label">问题类别</div>
            </div>
          </div>

          <div class="stat-card" style="--card-color: #3B82F6;">
            <div class="stat-icon">
              <i class="fa fa-line-chart"></i>
            </div>
            <div class="stat-content">
              <div class="stat-value">5</div>
              <div class="stat-label">分析方法</div>
            </div>
          </div>
        </div>

        <div class="dashboard-divider"></div>

        <div class="content-row">
          <div class="hot-questions card-style">
            <div class="card-header" style="--header-color: #EC4899;">
              <h3><i class="fa fa-fire"></i> 问题类别</h3>
            </div>
            <ul class="question-list">
              <li v-for="(question, index) in hotQuestions" :key="'question-'+index" class="question-item">
                <span class="question-rank" :style="{ backgroundColor: rankColors[index] }">{{ index + 1 }}</span>
                <span class="question-text">{{ question.text }}</span>
              </li>
            </ul>
          </div>

          <div class="hot-tags card-style">
            <div class="card-header" style="--header-color: #8B5CF6;">
              <h3><i class="fa fa-tag"></i> 热门标签</h3>
              <div class="card-actions">
              </div>
            </div>
            <div class="tag-cloud">
              <span 
                v-for="(tag, index) in hotTags" 
                :key="'tag-'+index" 
                class="tag-item"
                :style="{
                  color: 'white',
                  backgroundColor: tagColors[index % tagColors.length],
                  opacity: 0.8 + tag.weight * 0.2,
                }"
              >
                {{ tag.text }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Nav from './Nav.vue';
import Title from './Title.vue';

// 热门问题数据
const hotQuestions = ref([
  { text: '上手简单', count: 1245 },
  { text: '空间大', count: 987 },
  { text: '效果显著', count: 876 },
  { text: '即插即用', count: 765 },
  { text: '穿着无压力', count: 654 },
  { text: '购物体验好', count: 543 },
  { text: '效果差', count: 432 },
  { text: '包装舒服', count: 321 }
])

// 热门标签数据
const hotTags = ref([
  { text: '产品品质保证'},
  { text: '配送速度快'},
  { text: '服务态度好'},
  { text: '回购意愿强'},
  { text: '品牌可信度高'},
  { text: '推荐意愿强烈'},
  { text: '价格公道'},
  { text: '商家服务热忱'},
  { text: '性价比高'},
  { text: '细节完美'},
  { text: '售后靠谱'}
])

// 颜色系统
const tagColors = ref([
  '#6366F1', '#EC4899', '#10B981', '#F59E0B',
  '#3B82F6', '#8B5CF6', '#EF4444', '#14B8A6',
  '#F97316', '#8B5CF6', '#EC4899', '#3B82F6'
])

const rankColors = ref([
  '#EF4444', '#F59E0B', '#F59E0B', '#10B981',
  '#10B981', '#3B82F6', '#3B82F6', '#8B5CF6'
])
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
  background-color: #f8fafc;
}

#main {
  display: grid;
  grid-template-areas:
    "header header"
    "left right";
  grid-template-rows: auto 1fr;
  grid-template-columns: 220px 1fr;
  height: 100vh;
}

#right {
  grid-area: right;
  overflow-y: auto;
  padding: 30px;
  z-index: 10;
  background-color: #f8fafc;
}

/* 仪表板样式 */
.dashboard-section {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  padding: 30px;
  border: 1px solid #e2e8f0;
}

.dashboard-header {
  margin-bottom: 30px;
}

.dashboard-header h2 {
  color: #1e293b;
  font-size: 26px;
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-weight: 600;
}

.dashboard-header h2 i {
  margin-right: 12px;
  color: #6366F1;
}

.dashboard-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, #e2e8f0, transparent);
  margin: 30px 0;
}

/* 统计卡片样式 */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-left: 4px solid var(--card-color);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(var(--card-color-rgb), 0.1) 0%, transparent 100%);
  z-index: 0;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 50px;
  height: 50px;
  background-color: var(--card-color);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  color: white;
  font-size: 20px;
  z-index: 1;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.stat-content {
  flex: 1;
  z-index: 1;
}

.stat-value {
  font-size: 26px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 5px;
}

/* 卡片通用样式 */
.card-style {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e2e8f0;
  background-color: white;
}

.card-header h3 {
  color: #1e293b;
  font-size: 18px;
  display: flex;
  align-items: center;
  margin: 0;
}

.card-header h3 i {
  margin-right: 10px;
  color: var(--header-color);
}

.card-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f1f5f9;
  color: #64748b;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background-color: #e2e8f0;
  color: #475569;
}

.content-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

@media (max-width: 992px) {
  .content-row {
    grid-template-columns: 1fr;
  }
}

.hot-questions {
  height: 100%;
}

.question-list {
  list-style: none;
  padding: 0 20px 20px;
}

.question-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px dashed #e2e8f0;
  transition: all 0.2s ease;
}

.question-item:hover {
  background-color: #f8fafc;
}

.question-item:last-child {
  border-bottom: none;
}

.question-rank {
  width: 26px;
  height: 26px;
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  margin-right: 15px;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.question-text {
  flex: 1;
  font-size: 14px;
  color: #334155;
}

.question-count {
  font-size: 12px;
  color: #64748b;
  min-width: 50px;
  text-align: right;
  font-weight: 500;
}

.hot-tags {
  height: 100%;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 20px;
}

.tag-item {
  padding: 8px 14px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.tag-item:hover {
  transform: scale(1.05) rotate(0deg) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 滚动条样式 */
div::-webkit-scrollbar {
  width: 10px;
}

div::-webkit-scrollbar-thumb {
  cursor: pointer;
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