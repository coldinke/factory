<script setup>
import Table from "../components/Table.vue";
import HeartMap from "../components/HeartMap.vue";
import { ref, onMounted } from 'vue';
import axios from 'axios';

const apiData = ref([])

const fetchData = (async()=> {
  try {
    const res = await axios.get("http://127.0.0.1:8000/all_sensor_data")
    apiData.value = res.data
  } catch(error) {
    console.error('Error fetching data: ', error);
  }
});

onMounted(() => {
  fetchData();
});

defineExpose({ apiData });
</script>

<template>
  <el-row :gutter="20">
    <el-col :span="12"><HeartMap /></el-col>
    <el-col :span="12"><Table :data="apiData" /></el-col>
  </el-row>
</template>

<style>
.el-row {
  margin-bottom: 0px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.ep-bg-purple {
  background-color: #f5f7fa; /* 与 .grid-content 背景色保持一致 */
}

.chart {
  height: 200px; /* 热力图容器的高度 */
  width: 100%; /* 热力图容器的宽度 */
}
</style>
