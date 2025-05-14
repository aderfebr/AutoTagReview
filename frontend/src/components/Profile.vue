<template>
  <div id="main">
    <Title></Title>
    <Nav></Nav>

    <div id="right">
      <div class="content-section input-section">
        <div id="input-container">
          <h3><i class="fa fa-search"></i> 查询画像</h3>
          <div class="search-container">
            <input type="text" v-model="productId" placeholder="请输入产品ID..." @keyup.enter="fetchProfile">
            <button id="search" @click="fetchProfile" :disabled="isLoading">
              <i class="fa" :class="isLoading ? 'fa-spinner fa-spin' : 'fa-search'"></i>
              {{ isLoading ? '查询中...' : '查询画像' }}
            </button>
          </div>
        </div>
      </div>

      <div class="content-section results-section">
        <div id="results-header">
          <h3><i class="fa fa-id-card"></i> 产品画像</h3>
          <div class="section-divider"></div>
        </div>

        <div class="chart-container">
          <VChart v-if="hasChartData" class="chart" :option="option" :autoresize="true" />
          <div v-else class="no-chart-data">
            <i class="fa fa-bar-chart"></i>
            <p>无可用图表数据</p>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent, VisualMapComponent } from 'echarts/components';
import VChart from 'vue-echarts';
import Nav from './Nav.vue';
import Title from './Title.vue';

use([CanvasRenderer, BarChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent, VisualMapComponent]);

const productId = ref('');
const isLoading = ref(false);
const hasChartData = ref(false);

const route = useRoute()
onMounted(() => {
  if (route.query.id) {
    productId.value = route.query.id
    fetchProfile()
  }
});

const option = ref();

const fetchProfile = async () => {
  if (!productId.value.trim()) {
    alert("请输入产品ID")
    return
  }
  isLoading.value = true;
  try {
    const params = new URLSearchParams()
    params.append('product_id', productId.value.trim())
    
    const response = await fetch(`http://localhost:8000/api/profile/?${params.toString()}`)
    const data = await response.json();

    if (data && data.labels && data.probs) {
      option.value = {
        xAxis: {
          type: 'category',
          data: data.labels,  // Use the labels from API for x-axis
          axisLabel: {
            rotate: 30,  // Rotate labels if they're long
            interval: 0  // Show all labels
          }
        },
        yAxis: {
          type: 'value'
        },
        title: {
          text: '产品画像可视化'
        },
        visualMap: {
          show: false,
          min: 0,
          max: 15,
          inRange: {
            color: ['#67e0e3', '#37a2da', '#fd666d']
          }
        },
        series: [
          {
            data: data.probs.map(prob =>
              (prob * 100).toFixed(1)
            ),
            type: 'bar',
            label: {
              show: true,
              position: 'top',
              formatter: '{c}%'  // Show percentage labels on bars
            }
          }
        ],
        tooltip: {
          trigger: 'axis',
          formatter: '{b}: {c}%'  // Show tooltip with percentage
        }
      };
    }

    hasChartData.value = true;

  } catch (error) {
    console.error('获取数据失败:', error);
    alert('获取数据失败，请稍后重试');
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
  border: 1px solid rgba(0, 0, 0, 0.05);
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

/* 结果标题 */
#results-header {
  padding: 20px 30px 0px;
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

.chart-container {
  background: white;
  border-radius: 8px;
  margin: 30px;
  padding: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  min-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.chart {
  width: 100%;
  height: 600px;
}

.no-chart-data {
  text-align: center;
  color: #999;
}

.no-chart-data i {
  font-size: 50px;
  margin-bottom: 15px;
  color: #ccc;
}

.no-chart-data p {
  font-size: 16px;
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