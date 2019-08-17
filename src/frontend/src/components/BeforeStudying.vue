<template>
  <div>
    <img src="../images/1_bg1.png" />
    <main-show-top></main-show-top>
    <el-row>
      <main-show :showStudying="showStudying"></main-show>
      <el-col :span="1">&nbsp;</el-col>
      <el-col :span="13">
        <div class="white-box">
          <div class="white-box-top">
            <input type="button" value="切换单词书" class="button-type-1" @click="goQueryCourse($event)"/>
            <input type="button" value="订阅新课程" class="button-type-1" @click="goQueryCourse($event)" />
          </div>
          <div class="white-box-middle">
            <img src="../images/4_class1.png" class="image-class" />
            {{classname}}
            <br />
            <el-row>
              <el-col :span="8">&nbsp;</el-col>
              <el-col :span="16">
                <div class="grade">
                  <div :class="[isLearning ? 'number' : 'question']">{{studyBeforeGrade}}</div>&nbsp;学前检测
                </div>
                <img src="../images/3_vs.png" class="image-vs" />
                <div class="grade">
                  <div :class="[isComplete ? 'number' : 'question']">{{studyAfterGrade}}</div>&nbsp;学后检测
                </div>
              </el-col>
            </el-row>
            <br />
            <img src="../images/19_teaching material.png" class="image-class" />
            {{bookname}}
            <el-row>
              <el-col :span="9">&nbsp;</el-col>
              <el-col :span="15">
                <el-progress type="circle" :percentage="precent"></el-progress>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="7">&nbsp;</el-col>
              <el-col :span="17">
                <input
                  v-if="isLearning === true"
                  type="button"
                  value="继续学习"
                  class="button-type-2"
                  @click="goStudyCardOne"
                />
                <input
                  v-if="isLearning === true"
                  type="button"
                  value="巩固测试"
                  class="button-type-3"
                  @click="goReviewTest"
                />
                <input
                  v-if="isNotLearn === true"
                  type="button"
                  value="学前检测"
                  class="button-type-4"
                  @click="goPreTest"
                />
                <input
                  v-if="isComplete === true"
                  type="button"
                  value="学后检测"
                  class="button-type-2"
                  @click="goAfterTest"
                />
                <input
                  v-if="isComplete === true"
                  type="button"
                  value="一测到底"
                  class="button-type-3"
                  @click="goAllTest"
                />
              </el-col>
            </el-row>
            <br />
            <el-row>
              <div v-for="(unit, index) in unitInfo" :key="index">
                <div v-if="unit.fields.status === 'complete'" class="circle-border-green">
                  <input type="button" :value="unit.fields.unit_num" class="circle-green" />
                  <img src="../images/37_choose.png" class="image-choose" />
                </div>
                <div v-if="unit.fields.status === 'islearning'" class="circle-border-red">
                  <input type="button" :value="unit.fields.unit_num" class="circle-red" />
                </div>
                <div v-if="unit.fields.status === 'beforelearning'" class="circle-border-grey">
                  <input type="button" :value="unit.fields.unit_num" class="circle-grey" />
                </div>
              </div>
            </el-row>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import MainShow from './common/MainShow'
import MainShowTop from './common/MainShowTop'
const axios = require('axios')
export default {
  data: function () {
    return {
      showStudying: true,
      classname: '初一突破班',
      studyBeforeGrade: '?',
      studyAfterGrade: '?',
      bookname: '人教新课标-七年级上',
      precent: 0,
      unitInfo: [],
      studentId: 1,
      categoryId: 1,
      isNotLearn: true,
      isComplete: false,
      isLearning: false
    }
  },
  methods: {
    goQueryCourse: function (e) {
      this.$router.push({
        name: 'querycourse',
        params: {
          type: e.target.value
        }
      })
    },
    goStudyCardOne: function () {
      this.$router.push('/studycardone')
    },
    goReviewTest: function () {
      this.$router.push({
        name: 'test',
        params: {
          type: 'reviewTest'
        }
      })
    },
    goPreTest: function () {
      this.$router.push({
        name: 'test',
        params: {
          type: 'preTest'
        }
      })
    },
    getCurrentCourse () {
      axios.get(this.$store.state.BASEURL + 'study/get_current_course?student_id=' + this.studentId).then(res => {
        if (res.data === 'get_current_course_failed'){
          this.$message('尚未开通课程，快去找老师开通课程吧～')
        } else {
          this.$store.state.CATEGORY.id = res.data.book_id
          this.$store.state.CATEGORY.name = res.data.book_name
          this.bookname = this.$store.state.CATEGORY.name
          this.categoryId = res.data.book_id
          this.updateUnitList()
          this.getPreScore()
          this.getAfterScore()
        }
      })
    },
    goAfterTest: function () {
      this.$router.push({
        name: 'test',
        params: {
          type: 'afterTest'
        }
      })
    },
    goAllTest: function () {
      this.$router.push({
        name: 'test',
        params: {
          type: 'allTest'
        }
      })
    },
    getUnitList () {
      axios.get(this.$store.state.BASEURL + 'study/get_unit_list?category_id=' + this.categoryId + '&student_id=' + this.studentId).then(res => {
        this.unitInfo = res.data
        let complete = true
        let times = 0
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].fields.status === 'beforelearning') {
            complete = false
          }
          if (res.data[i].fields.status === 'complete') {
            this.isLearning = true
            this.isNotLearn = false
            times = times + 1
          }
        }
        if (complete === true) {
          this.isLearning = false
          this.isNotLearn = false
        }
        this.precent = Math.round((times / res.data.length) * 100)
        this.isComplete = complete
      })
    },
    updateUnitList () {
      axios.get(this.$store.state.BASEURL + 'study/update_unit_status?student_id=' + this.studentId + '&category_id=' + this.categoryId).then(
        res=>{
          if (res.data !== 'update_unit_status failed') {
            this.getUnitList()
          }
        }
      )
    }
    ,
    getPreScore () {
      axios.get(this.$store.state.BASEURL + 'study/get_test_score?book_id=' + this.categoryId + '&student_id=' + this.studentId + '&test_type=' + 'preTest').then(res => {
        if (res.data !== 'none') {
          this.isLearning = true
          this.isNotLearn = false
          this.studyBeforeGrade = res.data
        }
      })
    },
    getAfterScore () {
      axios.get(this.$store.state.BASEURL + 'study/get_test_score?book_id=' + this.categoryId + '&student_id=' + this.studentId + '&test_type=' + 'afterTest').then(res => {
        if (res.data !== 'none') {
          this.studyAfterGrade = res.data
          this.isComplete = true
          this.isLearning = false
        }
      })
    },
    getClassInfo () {
      axios.get(this.$store.state.BASEURL + 'information/get_student_classes?student_id=' + this.studentId).then(res => {this.classname = res.data})
    }
  },
  mounted () {
    this.studentId = sessionStorage.getItem('student')
    this.getClassInfo()
    this.getCurrentCourse()
  },
  components: {
    MainShow,
    MainShowTop
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
  background-color: white;
  margin-top: 50px;
  border-radius: 5px;
  height: 465px;
  padding: 20px;
  box-shadow: 1px 1px 1px 1px rgb(188, 221, 221);
}

