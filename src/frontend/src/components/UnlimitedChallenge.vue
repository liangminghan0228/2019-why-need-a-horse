<template>
  <div>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <img src="../images/1_bg1.png" />
    <div class="top">
      <main-show-top></main-show-top>
    </div>
    <el-row>
      <el-col :span="4"></el-col>
      <el-col :span="16">
        <div class="problem-board">
          <img class="vs-img" src="../images/2_vs bg.png" />
          <el-col :span="6">
            <div class="error-number">错误{{wrongTimes}}次</div>
            <div class="tools-description">道具</div>
            <div class="tools">
              <div>
                <input class="reduce-number" type="button" @click="useToolsDownTimes"/>
                <p class="errors">错误次数-1</p>
              </div>
              <div>
                <input class="add-time" type="button" @click="useToolsAddTime"/>
                <p class="time">答题时间+2s</p>
              </div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="timing">{{currentTimeLeave}} s</div>
            <div class="input-question">{{currQuestion}}</div>
            <button class="choosea" :class="{'active-right': aIsRight}" @click="choose">{{currOptions[0]}}</button>
            <button class="chooseb" :class="{'active-right': bIsRight}" @click="choose">{{currOptions[1]}}</button>
            <button class="choosec" :class="{'active-right': cIsRight}" @click="choose">{{currOptions[2]}}</button>
            <button class="choosed" :class="{'active-right': dIsRight}" @click="choose">{{currOptions[3]}}</button>
          </el-col>
          <el-col :span="6">
            <img class="head-img" src="../images/avatar3.jpg" />
            <div class="progress-bar">
              <span class="own-font">{{tensScore}}</span>
              <div class="el-progress-bar__outer">
                <div class="el-progress-bar__inner" :style="{height: score + '%'}"></div>
              </div>
            </div>
          </el-col>
        </div>
      </el-col>
      <el-col :span="4"></el-col>
    </el-row>
    <el-row>
      <el-col :span="18">&nbsp;</el-col>
      <el-col :span="1">
        <button class="cancel-button" @click="goExit">退出</button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
