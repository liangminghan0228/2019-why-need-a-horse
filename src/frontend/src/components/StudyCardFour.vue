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
            <el-button type="success" class="word-btn" @click="goToNext">下一个</el-button>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
    <button class="next-button" @click="studyOut">退出学习</button>
  </div>
</template>

<script>
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
      sentence: {},
      explain: ''
    }
  },
  methods: {
    goToNext () {
      this.$router.push('/studycardtwo')
    },
    studyOut () {
      this.$router.push('/beforestudying')
    }
  },
  mounted () {
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
  z-index: -2;
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
  margin-top: 15px;
  margin-left: 30px;
  position: relative;
  float: right;
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
