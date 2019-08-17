<template>
  <div>
    <img src="../images/1_bg1.png" />
    <main-show-top></main-show-top>
    <el-row>
      <main-show :showStudying="true"></main-show>
      <el-col :span="1">&nbsp;</el-col>
      <el-col :span="12">
        <div class="white-box">
          <div class="white-box-top">
            <img src="../images/4_class1.png" class="image-class" />
            <label class="title-font">{{title}}</label>
            <div class="timer">{{timeObj.tmpTimeStr}}</div>
          </div>
          <div class="white-box-middle">
            <en-to-zn
              v-if="current.question_type === '中选英'"
              :number="num"
              :option="current"
              @sendAnswer="nextWord"
            ></en-to-zn>
            <en-to-zn
              v-if="current.question_type === '英选中'"
              :number="num"
              :option="current"
              @sendAnswer="nextWord"
            ></en-to-zn>
            <listen-to-zn v-if="current.question_type === '听选中'" :option="current"></listen-to-zn>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
const axios = require('axios')
import MainShow from './common/MainShow'
import MainShowTop from './common/MainShowTop'
import EnToZn from './common/EnToZn'
import ListenToZn from './common/ListenToZn'
export default {
  data: function () {
    return {
      word: [],
      alterWord: [],
      oneWord: {},
      score: 0,
      num: 0,
      left: 0,
      right: 0,
      studentId: 0,
      bookId: 1,
      groupNum: 0, //每组已学单词数
      groupRightNum: 0, //每组答对单词数
      middle: 0,
      group: 0, //最大组数
      groupMaxNum: 3, //每组测试单词数
      maxNum: 28,
      preQuestionId: [],
      preQuestion: {
        question_set: [],
        student_id: '',
        book_id: ''
      },
      current: {},
      oneGroupCount: 5,
      title: '',
      timeObj: {
        m: 0,
        s: 0,
        timeClear: 0,
        tmpTimeStr: '00:00'
      }
    }
  },
  methods: {
    nextWord: function (isRight) {
      if (this.$route.params.type === 'preTest') {
        this.preTest(isRight)
      } else if (this.$route.params.type === 'reviewTest') {
        this.otherTest(isRight)
      } else if (this.$route.params.type === 'afterTest') {
        this.otherTest(isRight)
      } else if (this.$route.params.type === 'allTest') {
        this.allTest(isRight)
      }
    },
    preTest: function (isRight) {
      if (this.num < this.maxNum) {
        if (isRight === true) {
          this.groupRightNum += 1
        }
        this.num += 1
        if (this.middle !== this.group) {
          if (this.groupNum < this.groupMaxNum) {
            let index = this.word.indexOf(this.oneWord) + 1
            this.oneWord = this.word[index]
            this.current = this.oneWord.question
            this.preQuestionId.push(this.oneWord.id)
            this.groupNum += 1
          } else {
            if (this.groupRightNum < Math.ceil(this.groupMaxNum / 2)) {
              this.right = this.middle - 1
            } else {
              this.left = this.middle + 1
            }
            if (this.left < this.right) {
              this.middle = Math.floor((this.left + this.right) / 2)
              let index = this.groupMaxNum * (this.middle - 1)
              this.oneWord = this.word[index]
              this.current = this.oneWord.question
              this.preQuestionId.push(this.oneWord.id)
              this.groupNum = 1
            } else if (this.left === this.right) {
              let index = (this.left - 1) * this.groupMaxNum
              this.oneWord = this.word[index]
              this.current = this.oneWord.question
              this.preQuestionId.push(this.oneWord.id)
              this.middle = this.left
              this.groupNum = 1
            } else {
              this.$message({
                message: '你已完成测试',
                type: 'success'
              })
              this.sendPreLog()
              this.sendTestLog()
              clearInterval(this.timeObj.timeClear)
              this.$router.push('/beforestudying')
            }
          }
        } else {
          if (this.word.indexOf(this.oneWord) < this.word.length - 1) {
            let index = this.word.indexOf(this.oneWord) + 1
            this.oneWord = this.word[index]
            this.current = this.oneWord.question
            this.preQuestionId.push(this.oneWord.id)
          } else {
            this.$message({
              message: '你已完成测试',
              type: 'success'
            })
            this.sendPreLog()
            this.sendTestLog()
            clearInterval(this.timeObj.timeClear)
            this.$router.push('/beforestudying')
          }
        }
      }
    },
    otherTest: function (isRight) {
      if (isRight === true) {
        this.score += 1
      }
      this.num += 1
      let index = this.word.indexOf(this.oneWord) + 1
      if (index < this.word.length) {
        this.oneWord = this.word[index]
        this.current = this.oneWord.fields
      } else {
        this.$message({
          message: '你已完成测试',
          type: 'success'
        })
        this.sendTestLog()
        clearInterval(this.timeObj.timeClear)
        this.$router.push('/beforestudying')
      }
    },
    allTest: function (isRight){
      if (isRight === true) {
        this.score += 1
      }
      this.num += 1
      let index = this.word.indexOf(this.oneWord) + 1
      if (index === 3){
        this.group += 1
        axios.get(
          this.$store.state.BASEURL +
        'study/get_book_test?book_id=' +
        this.bookId +
        '&group=' +
        this.group +
        '&oneGroupCount=' +
        this.oneGroupCount
        ).then(
          res=>{
            if (res.data !== 'none'){
              this.alterWord = res.data
            }
          }
        )
      }
      if (index < this.word.length) {
        this.oneWord = this.word[index]
        this.current = this.oneWord.fields
      } else {
        if (this.alterWord.length > 0){
          this.word = this.alterWord
          this.alterWord = []
          this.oneWord = this.word[0]
          this.current = this.oneWord.fields
        } else {
          this.$message({
            message: '你已完成测试',
            type: 'success'
          })
          this.sendTestLog()
          clearInterval(this.timeObj.timeClear)
          this.$router.push('/beforestudying')
        }
      }
    },
    sendPreLog: function () {
      this.preQuestion.question_set = this.preQuestionId
      this.preQuestion.student_id = this.studentId
      this.preQuestion.book_id = this.bookId
      const url = this.$store.state.BASEURL + 'study/add_pretest_log'
      axios.post(url, JSON.stringify(this.preQuestion)).then()
    },
    sendTestLog: function () {
      if (this.$route.params.type === 'preTest') {
        this.score =
          ((this.word.indexOf(this.oneWord) + 1) / this.word.length) * 100
      } else {
        this.score = (this.score / (this.num - 1)) * 100
      }
      this.score = Math.round(this.score)
      axios
        .get(
          this.$store.state.BASEURL +
            'study/add_test_log?student_id=' +
            this.studentId +
            '&book_id=' +
            this.bookId +
            '&test_type=' +
            this.$route.params.type +
            '&score=' +
            this.score
        )
        .then()
    },
    addZero (n) {
      if (n < 10) {
        return '0' + n
      } else {
        return '' + n
      }
    },
    addTimer () {
      let timeObj = this.timeObj
      timeObj.s++
      if (timeObj.s > 59) {
        timeObj.s = 0
        timeObj.m++
      }
      let timeStr = this.addZero(timeObj.m) + ':' + this.addZero(timeObj.s)
      timeObj.tmpTimeStr = timeStr
    },
    addTimeFunc () {
      let timeObj = this.timeObj
      clearInterval(timeObj.timeClear)
      timeObj.m = 0
      timeObj.s = 0
      let timeStr = this.addZero(timeObj.m) + ':' + this.addZero(timeObj.s)
      timeObj.tmpTimeStr = timeStr
      timeObj.timeClear = setInterval(this.addTimer, 1000)
    }
  },
  components: {
    MainShow,
    MainShowTop,
    EnToZn,
    ListenToZn
  },
  mounted () {
    this.studentId = sessionStorage.getItem('student')
    this.bookId = this.$store.state.CATEGORY.id
    this.addTimeFunc()
    if (this.$route.params.type === 'preTest') {
      this.title = '学前测试'
      axios
        .get(
          this.$store.state.BASEURL +
            'study/get_pretest_word?student_id=' +
            this.studentId +
            '&category_id=' +
            this.bookId
        )
        .then(res => {
          this.word = res.data
          if (this.$route.params.type === 'preTest') {
            this.group = Math.ceil(this.word.length / this.groupMaxNum)
            this.left = 1
            this.right = this.group
            this.middle = Math.floor((this.left + this.right) / 2)
            let index = this.groupMaxNum * (this.middle - 1)
            this.oneWord = this.word[index]
            this.current = this.oneWord.question
            this.preQuestionId.push(this.oneWord.id)
            this.groupNum += 1
            this.num += 1
          }
        })
    } else if (this.$route.params.type === 'reviewTest') {
      this.title = '巩固测试'
      axios
        .get(
          this.$store.state.BASEURL +
            'study/get_review_test?book_id=' +
            this.bookId +
            '&student_id=' +
            this.studentId
        )
        .then(res => {
          this.word = res.data
          this.oneWord = this.word[0]
          this.current = this.oneWord.fields
          this.num = 1
        })
    } else if (this.$route.params.type === 'afterTest') {
      this.title = '学后测试'
      axios.get(
        this.$store.state.BASEURL +
        'study/get_after_test?book_id=' +
        this.bookId +
        '&student_id=' +
        this.studentId
      ).then(
        res=>{
          this.word = res.data
          this.oneWord = this.word[0]
          this.current = this.oneWord.fields
          this.num = 1
        }
      )
    } else if (this.$route.params.type === 'allTest') {
      this.title = '一测到底'
      this.group = 1
      axios.get(
        this.$store.state.BASEURL +
        'study/get_book_test?book_id=' +
        this.bookId +
        '&group=' +
        this.group +
        '&oneGroupCount=' +
        this.oneGroupCount
      ).then(
        res=>{
          this.word = res.data
          this.oneWord = this.word[0]
          this.current = this.oneWord.fields
          this.num = 1
        }
      )
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  top: 0;
  left: 0;
}

.title-font {
  font-family: "Microsoft YaHei";
  font-size: 16px;
  font-weight: bold;
}

img {
  position: absolute;
  top: 50px;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: -10;
  margin: 0;
  padding: 0;
}

.image-class {
  height: 20px;
  width: 20px;
  position: inherit;
  padding-right: 5px;
  margin-top: 16px;
}

.white-box {
  background-color: white;
  margin-top: 50px;
  border-radius: 5px;
  height: 465px;
  padding: 20px;
  box-shadow: 1px 1px 1px 1px rgb(188, 221, 221);
}

.white-box-top {
  height: 50px;
}

.white-box-middle {
  border-top: 1px solid rgb(197, 197, 197);
  padding-top: 15px;
  padding-left: 10px;
  font-size: 13px;
  font-weight: bold;
}

.timer {
  float: right;
  background: url("../images/28_time1.png") no-repeat;
  height: 120px;
  width: 120px;
  background-size: 120px;
  text-align: center;
  line-height: 40px;
  margin-top: 10px;
  color: rgb(255, 177, 40);
  font-weight: bold;
  padding-left: 8px;
}
</style>
