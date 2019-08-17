<template>
  <div class="inteval-card">
    <div class="inner">
      <el-dialog class="dialog" :visible.sync="dialogVisible" :close-on-click-modal="false">
        <img src="../../images/63_intervalCard.png" />
        <el-button type="success" @click="dialogVisible = false">开始学习</el-button>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {}
  },
  props: {
    dialogVisible: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.inteval-card {
  position: absolute;
  width: 100%;
  height: 100%;
}

.inner {
  position: relative;
  left: 50%;
  top: 40%;
  margin-top: -320px;
  margin-left: -500px;
  width: 1000px;
  height: 1000px;
  overflow: hidden;
}

img {
  margin-left: 30px !important;
}

.el-button--success {
  width: 250px;
  height: 50px;
  line-height: 50px;
  font-size: 20px;
  padding: 0;
  margin-left: 90px;
  margin-top: 40px;
}
.inner /deep/ .dialog {
  overflow: hidden;
  position: absolute;
  height: 100%;
  width: 100%;
}
</style>
