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
          <h3><i class="fa fa-comment"></i> 输入评论</h3>
          <textarea 
            v-model="userInput" 
            placeholder="请输入要分析的评论内容..."
            rows="4"
          ></textarea>
          <button id="analyze" @click="analyze()" :disabled="isLoading">
            <i class="fa" :class="isLoading ? 'fa-spinner fa-spin' : 'fa-play'"></i> 
            {{ isLoading ? '分析中...' : '开始分析' }}
          </button>
        </div>
      </div>
      
      <div class="content-section results-section">
        <div id="results-header">
          <h3><i class="fa fa-calculator"></i> 分析结果</h3>
          <div class="section-divider"></div>
        </div>
        
        <div id="results-container">
          <!-- TF-IDF 算法结果 -->
          <div class="algorithm-card">
            <div class="algorithm-header">
              <span class="algorithm-icon" style="background-color: #FFB7B2;"></span>
              <span class="algorithm-name">TF-IDF</span>
            </div>
            <div class="algorithm-result">
              <div v-if="results.tfidf.length > 0" class="result-tags large">
                <span v-for="(tag, index) in results.tfidf" :key="'tfidf-'+index" class="tag">{{ tag }}</span>
              </div>
              <div v-else class="empty-state">
                <i class="fa fa-info-circle"></i> 暂无标签数据
              </div>
            </div>
          </div>
          
          <div class="algorithm-divider"></div>
          
          <!-- LDA 算法结果 -->
          <div class="algorithm-card">
            <div class="algorithm-header">
              <span class="algorithm-icon" style="background-color: #FFDAC1;"></span>
              <span class="algorithm-name">LDA</span>
            </div>
            <div class="algorithm-result">
              <div v-if="results.lda.length > 0" class="result-tags large">
                <span v-for="(tag, index) in results.lda" :key="'lda-'+index" class="tag">{{ tag }}</span>
              </div>
              <div v-else class="empty-state">
                <i class="fa fa-info-circle"></i> 暂无标签数据
              </div>
            </div>
          </div>
          
          <div class="algorithm-divider"></div>
          
          <!-- TextRank 算法结果 -->
          <div class="algorithm-card">
            <div class="algorithm-header">
              <span class="algorithm-icon" style="background-color: #E2F0CB;"></span>
              <span class="algorithm-name">TextRank</span>
            </div>
            <div class="algorithm-result">
              <div v-if="results.textrank.length > 0" class="result-tags large">
                <span v-for="(tag, index) in results.textrank" :key="'textrank-'+index" class="tag">{{ tag }}</span>
              </div>
              <div v-else class="empty-state">
                <i class="fa fa-info-circle"></i> 暂无标签数据
              </div>
            </div>
          </div>
          
          <div class="algorithm-divider"></div>
          
          <!-- 大模型（无微调）结果 -->
          <div class="algorithm-card">
            <div class="algorithm-header">
              <span class="algorithm-icon" style="background-color: #B5EAD7;"></span>
              <span class="algorithm-name">大模型（无微调）</span>
            </div>
            <div class="algorithm-result">
              <div v-if="results.llm_wo.length > 0" class="result-tags large">
                <span v-for="(tag, index) in results.llm_wo" :key="'llmwo-'+index" class="tag">{{ tag }}</span>
              </div>
              <div v-else class="empty-state">
                <i class="fa fa-info-circle"></i> 暂无标签数据
              </div>
            </div>
          </div>
          
          <div class="algorithm-divider"></div>
          
          <!-- 大模型（微调）结果 -->
          <div class="algorithm-card">
            <div class="algorithm-header">
              <span class="algorithm-icon" style="background-color: #C7CEEA;"></span>
              <span class="algorithm-name">大模型（微调）</span>
            </div>
            <div class="algorithm-result">
              <div v-if="results.llm_w.length > 0" class="result-tags large">
                <span v-for="(tag, index) in results.llm_w" :key="'llmw-'+index" class="tag">{{ tag }}</span>
              </div>
              <div v-else class="empty-state">
                <i class="fa fa-info-circle"></i> 暂无标签数据
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Nav from './Nav.vue';

