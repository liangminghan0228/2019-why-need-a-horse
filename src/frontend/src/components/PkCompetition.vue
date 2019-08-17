<template>
  <div>
    <img class ="bg" src="../images/1_bg1.png" />
    <div class="top">
      <main-show-top></main-show-top>
    </div>
    <el-row>
      <el-col :span="4">&nbsp;</el-col>
      <el-col :span="16">
        <div class="problem-board">
          <img class="vs-img" src="../images/2_vs bg.png" />
          <el-col :span="6">
            <img class="head-img-left" src="../images/avatar2.jpg" />
            <div class="progress-bar1">
              <span class="other-font">{{tensOtherScore}}</span>
              <div class="el-progress-bar__outer">
                <div class="el-progress-bar__inner" :style="{height: otherPercents + '%'}"></div>
              </div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="timing">{{currentTimeLeave}}s</div>
            <div class="input-question">{{currQuestion}}</div>
            <div class="answer-btn">
              <button class="choose" :class="{'active-right': aIsRight, 'other-choose': aIsChoosed}" @click="choose">{{currOptions[0]}}</button>
              <button class="choose" :class="{'active-right': bIsRight, 'other-choose': bIsChoosed}" @click="choose">{{currOptions[1]}}</button>
              <button class="choose" :class="{'active-right': cIsRight, 'other-choose': cIsChoosed}" @click="choose">{{currOptions[2]}}</button>
              <button class="choose" :class="{'active-right': dIsRight, 'other-choose': dIsChoosed}" @click="choose">{{currOptions[3]}}</button>
            </div>
          </el-col>
          <el-col :span="6">
            <img class="head-img-right" src="../images/avatar1.png" />
            <div class="progress-bar2">
              <span class="own-font">{{tensOwnScore}}</span>
              <div class="el-progress-bar__outer">
                <div class="el-progress-bar__inner" :style="{height: percents + '%'}">
                </div>
              </div>
            </div>
          </el-col>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="18">&nbsp;</el-col>
      <el-col :span="1">
        <button class="cancel-button" @click="clickGoExit">退出</button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import MainShowTop from './common/MainShowTop'
