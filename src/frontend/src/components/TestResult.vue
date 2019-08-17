<template>
  <div class="test-result">
    <el-button type="text" @click="dialogVisible = true">点击打开</el-button>
    <div class="inner">
      <el-dialog :visible.sync="dialogVisible" :close-on-click-modal="false">
        <div class="green-line">【测试结果】</div>
        <div class="tip">
          <br />本次测试
          <span>{{score}}</span>分！收获
          <span>{{coinNumber}}</span>金币！
        </div>
        <div class="pass">
          <div class="choose">
            <span class="hook">✔</span>
          </div>Pass
        </div>
        <div class="fail">
          <div class="choose">
            <span class="hook">✔</span>
          </div>Fail
        </div>
        <div class="button-region">
          <el-button type="success" @click="dialogVisible = false">查看学习计划</el-button>
        </div>
        <div class="button-region">
          <el-button type="success" @click="dialogVisible = false">开始学习</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      dialogVisible: false,
      score: 0,
      coinNumber: 0,
      result: '✔'
    }
  }
}
</script>


<style scoped>
.test-result {
  position: absolute;
  width: 100%;
  height: 100%;
}

.inner {
  position: absolute;
  left: 50%;
  top: 40%;
  margin-top: -12%;
  margin-left: -15%;
  width: 35%;
  height: 50%;
  overflow: hidden;
}

.green-line {
  height: 10%;
  width: 100%;
  background-color: rgb(150, 191, 1);
  color: rgb(235, 245, 220);
  text-align: left;
  font-size: 3vh;
}

.tip {
  width: 100%;
  height: 30%;
  text-align: center;
  font-size: 2vw;
  font-weight: bolder;
  color: rgb(0, 128, 0);
}

.inner /deep/ .el-dialog__wrapper {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.inner /deep/ .el-dialog__header {
  display: none;
}

.inner /deep/ .el-dialog {
  padding: 0;
  width: 100%;
  height: 100%;
  margin: 0 !important;
}

.inner /deep/ .el-dialog__body {
  padding: 0;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

span {
  color: rgb(255, 0, 0);
  font-size: 3.5vw;
}

.choose {
  position: absolute;
  top: 10%;
  left: 25%;
  height: 3vw;
  width: 3vw;
  border: 0.2vh solid rgb(248, 75, 60);
}

.hook {
  color: rgb(130, 190, 55);
  font-weight: bolder;
  font-size: 6vw;
  position: absolute;
  bottom: -3vh;
  right: -1.5vw;
}

.pass {
  width: 100%;
  height: 15%;
  font-size: 3vw;
  font-weight: bolder;
  text-align: center;
  color: rgb(100, 145, 40);
  position: relative;
}

.fail {
  width: 100%;
  height: 15%;
  font-size: 3vw;
  font-weight: bolder;
  text-align: center;
  color: rgb(255, 55, 35);
  position: relative;
}

.el-button--success {
  width: 40%;
  height: 50%;
  font-size: 1.5vw;
  padding: 0;
  position: absolute;
  left: 30%;
  top: 30%;
  background-color: rgb(0, 128, 2);
  color: rgb(250, 250, 250);
  border-radius: 5px;
}

.button-region {
  position: relative;
  width: 100%;
  height: 15%;
}
</style>
