<template>
  <div class="container">
    <h1>电商用户评论问题分类与标签自动生成系统</h1>
    <div class="divider"></div>
  </div>
</template>

<style scoped>
.container {
  grid-area: header;
  position: static;
  background: linear-gradient(135deg, rgb(40, 198, 255), rgb(134, 47, 255));
  color: white;
  padding: 20px 0;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 10;
}

.container h1 {
  font-size: 30px;
  margin: 0;
  font-weight: 500;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.container h1 i {
  margin-right: 10px;
}

.divider {
  height: 2px;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.5), transparent);
  margin: 8px auto 0;
  width: 80%;
}
</style>