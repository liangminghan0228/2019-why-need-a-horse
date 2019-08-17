<template>
  <div class="card-container">
    <img src="../images/5_bg2.png" class="img"/>
    <el-row class="header-row">
      <el-col :span="14" :offset="5">
        <study-card-top :wordCount="wordCount" :recallCount="recallCount"></study-card-top>
      </el-col>
    </el-row>
    <el-row class="head-row">
      <el-col :span="14" :offset="5" class="cutain">
        <el-row>
          <el-col :span="16" :offset="4">
            <word-and-pronunciation :word="word.word" :pronunciation="word.pronunciation"></word-and-pronunciation>
            <span class="word-title">单词解释:</span>
            <word-explanation :explain="explain"></word-explanation>
            <span class="word-title">例句：</span>
            <word-sentence :sentence="sentence"></word-sentence>
            <el-button type="danger" class="word-btn" @click="recallWrong"><span class="label-of-btn">2</span>回想错误</el-button>
            <el-button type="success" class="word-btn" @click="recallRight"><span class="label-of-btn">1</span>回想正确</el-button>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
    <button class="next-button" @click="studyOut">退出学习</button>
  </div>
</template>

<script>
const axios = require('axios')
import WordAndPronunciation from './common/WordAndPronunciation'
import StudyCardTop from './common/StudyCardTop'
import WordExplanation from './common/WordExplanation'
import WordSentence from './common/WordSentence'
export default {
  data: function () {
    return {
      word: {},
      wordCount: 7,
      recallCount: 0,
      dialogVisible: false,
      sentence: {},
      explain: ''
    }
  },
  methods: {
    recallRight () {
      if (this.$store.state.WORD_LEVEL < 0) {
        if (this.$store.state.IS_KNOW) {
          this.$store.state.WORD_LEVEL = 5
        } else if (this.$store.state.IS_RECALL) {
          this.$store.state.WORD_LEVEL = 3
        }
        if (!this.$store.state.IS_KNOW && this.$store.state.ISFOUR) {
          this.$store.state.WORD_LEVEL = 1
        }
        this.setWordRank()
      }
      this.$store.state.TOMATO_WORDS.push(this.$store.state.WORD_NOW)
      let index = this.$store.state.WORDS.indexOf(this.$store.state.WORD_NOW)
      if (index === (this.$store.state.WORDS.length - 1)) {
        this.$store.state.WORD_NOW = this.$store.state.WORDS[0]
        this.$store.state.WORD_COUNT = this.$store.state.WORDS.length
        this.$store.state.RECALL_COUNT = 0
        this.$router.push('/spellingcard')
        return
      }
      this.$store.state.WORD_NOW = this.$store.state.WORDS[index + 1]
      this.$store.state.WORD_LEVEL = -1
      this.$store.state.IS_KNOW = false
      this.$store.state.IS_RECALL = false
      this.$store.state.ISFOUR = false
      this.$store.state.WORD_COUNT -= 1
      this.$router.push('/studycardone')
    },
    recallWrong () {
      if (this.$store.state.WORD_LEVEL < 0) {
        if (this.$store.state.IS_KNOW) {
          this.$store.state.WORD_LEVEL = 4
        } else if (this.$store.state.IS_RECALL) {
          this.$store.state.WORD_LEVEL = 2
        }
        if (!this.$store.state.IS_KNOW && this.$store.state.ISFOUR) {
          this.$store.state.WORD_LEVEL = 0
        }
        this.setWordRank()
      }
      this.$router.push('/studycardfour')
    },
    studyOut () {
      this.$router.push('/beforestudying')
    },
    setWordRank () {
      let url = this.$store.state.BASEURL + 'study/set_word_rank?word_id=' + this.$store.state.WORD_NOW.sentence.word + '&student_id=' + sessionStorage.getItem('student') + '&word_level=' + this.$store.state.WORD_LEVEL
      axios.get(url).then(res => {
        if (res.data) {
          return
        }
      })
      url = this.$store.state.BASEURL + 'study/set_word_status?word_id=' + this.$store.state.WORD_NOW.sentence.word + '&student_id=' + sessionStorage.getItem('student') + '&word_status=' + 1
      axios.get(url).then(res => {
        if (res.data) {
          return
        }
      })
    }
  },
  mounted () {
    this.$store.state.STUDY_STATUS = true
    this.word = this.$store.state.WORD_NOW.data
    this.explain = this.$store.state.WORD_NOW.data.explains
    this.sentence = this.$store.state.WORD_NOW.sentence
    this.wordCount = this.$store.state.WORD_COUNT
    this.recallCount = this.$store.state.RECALL_COUNT
  },
  components: {
    WordAndPronunciation,
    StudyCardTop,
    WordExplanation,
    WordSentence
  }
}
</script>

<style scoped>
.img {
  top: 0;
  left: 0;
  position: absolute;
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  z-index: -3;
}

.header-row {
  margin-top: 15px;
  text-align: center;
}

.cutain {
  background-color: #F8F8F8;
  border-radius: 10px;
  margin-top: 30px;
  padding-bottom: 30px;
  z-index: -100;
}

.word-title {
  display: block;
  font-size: 15px;
  font-weight: bold;
  height: 15px;
  margin-bottom: 15px;
  color: #606060;
}

.word-btn {
  width: 140px;
  height: 35px;
  margin-top: 30px;
  margin-left: 30px;
  position: relative;
  float: right;
}

.label-of-btn {
  position: absolute;
  left: 10px;
  top: 8px;
  width: 20px;
  background: #F8F8F8;
  border-radius: 5px;
  opacity: 0.8;
  color: #686868;
  height: 18px;
  font-size: 15px;
  text-align: center;
  padding-top: 1px;
}

.next-button {
  float: right;
  width: 100px;
  height: 40px;
  margin-right: 100px;
  background-color: rgb(74, 199, 73);
  border: 0;
  font-weight: 500;
  font-size: 14px;
  outline: 0;
  color: white;
  border-radius: 10px;
  box-shadow: 1px 1px 1px 1px rgb(74, 199, 73);
  cursor: pointer;
}
</style>