const userInput = ref('');
const isLoading = ref(false);
const results = ref({
  tfidf: [],
  lda: [],
  textrank: [],
  llm_wo: [],
  llm_w: []
});

const analyze = async () => {
  // 清空之前的结果和进度
  results.value = {
    tfidf: [],
    lda: [],
    textrank: [],
    llm_wo: [],
    llm_w: []
  };
  
  if (!userInput.value.trim()) {
    alert('请输入评论内容');
    return;
  }
  
  isLoading.value = true;
  
  try {
    const response = await fetch('http://localhost:8000/api/compare/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({'input': userInput.value})
    });
    
    if (!response.ok) throw new Error('服务器无响应');
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      buffer += decoder.decode(value, { stream: true });
      
      // 处理可能的多条消息
      let boundary;
      while ((boundary = buffer.indexOf('\n')) !== -1) {
        const message = buffer.slice(0, boundary);
        buffer = buffer.slice(boundary + 1);
        
        if (message.trim() === '') continue;
        
        try {
          const data = JSON.parse(message);
          
          // 更新进度和结果
          if (data.algorithm) {
            if (data.result !== undefined) {
              const resultArray = Array.isArray(data.result) ? data.result : [data.result];
              results.value[data.algorithm] = [...results.value[data.algorithm], ...resultArray];
            }
          }
        } catch (e) {
          console.error('解析消息失败:', e);
        }
      }
    }
  } catch (error) {
    console.error('API调用失败:', error);
    // 为每个算法设置错误状态
    Object.keys(results.value).forEach(key => {
      results.value[key] = ['分析失败'];
    });
  } finally {
    isLoading.value = false;
  }
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

#input-container h3 {
  font-size: 18px;
  color: #4a6fa5;
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

#input-container h3 i {
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

/* 结果标题 */
#results-header {
  padding: 20px 30px 10px;
}

#results-header h3 {
  font-size: 18px;
  color: #4a6fa5;
  display: flex;
  align-items: center;
  margin: 0;
}

#results-header h3 i {
  margin-right: 10px;
}

/* 算法结果容器 */
#results-container {
  padding: 0 30px 20px;
}

.algorithm-card {
  padding: 20px 0;
  transition: all 0.3s ease;
  border-radius: 8px;
  padding: 15px;
  margin: 0 -15px;
}

.algorithm-card:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.algorithm-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.algorithm-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  margin-right: 15px;
}

.algorithm-name {
  font-weight: 600;
  font-size: 17px;
  color: #333;
}

.algorithm-result {
  padding-left: 55px;
}

.algorithm-divider {
  height: 1px;
  background: #ddd;
  margin: 20px 0;
}

.result-item {
  margin-bottom: 12px;
  display: flex;
  align-items: flex-start;
}

.result-label {
  font-weight: 500;
  min-width: 100px;
  color: #666;
}

.result-value {
  flex: 1;
}

.positive {
  color: #28a745;
  font-weight: 500;
}

.negative {
  color: #dc3545;
  font-weight: 500;
}

.result-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.result-tags.large {
  gap: 10px;
}

.result-tags.large .tag {
  padding: 6px 12px;
  font-size: 14px;
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

button#analyze {
  background: linear-gradient(to right, #007bff, #17a2b8);
  color: white;
  font-size: 16px;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
}

button#analyze:hover {
  background: linear-gradient(to right, #0069d9, #138496);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.4);
}

button#analyze i {
  margin-right: 8px;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.empty-state {
  color: #666;
  font-style: italic;
  display: flex;
  align-items: center;
}

.empty-state i {
  margin-right: 8px;
  color: #4a6fa5;
}

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