const axios = require('axios')
import MainShowTop from './common/MainShowTop'
export default {
  components: {
    MainShowTop
  },
  data: function () {
    return {
      tensScore: 0,
      groupQuestionNum: 10,
      questionOrder: 0,
      maxWrongTimes: 5,
      wrongTimes: 0,
      duration: 10,
      totalRightQuestions: 0,
      currentTimeLeave: 6,
      interval: 500,
      standardInterval: 1000,
      questionListShow: [],
      questionListStore: [],
      backResponse: [],
      question: [],
      totalCoins: 0,
      coinCost: 50,
      score: 0,
      isRight: 0,
      currQuestion: '',
      currOptions: [],
      rightOptionId: 0,
      aIsRight: false,
      bIsRight: false,
      cIsRight: false,
      dIsRight: false,
      transFlag: false,
      getFlag: false
    }
  },
  methods: {
    useToolsAddTime () {
      if (this.totalCoins < this.coinCost) {
        this.$message({
          type: 'warning',
          message: '金币不足！'
        })
        return false
      } else {
        this.$message({
          type: 'success',
          message: '使用成功！金币-50'
        })
        this.currentTimeLeave += 2
        this.totalCoins -= this.coinCost
        return true
      }
    },
    useToolsDownTimes () {
      if (this.totalCoins < this.coinCost) {
        this.$message({
          type: 'warning',
          message: '金币不足！'
        })
        return false
      } else {
        if (this.wrongTimes > 0) {
          this.$message({
            type: 'success',
            message: '使用成功！金币-50'
          })
          this.wrongTimes -= 1
          this.totalCoins -= this.coinCost
          return true
        } else {
          this.$message({
            type: 'warning',
            message: '并未错误，无需使用该道具！'
          })
          return false
        }
      }
    },
    rand () {
      this.currOptions = []
      this.currQuestion = this.questionListShow[this.questionOrder].fields.question
      const optionsNum = 4
      this.rightOptionId = Math.floor(Math.random() * optionsNum)
      let disturbance_options = []
      disturbance_options.push(this.questionListShow[this.questionOrder].fields.disturbance_option1)
      disturbance_options.push(this.questionListShow[this.questionOrder].fields.disturbance_option2)
      disturbance_options.push(this.questionListShow[this.questionOrder].fields.disturbance_option3)
      for (let i = 0, j = 0; i < optionsNum; i++) {
        if (i === this.rightOptionId) {
          this.currOptions.push(this.questionListShow[this.questionOrder].fields.correct_option)
        } else {
          this.currOptions.push(disturbance_options[j])
          j++
        }
      }
    },
    goExit () {
      this.$message({
        type: 'error',
        message: '很遗憾！挑战失败。您的得分为' + this.tensScore
      })
      const url = this.$store.state.BASEURL + 'competitions/add_infinite_challenge_log'
      let paramx = []
      paramx.push(this.backResponse)
      paramx.push(sessionStorage.getItem('student'))
      paramx.push(this.$store.state.COMPETITIONID)
      paramx.push(this.tensScore)
      axios.post(url, JSON.stringify(paramx)).then(res => {
        if (res.data === 'SuccessInsert') {
          this.backResponse = []
          return
        }
      })
      let param = []
      param.push(sessionStorage.getItem('student'))
      param.push(this.totalCoins)
      axios.post(this.$store.state.BASEURL + 'competitions/update_coins', JSON.stringify(param))
      this.$router.push('/competitiondetails')
    },
    highLightRight () {
      if (this.rightOptionId === 3) {
        this.dIsRight = true
      } else if (this.rightOptionId === 2) {
        this.cIsRight = true
      } else if (this.rightOptionId === 1) {
        this.bIsRight = true
      } else {
        this.aIsRight = true
      }
    },
    eliminate () {
      this.aIsRight = false
      this.bIsRight = false
      this.cIsRight = false
      this.dIsRight = false
    },
    choose (event) {
      if (this.questionListShow[this.questionOrder].fields.correct_option === event.target.innerText) {
        this.isRight = 1
        this.score += 1
        this.totalRightQuestions += 1
      } else {
        this.isRight = 0
        event.target.style['backgroundColor'] = 'rgb(255, 142, 113)'
        this.wrongTimes += 1
      }
      this.highLightRight()
      this.backResponse.push({
        'isRight': this.isRight,
        'competitionId': this.$store.state.COMPETITIONID,
        'questionId': this.questionListShow[this.questionOrder].pk,
        'studentId': sessionStorage.getItem('student')
      })
      if (this.questionOrder === this.groupQuestionNum - 1) {
        this.questionOrder = 0
        this.transfer()
        let paramx = []
        paramx.push(this.backResponse)
        paramx.push(sessionStorage.getItem('student'))
        paramx.push(this.$store.state.COMPETITIONID)
        paramx.push(this.tensScore)
        const url = this.$store.state.BASEURL + 'competitions/add_infinite_challenge_log'
        axios.post(url, JSON.stringify(paramx)).then(res => {
          if (res.data === 'SuccessInsert') {
            this.backResponse = []
          }
        })
      } else {
        this.questionOrder += 1
      }
      setTimeout(() => {
        this.updateShow()
        event.target.style['backgroundColor'] = ''
      }, this.interval)
    },
    updateShow () {
      this.eliminate()
      this.rand()
      clearInterval(this.count)
      this.currentTimeLeave = this.duration
      this.countTime()
    },
    countTime () {
      this.count = setInterval(() => {
        this.currentTimeLeave -= 1
      }, this.standardInterval)
    },
    getGroupQuestion () {
      const url = this.$store.state.BASEURL + 'competitions/get_group_question'
      let param = []
      param.push(this.groupQuestionNum)
      param.push(this.$store.state.COMPETITIONID)
      axios.post(url, JSON.stringify(param)).then(res => {
        this.questionListStore = res.data
      })
    },
    transfer () {
      this.questionListShow = this.questionListStore
      this.transFlag = true
    }
  },
  mounted () {
    const url = this.$store.state.BASEURL + 'competitions/get_group_question'
    let param = []
    param.push(this.groupQuestionNum)
    param.push(this.$store.state.COMPETITIONID)
    axios.post(url, JSON.stringify(param)).then(res => {
      if (res.data === 'FailResponse') {
        this.$router.push('/competitiondetails')
      } else {
        this.questionListStore = res.data
        this.transfer()
        this.updateShow()
      }
    })
    axios.get(this.$store.state.BASEURL +
      'competitions/get_total_coins?student_id=' +
      sessionStorage.getItem('student')).then(res => {
      if (res.data !== 'FailResponse') {
        this.totalCoins = res.data
      }
    })
  },
  watch: {
    score: function () {
      this.tensScore = this.score * 10
    },
    wrongTimes: function () {
      if (this.wrongTimes === this.maxWrongTimes - 1) {
        setTimeout(() => {
          this.$message({
            type: 'warning',
            message: '错误次数即将达到上限，您可以使用道具，否则再次错误挑战失败自动退出！'
          })
        }, this.interval)
      }
      if (this.wrongTimes === this.maxWrongTimes) {
        this.goExit()
      }
    },
    transFlag: function () {
      if (this.transFlag === true) {
        this.getGroupQuestion()
        this.transFlag = false
      }
    },
    currentTimeLeave: function () {
      if (this.currentTimeLeave === 0) {
        this.isRight = 0
        this.wrongTimes += 1
        this.highLightRight()
        this.backResponse.push({
          'isRight': this.isRight,
          'competitionId': this.$store.state.COMPETITIONID,
          'questionId': this.questionListShow[this.questionOrder].pk,
          'studentId': sessionStorage.getItem('student')
        })
        if (this.questionOrder === this.groupQuestionNum - 1) {
          this.questionOrder = 0
          this.transfer()
          let paramx = []
          paramx.push(this.backResponse)
          paramx.push(sessionStorage.getItem('student'))
          paramx.push(this.$store.state.COMPETITIONID)
          paramx.push(this.tensScore)
          const url = this.$store.state.BASEURL + 'competitions/add_infinite_challenge_log'
          axios.post(url, JSON.stringify(paramx)).then(res => {
            if (res.data === 'SuccessInsert') {
              this.backResponse = []
            }
          })
        } else {
          this.questionOrder += 1
        }
        setTimeout(() => {
          this.updateShow()
        }, this.interval)
      }
    }
  }
}
</script>

