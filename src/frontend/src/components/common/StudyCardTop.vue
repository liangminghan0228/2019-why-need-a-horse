<template>
  <div class="top-container">
    <el-dialog
      :visible.sync="centerDialogVisible"
      width="30%"
      center
      :close-on-click-modal="false">
      <span slot="footer" class="dialog-footer">
        <img src="../../images/63_intervalCard.png" class="dialog-img" />
        <el-button type="primary" @click="goToTomato">开始复习</el-button>
      </span>
    </el-dialog>
    <div class="label-container">
      <span class="word-label">当前生词数: {{wordCount}}</span>
      <span class="recall-label">回想次数: {{recallCount}}</span>
    </div>
    <dir class="time-container">
      <div class="time-div">
        <img src="../../images/31_time4.png" class="time-img">
        <span class="countdown">{{timeObj.tmpTimeStr}}</span>
        <img src="../../images/40_music.png" class="music-img">
      </div>
    </dir>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      timeObj: {
        m: 0,
        s: 0,
        timeClear: 0,
        tmpTimeStr: '00:00'
      },
      centerDialogVisible: false
    }
  },
  props: ['wordCount', 'recallCount'],
  methods: {
    addZero (n) {
      if (n < 10) {
        return '0' + n
      } else {
        return '' + n
      }
    },
    addTimer () {
      let timeObj = this.timeObj
      this.$store.state.STUDYMINUTE = timeObj.m
      this.$store.state.STUDYSECOND = timeObj.s
      timeObj.s++
      if (timeObj.s > 59) {
        timeObj.s = 0
        timeObj.m++
      }
      let timeStr = this.addZero(timeObj.m) + ':' + this.addZero(timeObj.s)
      timeObj.tmpTimeStr = timeStr
      if (timeObj.m >= 25) {
        clearInterval(timeObj.timeClear)
        this.centerDialogVisible = true
        this.$store.state.STUDYMINUTE = 0
        this.$store.state.STUDYSECOND = 0
        this.$store.state.TOMATO_COUNT += 1
        return
      }
    },
    addTimeFunc () {
      let timeObj = this.timeObj
      clearInterval(timeObj.timeClear)
      timeObj.m = this.$store.state.STUDYMINUTE
      timeObj.s = this.$store.state.STUDYSECOND + 1
      let timeStr = this.addZero(timeObj.m) + ':' + this.addZero(timeObj.s)
      timeObj.tmpTimeStr = timeStr
      timeObj.timeClear = setInterval(this.addTimer, 1000)
    },
    goToTomato () {
      this.centerDialogVisible = true
      this.$router.push('/tomatocard')
    }
  },
  mounted () {
    this.addTimeFunc()
  }
}
</script>

<style scoped>
.top-container {
  margin-top: 10px;
  height: 50px;
  line-height: 50px;
}

.label-container {
  margin-top: 20px;
  float: left;
}

.word-label {
  font-size: 14px;
  color: #303030;
  margin-right: 30px;
}

.recall-label {
  font-size: 14px;
  color: #303030;
}

.time-container {
  float: right;
}

.time-div {
  position: relative;
  display: inline;
}

.time-img {
  height: 30px;
  width: 100px;
  margin-right: 15px;
  line-height: 30px;
}

.countdown {
  position: absolute;
  top: -20px;
  left: 38px;
  font-size: 14px;
  color: #303030;
}

.music-img {
  position: relative;
  top: 10px;
  height: 48px;
  width: 48px;
}

.dialog-img {
  margin-left: 8%;
  margin-bottom: 10%;
  width: 250px;
  height: 250px;
}
</style>