.button-type-1 {
  width: 80px;
  height: 30px;
  background-color: #f8f8f8;
  float: right;
  margin-left: 30px;
  margin-top: 10px;
  font-size: 12px;
}

input.button-type-1 {
  border-radius: 5px;
  outline: none;
  border: 0;
}

input.button-type-1:hover {
  color: white;
  background-color: rgb(74, 199, 103);
  transition-duration: 0.2s;
}

.button-type-2 {
  width: 80px;
  height: 30px;
  background-color: rgb(74, 199, 103);
  margin-left: 20px;
  margin-top: 10px;
  font-size: 12px;
  box-shadow: 1px 1px 1px 1px rgb(188, 221, 221);
}

input.button-type-2 {
  color: white;
  border-radius: 5px;
  outline: none;
  border: 0;
}

input.button-type-2:hover {
  color: white;
  background-color: rgb(115, 207, 137);
  transition-duration: 0.2s;
}

.button-type-3 {
  width: 80px;
  height: 30px;
  background-color: rgb(255, 177, 40);
  margin-left: 30px;
  margin-top: 10px;
  font-size: 12px;
  box-shadow: 1px 1px 1px 1px rgb(188, 221, 221);
}

input.button-type-3 {
  color: white;
  border-radius: 5px;
  outline: none;
  border: 0;
}

input.button-type-3:hover {
  color: white;
  background-color: rgb(255, 189, 74);
  transition-duration: 0.2s;
}

.button-type-4 {
  width: 80px;
  height: 30px;
  background-color: rgb(22, 155, 213);
  margin-left: 80px;
  margin-top: 10px;
  font-size: 12px;
  box-shadow: 1px 1px 1px 1px rgb(188, 221, 221);
}

input.button-type-4 {
  color: white;
  border-radius: 5px;
  outline: none;
  border: 0;
}

input.button-type-4:hover {
  color: white;
  background-color: rgb(86, 166, 201);
  transition-duration: 0.2s;
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

.image-class {
  height: 20px;
  width: 20px;
  position: inherit;
  padding-right: 5px;
}

.image-choose {
  float: right;
  height: 10px;
  width: 10px;
  position: inherit;
}

.number {
  color: rgb(255, 177, 40);
  font-size: 30px;
  font-weight: normal;
  margin-bottom: 5px;
  text-align: center;
}

.grade {
  float: left;
  font-size: 11px;
  color: rgb(183, 183, 183);
  font-weight: normal;
  margin-top: 20px;
}

.image-vs {
  float: left;
  height: 60px;
  width: 50px;
  position: inherit;
  padding-right: 5px;
  margin-left: 20px;
  margin-top: 20px;
  margin-right: 20px;
}

.question {
  color: rgb(163, 163, 163);
  font-size: 33px;
  text-align: center;
}

.circle-green {
  text-align: center;
  line-height: 25px;
  background-color: rgb(139, 229, 117);
  color: white;
  border-radius: 50%;
  height: 25px;
  width: 25px;
}

input.circle-green {
  outline: none;
  border: 0;
}

.circle-border-green {
  float: left;
  border-radius: 50%;
  height: 25px;
  width: 25px;
  background-color: transparent;
  border: 2px solid rgb(220, 247, 213);
  padding: 3px;
  margin: 5px;
}

.circle-red {
  text-align: center;
  line-height: 25px;
  background-color: rgb(255, 142, 113);
  color: white;
  border-radius: 50%;
  height: 25px;
  width: 25px;
}

input.circle-red {
  outline: none;
  border: 0;
}

.circle-border-red {
  float: left;
  border-radius: 50%;
  height: 25px;
  width: 25px;
  background-color: transparent;
  border: 2px solid rgb(255, 221, 212);
  padding: 3px;
  margin: 5px;
}

.circle-grey {
  text-align: center;
  line-height: 25px;
  background-color: rgb(222, 222, 222);
  color: white;
  border-radius: 50%;
  height: 25px;
  width: 25px;
}

input.circle-grey {
  outline: none;
  border: 0;
}

.circle-border-grey {
  float: left;
  border-radius: 50%;
  height: 25px;
  width: 25px;
  background-color: transparent;
  border: 2px solid rgb(245, 245, 245);
  padding: 3px;
  margin: 5px;
}
</style>