<style scoped>
img {
  top: 0;
  position: absolute;
  width: 100%;
  margin: 0;
  padding: 0;
  z-index: -3;
}

.top {
  background-color: white;
  height: 50px;
}

.el-col {
  border-radius: 4px;
  text-align: center;
  height: auto;
}

.problem-board {
  position: absolute;
  top: 70px;
  left: 50%;
  margin-left: -35%;
  margin-top: 0;
  background: #ffffff;
  height: 450px;
  width: 70%;
  z-index: -2;
  border-radius: 5px;
}

.vs-img {
  position: relative;
  height: 75px;
  z-index: 1;
  border-radius: 5px;
}

.cancel-button {
  height: 26px;
  width: 120px;
  margin-top: 15px;
  position: absolute;
  top: 38em;
  border-radius: 5px;
  background-color: #00cc66;
  padding: 0;
  border: 0;
}

.input-question {
  margin-top: 4.5em;
}

.choosea {
  margin-top: 20px;
  height: 30px;
  width: 80%;
  border-radius: 10px;
  background-color: #ffffff;
  color: black;
  padding: 0;
  border: 1px solid #c0c0c0;
  outline: none;
  z-index: 1000;
}

.active-right {
  background-color: rgb(74, 199, 103) !important;
}

.chooseb {
  margin-top: 20px;
  height: 30px;
  width: 80%;
  border-radius: 10px;
  background-color: #ffffff;
  color: black;
  padding: 0;
  border: 1px solid #c0c0c0;
  outline: none;
}

.choosec {
  margin-top: 20px;
  height: 30px;
  width: 80%;
  border-radius: 10px;
  background-color: #ffffff;
  color: black;
  padding: 0;
  border: 1px solid #c0c0c0;
  outline: none;
}

.choosed {
  margin-top: 20px;
  height: 30px;
  width: 80%;
  border-radius: 10px;
  background-color: #ffffff;
  color: black;
  padding: 0;
  border: 1px solid #c0c0c0;
  outline: none;
}