const axios = require('axios')
export default {
  data: function () {
    return {
      realLeaveTime: 0,
      questionsNum: 0,
      questionOrder: 0,
      interval: 500,
      standardInterval: 100,
      otherScore: 0,
      other: {},
      percents: 0,
      otherPercents: 0,
      otherChooseId: -1,
      otherUsedTime: 0,
      otherIsRight: false,
      aIsChoosed: false,
      bIsChoosed: false,
      cIsChoosed: false,
      dIsChoosed: false,
      otherFlag: false,
      usedTime: 0,
      ownScore: 0,
      tensOwnScore: 0,
      tensOtherScore: 0,
      clickTimes: 0,
      isWin: false,
      isRight: 0,
      currentTimeLeave: 10,
      duration: 10000,
      questionList: [],
      backResponse: [],
      rightOptionId: 0,
      currOptions: [],
      currQuestion: '',
      choosedAnswer: '-',
      aIsRight: false,
      bIsRight: false,
      cIsRight: false,
      dIsRight: false,
      transFlag: false,
      otherAnswer: '-',
      resultMessage: ''
    }
  },
  components: {
    MainShowTop
  },
  methods: {
    rand () {
      if (this.questionOrder === this.questionNum) {
        return false
      }
      this.currOptions = []
      this.currQuestion = this.questionList[this.questionOrder]['question']
      this.otherUsedTime = this.questionList[this.questionOrder]['time']
      const optionsNum = 4
      this.otherAnswer = this.questionList[this.questionOrder]['other_choose']
      this.rightOptionId = Math.floor(Math.random() * optionsNum)
      let disturbance_options = []
      this.otherIsRight = this.questionList[this.questionOrder]['is_right']
      disturbance_options.push(this.questionList[this.questionOrder]['disturbance_option1'])
      disturbance_options.push(this.questionList[this.questionOrder]['disturbance_option2'])
      disturbance_options.push(this.questionList[this.questionOrder]['disturbance_option3'])
      for (let indexOne = 0, indexTwo = 0; indexOne < optionsNum; indexOne++) {
        if (indexOne === this.rightOptionId) {
          this.currOptions.push(this.questionList[this.questionOrder]['correct_option'])
        } else {
          this.currOptions.push(disturbance_options[indexTwo])
          indexTwo++
        }
      }
      if (this.otherAnswer !== '-') {
        for (let index = 0; index < optionsNum; index++) {
          if (this.questionList[this.questionOrder]['other_choose'] === this.currOptions[index]) {
            this.otherChooseId = index
            break
          }
        }
      } else {
        this.otherChooseId = -1
        this.otherUsedTime = this.duration
      }
    },
    choose (event) {
      if (this.clickTimes !== 0) {
        return false
      }
      this.clickTimes += 1
      this.choosedAnswer = event.target.innerText
      if (this.questionList[this.questionOrder].correct_option === this.choosedAnswer) {
        this.isRight = 1
        if (this.otherFlag === true) {
          if (this.otherIsRight === true) {
            this.otherScore += 1
          } else {
            this.ownScore += 1
          }
        } else {
          this.ownScore += 1
        }
        this.totalRightQuestions += 1
        event.target.style['backgroundColor'] = '#00cc66'
      } else {
        this.isRight = 0
        event.target.style['backgroundColor'] = 'rgb(255, 142, 113)'
      }
      this.backResponse.push({
        'isRight': this.isRight,
        'competitionId': this.$store.state.COMPETITIONID,
        'questionId': this.questionList[this.questionOrder]['question_id'],
        'studentId': sessionStorage.getItem('student'),
        'time': this.usedTime,
        'answer': event.target.innerText
      })
      if (this.isRight === 1) {
        if (this.questionOrder === this.questionsNum - 1) {
          this.goExit()
          return false
        } else {
          this.questionOrder += 1
          this.otherFlag = false
        }
        setTimeout(() => {
          event.target.style['backgroundColor'] = ''
          this.updateShow()
        }, this.interval)
      } else {
        setTimeout(() => {
          event.target.style['backgroundColor'] = ''
        }, this.interval)
      }
    },
    countTime () {
      this.count = setInterval(() => {
        this.realLeaveTime -= 100
      }, this.standardInterval)
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
    highLightOther () {
      if (this.otherChooseId === 3) {
        this.dIsChoosed = true
      } else if (this.otherChooseId === 2) {
        this.cIsChoosed = true
      } else if (this.otherChooseId === 1) {
        this.bIsChoosed = true
      } else {
        if (this.otherChooseId === 0) {
          this.aIsChoosed = true
        }
      }
    },
    clickGoExit () {
      this.resultMessage = '您认输了，您的成绩为：' + this.tensOwnScore
      this.$message({
        type: 'error',
        message: this.resultMessage
      })
      const url = this.$store.state.BASEURL + 'competitions/add_pk_log'
      let param = []
      param.push(this.backResponse)
      param.push(sessionStorage.getItem('student'))
      param.push(this.$store.state.COMPETITIONID)
      param.push(this.tensOwnScore)
      axios.post(url, JSON.stringify(param))
      this.$router.push('/competitiondetails')
    },
    goExit () {
      if (this.ownScore > this.otherScore) {
        this.resultMessage = '恭喜您，获胜了！您的成绩为：' + this.tensOwnScore
        this.$message({
          type: 'success',
          message: this.resultMessage
        })
      } else if (this.ownScore === this.otherScore) {
        this.resultMessage = '获得平局！请再接再厉。您的成绩为：' + this.tensOwnScore
        this.$message({
          type: 'warning',
          message: this.resultMessage
        })
      } else {
        this.resultMessage = '很遗憾，您输了！您的成绩为：' + this.tensOwnScore
        this.$message({
          type: 'error',
          message: this.resultMessage
        })
      }
      const url = this.$store.state.BASEURL + 'competitions/add_pk_log'
      let param = []
      param.push(this.backResponse)
      param.push(sessionStorage.getItem('student'))
      param.push(this.$store.state.COMPETITIONID)
      param.push(this.tensOwnScore)
      axios.post(url, JSON.stringify(param))
      this.$router.push('/competitiondetails')
    },
    eliminate () {
      this.aIsRight = false
      this.bIsRight = false
      this.cIsRight = false
      this.dIsRight = false
      this.aIsChoosed = false
      this.bIsChoosed = false
      this.cIsChoosed = false
      this.dIsChoosed = false
    },
    updateShow () {
      this.eliminate()
      this.choosedAnswer = '-'
      this.rand()
      this.clickTimes = 0
      this.isRight = 0
      this.otherFlag = false
      clearInterval(this.count)
      this.realLeaveTime = this.duration
      this.countTime()
    }
  },
  mounted () {
    const url = this.$store.state.BASEURL + 'competitions/get_pk_data'
    let param = []
    param.push(sessionStorage.getItem('student'))
    param.push(this.$store.state.COMPETITIONID)
    axios.post(url, JSON.stringify(param)).then(res => {
      if (res.data === 'FailResponse') {
        this.clickGoExit()
      } else {
        this.other = res.data['other']
        this.questionList = res.data['pk_data']
        this.questionNum = this.questionList.length
        this.rand()
        this.realLeaveTime = this.duration
        this.countTime()
      }
    })
  },
  watch: {
    ownScore: function () { 
      this.tensOwnScore = this.ownScore * 10
      this.percents = this.ownScore * 3.3
    },    
    otherScore: function () { 
      this.tensOtherScore = this.otherScore * 10
      this.otherPercents = this.otherScore * 3.3
    },
    realLeaveTime: function () {
      this.currentTimeLeave = Math.ceil(this.realLeaveTime / 1000)
      this.usedTime = this.duration - this.realLeaveTime
      if (this.duration - this.realLeaveTime === this.otherUsedTime) {
        this.highLightOther()
        this.otherFlag = true
      }
      if (this.clickTimes === 0) {
        if (this.realLeaveTime === 0) {
          this.isRight = 0
          this.highLightRight()
          this.backResponse.push({
            'isRight': this.isRight,
            'competitionId': this.$store.state.COMPETITIONID,
            'questionId': this.questionList[this.questionOrder]['question_id'],
            'studentId': sessionStorage.getItem('student'),
            'time': this.usedTime,
            'answer': this.choosedAnswer
          })
          if (this.questionOrder === this.questionsNum - 1) {
            this.goExit()
            return false
          } else {
            this.questionOrder += 1
            this.otherFlag = false
          }
          setTimeout(() => {
            this.updateShow()
          }, this.interval)
        }
      }
      if (this.clickTimes === 1) {
        if (this.realLeaveTime === 0 || (this.otherFlag === true && this.otherIsRight === false)) {
          this.isRight = 0
          this.highLightRight()
          if (this.questionOrder === this.questionsNum - 1) {
            this.goExit()
            return false
          } else {
            this.questionOrder += 1
            this.otherFlag = false
          }
          setTimeout(() => {
            this.updateShow()
          }, this.interval)        
        }
      }
    },
    otherFlag: function () {
      if (this.otherFlag === true && this.otherIsRight === true) {
        this.isRight = 0
        this.highLightRight()
        this.backResponse.push({
          'isRight': this.isRight,
          'competitionId': this.$store.state.COMPETITIONID,
          'questionId': this.questionList[this.questionOrder]['question_id'],
          'studentId': sessionStorage.getItem('student'),
          'time': this.usedTime,
          'answer': this.choosedAnswer
        })
        this.otherScore += 1
        if (this.questionOrder === this.questionsNum - 1) {
          this.goExit()
          return false
        } else {
          this.questionOrder += 1
          this.otherFlag = false
        }
        setTimeout(() => {
          this.updateShow()
        }, this.interval)
      }
    },
    questionOrder: function () {
      if (this.questionOrder === this.questionNum) {
        this.goExit()
        return false
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
  height: 90px;
  text-align: center;
}

.problem-board {
  background: #ffffff;
  height: 450px;
  width: 70%;
  z-index: -2;
  border-radius: 5px;
  box-shadow: 0 2px 4px 0 rgb(0, 0, 0, 0.1);
  position: absolute;
  top: 70px;
  left: 50%;
  margin-left: -35%;
  margin-top: 0;
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
  top: 25em;
  border-radius: 5px;
  background-color: #00cc66;
  padding: 0;
  border: 0;
  color: #ffffff;
  box-shadow: 0 2px 4px 1 #00cc66;
}

.input-question {
  margin-top: 4.5em;
}

.choose {
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

.progress-bar1 {
  float: left;
  border-radius: 10px 10px 10px 10px;
  margin-top: 30px;
  margin-right: 60px;
  margin-left: 5em;
  height: 300px;
  width: 60px;
  background: rgb(239, 249, 255);
  position: relative;
}

.progress-bar2 {
  float: right;
  border-radius: 10px 10px 10px 10px;
  margin-top: 30px;
  margin-right: 4em;
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
  top: 85px;
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

.head-img-left {
  height: 60px;
  width: 60px;
  color: #ffffff;
  position: absolute;
  top: 1.5em;
  z-index: 2;
  left: 5em !important;
  background: transparent;
  border-radius: 50%;
  border: 1px solid rgb(0, 194, 255);
}

.head-img-right {
  height: 60px;
  width: 60px;
  color: #ffffff;
  position: absolute;
  right: 4em !important;
  top: 1.5em;
  z-index: 2;
  background: transparent;
  border-radius: 50%;
  border: 1px solid rgb(252, 134, 52);
}

.progress-bar1 /deep/ .el-progress-bar__outer {
  border-radius: 50px;
  background-color: rgb(239, 249, 255);
  overflow: hidden;
  position: relative;
  vertical-align: middle;
  height: 230px;
  width: 20px;
  margin: auto;
  margin-top: 60px;
  border: 2px solid #409eff;
}

.other-font{
  color: #409eff;
  font-weight: bold;
  position: absolute;
  margin-top: 20px;
  left: 20px;
}

.own-font{
  color: rgb(255, 107, 0);
  font-weight: bold;
  position: absolute;
  margin-top: 20px;
  left: 20px;
}

.progress-bar1 /deep/ .el-progress-bar__inner {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: #409eff;
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

.progress-bar2 /deep/ .el-progress-bar__outer {
  border-radius: 50px;
  background-color: rgb(255, 249, 233);
  overflow: hidden;
  position: relative;
  vertical-align: middle;
  height: 230px;
  width: 20px;
  margin: auto;
  margin-top: 60px;
  border: 2px solid rgb(255, 107, 0);
}

.progress-bar2 /deep/ .el-progress-bar__inner {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: rgb(255, 107, 0);
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

.other-choose {
  background-color: #409eff;
}

.active-right {
  border: #00cc66;
  box-shadow: 0 2px 4px 0 #00cc66;
}
</style>
