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
            <div class="comment-section">
                <div class="comment-label"><h3><i class="fa fa-comments"></i>评论内容：</h3></div>
                <div class="comment-content">{{ currentItem.comment }}</div>
                <div class="history-divider"></div>
                <div class="analysis-results">
                    <div class="analysis-column">
                        <div class="analysis-item">
                            <div class="analysis-label">TF-IDF：</div>
                            <div class="tag-list">
                                <span v-for="(tag, tagIndex) in currentItem.tfidf" :key="'tfidf-'+tagIndex" class="tag">{{ tag }}</span>
                                <span v-if="!currentItem.tfidf || currentItem.tfidf.length === 0" class="no-data">无数据</span>
                            </div>
                        </div>
                        
                        <div class="analysis-item">
                            <div class="analysis-label">LDA：</div>
                            <div class="tag-list">
                                <span v-for="(tag, tagIndex) in currentItem.lda" :key="'lda-'+tagIndex" class="tag">{{ tag }}</span>
                                <span v-if="!currentItem.lda || currentItem.lda.length === 0" class="no-data">无数据</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="analysis-column">
                        <div class="analysis-item">
                            <div class="analysis-label">TextRank：</div>
                            <div class="tag-list">
                                <span v-for="(tag, tagIndex) in currentItem.textrank" :key="'textrank-'+tagIndex" class="tag">{{ tag }}</span>
                                <span v-if="!currentItem.textrank || currentItem.textrank.length === 0" class="no-data">无数据</span>
                            </div>
                        </div>
                        
                        <div class="analysis-item">
                            <div class="analysis-label">LLM（无微调）：</div>
                            <div class="tag-list">
                                <span v-for="(tag, tagIndex) in currentItem.llm_wo" :key="'llmwo-'+tagIndex" class="tag">{{ tag }}</span>
                                <span v-if="!currentItem.llm_wo || currentItem.llm_wo.length === 0" class="no-data">无数据</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="analysis-column">
                        <div class="analysis-item">
                            <div class="analysis-label">LLM（微调）：</div>
                            <div class="tag-list">
                                <span v-for="(tag, tagIndex) in currentItem.llm_w" :key="'llmw-'+tagIndex" class="tag">{{ tag }}</span>
                                <span v-if="!currentItem.llm_w || currentItem.llm_w.length === 0" class="no-data">无数据</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="history-divider"></div>
                <div class="chart-container">
                    <VChart
                        v-if="hasChartData"
                        class="chart"
                        :option="option1"
                        :autoresize="true"
                    />
                    <VChart
                        v-if="hasChartData"
                        class="chart"
                        :option="option2"
                        :autoresize="true"
                    />
                    <div v-else class="no-chart-data">
                        <i class="fa fa-bar-chart"></i>
                        <p>无可用图表数据</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
</div>
</template>
    
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers';
import { Scatter3DChart } from 'echarts-gl/charts';
import { Grid3DComponent } from 'echarts-gl/components';
import {TitleComponent, TooltipComponent, LegendComponent} from 'echarts/components';
import VChart from 'vue-echarts';
import Nav from './Nav.vue'

// 注册必要的组件
use([CanvasRenderer, Scatter3DChart, Grid3DComponent, TitleComponent, TooltipComponent, LegendComponent]);

const isLoadingHistory = ref(false)
const historyId = ref([])
const hasChartData = ref(false)
const currentItem = ref({
    comment: '',
    tfidf: [],
    lda: [],
    textrank: [],
    llm_wo: [],
    llm_w: []
})

const route = useRoute()
onMounted(() => {
    if (route.query.id) {
        historyId.value = decodeURIComponent(route.query.id);
        fetchHistory();
    }
});

// 图表配置
const option1 = ref({
  grid3D: {
    viewControl: {
      distance: 250,
      alpha: 45,
      beta: 45,
    },
    axisLine: {
      lineStyle: { color: '#999' },
    },
    axisPointer: {
      lineStyle: { color: '#999' },
    },
  },
  xAxis3D: {
    type: 'value',
    name: 'PCA成分1',
  },
  yAxis3D: {
    type: 'value',
    name: 'PCA成分2',
  },
  zAxis3D: {
    type: 'value',
    name: 'PCA成分3',
  },
  title: {
    text: '词嵌入可视化',
    subtext: '按类别',
  },
  tooltip: {
    formatter: (params) => {
      return `坐标: (${params.value[0].toFixed(2)}, ${params.value[1].toFixed(2)}, ${params.value[2].toFixed(2)})<br>
              类别: ${params.seriesName}<br>
              标签: ${params.value[3]}`;
    }
  },
  legend:{
    bottom:0,
  }
});

