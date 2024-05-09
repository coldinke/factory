<template>
  <v-chart class="chart" :option="option" autoresize />
</template>

<script setup>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { HeatmapChart } from "echarts/charts";
import {
  GridComponent,
  VisualMapComponent,
  TooltipComponent,
} from "echarts/components";
import VChart from "vue-echarts";
import { ref,  onMounted } from "vue";
import axios from "axios";

use([
  CanvasRenderer,
  GridComponent,
  VisualMapComponent,
  HeatmapChart,
  TooltipComponent,
]);
const apiData = ref([])
const flatData = ref([]);
const xAxisData = ["10m", "20m"];
const yAxisData = ["10m", "20m", "30m", "40m"];

const getApiData = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/all_sensor_data")
    apiData.value = res.data
    console.log(apiData.value)
  } catch(error) {
    console.error('Error fetching data: ', error);
  }
}

onMounted(async () => {
  await getApiData(); // 确保等待数据获取
  if (apiData.value && apiData.value.length > 0) {
    // console.log('API Data:', apiData.value);
    const sensorData = yAxisData.map((yLabel, yIndex) => {
      return xAxisData.map((xLabel, xIndex) => {
        const nodeData = apiData.value.find(
          (data) => data.nodeno === (xIndex + 1) * (yIndex + 1)
        );
        // console.log(`Node data for (${xIndex + 1},${yIndex + 1}):`, nodeData); // 打印找到的节点数据
        if (nodeData) {
          return [xIndex, yIndex, nodeData.temperature];
        }
        return [xIndex, yIndex, 0];
      });
    });
    flatData.value = sensorData.flat();
    // console.log('Flat Data:', flatData.value); // 打印一维数组
  } else {
    flatData.value = [];
  }
});

const maxValue =  Math.max(...apiData.value.map(data => data.temperature));

const option = ref({
  tooltip: {
    position: "top",
    formatter: (params) => {
      return `Area Temperature: ${params.value[2]}°C`;
    },
  },
  grid: {
    containLabel: true,
    width: "80%",
    height: "80%",
    left: "5%",
    top: "2%",
  },
  xAxis: {
    type: "category",
    data: xAxisData,
    splitArea: {
      show: true,
    },
  },
  yAxis: {
    type: "category",
    data: yAxisData,
    splitArea: {
      show: true,
    },
  },
  visualMap: {
    min: 15,
    max: 40,
    calculable: true,
    orient: "horizontal",
    left: "35%",
    bottom: "10%",
  },
  series: [
    {
      name: "Temperature Heatmap",
      type: "heatmap",
      data: flatData,
      label: {
        show: true,
        color: "#fff",
        formatter: (params) => {
          return `${params.value[2]}°C`;
        },
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: "rgba(0, 0, 0, 0.5)",
        },
      },
    },
  ],
});
</script>

<style scoped>
.chart {
  height: 100vh;
}
</style>
