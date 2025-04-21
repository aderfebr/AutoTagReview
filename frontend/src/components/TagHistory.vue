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
    <div class="content-section history-section">
        <div id="history-header">
            <h3><i class="fa fa-history"></i> 历史记录</h3>
            <div v-if="history.length > 0" class="pagination-info">
                共 {{ pagination.total }} 条评论，第 {{ pagination.current }} 页/共 {{ pagination.pages }} 页
            </div>
        </div>
        
        <div id="history-container">
            <div>
                <div class="history-list">
                    <div v-for="(item, index) in history" :key="index" class="history-item">
                        <div class="comment-section">
                            <div class="comment-label">评论内容：</div>
                            <div class="comment-content">{{ item.comment }}</div>
                        </div>
                        <div class="history-divider"></div>
                        <div class="analysis-results">
                            <div class="analysis-column">
                                <div class="analysis-item">
                                    <div class="analysis-label">TF-IDF：</div>
                                    <div class="tag-list">
                                        <span v-for="(tag, tagIndex) in item.tfidf" :key="'tfidf-'+tagIndex" class="tag">{{ tag }}</span>
                                    </div>
                                </div>
                                
                                <div class="analysis-item">
                                    <div class="analysis-label">LDA：</div>
                                    <div class="tag-list">
                                        <span v-for="(tag, tagIndex) in item.lda" :key="'lda-'+tagIndex" class="tag">{{ tag }}</span>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="analysis-column">
                                <div class="analysis-item">
                                    <div class="analysis-label">TextRank：</div>
                                    <div class="tag-list">
                                        <span v-for="(tag, tagIndex) in item.textrank" :key="'textrank-'+tagIndex" class="tag">{{ tag }}</span>
                                    </div>
                                </div>
                                
                                <div class="analysis-item">
                                    <div class="analysis-label">LLM（无微调）：</div>
                                    <div class="tag-list">
                                        <span v-for="(tag, tagIndex) in item.llm_wo" :key="'llmwo-'+tagIndex" class="tag">{{ tag }}</span>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="analysis-column">
                                <div class="analysis-item">
                                    <div class="analysis-label">LLM（微调）：</div>
                                    <div class="tag-list">
                                        <span v-for="(tag, tagIndex) in item.llm_w" :key="'llmw-'+tagIndex" class="tag">{{ tag }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 分页器 -->
                <div class="pagination-container">
                <button 
                @click="changePage(pagination.current - 1)"
                :disabled="pagination.current === 1"
                class="pagination-button"
                >
                <i class="fa fa-chevron-left"></i> 上一页
                </button>
                
                <div class="page-numbers-wrapper">
                <div class="page-numbers">
                    <button
                    v-for="page in visiblePages"
                    :key="page"
                    @click="changePage(page)"
                    :class="{ active: page === pagination.current }"
                    class="page-number"
                    >
                    {{ page }}
                    </button>
                    <span v-if="showEllipsis" class="ellipsis">...</span>
                </div>
                </div>
                
                <button 
                @click="changePage(pagination.current + 1)"
                :disabled="pagination.current === pagination.pages"
                class="pagination-button"
                >
                下一页 <i class="fa fa-chevron-right"></i>
                </button>
            </div>
            </div>
        </div>
    </div>

    </div>
</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Nav from './Nav.vue'

const history = ref([])
const isLoadingHistory = ref(false)
const pagination = ref({
    total: 0,
    pages: 0,
    current: 1
})

onMounted(() => {
  fetchHistory();
});

// 计算显示的页码范围
const visiblePages = computed(() => {
    const current = pagination.value.current
    const totalPages = pagination.value.pages
    const range = 2 
    let start = Math.max(1, current - range)
    let end = Math.min(totalPages, current + range)
    
    if (current <= range + 1) {
        end = Math.min(2 * range + 1, totalPages)
    }
    if (current >= totalPages - range) {
        start = Math.max(1, totalPages - 2 * range)
    }
    
    const pages = []
    for (let i = start; i <= end; i++) {
        pages.push(i)
    }
    return pages
})

// 是否显示省略号
const showEllipsis = computed(() => {
    return pagination.value.pages > visiblePages.value.length && 
           visiblePages.value[visiblePages.value.length - 1] < pagination.value.pages
})

const fetchHistory = async () => {
  isLoadingHistory.value = true
  try {
    const response = await fetch(`http://localhost:8000/api/taghistory/?page=${pagination.value.current}`)
    if (!response.ok) {
      throw new Error('获取评论失败')
    }
    const data = await response.json()
    
    history.value = data.results
    pagination.value = {
      total: data.count,
      pages: data.num_pages,
      current: data.current_page
    }
    
  } catch (error) {
    console.error('获取评论失败:', error)
    alert('获取评论失败，请稍后重试')
  } finally {
    isLoadingHistory.value = false
  }
}

// 切换页码
const changePage = (page) => {
    if (page < 1 || page > pagination.value.pages || page === pagination.value.current) {
        return
    }
    pagination.value.current = page
    fetchHistory()
}
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

/* 左右区域样式 */
#left {
  grid-area: left;
  background: rgba(0, 120, 240, 0.15);
}

