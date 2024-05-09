<template>
  <div class="common-layout">
    <el-container>
      <el-header class="header-style">烟叶仓库温度监测系统</el-header>
      <Layout />
    </el-container>
  </div>
</template>

<script setup>
import Layout from "../components/Layout.vue";
</script>
<style scoped>
.header-style {
  justify-content: space-between;
  align-items: center;
  background-color: #6b8e23;
  color: black;
  font-size: 24px;
  padding: 10px 20px; 
  text-align: center;
}
</style>