const option2 = ref({
  grid3D: {
    viewControl: {
      distance: 250,
      alpha: 45,
      beta: 45,
    },
    axisLine: {
      lineStyle: { color: '#999' },
    },
    axisPointer: {
      lineStyle: { color: '#999' },
    },
  },
  xAxis3D: {
    type: 'value',
    name: 'PCA成分1',
  },
  yAxis3D: {
    type: 'value',
    name: 'PCA成分2',
  },
  zAxis3D: {
    type: 'value',
    name: 'PCA成分3',
  },
  title: {
    text: '词嵌入可视化',
    subtext: '按聚类',
  },
  tooltip: {
    formatter: (params) => {
      return `坐标: (${params.value[0].toFixed(2)}, ${params.value[1].toFixed(2)}, ${params.value[2].toFixed(2)})<br>
              类别: ${params.seriesName}<br>
              标签: ${params.value[3]}`;
    }
  },
  legend:{
    bottom:0,
  }
});

const fetchHistory = async () => {
  isLoadingHistory.value = true;
  try {
    const response = await fetch(`http://localhost:8000/api/visualization/?id=${historyId.value}`);
    if (!response.ok) {
      throw new Error('获取可视化数据失败');
    }
    const data = await response.json();
    
    // 更新历史记录数据
    currentItem.value = data.history || {
      comment: '',
      tfidf: [],
      lda: [],
      textrank: [],
      llm_wo: [],
      llm_w: []
    };

    // 自动初始化 series 基于 type 数据
    if (data.type) {
      // 生成随机但可区分的颜色映射
      const generateDistinctColors = (count) => {
        const colors = [];
        const hueStep = 360 / count;
        const saturation = 70 + Math.random() * 30;  // 70-100%
        const lightness = 50 + Math.random() * 10;   // 50-60%
        
        for (let i = 0; i < count; i++) {
          const hue = Math.floor(i * hueStep + Math.random() * 20);
          colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
        }
        return colors;
      };

      // 获取所有有效的方法键
      const methods = Object.keys(data.type).filter(
        key => data.type[key] && data.type[key].length > 0
      );
      
      const colors = generateDistinctColors(methods.length);

      option1.value.series = [];
      option2.value.series = [];

      methods.forEach((key, index) => {
        option1.value.series.push({
          type: 'scatter3D',
          name: key,
          data: data.type[key],
          symbolSize: 14,
          itemStyle: {
            color: colors[index]
          },
          label: {
            show: true,
            formatter: (params) => params.value[3],
            textStyle: {
              fontSize: 12,
              color: '#333',
              backgroundColor: 'rgba(255,255,255,0.7)',
              padding: [2, 4],
              borderRadius: 2,
            },
            position: 'top',
          },
          emphasis: {
            label: {
              show: true,
            },
          }
        });
      });
    }
    
    if (data.cluster) {
      // 生成随机但可区分的颜色映射
      const generateDistinctColors = (count) => {
        const colors = [];
        const hueStep = 360 / count;
        const saturation = 70 + Math.random() * 30;  // 70-100%
        const lightness = 50 + Math.random() * 10;   // 50-60%
        
        for (let i = 0; i < count; i++) {
          const hue = Math.floor(i * hueStep + Math.random() * 20);
          colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
        }
        return colors;
      };

      // 获取所有有效的方法键
      const methods = Object.keys(data.cluster).filter(
        key => data.cluster[key] && data.cluster[key].length > 0
      );
      
      const colors = generateDistinctColors(methods.length);

      option2.value.series = [];

      methods.forEach((key, index) => {
        option2.value.series.push({
          type: 'scatter3D',
          name: key,
          data: data.cluster[key],
          symbolSize: 14,
          itemStyle: {
            color: colors[index]
          },
          label: {
            show: true,
            formatter: (params) => params.value[3],
            textStyle: {
              fontSize: 12,
              color: '#333',
              backgroundColor: 'rgba(255,255,255,0.7)',
              padding: [2, 4],
              borderRadius: 2,
            },
            position: 'top',
          },
          emphasis: {
            label: {
              show: true,
            },
          }
        });
      });
    }

    hasChartData.value = true;
    
  } catch (error) {
    console.error('获取可视化数据失败:', error);
    alert('获取可视化数据失败，请稍后重试');
  } finally {
    isLoadingHistory.value = false;
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
    padding: 30px;
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
    border: 1px solid #d0e3ff;
}

.no-data {
    color: #999;
    font-size: 13px;
    font-style: italic;
}

.history-divider {
    height: 2px;
    background-color: #d0d0d0;
    margin: 16px 0;
}

.chart-container {
    background: white;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
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