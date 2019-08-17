<template>
  <div class="query-course">
    <img src="../images/1_bg1.png" />
    <el-row>
      <el-col :span="24">
        <div class="main-top">
          <main-show-top></main-show-top>
        </div>
      </el-col>
      <main-show :showStudying="true"></main-show>
      <el-col :span="13" :offset="1">
        <div class="problem-board">
          <el-row>
            <el-col class="top" :span="10">
              <img class="top-title-img" src="../images/top-title.png" />
              <label class="top-title">选课中心</label>
            </el-col>
            <el-col class="top" :span="7">
              <input class="search-course" v-model="searchKey" placeholder="找课程" />
            </el-col>
          </el-row>
          <el-row class="middle-down">
            <el-col class="list" :span="8">
              <el-table :data="courseInfo" border height="300px">
                <el-table-column prop="name" label="课程"></el-table-column>
              </el-table>
            </el-col>
            <el-col :span="16" class="book-board">
              <div class="book" v-for="(course, index) in coursePage()" :key="index">
                <div>
                  <div class="course-cover">{{course.name}}</div>
                  <button
                    class="subscribe-course"
                    :value="JSON.stringify(course)"
                    @click="operateCourse($event)"
                  >{{judgeStatus(course.status)}}</button>
                </div>
              </div>
            </el-col>
          </el-row>
          <el-row class="bottom">
            <el-col :span="24">
              <el-pagination
                :total="total"
                layout="total, prev, pager, next"
                :page-size="4"
                :current-page="currentPage"
                @current-change="handleCurrentChange"
              ></el-pagination>
            </el-col>
          </el-row>
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
  name: 'querycourse',
  data () {
    return {
      total: 0,
      dataChanged: false,
      courseInfo: [],
      currentPage: 1,
      searchKey: '',
      studentId: '',
      type: ''
    }
  },
  methods: {
    judgeStatus (status) {
      if (status === 2) {
        return '学习中'
      }
      else if (status === 1) {
        return '切换'
      }
      else {
        return '未开通'
      }
    },
    handleCurrentChange (currentPage) {
      this.currentPage = currentPage
    },
    coursePage () {
      this.tempInfo = []
      if (this.searchKey.length > 0 && this.courseInfo.length > 0) {
        this.currentPage = 1
        this.tempInfo = this.courseInfo.filter(e => e.name.indexOf(this.searchKey) > -1)
      }
      if (this.tempInfo.length === 0) {
        this.tempInfo = this.courseInfo
      }
      this.total = this.tempInfo.length
      return this.tempInfo.slice((this.currentPage - 1) * 4, this.currentPage * 4)
    },
    operateCourse (e) {
      let status = e.target.innerHTML
      if (status === '切换') {
        let course = JSON.parse(e.target.value)
        this.$store.state.CATEGORY.id = course.id
        this.$store.state.CATEGORY.name = course.name
        let message = new URLSearchParams()
        message.append('student_id', this.studentId)
        message.append('book_id', this.$store.state.CATEGORY.id)
        axios.post(this.$store.state.BASEURL + 'study/change_course', message)
        this.getOpenCourse()
      }
    },
    getOpenCourse () {
      this.courseInfo = []
      axios.get(this.$store.state.BASEURL + 'books/get_course_info').then((res) => {
        this.total = res.data.length
        for (let index = 0; index < res.data.length; index++) {
          let aCourse = new Object()
          aCourse.name = res.data[index].fields.category
          aCourse.id = res.data[index].pk
          aCourse.status = 0
          this.courseInfo.push(aCourse)
        }
        axios.get(this.$store.state.BASEURL + 'study/get_opened_course?student_id=' + this.studentId).then((res) => {
          console.log(res.data)
          if (res.data !== 'get_current_course_failed') {
            let temp = []
            for (let i = 0; i < res.data.length; i++) {
              let id = res.data[i].fields.book
              let status = res.data[i].fields.status
              this.courseInfo.forEach(element => {
                if (element.id === id) {
                  element.status = status + 1
                  temp.push(element)
                  delete this.courseInfo[this.courseInfo.indexOf(element)]
                }
              })
            }
            if (this.type === '切换单词书') {
              this.courseInfo = temp
            } else {
              this.courseInfo = this.courseInfo.filter(Boolean)
            }
            this.tempInfo = this.courseInfo
          }
        })
      })
    }
  },
  mounted () {
    this.type = this.$route.params.type
    this.studentId = sessionStorage.getItem('student')
    this.getOpenCourse()
  },
  components: {
    MainShow,
    MainShowTop
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

.main-top {
  background-color: white;;
  height: 50px;
}

.problem-board {
  height: 450px;
  z-index: -2;
  margin-top: 50px;
  border-radius: 5px;
  background: rgb(243, 243, 243);
}

.top {
  margin-top: 30px;
  height: 50px;
  border-bottom: 1px solid #d8d8d8;
}

.top-title {
  font-family: SimSun;
  font-size: 16px;
  font-weight: bolder;
  color: rgb(118, 118, 118);
}

.search-course {
  border: 1px solid rgb(222, 222, 223);
  border-radius: 5px;
}

input.search-course {
  height: 50%;
  width: 80%;
}

.top-title-img {
  position: relative;
  top: 5px;
  margin-left: 30px;
  margin-right: 5px;
  height: 25px;
  width: 25px;
  z-index: 0;
}

.middle-up {
  margin-top: 10px;
}

.middle-down {
  height: 290px;
  border-bottom: 1px solid #d8d8d8;
  margin-top: 3%;
}

button {
  padding: 0;
  width: 60px;
  height: 20px;
  margin-left: 5px;
  font-size: 12px;
  border: 0;
  outline: none;
  background: transparent;
  font-family: SimSun;
}

button:hover {
  color: #ffffff;
  background-color: rgb(6, 173, 118);
}

.book-board {
  height: 100%;
  position: absolute;
  right: 0;
}

.book {
  height: 100%;
  width: 25%;
  float: left;
}

.subscribe-course {
  border-radius: 5px;
  background-color: rgb(236, 236, 236);
  border: 1px solid #D8D8D8;
  position: absolute;
  bottom: 0;
  width: 10%;
  margin-left: 7%;
  margin-bottom: 2%;
}

.course-cover {
  position: absolute;
  top: 30%;
  width: 18%;
  height: 50%;
  margin-left: 3%;
  line-height: 200%;
  text-align: center;
  border: 1px solid black;
  background-color: white;
}

.list {
  height: 270px;
}

.query-course /deep/ .pager {
  margin: 0;
  width: 100%;
  padding-left: 20%;
}

.el-pagination /deep/ {
  float: right;
}

.el-table {
  margin: 5%;
}
</style>

