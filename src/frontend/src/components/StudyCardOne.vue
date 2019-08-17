<template>
  <div class="card-container">
    <img src="../images/5_bg2.png" />
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
const axios = require('axios')
export default {
  data: function () {
    return {
      word: {},
      wordCount: 7,
      recallCount: 0,
      options: [
        {
          index: 1,
          option: '认识'
        },
        {
          index: 2,
          option: '不认识'
        },
        {
          index: 3,
          option: 'Kill（烂熟）'
        }
      ]
    }
  },
  methods: {
    selectOption (option) {
      if (option === '认识') {
        if (this.$store.state.WORD_LEVEL < 0) {
          this.$store.state.IS_KNOW = true
        }
        setTimeout(() => {
          this.$router.push('/studycardthree')
        }, 100)
      }
      if (option === '不认识') {
        if (this.$store.state.WORD_LEVEL < 0) {
          this.$store.state.IS_KNOW = false
        }
        setTimeout(() => {
          this.$router.push('/studycardtwo')
        }, 100)
      }
      if (option === 'Kill（烂熟）') {
        this.$store.state.STUDY_STATUS = true
        let url = this.$store.state.BASEURL + 'study/set_word_rank?word_id=' + this.$store.state.WORD_NOW.sentence.word + '&student_id=' + sessionStorage.getItem('student') + '&word_level=' + 5
        axios.get(url).then(res => {
          if (res.data) {
            this.$store.state.WORD_LEVEL = -1
            this.$store.state.IS_KNOW = false
            this.$store.state.IS_RECALL = false
            this.$store.state.ISFOUR = false
          }
        })
        url = this.$store.state.BASEURL + 'study/set_word_status?word_id=' + this.$store.state.WORD_NOW.sentence.word + '&student_id=' + sessionStorage.getItem('student') + '&word_status=' + 2
        axios.get(url).then(res => {
          if (res.data) {
            return
          }
        })
        setTimeout(() => {
          let buttonItem = document.getElementsByTagName('input')[2]
          buttonItem.setAttribute('class', 'choose-button')
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
          this.word = this.$store.state.WORD_NOW.data
          this.wordCount = this.$store.state.WORD_COUNT - 1
          this.$store.state.WORD_COUNT = this.wordCount
        }, 100)
      }
    },
    studyOut () {
      this.$router.push('/beforestudying')
    }
  },
  mounted () {
    if (!this.$store.state.STUDY_STATUS) {
      let url = this.$store.state.BASEURL + 'books/get_word?student_id=' + sessionStorage.getItem('student') + '&category=' + this.$store.state.CATEGORY.id
      axios.get(url).then(res => {
        if (res.data) {
          if (res.data.length <= 0) {
            this.$router.push('/beforestudying')
            this.$message({
              message: '本书已经学完啦，去找老师开通新课程吧',
              type: 'success'
            })
          }
          let words = []
          let word = {}
          for (let i = 0; i < res.data.length; i++) {
            word.data = res.data[i].data[0].fields
            word.sentence = res.data[i].sentence[0].fields
            words.push(word)
            word = {}
          }
          this.word = words[0].data
          this.$store.state.WORD_NOW = words[0]
          this.$store.state.WORDS = words
          this.$store.state.WORD_COUNT = res.data.length
          this.wordCount = res.data.length
          this.recallCount = this.$store.state.RECALL_COUNT
        }
      })
    } else {
      this.word = this.$store.state.WORD_NOW.data
      this.wordCount = this.$store.state.WORD_COUNT
      this.recallCount = this.$store.state.RECALL_COUNT
    }
  },
  components: {
    WordAndPronunciation,
    WordOption,
    StudyCardTop
  }
}
</script>

<style scoped>
img {
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
  width: 100%;
  margin-top: 20px;
  text-align: center;
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
