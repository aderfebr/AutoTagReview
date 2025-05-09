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
    <div class="content-section">
        <div id="input-container">
        <h3><i class="fa fa-search"></i> 查询评论</h3>
        <div class="search-container">
            <input 
            type="text" 
            v-model="productId" 
            placeholder="请输入产品ID..."
            @keyup.enter="fetchReviews"
            >
            <button id="search" @click="fetchReviews" :disabled="isLoadingReviews">
            <i class="fa" :class="isLoadingReviews ? 'fa-spinner fa-spin' : 'fa-search'"></i> 
            {{ isLoadingReviews ? '查询中...' : '查询评论' }}
            </button>
        </div>
        </div>
    </div>
    
    <div class="content-section reviews-section">
        <div id="reviews-header">
            <h3><i class="fa fa-comments"></i> 评论列表</h3>
            <div v-if="reviews.length > 0" class="pagination-info">
                共 {{ pagination.total }} 条评论，第 {{ pagination.current }} 页/共 {{ pagination.pages }} 页
            </div>
        </div>
        
        <div id="reviews-container">
            <div v-if="reviews.length === 0" class="empty-reviews">
                <i class="fa fa-review-slash"></i>
                <p>暂无评论数据</p>
            </div>
            
            <div v-else>
                <div class="review-list">
                    <div v-for="(review, index) in reviews" :key="index" class="review-item">
                        <div class="review-header">
                            <span class="review-user">{{ review.nickname }}</span>
                            <span class="review-date">{{ review.time }}</span>
                        </div>
                        <div class="review-content">{{ review.review }}</div>
                        <div class="review-actions">
                            <button class="analyze-btn" @click="analyzeReview(review.review)">
                                <i class="fa fa-tag"></i> 标签生成
                            </button>
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
import { useRoute, useRouter } from 'vue-router'
import Nav from './Nav.vue'

const productId = ref('')
const reviews = ref([])
const isLoadingReviews = ref(false)
const pagination = ref({
    total: 0,
    pages: 0,
    current: 1
})

const route = useRoute()
onMounted(() => {
  if (route.query.id) {
    productId.value = route.query.id
    fetchReviews()
  } else {
    fetchReviews()
  }
})

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

const fetchReviews = async () => {
  isLoadingReviews.value = true
  try {
    const params = new URLSearchParams()
    params.append('page', pagination.value.current)
    
    if (productId.value.trim()) {
      params.append('product_id', productId.value.trim())
    } else {
      params.append('all', 'true')
    }
    
    const response = await fetch(`http://localhost:8000/api/review/?${params.toString()}`)
    if (!response.ok) {
      throw new Error('获取评论失败')
    }
    const data = await response.json()
    
    reviews.value = data.results
    pagination.value = {
      total: data.count,
      pages: data.num_pages,
      current: data.current_page
    }
    
  } catch (error) {
    console.error('获取评论失败:', error)
    alert('获取评论失败，请稍后重试')
  } finally {
    isLoadingReviews.value = false
  }
}

// 切换页码
const changePage = (page) => {
    if (page < 1 || page > pagination.value.pages || page === pagination.value.current) {
        return
    }
    pagination.value.current = page
    fetchReviews()
}

const router = useRouter()
const analyzeReview = (review) => {
  const encodedReview = encodeURIComponent(review)
  
  router.push({
    path: '/tag/single',
    query: {
      text: encodedReview
    }
  })
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
  background: linear-gradient(135deg,rgb(40, 198, 255),rgb(134, 47, 255));
  color: white;
  padding: 20px 0;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 10;
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
  background: #f8fafc;
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

/* 输入区域样式 */
#input-container {
    background: rgba(180, 210, 240, 0.15);
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

.search-container {
  display: flex;
  gap: 10px;
}

.search-container input {
  flex: 1;
  padding: 12px 15px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  font-size: 15px;
  transition: all 0.3s ease;
}

.search-container input:focus {
  outline: none;
  border-color: #4a6fa5;
  box-shadow: 0 0 0 3px rgba(74, 111, 165, 0.1);
}

/* 按钮样式 */
button {
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  align-items: center;
}

button#search {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  color: white;
  font-size: 16px;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
}

button#search:hover {
  background: linear-gradient(to right, #4338ca, #6d28d9);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 评论列表样式 */
.reviews-section {
    background: rgba(240, 180, 210, 0.15);
}

#reviews-header {
  padding: 20px 25px 0;
}

#reviews-header h3 {
  font-size: 18px;
  color: #4a6fa5;
  display: flex;
  align-items: center;
}

#reviews-header h3 i {
  margin-right: 10px;
}

.empty-reviews {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.empty-reviews i {
  font-size: 50px;
  margin-bottom: 15px;
  color: #cbd5e1;
}

.empty-reviews p {
  font-size: 16px;
  margin-top: 10px;
}

.review-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 0 25px 25px;
}

.review-item {
  border-radius: 10px;
  padding: 20px;
  transition: all 0.3s ease;
  border: 1px solid #f1f5f9;
}

.review-item:hover {
background-color: rgba(255, 255, 255, 0.3);
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
  color: #64748b;
  gap: 15px;
}

.review-user {
  font-weight: 600;
  color: #1e293b;
}

.review-rating {
  color: #f59e0b;
}

.review-date {
  margin-left: auto;
  color: #94a3b8;
  font-size: 13px;
}

.review-content {
  line-height: 1.7;
  margin-bottom: 15px;
  color: #334155;
  font-size: 15px;
}

.review-actions {
  display: flex;
  justify-content: flex-end;
}

.analyze-btn {
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
  padding: 6px 14px;
  font-size: 13px;
  border-radius: 20px;
}

.analyze-btn:hover {
  background: rgba(99, 102, 241, 0.2);
}

.analyze-btn i {
  margin-right: 6px;
  font-size: 12px;
}

.pagination-info {
    margin: 10px 0;
    font-size: 14px;
    color: #64748b;
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