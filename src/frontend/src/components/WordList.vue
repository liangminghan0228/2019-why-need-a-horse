<template>
  <div>
    <main-show-top></main-show-top>
    <img src="../images/1_bg1.png">
    <div>
      <el-row>
        <main-show :showList="true"></main-show>
        <el-col :span="1">&nbsp;</el-col>
        <el-col :span="13">
          <div class="white-box">
            <div>
              <p>复习顺序：</p>
              <input
                type="button"
                value="熟悉程度"
                :class="isfamilar ? 'font-active' : 'font-color'"
                @click="changeToFamilar"
              />
              <input
                type="button"
                value="字母顺序"
                :class="isfamilar ? 'font-color' : 'font-active'"
                @click="changeToWord"
              />
              <div class="signal">
                <label class="familar-font">熟练</label>
                <div class="green-circle"></div>
              </div>
              <div class="signal">
                <label class="familar-font">熟悉</label>
                <div class="blue-circle"></div>
              </div>
              <div class="signal">
                <label class="familar-font">生词</label>
                <div class="red-circle"></div>
              </div>
            </div>
            <div class="word-area">
              <div v-for="(oneWord, index) in word" :key="index">
                <el-col :span="8">
                  <div
                    v-if="oneWord['status'] === 0 || oneWord['status'] === -1"
                    class="red-word"
                  >{{oneWord['spelling']}}</div>
                  <div v-if="oneWord['status'] === 1" class="blue-word">{{oneWord['spelling']}}</div>
                  <div v-if="oneWord['status'] === 2" class="green-word">{{oneWord['spelling']}}</div>
                </el-col>
              </div>
            </div>
            <input
              v-if="group !== 1"
              value="上一组"
              type="button"
              :class="isfinish ? 'next-button-next' : 'next-button-last'"
              @click="lastGroup"
            />
            <input
              v-if="isfinish === false"
              value="下一组"
              type="button"
              class="next-button-next"
              @click="nextGroup"
            />
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
const axios = require('axios')
import MainShow from './common/MainShow'
import MainShowTop from './common/MainShowTop'
export default {
  data: function () {
    return {
      word: [],
      studentId: 1,
      categoryId: 1,
      group: 1,
      oneGroupCount: 9,
      isfinish: false,
      order: 'familar',
      isfamilar: true
    }
  },
  components: {
    MainShow,
    MainShowTop
  },
  methods: {
    nextGroup: function () {
      this.group += 1
      axios
        .get(
          this.$store.state.BASEURL +
            'study/get_word?student_id=' +
            this.studentId +
            '&category_id=' +
            this.categoryId +
            '&group=' +
            this.group +
            '&oneGroupCount=' +
            this.oneGroupCount +
            '&order=' +
            this.order
        )
        .then(res => {
          if (res.data !== 'none') {
            this.word = res.data
          } else {
            this.$message({
              type: 'error',
              message: '这已经是最后一组单词了'
            })
            this.group = 1
          }
        })
    },
    lastGroup: function () {
      this.group -= 1
      axios
        .get(
          this.$store.state.BASEURL +
            'study/get_word?student_id=' +
            this.studentId +
            '&category_id=' +
            this.categoryId +
            '&group=' +
            this.group +
            '&oneGroupCount=' +
            this.oneGroupCount +
            '&order=' +
            this.order
        )
        .then(res => {
          this.word = res.data
        })
    },
    changeToWord: function () {
      if (this.isfamilar === true) {
        this.isfamilar = false
        this.order = 'word'
        this.group = 1
        axios
          .get(
            this.$store.state.BASEURL +
              'study/get_word?student_id=' +
              this.studentId +
              '&category_id=' +
              this.categoryId +
              '&group=' +
              this.group +
              '&oneGroupCount=' +
              this.oneGroupCount +
              '&order=' +
              this.order
          )
          .then(res => {
            this.word = res.data
          })
      }
    },
    changeToFamilar: function () {
      if (this.isfamilar === false) {
        this.isfamilar = true
        this.order = 'familar'
        this.group = 1
        axios
          .get(
            this.$store.state.BASEURL +
              'study/get_word?student_id=' +
              this.studentId +
              '&category_id=' +
              this.categoryId +
              '&group=' +
              this.group +
              '&oneGroupCount=' +
              this.oneGroupCount +
              '&order=' +
              this.order
          )
          .then(res => {
            this.word = res.data
          })
      }
    }
  },
  mounted () {
    var vm = this
    vm.studentId = sessionStorage.getItem('student')
    vm.categoryId = this.$store.state.CATEGORY.id
    axios
      .get(
        this.$store.state.BASEURL +
          'study/get_word?student_id=' +
          this.studentId +
          '&category_id=' +
          this.categoryId +
          '&group=' +
          this.group +
          '&oneGroupCount=' +
          this.oneGroupCount +
          '&order=' +
          this.order
      )
      .then(res => {
        vm.word = res.data
        if (vm.word.length < this.oneGroupCount){
          this.isfinish = true
        }
      })
  },
  watch: {
    word: function (val) {
      if (val.length < this.oneGroupCount) {
        this.isfinish = true
      } else {
        this.isfinish = false
      }
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

p {
  font-weight: 550;
  font-size: 15px;
  color: rgb(52, 52, 52);
  display: inline;
}

.familar-font {
  color: rgb(103, 103, 103);
  font-size: 14px;
  float: right;
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

.white-box {
  position: relative;
  background-color: white;
  margin-top: 50px;
  border-radius: 5px;
  height: 450px;
  padding: 30px;
  box-shadow: 1px 1px 1px 1px rgb(188, 221, 221);
}

.white-box-top {
  height: 50px;
}

.white-box-middle {
  padding-top: 15px;
  padding-left: 10px;
  font-size: 15px;
  font-weight: bold;
}

.font-color {
  color: rgb(103, 103, 103);
  text-decoration: none;
  font-size: 14px;
  display: inline;
  margin-right: 10px;
}

input.font-color {
  border: 0;
  background-color: transparent;
  outline: none;
}

input.font-color:hover {
  color: rgb(95, 206, 121);
  cursor: pointer;
}

.font-active {
  color: rgb(95, 206, 121);
  text-decoration: none;
  font-size: 14px;
  display: inline;
  margin-right: 10px;
}

input.font-active {
  border: 0;
  background-color: transparent;
  outline: none;
}

.red-circle {
  float: right;
  background-color: rgb(255, 142, 113);
  width: 2px;
  height: 2px;
  border-radius: 50%;
  box-shadow: 0 0 10px rgb(255, 142, 113);
  padding: 5px;
  margin: 3px;
  margin-right: 10px;
  margin-left: 20px;
}

.blue-circle {
  float: right;
  background-color: rgb(132, 211, 255);
  width: 2px;
  height: 2px;
  border-radius: 50%;
  box-shadow: 0 0 10px rgb(132, 211, 255);
  padding: 5px;
  margin: 3px;
  margin-right: 10px;
  margin-left: 20px;
}

.green-circle {
  float: right;
  background-color: rgb(139, 229, 117);
  width: 2px;
  height: 2px;
  border-radius: 50%;
  box-shadow: 0 0 10px rgb(139, 229, 117);
  padding: 5px;
  margin: 3px;
  margin-right: 10px;
  margin-left: 20px;
}

.signal {
  text-align: center;
  padding: 0;
  display: inline;
}

.word-area {
  padding: 40px 0 40px 45px;
  position: relative;
}

.red-word {
  width: 120px;
  height: 60px;
  border: 2px solid rgb(255, 142, 113);
  border-radius: 5px;
  box-shadow: 0 3px 0 rgb(255, 142, 113);
  text-align: center;
  line-height: 60px;
  float: left;
  margin-top: 30px;
}

.blue-word {
  width: 120px;
  height: 60px;
  border: 2px solid rgb(132, 211, 255);
  border-radius: 5px;
  box-shadow: 0 3px 0 rgb(132, 211, 255);
  text-align: center;
  line-height: 60px;
  float: left;
  margin-top: 30px;
}

.green-word {
  width: 120px;
  height: 60px;
  border: 2px solid rgb(139, 229, 117);
  border-radius: 5px;
  box-shadow: 0 3px 0 rgb(139, 229, 117);
  text-align: center;
  line-height: 60px;
  float: left;
  margin-top: 30px;
}

.next-button-next {
  position: absolute;
  top: 390px;
  left: 180px;
  display: block;
  width: 100px;
  height: 40px;
  margin-top: 50px;
  margin-left: 300px;
  text-align: left;
  background-color: rgb(74, 199, 73);
  border: 0;
  font-weight: 500;
  font-size: 14px;
  outline: 0;
  color: white;
  border-radius: 10px;
  text-align: center;
  box-shadow: 1px 1px 1px 1px rgb(74, 199, 73);
  cursor: pointer;
}

.next-button-next:hover {
  background-color: rgb(123, 199, 123);
}

.next-button-last {
  position: absolute;
  top: 390px;
  left: 180px;
  display: block;
  width: 100px;
  height: 40px;
  margin-top: 50px;
  margin-left: 180px;
  text-align: left;
  background-color: rgb(74, 199, 73);
  border: 0;
  font-weight: 500;
  font-size: 14px;
  outline: 0;
  color: white;
  border-radius: 10px;
  text-align: center;
  box-shadow: 1px 1px 1px 1px rgb(74, 199, 73);
  cursor: pointer;
}

.next-button-last:hover {
  background-color: rgb(123, 199, 123);
}
</style>
