<template>
  <h2>继电器状态</h2>
  <el-row :span="6">
    <div class="flex flex-col items-start gap-4">
      <el-statistic :value="stateText" :title="title">
        <template #suffix>
          <span v-if="loading" class="text-sm text-gray-500">获取中...</span>
        </template>
      </el-statistic>
    </div>
  </el-row>
  <h2>节点列表</h2>
  <el-table :data="data" style="width: 100%">
    <el-table-column prop="nodeno" label="节点" width="180" />
    <el-table-column prop="temperature" label="温度" width="180" />
    <el-table-column prop="timestamp" label="查询时间">
      <template #default="scope">
        {{ formatTimestamp(scope.row.timestamp) }}
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { ElMessageBox } from "element-plus";

const open = () => {
  ElMessageBox.alert("当前仓库温度已达到 35 ℃", "警告", {
    confirmButtonText: "OK",
  });
};

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
});

const formatTimestamp = (timestamp) => {
  return new Date(timestamp).toLocaleString();
};

const stateText = ref('')
const title = ref('继电器状态')
const loading = ref(true)

const getState = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/control_state')
    const state = res.data.state
    stateText.value = state === 1 ? '开' : state === 0 ? '关' : '初始化'
    if (state === 1) {
      // ElMessage.warning('继电器已打开，请注意安全!')
      open();
    }
  } catch (error) {
    console.error('获取继电器状态失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  getState();
  if (stateText.value === '开') {
    open();
  }
});
</script>
