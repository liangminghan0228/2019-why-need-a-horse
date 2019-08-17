<template>
  <div>
    <main-show-top></main-show-top>
    <img class="background-photo" src="../images/1_bg1.png" alt="background">
    <main-show showStudying="true"></main-show>
    <el-col :span="1">&nbsp;</el-col>
    <el-col :span="13">
      <div class="main-show">
        <h2 class="book-name">{{bookName}}</h2>
        <div class="block-center">
          <img src="../images/56_preschool test.png" alt="testLogo">
          <h6>三分钟测出你的词汇掌握水平</h6>
          <p class="introduce1">根据检测结果定制针对性学习方案</p>
          <p class="introduce2">你需要在3分钟内完成以下题目，请保持专注</p>
          <el-button type="primary" size="small" @click="goTest">立即开始</el-button>
        </div>
      </div>
    </el-col>
  </div>
</template>

<script>
import MainShowTop from './common/MainShowTop'
import MainShow from './common/MainShow'
export default {
  data: function () {
    return {
      bookName: '初中核心词'
    }
  },
  methods: {
    goTest () {
      this.$router.push('/test')
    }
  },
  components: {
    MainShow,
    MainShowTop
  }
}
</script>

<style scoped>
.background-photo {
  position: absolute;
  left: 0;
  top: 50px;
  width: 100%;
  height: 100%;
  overflow-y: hidden;
  z-index: -1000;
}

.main-show {
  margin-top: 60px;
  padding-top: 10px;
  background-color: #fff;
  border-radius: 5px;
  height: 55ex;
  position: relative;
}

.book-name {
  margin-left: 10px;
  font-family: Arial, Helvetica, sans-serif;
}

.block-center {
  position: absolute;
  left: 50%;
  top: 50%;
  text-align: center;
  margin-left: -135px;
  margin-top: -120px;
}

.main-show img {
  height: 150px;
}

h2 {
  padding-left: 50px;
  margin-top: 50px;
  font-family: cursive;
}

h6 {
  color: rgb(152, 152, 152);
  font-weight: 600;
  font-size: 15px;
  margin: 5px;
}

p.introduce1 {
  font-size: 13px;
  color: rgb(152, 152, 152);
}

p.introduce2 {
  font-size: 13px;
  margin-top: 40px;
}
</style>
