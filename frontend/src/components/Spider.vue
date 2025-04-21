<template>
  <div id="main">
    <div id="page-title">
      <h1>电商用户评论问题分类与标签自动生成系统</h1>
      <div class="title-divider"></div>
    </div>

    <div id="left">
      <Nav></Nav>
    </div>
    
    <div id="right">
      <div class="content-section input-section">
        <div id="input-container">
          <h3><i class="fa fa-link"></i> 输入链接</h3>
          <textarea 
            v-model="userInput" 
            placeholder="请输入要分析的网页地址..."
            rows="4"
          ></textarea>
          <div class="batch-actions">
            <button 
              id="analyze" 
              @click="spider" 
              :disabled="isLoading"
              :class="{ 'loading': isLoading }"
            >
              <i class="fa" :class="isLoading ? 'fa-spinner fa-spin' : 'fa-play'"></i> 
              {{ isLoading ? '分析中...' : '开始自动爬虫' }}
            </button>
            <div v-if="isLoading" class="progress-bar">
              <div class="progress" :style="{ width: progress + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="content-section results-section">
        <div id="input-container">
          <h3><i class="fa fa-table"></i> 自动爬虫结果</h3>
          
          <div v-if="batchResults.length > 0" class="results-container">
            <div v-if="isLoading" class="processing-indicator">
              <i class="fa fa-spinner fa-spin"></i>
              <span>正在处理第 {{ batchResults.length + 1 }} 条评论，共 {{ totalComments }} 条评论</span>
            </div>
            
            <div v-for="(result, index) in paginatedResults" :key="'result-'+index" class="result-item">
              <div class="comment-content">{{ result.comment }}</div>
              <div class="tags-container">
              <div class="tag-group">
                <h4>TF-IDF 标签</h4>
                <div class="tags-cell"><span v-for="tag in result.tfidf" class="tag">{{ tag }}</span></div>
              </div>
              <div class="tag-group">
                <h4>LDA 标签</h4>
                <div class="tags-cell"><span v-for="tag in result.lda" class="tag">{{ tag }}</span></div>
              </div>
              <div class="tag-group">
                <h4>TextRank 标签</h4>
                <div class="tags-cell"><span v-for="tag in result.textrank" class="tag">{{ tag }}</span></div>
              </div>
              <div class="tag-group">
                <h4>大模型(无微调)标签</h4>
                <div class="tags-cell"><span v-for="tag in result.llm_wo" class="tag">{{ tag }}</span></div>
              </div>
              <div class="tag-group">
                <h4>大模型(微调)标签</h4>
                <div class="tags-cell"><span v-for="tag in result.llm_w" class="tag">{{ tag }}</span></div>
              </div>
              </div>
            </div>
          </div>
          
          <div v-else-if="isLoading && batchResults.length === 0" class="processing-indicator first-item">
            <i class="fa fa-spinner fa-spin"></i>
            <span>正在处理第 1 条评论，共 {{ totalComments }} 条评论</span>
          </div>
          
          <div v-else class="empty-state">
            <i class="fa fa-info-circle"></i>
            <p>请输入链接并开始分析</p>
          </div>
          
          <div class="pagination-controls" v-if="batchResults.length > 0">
            <button @click="prevPage" :disabled="currentPage === 1">
              <i class="fa fa-chevron-left"></i>
            </button>
            <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">
              <i class="fa fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import Nav from './Nav.vue';

const userInput = ref('');
const isLoading = ref(false);
const progress = ref(0);
const batchResults = ref([]);
const currentPage = ref(1);
const totalComments = ref(0);

const spider = async () => {
  if (!userInput.value.trim()) return;
  
  try {
    isLoading.value = true;
    progress.value = 0;
    batchResults.value = [];
    currentPage.value = 1;
    
    const response = await fetch('http://localhost:8000/api/spider/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ input: userInput.value })
    });
    
    if (!response.ok) throw new Error('Server response error');
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let currentResult = null;
    let commentCount = 0;
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      buffer += decoder.decode(value, { stream: true });
      
      let boundary;
      while ((boundary = buffer.indexOf('\n')) !== -1) {
        const message = buffer.slice(0, boundary);
        buffer = buffer.slice(boundary + 1);
        
        if (!message.trim()) continue;
        
        try {
          const data = JSON.parse(message);
          
          if(data.total){
            totalComments.value=data.total
          }

          if (data.comment) {
            if (currentResult) {
              batchResults.value.push(currentResult);
            }
            currentResult = {
              comment: data.comment,
              tfidf: [],
              lda: [],
              textrank: [],
              llm_wo: [],
              llm_w: []
            };
            commentCount++;
            continue;
          }
          
          if (currentResult && data.algorithm && data.result) {
            const resultArray = Array.isArray(data.result) ? data.result : [data.result];
            
            switch(data.algorithm.toLowerCase()) {
              case 'tfidf':
                currentResult.tfidf = resultArray;
                break;
              case 'lda':
                currentResult.lda = resultArray;
                break;
              case 'textrank':
                currentResult.textrank = resultArray;
                break;
              case 'llm_wo':
                currentResult.llm_wo = resultArray;
                break;
              case 'llm_w':
                currentResult.llm_w = resultArray;
                break;
            }
          }
          progress.value = Math.round(((batchResults.value.length + 1) / data.total) * 100);
        } catch (e) {
          console.error('Error parsing message:', e);
        }
      }
    }
    
    if (currentResult) {
      batchResults.value.push(currentResult);
    }
    
  } catch (error) {
    console.error('分析失败:', error);
    alert(`分析失败: ${error.message}`);
  } finally {
    isLoading.value = false;
  }
};

