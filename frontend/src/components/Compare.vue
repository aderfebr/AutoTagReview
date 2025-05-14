<template>
  <div id="main">
    <Title></Title>
    <Nav></Nav>

    <div id="right">
      <div class="content-section input-section">
        <div id="input-container">
          <h3><i class="fa fa-edit"></i> 输入评论</h3>
          <textarea v-model="userInput" placeholder="请输入要分析的评论内容" rows="4"></textarea>
          <div class="batch-actions">
            <button id="analyze" @click="analyze" :disabled="isLoading" :class="{ 'loading': isLoading }">
              <i class="fa" :class="isLoading ? 'fa-spinner fa-spin' : 'fa-play'"></i>
              {{ isLoading ? '分析中...' : '开始分析' }}
            </button>
          </div>
        </div>
      </div>

      <div class="content-section results-section">
        <div id="results-header">
          <h3><i class="fa fa-calculator"></i> 分类结果</h3>
          <div class="section-divider"></div>
        </div>

        <div class="chart-container">
          <VChart v-if="hasChartData" class="chart" :option="option1" :autoresize="true" />
          <VChart v-if="hasChartData" class="chart" :option="option2" :autoresize="true" />
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
import { useRoute, useRouter } from 'vue-router';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent, VisualMapComponent } from 'echarts/components';
import VChart from 'vue-echarts';
import Nav from './Nav.vue';
import Title from './Title.vue';

use([CanvasRenderer, BarChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent, VisualMapComponent]);

const userInput = ref('');
const isLoading = ref(false);
const hasChartData = ref(false);

const route = useRoute()
onMounted(() => {
  if (route.query.text) {
    userInput.value = decodeURIComponent(route.query.text);
    analyze();
  }
});

const router = useRouter();
const option1 = ref();
const option2 = ref();

const analyze = async () => {
  isLoading.value = true;
  try {
    const response = await fetch('http://localhost:8000/api/compare/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 'input': userInput.value })
    });
    const data = await response.json();

    if (data.bert_wo && data.bert_wo.labels && data.bert_wo.probs) {
      option1.value = {
        xAxis: {
          type: 'category',
          data: data.bert_wo.labels,
          axisLabel: {
            rotate: 30,
            interval: 0
          }
        },
        yAxis: {
          type: 'value',
          max: 100,
          min: 0
        },
        title: {
          text: '分类结果可视化',
        },
        visualMap: {
          show: false,
          min: 0,
          max: 100,
          inRange: {
            color: ['#67e0e3', '#37a2da', '#fd666d']
          }
        },
        series: [
          {
            data: data.bert_wo.probs.map(prob =>
              (prob * 100).toFixed(1)
            ),
            type: 'bar',
            label: {
              show: true,
              position: 'top',
              formatter: '{c}%'
            }
          }
        ],
        tooltip: {
          trigger: 'axis',
          formatter: '{b}: {c}%'
        }
      };
    }

    if (data.bert_w && data.bert_w.labels && data.bert_w.probs) {
      option2.value = {
        xAxis: {
          type: 'category',
          data: data.bert_w.labels,
          axisLabel: {
            rotate: 30,
            interval: 0
          }
        },
        yAxis: {
          type: 'value',
          max: 100,
          min: 0
        },
        title: {
          text: '分类结果可视化',
          subtext: '语义对齐+标签引导',
        },
        visualMap: {
          show: false,
          min: 0,
          max: 100,
          inRange: {
            color: ['#67e0e3', '#37a2da', '#fd666d']
          }
        },
        series: [
          {
            data: data.bert_w.probs.map(prob =>
              (prob * 100).toFixed(1)
            ),
            type: 'bar',
            label: {
              show: true,
              position: 'top',
              formatter: '{c}%'
            }
          }
        ],
        tooltip: {
          trigger: 'axis',
          formatter: '{b}: {c}%'
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