#right {
  grid-area: right;
  overflow-y: auto;
  padding: 30px;
  z-index: 10;
}

/* 内容区块通用样式 */
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

/* 评论列表样式 */
.history-section {
  background: rgba(180, 210, 240, 0.15);
}

#history-header {
  padding: 20px 25px 0;
}

#history-header h3 {
  font-size: 18px;
  color: #4a6fa5;
  display: flex;
  align-items: center;
}

#history-header h3 i {
  margin-right: 10px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 0 25px 25px;
}

.history-item {
  border-radius: 10px;
  padding: 20px;
  transition: all 0.3s ease;
  border: 1px solid #f1f5f9;
}

.history-item:hover {
background-color: rgba(255, 255, 255, 0.3);
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.comment-section {
    margin-bottom: 16px;
    border-radius: 6px;
}

.comment-label {
    font-weight: bold;
    color: #555;
    margin-bottom: 6px;
}

.comment-content {
    line-height: 1.5;
    color: #333;
}

.analysis-results {
    display: flex;
    gap: 16px;
    margin-top: 12px;
}

.analysis-column {
    flex: 1;
    min-width: 0;
}

.analysis-item {
    margin-bottom: 12px;
}

.analysis-label {
    font-weight: bold;
    color: #555;
    margin-bottom: 6px;
    font-size: 14px;
}

.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.tag {
    background-color: #e9f5ff;
    color: #1a73e8;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 13px;
    white-space: nowrap;
}

.pagination-info {
    margin: 10px 0;
    font-size: 14px;
    color: #64748b;
}

.history-divider {
    height: 2px;
    background-color: #d0d0d0;
    margin: 16px 0;
}

.pagination-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
    gap: 10px;
}

.pagination-button {
    padding: 8px 16px;
    background-color: #f1f5f9;
    color: #4a6fa5;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    transition: all 0.3s ease;
}

.pagination-button:hover:not(:disabled) {
    background-color: #e2e8f0;
    transform: translateY(-1px);
}

.pagination-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.page-numbers {
    display: flex;
    gap: 5px;
    justify-content: center;
    flex-wrap: wrap;
}

/* 页码按钮样式 */
.page-number {
    min-width: 36px;
    height: 36px;
    padding: 0 8px;
    background-color: #f1f5f9;
    color: #4a6fa5;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.page-number:hover {
    background-color: #e2e8f0;
}

.page-number.active {
    background-color: #4a6fa5;
    color: white;
    border-color: #4a6fa5;
}

.ellipsis {
    display: flex;
    align-items: center;
    padding: 0 8px;
    color: #94a3b8;
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