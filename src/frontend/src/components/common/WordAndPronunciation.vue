<template>
  <div class="word-container">
    <p class="word">{{word}}</p>
    <p class="pronunciation">{{pronunciation}}</p>
    <el-button type="warning" plain round class="el-btn-pron">
      <img src="../../images/42_voice2.png" class="card-img">
      <label class="card-label">英</label>
    </el-button>
    <el-button type="info" plain round class="el-btn-pron">
      <img src="../../images/43_voice3.png" class="card-img">
      <label class="card-label">美</label>
    </el-button>
  </div>
</template>

<script>
export default {
  data: function () {
    return {}
  },
  props: ['word', 'pronunciation']
}
</script>

<style scoped>
.word-container {
  margin-top: 10px;
  margin-bottom: 15px;
}

.word {
  font-size: 28px;
  font-weight: bold;
  height: 28px;
  color: #484848;
}

.pronunciation {
  display: inline;
  font-size: 20px;
  color: #888;
  margin-right: 30px;
}

.el-btn-pron {
  border: 0;
  position: relative;
  height: 30px;
  width: 85px;
  outline: none;
}

.card-img {
  position: absolute;
  left: 20px;
  top: 5px;
  width: 20px;
  height: 20px;
}

.card-label {
  position: absolute;
  right: 18px;
  top: 7px;
  font-size: 15px;
}
</style>