// 分页计算属性
const totalPages = computed(() => batchResults.value.length);
const paginatedResults = computed(() => {
  return batchResults.value.slice(currentPage.value - 1, currentPage.value);
});

// 分页控制
const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};
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
  display: grid;
  grid-template-areas: 
    "header header"
    "left right";
  grid-template-rows: auto 1fr;
  grid-template-columns: 220px 1fr;
  height: 100vh;
}

#page-title {
  grid-area: header;
  position: static;
  background: linear-gradient(135deg,rgba(0, 139, 189, 0.7),rgba(80, 0, 192, 0.7));
  color: white;
  padding: 20px 0;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

#page-title h1 {
  font-size: 30px;
  margin: 0;
  font-weight: 500;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

#page-title h1 i {
  margin-right: 10px;
}

.title-divider {
  height: 2px;
  background: linear-gradient(to right, transparent, rgba(255,255,255,0.5), transparent);
  margin: 8px auto 0;
  width: 80%;
}

/* 左侧导航栏 */
#left {
  background: rgba(0, 120, 240, 0.15);
  grid-area: left;
}

#right {
  grid-area: right;
  background: linear-gradient(to bottom, rgba(230, 235, 245, 0.5), rgba(220, 225, 240, 0.5));
  overflow-y: auto;
  padding: 30px 0;
  z-index: 10;
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

.input-section {
  background: rgba(180, 210, 240, 0.15);
}

.results-section {
  background: rgba(240, 180, 210, 0.15);
}

.section-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(200, 210, 220, 0.3), transparent);
  margin: 10px 30px;
}

/* 输入区域 */
#input-container {
  padding: 30px;
}

h3 {
  font-size: 18px;
  color: #4a6fa5;
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

h3 i {
  margin-right: 10px;
}

textarea {
  width: 100%;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-family: inherit;
  font-size: 15px;
  resize: vertical;
  min-height: 100px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

textarea:focus {
  outline: none;
  border-color: #4a6fa5;
  box-shadow: 0 0 0 3px rgba(74, 111, 165, 0.2);
}

.upload-area {
  border: 2px dashed #aaa;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  background-color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
}

.upload-area.dragover {
  border-color: #4a6fa5;
  background-color: rgba(74, 111, 165, 0.1);
}

.upload-prompt {
  color: #666;
}

.upload-prompt i {
  font-size: 48px;
  color: #4a6fa5;
  margin-bottom: 10px;
}

.upload-prompt p {
  margin: 10px 0;
}

.file-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: rgba(255, 255, 255, 0.7);
  padding: 10px 15px;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.file-details {
  display: flex;
  align-items: center;
  gap: 15px;
}

.file-details i {
  font-size: 24px;
  color: #4a6fa5;
}

.filename {
  font-weight: 500;
  margin-bottom: 5px;
}

.filesize {
  font-size: 12px;
  color: #666;
}

.remove-file-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-file-btn:hover {
  color: #d33;
}

.file-requirements {
  background-color: rgba(255, 255, 255, 0.7);
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.file-requirements h4 {
  margin-bottom: 10px;
  color: #4a6fa5;
  font-size: 15px;
}

.file-requirements ul {
  padding-left: 20px;
  font-size: 14px;
  color: #555;
}

.file-requirements li {
  margin-bottom: 5px;
}

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

button#analyze {
  background: linear-gradient(to right, #007bff, #17a2b8);
  color: white;
  font-size: 16px;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
  flex: 1;
  justify-content: center;
}

button#analyze:hover:not(:disabled) {
  background: linear-gradient(to right, #0069d9, #138496);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.4);
}

button#analyze.loading {
  background: linear-gradient(to right, #0069d9, #138496);
}

button i {
  margin-right: 8px;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.batch-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #eee;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: linear-gradient(to right, #4a6fa5, #17a2b8);
  transition: width 0.3s ease;
}

.results-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-item {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.comment-content {
  font-weight: 500;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.tags-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.tag-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.tag-group h4 {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.tags-cell {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: #e1f5fe;
  color: #0288d1;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  font-size: 0.85rem;
}

.processing-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #4a6fa5;
  padding: 15px;
  background: rgba(255,255,255,0.8);
  border-radius: 8px;
  margin-top: 15px;
}

.tag.processing {
  background: #f0f0f0;
  color: #999;
  font-style: italic;
}

/* 分页控件 */
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.pagination-controls button {
  background-color: #4a6fa5;
  color: white;
  width: 36px;
  height: 36px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.pagination-controls button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #555;
}

/* 加载指示器 */
.loading-indicator {
  text-align: center;
  padding: 40px;
  color: #4a6fa5;
}

.loading-indicator i {
  font-size: 36px;
  margin-bottom: 15px;
}

.loading-indicator p {
  margin-bottom: 20px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #eee;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: linear-gradient(to right, #4a6fa5, #17a2b8);
  transition: width 0.3s ease;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.empty-state i {
  font-size: 36px;
  margin-bottom: 15px;
  color: #4a6fa5;
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