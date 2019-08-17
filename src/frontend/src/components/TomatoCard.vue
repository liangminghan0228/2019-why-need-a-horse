<template>
  <div class="card-container">
    <img src="../images/5_bg2.png" />
    <el-row class="head-row">
      <el-col :span="14" :offset="5" class="cutain">
        <el-row>
          <el-col :span="16" :offset="4">
            <word-and-pronunciation :word="word.data.word" :pronunciation="word.data.pronunciation"></word-and-pronunciation>
            <div v-for="option in options" :key="option.index">
              <word-option :index="option.index" :option="option.option" class="word-option" @selectOption="selectOption"></word-option>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import WordAndPronunciation from './common/WordAndPronunciation'
import WordOption from './common/WordOption'
const axios = require('axios')
export default {
  data: function () {
    return {
      word: {},
      words: [],
      wordIndex: 0,
      options: [
        {
          index: 1,
          option: '认识'
        },
        {
          index: 2,
          option: '不认识'
        }
      ]
    }
  },
  methods: {
    selectOption (option) {
      if (option === '认识') {
        this.goToNext(-1)
      }
      if (option === '不认识') {
        this.goToNext(0)
      }
    },
    goToNext (status) {
      let url = this.$store.state.BASEURL + 'study/set_word_status?word_id=' + this.word.sentence.word + '&student_id=' + sessionStorage.getItem('student') + '&word_status=' + status
      axios.get(url).then(res => {
        if (res.data) {
          return
        }
      })
      if (this.wordIndex === (this.$store.state.TOMATO_WORDS.length - 1)) {
        this.$store.state.TOMATO_WORDS = []
        this.$message({
          message: '番茄复习完成，继续学习吧',
          type: 'success'
        })
        this.$router.push('/studycardone')
        return
      }
      this.wordIndex += 1
      this.word = this.$store.state.TOMATO_WORDS[this.wordIndex]
      setTimeout(() => {
        let buttonOne = document.getElementsByTagName('input')[0]
        buttonOne.setAttribute('class', 'choose-button')
        let buttonTwo = document.getElementsByTagName('input')[1]
        buttonTwo.setAttribute('class', 'choose-button')
      }, 100)
    }
  },
  mounted () {
    this.words = this.$store.state.TOMATO_WORDS
    this.word = this.$store.state.TOMATO_WORDS[0]
  },
  components: {
    WordAndPronunciation,
    WordOption
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
</style>
