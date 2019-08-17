<template>
  <div class="bg-img">
    <el-row class="header-row">
      <el-col :span="14" :offset="5">
        <study-card-top :wordCount="wordCount" :recallCount="recallCount"></study-card-top>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="5">&nbsp;</el-col>
      <el-col :span="14">
        <div class="white-box">
          <span class="word-font">{{question.explain}}</span>
          <div class="pronouce">
            <div class="english-pronouce">
              <img src="../images/42_voice2.png" class="img-voice" />
              <span class="country-font">英</span>
            </div>
            <div class="america-pronouce">
              <img src="../images/43_voice3.png" class="img-voice" />
              <span class="country-font">美</span>
            </div>
          </div>
          <input type="text" v-model="input" readonly="readonly" :class="spellingStatus" />
          <div class="letter-area">
            <div v-for="(item, index) in letter" :key="index">
              <input
                type="button"
                :value="item"
                class="letter-button"
                @click="addLetter(item)"
              />
            </div>
            <input type="button" value="×" class="delete-button" @click="deleteLetter" />
          </div>
        </div>
      </el-col>
      <el-col :span="5">&nbsp;</el-col>
    </el-row>
    <button class="next-button" @click="studyOut">退出学习</button>
  </div>
</template>

<script>
import StudyCardTop from './common/StudyCardTop'
export default {
  data: function () {
    return {
      wordCount: 7,
      recallCount: 0,
      input: '',
      letter: [],
      question: {
        word: '',
        explain: ''
      },
      spellingStatus: 'process'
    }
  },
  methods: {
    addLetter: function (oneLetter) {
      oneLetter = oneLetter.toLowerCase()
      this.input = this.input + oneLetter
    },
    deleteLetter: function () {
      this.input = this.input.substring(0, this.input.length - 1)
    },
    getLetter: function () {
      let answer = new Array()
      answer = this.question.word.toUpperCase().split('')
      let option = new Array()
      let source = new Array('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
      for (let i = 0; i < 23; i++) {
        option[i] = ''
      }
      for (let i = 0; i < answer.length; i++) {
        let index = Math.floor(Math.random() * 22)
        if (option[index] !== '') {
          while (option[index] !== '') {
            index = Math.floor(Math.random() * 22)
          }
        }
        option[index] = answer[i]
      }
      for (let i = 0; i < 23; i++) {
        if (option[i] === '') {
          let index = Math.floor(Math.random() * 25)
          option[i] = source[index]
        }
      }
      for (let i = 0; i < 23; i++) {
        this.letter += option[i]
      }
    },
    studyOut () {
      this.$router.push('/beforestudying')
    },
    nextWord () {
      let index = this.$store.state.WORDS.indexOf(this.$store.state.WORD_NOW)
      if (index === (this.$store.state.WORDS.length - 1)) {
        this.$store.state.STUDY_STATUS = false
        this.$store.state.WORD_COUNT = 7
        this.$store.state.RECALL_COUNT = 0
        this.$store.state.WORD_LEVEL = -1
        this.$store.state.IS_KNOW = false
        this.$store.state.IS_RECALL = false
        this.$store.state.ISFOUR = false
        this.$store.state.WORD_NOW = {}
        this.$store.state.WORDS = []
        this.$router.push('/studycardone')
        return
      }
      this.$store.state.WORD_NOW = this.$store.state.WORDS[index + 1]
      this.$store.state.WORD_COUNT -= 1
      this.$store.state.RECALL_COUNT += 1
      this.reload()
    }
  },
  watch: {
    input: function (val) {
      if (val.length === this.question.word.length) {
        this.question.word = this.question.word.toUpperCase()
        val = val.toUpperCase()
        if (val === this.question.word) {
          this.spellingStatus = 'right'
          setTimeout(() => {
            this.nextWord()
          }, 100)
        } else {
          this.spellingStatus = 'wrong'
          this.input = ''
          setTimeout(() => {
            this.nextWord()
          }, 100)
        }
      }
    }
  },
  mounted () {
    this.question.word = this.$store.state.WORD_NOW.data.word
    this.question.explain = this.$store.state.WORD_NOW.data.explains
    this.wordCount = this.$store.state.WORD_COUNT
    this.recallCount = this.$store.state.RECALL_COUNT
    this.getLetter()
  },
  components: {
    StudyCardTop
  },
  inject: ['reload']
}
</script>

<style scoped>
.bg-img {
  background-image: url('../images/1_bg1.png');
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  z-index: -3;
  background-size: 100%;
  background-repeat: no-repeat;
  background-attachment: fixed;
  overflow: hidden;
}

.img-music {
  width: 40px;
  height: 40px;
  float: right;
  position: relative;
}

.header-row {
  width: 100%;
  margin-top: 20px;
  text-align: center;
}

.white-box {
  background-color: white;
  height: 350px;
  margin-top: 30px;
  border-radius: 5px;
  box-shadow: 0 0 5px rgb(196, 196, 196);
  padding: 40px 150px;
}

.top-area {
  margin-top: 30px;
  line-height: 40px;
}

.timer {
  float: right;
  background: url("../images/31_time4.png") no-repeat;
  background-size: 100px;
  text-align: center;
  line-height: 25px;
  color: white;
  padding-left: 8px;
  width: 90px;
  height: 40px;
  position: relative;
  float: right;
  margin: 10px;
}

.word-font {
  font-size: 17px;
  font-weight: bold;
  color: rgb(95, 90, 90);
}

.english-pronouce {
  float: left;
  background-color: rgb(255, 246, 230);
  width: 70px;
  height: 20px;
  border-radius: 10px;
  font-size: 12px;
  text-align: center;
  line-height: 20px;
  margin-right: 10px;
  position: relative;
}

.america-pronouce {
  float: left;
  background-color: rgb(249, 249, 249);
  width: 70px;
  height: 20px;
  border-radius: 10px;
  font-size: 12px;
  text-align: center;
  line-height: 20px;
  margin-right: 10px;
  position: relative;
}

.pronouce {
  margin: 20px 0 60px 0;
}

.img-voice {
  width: 14px;
  height: 14px;
  line-height: 60px;
  position: absolute;
  top: 3px;
  left: 10px;
}

.country-font {
  position: absolute;
  left: 30px;
}

.process {
  width: 400px;
  height: 50px;
  -webkit-appearance: none;
  background-color: #fff;
  background-image: none;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  box-sizing: border-box;
  color: #606266;
  display: inline-block;
  font-size: inherit;
  line-height: 40px;
  outline: none;
  padding: 0 15px;
}

.right {
  width: 400px;
  height: 50px;
  -webkit-appearance: none;
  background-color: #fff;
  background-image: none;
  border-radius: 4px;
  border: 1px solid rgb(74, 199, 103);
  box-sizing: border-box;
  color: #606266;
  display: inline-block;
  font-size: inherit;
  line-height: 40px;
  outline: none;
  padding: 0 15px;
}

.wrong {
  width: 400px;
  height: 50px;
  -webkit-appearance: none;
  background-color: #fff;
  background-image: none;
  border-radius: 4px;
  border: 1px solid rgb(255, 97, 97);
  box-sizing: border-box;
  color: #606266;
  display: inline-block;
  font-size: inherit;
  line-height: 40px;
  outline: none;
  padding: 0 15px;
}

.letter-button {
  background-color: rgb(249, 249, 249);
  outline: none;
  border-radius: 5px;
  color: gray;
  border: 0;
  width: 40px;
  height: 40px;
  margin: 5px 5px 5px 5px;
  float: left;
}

.letter-area {
  margin-top: 40px;
  position: relative;
}

.letter-button:hover {
  background-color: rgb(46, 180, 255);
  color: white;
  cursor: pointer;
}

.delete-button {
  background-color: rgb(255, 223, 223);
  outline: none;
  border-radius: 5px;
  color: gray;
  border: 0;
  width: 40px;
  height: 40px;
  margin: 0 5px 0 5px;
  font-size: 20px;
  cursor: pointer;
}

.delete-button:hover {
  background-color: rgb(250, 183, 183);
}

.next-button {
  float: right;
  width: 100px;
  height: 40px;
  margin-right: 100px;
  margin-bottom: 30px;
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
