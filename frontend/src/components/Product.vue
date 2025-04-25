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
          <h3><i class="fa fa-search"></i> 查询产品</h3>
          <div class="search-container">
              <select v-model="searchType" class="search-type-select">
                  <option value="product_id">ID</option>
                  <option value="title">名称</option>
                  <option value="category">类别</option>
              </select>
              <input 
                  type="text" 
                  v-model="searchQuery" 
                  :placeholder="placeholderText"
                  @keyup.enter="fetchProducts"
              >
              <button id="search" @click="fetchProducts" :disabled="isLoadingProducts">
                  <i class="fa" :class="isLoadingProducts ? 'fa-spinner fa-spin' : 'fa-search'"></i> 
                  {{ isLoadingProducts ? '查询中...' : '查询产品' }}
              </button>
          </div>
      </div>
    </div>
      <div class="content-section">
          <div id="products-header">
              <h3><i class="fa fa-archive"></i> 产品列表</h3>
              <div v-if="products.length > 0" class="pagination-info">
                  共 {{ pagination.total }} 个产品，第 {{ pagination.current }} 页/共 {{ pagination.pages }} 页
              </div>
          </div>
          
          <div id="products-container">
              <div v-if="products.length === 0" class="empty-products">
                  <i class="fa fa-box-open"></i>
                  <p>暂无产品数据</p>
              </div>
              
              <div v-else>
                  <div class="product-grid">
                      <div v-for="(product, index) in products" :key="index" class="product-item">
                          <div class="product-image">
                              <img :src="product.img" :alt="product.title">
                          </div>
                          <div class="product-info">
                            <h4 class="product-name">{{ product.title }}</h4>
                            
                            <div class="product-id-row">
                              <span class="product-id-label">ID:</span>
                              <span class="product-id-value">{{ product.product_id }}</span>
                            </div>
                            
                            <div class="product-category-row">
                              <span class="product-category-label">类别:</span>
                              <span class="product-category-value">{{ product.category }}</span>
                            </div>
                          </div>
                          <div class="product-actions">
                              <button class="analyze-btn" @click="checkReview(product.product_id)">
                                  <i class="fa fa-comments"></i> 查看评论
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
import { useRouter } from 'vue-router'
import Nav from './Nav.vue'

const searchType = ref('title')
const searchQuery = ref('')
const products = ref([])
const isLoadingProducts = ref(false)
const pagination = ref({
    total: 0,
    pages: 0,
    current: 1
})

onMounted(() => {
  fetchProducts();
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

const fetchProducts = async () => {
  isLoadingProducts.value = true
  try {
    const params = new URLSearchParams()
    params.append('page', pagination.value.current)
    
    if (searchQuery.value.trim()) {
      params.append('type', searchType.value.trim())
      params.append('query', searchQuery.value.trim())
    } else {
      params.append('all', 'true')
    }
    
    const response = await fetch(`http://localhost:8000/api/product/?${params.toString()}`)
    if (!response.ok) {
      throw new Error('获取产品失败')
    }
    const data = await response.json()
    
    products.value = data.results
    pagination.value = {
      total: data.count,
      pages: data.num_pages,
      current: data.current_page
    }
    
  } catch (error) {
    console.error('获取产品失败:', error)
    alert('获取产品失败，请稍后重试')
  } finally {
    isLoadingProducts.value = false
  }
}

// 切换页码
const changePage = (page) => {
    if (page < 1 || page > pagination.value.pages || page === pagination.value.current) {
        return
    }
    pagination.value.current = page
    fetchProducts()
}

const router = useRouter()
const checkReview = (product) => {
  const encodedProduct = encodeURIComponent(product)
  
  router.push({
    path: '/data/review',
    query: {
      id: encodedProduct
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

/* 搜索容器样式 */
.search-container {
  display: flex;
  gap: 10px;
}

/* 搜索类型选择框 */
.search-type-select {
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 15px;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 16px;
  padding-right: 30px;
}

.search-type-select:focus {
  outline: none;
  border-color: #4a6fa5;
  box-shadow: 0 0 0 2px rgba(74, 111, 165, 0.1);
}

/* 搜索输入框 */
.search-container input {
  flex: 1;
  padding: 10px 15px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  font-size: 15px;
  transition: all 0.3s ease;
  min-width: 200px;
}

.search-container input:focus {
  outline: none;
  border-color: #4a6fa5;
  box-shadow: 0 0 0 3px rgba(74, 111, 165, 0.1);
}

#products-header {
  padding: 20px 25px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
  background: rgba(240, 180, 210, 0.15);
  backdrop-filter: blur(5px);
  position: sticky;
  top: 0;
  z-index: 5;
}

#products-header h3 {
  font-size: 18px;
  color: #4a6fa5;
  display: flex;
  align-items: center;
  margin: 0;
}

#products-header h3 i {
  margin-right: 10px;
}

/* 产品容器样式 */
#products-container {
  background: rgba(240, 180, 210, 0.15);
  border-radius: 0 0 12px 12px;
  overflow: hidden;
}

/* 空状态样式 */
.empty-products {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-products i {
  font-size: 50px;
  margin-bottom: 15px;
  color: #cbd5e1;
}

.empty-products p {
  font-size: 16px;
  margin-top: 10px;
  color: #94a3b8;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 24px;
  padding: 20px;
}

/* 产品卡片样式 */
.product-item {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.product-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

/* 产品图片 */
.product-image {
  position: relative;
  width: 100%;
  padding-top: 100%; 
  overflow: hidden;
  background: #f8fafc;
}

.product-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; 
  transition: transform 0.3s ease;
}

.product-item:hover .product-image img {
  transform: scale(1.03); 
}

/* 产品信息 */
.product-info {
  padding: 16px;
  flex-grow: 1;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

/* ID行样式 */
.product-id-row {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

/* 类别行样式 */
.product-category-row {
  display: flex;
  align-items: center;
}

/* 统一标签样式 */
.product-id-label,
.product-category-label {
  font-size: 12px;
  color: #64748b;
  margin-right: 8px;
  width: 28px;
  text-align: right;
}

/* 统一值样式 */
.product-id-value,
.product-category-value {
  font-size: 13px;
  padding: 4px 10px;
  border-radius: 4px;
  background-color: rgba(241, 245, 249, 0.7);
  border: 1px solid rgba(203, 213, 225, 0.5);
  color: #475569;
  flex-grow: 1;
}

/* 产品操作按钮 */
.product-actions {
  padding: 0 16px 16px;
  text-align: right;
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