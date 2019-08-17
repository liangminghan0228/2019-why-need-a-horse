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
            <div class="pron-div">
              <img src="../images/43_voice3.png" class="pron-img">
              <span class="pron-span">{{sentence}}</span>
            </div>
            <div v-for="option in options" :key="option.index">
              <word-option :index="option.index" :option="option.option" class="word-option" @selectOption="selectOption"></word-option>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
    <button class="next-button" @click="studyOut">退出学习</button>
  </div>
</template>

<script>
import WordAndPronunciation from './common/WordAndPronunciation'
import WordOption from './common/WordOption'
import StudyCardTop from './common/StudyCardTop'
export default {
  data: function () {
    return {
      word: {},
      wordCount: 7,
      recallCount: 0,
      options: [
        {
          index: 1,
          option: '想起来'
        },
        {
          index: 2,
          option: '没想起来'
        }
      ],
      sentence: ''
    }
  },
  methods: {
    selectOption (option) {
      if (option === '想起来') {
        if (this.$store.state.WORD_LEVEL < 0) {
          this.$store.state.IS_RECALL = true
        }
        setTimeout(() => {
          this.$router.push('/studycardthree')
        }, 100)
      }
      if (option === '没想起来') {
        if (this.$store.state.WORD_LEVEL < 0) {
          this.$store.state.ISFOUR = true
        }
        setTimeout(() => {
          this.$router.push('/studycardfour')
        }, 100)
      }
    },
    studyOut () {
      this.$router.push('/beforestudying')
    }
  },
  mounted () {
    this.$store.state.STUDY_STATUS = true
    this.$store.state.RECALL_COUNT += 1
    this.word = this.$store.state.WORD_NOW.data
    this.sentence = this.$store.state.WORD_NOW.sentence.example_sentence_en
    this.wordCount = this.$store.state.WORD_COUNT
    this.recallCount = this.$store.state.RECALL_COUNT
  },
  components: {
    WordAndPronunciation,
    WordOption,
    StudyCardTop
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
  margin-top: 20px;
  text-align: center;
}

.pron-div {
  position: relative;
  border-radius: 10px;
  background-color: #F0F0F0;
  height: 50px;
  width: 96%;
  margin-bottom: 40px;
}

.pron-img {
  position: absolute;
  margin-left: 20px;
  top: 13px;
}

.pron-span {
  position: absolute;
  top: 12px;
  left:65px;
  color: #606266;
}

.cutain {
  background-color: #F8F8F8;
  border-radius: 10px;
  margin-top: 50px;
  padding-bottom: 80px;
  z-index: -2;
}

.word-option {
  width: 100%;
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