.tools-description {
  float: left;
  border-radius: 10px 10px 0 0;
  margin-top: 50px;
  margin-left: 40px;
  height: 30px;
  width: 150px;
  padding: 10px 0 0 0;
  color: #ffffff;
  background: rgb(46, 180, 255);
}

.tools {
  margin-left: 40px;
  width: 150px;
  height: 220px;
  background: rgb(239, 249, 255);
  margin-top: 90px;
  border-radius: 0 0 10px 10px;
}

.reduce-number {
  display: inline-block;
  margin-top: 20px;
  background: transparent;
  width: 60px;
  height: 60px;
  border: 1px solid rgb(46, 180, 255);
  background: url("../images/9_tools.png") no-repeat center center;
  background-size: 40px 40px;
  outline: none;
}

.add-time {
  display: block;
  background: transparent;
  width: 60px;
  height: 60px;
  margin-left: auto;
  margin-right: auto;
  border: 1px solid rgb(252, 134, 52);
  background: url("../images/30_time3.png") no-repeat center center;
  background-size: 40px 40px;
  outline: none;
}

p {
  font-size: 12px;
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bolder;
}

.errors {
  color: rgb(46, 180, 255);
}

.time {
  color: rgb(252, 134, 52);
}

.progress-bar {
  float: right;
  border-radius: 10px 10px 10px 10px;
  margin-top: 30px;
  margin-right: 5em;
  height: 300px;
  width: 60px;
  background: rgb(255, 249, 233);
  position: relative;
}

.error-number {
  height: 40px;
  width: 60px;
  color: #ffffff;
  position: absolute;
  top: 23px;
  z-index: 2;
  margin-left: 80px;
  padding: 20px 0 0 0;
  background: rgb(255, 99, 99);
  border-radius: 50%;
  font-size: 12px;
  text-align: center;
  border: 1px solid #ffffff;
}

.timing {
  height: 26px;
  width: 96px;
  padding: 6px 0 0 0;
  margin-left: 155px;
  color: #ffffff;
  position: absolute;
  top: 35px;
  left: 50%;
  margin-left: -48px;
  z-index: 1000;
  background: rgb(34, 112, 156);
  border-radius: 20px;
  font-size: 16px;
  font-weight: bolder;
  font-family: KaiTi;
  text-align: center;
  border: 3px solid rgb(0, 194, 255);
  background-image: url("../images/26_lightning.png");
  background-repeat: no-repeat;
  background-position-x: 6px;
  background-position-y: 3px;
  background-size: 18px 24px;
  box-shadow: 0 4px 4px 0 rgb(197, 235, 255);
}

.head-img {
  height: 60px;
  width: 60px;
  color: #ffffff;
  position: absolute;
  right: 5em;
  top: 1.5em;
  z-index: 2;
  background: transparent;
  border-radius: 50%;
  border: 1px solid rgb(252, 134, 52);
}

.choose:active {
  background-color: #00cc66;
}

.reduce-number:active {
  background-color: rgb(46, 180, 255);
}

.add-time:active {
  background-color: rgb(252, 134, 52);
}

.own-font{
    color: rgb(255,107,0);
    font-weight: bold;
    position: absolute;
    margin-top: 20px;
    left: 20px;
}

.progress-bar /deep/ .el-progress-bar__outer {
  border-radius: 50px;
  background-color: rgb(255, 249, 233);
  overflow: hidden;
  position: relative;
  vertical-align: middle;
  height: 230px;
  width: 20px;
  margin: auto;
  margin-top: 60px;
  border: 2px solid rgb(255,107,0);
}

.progress-bar /deep/ .el-progress-bar__inner {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: rgb(255,107,0);
  text-align: right;
  line-height: 1;
  white-space: nowrap;
  transition: width 0.6s ease;
  background-image: repeating-linear-gradient(
    30deg,
    hsla(0, 0%, 100%, 0.1),
    hsla(0, 0%, 100%, 0.1) 15px,
    transparent 0,
    transparent 30px
  );
  border-radius: 20px;
  top: unset;
}
</style>
