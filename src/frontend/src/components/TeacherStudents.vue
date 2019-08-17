<template>
  <div class="teacher-students">
    <el-row class="top-row">
      <el-col :span="24"></el-col>
    </el-row>
    <el-row class="down-row">
      <teacher-side-bar :showStudents="true"></teacher-side-bar>
      <el-col :span="21" class="right-part">
        <el-row>
          <div class="tip">
            <i class="el-icon-search"></i>请选择班级
          </div>
        </el-row>
        <el-row>
          <div class="select-class">
            <select v-model="selectedClassInfo">
              <option v-for="(aClass, index) in classes" :key="index">班级ID:{{aClass.pk}}--班级名称:{{aClass.fields.class_name}}</option>
            </select>
            <button class="confirm" @click="showStudentsByClass">确认</button>
            <button class="showAllStudents" @click="showAllStudents">显示全部学生</button>
          </div>
        </el-row>
        <el-row>
          <div class="tip">
            <el-col :span="4"><i class="el-icon-search"></i>学生名册</el-col>
            <el-col :span="6" :offset="2"><input v-show="showSearch" v-model="searchKey" class="search" placeholder="学生姓名"/></el-col>
            <el-col :span="3"><button v-show="showSearch" @click="searchStudent" class="search">查找</button></el-col>
          </div>
        </el-row>
        <div>
          <el-row>
            <div class="button-region">
              <el-col :span="3">
                <register-course :home="this"></register-course>
              </el-col>
              <el-col :span="3">
                <teacher-test-record :home="this"></teacher-test-record>
              </el-col>
              <el-col :span="3">
                <el-button type="text" icon="el-icon-search" @click="changeShowSearch">查找学员</el-button>
              </el-col>
              <el-col :span="3">
                <new-student :classId="selectedClass" @regetStudentsInfo="getStudentsInfo"></new-student>
              </el-col>
              <el-col :span="3">
                <el-button type="text" icon="el-icon-delete" @click="deleteStudents">删除学员</el-button>
              </el-col>
              <el-col :span="3">
                <el-button type="text" icon="el-icon-document-remove" @click="cancelSelect">取消选择</el-button>
              </el-col>
            </div>
          </el-row>
          <div class="students-list">
            <el-table
              :data="studentsPage()"
              :row-class-name="rowClassName"
              :header-cell-style="headerCellStyle"
              highlight-current-row
              @current-change="selectStudents"
              height="450px"
              border
            >
              <el-table-column prop="pk" label="ID" min-width="5%" align="center"></el-table-column>
              <el-table-column prop="fields.student_name" label="姓名" min-width="10%" align="center"></el-table-column>
              <el-table-column prop="fields.email" label="邮箱" min-width="8%" align="center"></el-table-column>
              <el-table-column prop="fields.login_times" label="登录天数" min-width="5%" align="center"></el-table-column>
              <el-table-column prop="fields.coin_total" label="金币数量" min-width="10%" align="center"></el-table-column>
              <el-table-column prop="fields.login_times" label="连续未登录天数" min-width="10%" align="center"></el-table-column>
              <el-table-column label="上次登录时间" :formatter="formatTime" min-width="10%" align="center"></el-table-column>
              <el-table-column prop="fields.classes" label="班级" min-width="10%" align="center"></el-table-column>
              <el-table-column prop="fields.register_time" label="注册日期" min-width="10%" align="center"></el-table-column>
              <el-table-column label="状态" :formatter="judgeStatus" min-width="10%" align="center"></el-table-column>
            </el-table>
          </div>
        </div>
        <div class="turn-page">
          <el-pagination
            background
            layout="total, sizes, prev, pager, next"
            :total="total"
            :page-size="pageSize"
            :current-page="1"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          ></el-pagination>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import TeacherSideBar from './common/TeacherSideBar'
import RegisterCourse from './RegisterCourse'
import NewStudent from './NewStudent'
import TeacherTestRecord from './TeacherTestRecord'
const axios = require('axios')
export default {
  data: function () {
    return {
      even: 'even-row',
      odd: 'odd-row',
      students: [],
      classes: [],
      selectedStudents: {},
      showedStudents: [],
      total: 0,
      pageSize: 10,
      currentPage: 1,
      selectedClassInfo: '',
      selectedClass: '',
      studentToSub: {},
      showSearch: false,
      searchKey: '',
      last_login: 0
    }
  },
  methods: {
    formatTime (row) {
        let time = row.fields.last_login.split('T')[0] + '  ' + row.fields.last_login.split('T')[1].split('Z')[0]
        return time
    },
    judgeStatus (row) {
      if (row.fields.pay_status === true) {
        return '已付费'
      } else {
        return '未付费'
      }
    },
    changeShowSearch () {
      if (this.showSearch === false) {
        this.showSearch = true
      }
      else {
        this.showSearch = false
      }
    },
    searchStudent () {
      if (this.searchKey !== '' && this.selectedClass !== '') {
        this.currentPage = 1
        this.showedStudents = this.students.filter(e => e.fields.classes + '' === this.selectedClass).filter(e => e.fields.student_name.indexOf(this.searchKey) > -1)
        this.total = this.showedStudents.length
      }
      else if (this.searchKey !== '' && this.selectedClass === '') {
        this.currentPage = 1
        this.showedStudents = this.students.filter(e => e.fields.student_name.indexOf(this.searchKey) > -1)
        this.total = this.showedStudents.length
      } else {
        this.total = 0
        this.showedStudents = []
      }
      this.searchKey = ''
    },
    studentsPage () {
      return this.showedStudents.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    },
    handleSizeChange (pageSize) {
      this.pageSize = pageSize
    },
    handleCurrentChange (currentPage) {
      this.currentPage = currentPage
    },
    rowClassName (rowIndex) {
      if (rowIndex.rowIndex % 2 === 0) {
        return 'even-row'
      }
      else {
        return 'odd-row'
      }
    },
    headerCellStyle () {
      return 'background: linear-gradient(rgb(213, 223, 236), rgb(190, 204, 224));'
    },
    getStudentsInfo () {
      this.students = []
      axios.get(this.$store.state.BASEURL + 'information/teacher_students/').then((res) => {
        this.total = res.data.length
        this.students = res.data
        this.showedStudents = this.students
      })
    },
    getClassesInfo () {
      this.classesInfo = []
      axios.get(this.$store.state.BASEURL + 'information/teacher_classes/').then((res) => {this.classes = res.data})
    },
    selectStudents (currentRow) {
      this.selectedStudents = currentRow
    },
    deleteStudents () {
      if (this.selectedStudents === null || this.selectedStudents.hasOwnProperty('pk') === false) {
        this.$message.error({
          showClose: true,
          message: '请选择要删除的学生'
        })
      }
      else {
        axios.post(this.$store.state.BASEURL + 'information/teacher_delete_students/', JSON.stringify(this.selectedStudents)).then((res) => {
          this.total = res.data.length
          this.students = res.data
          this.showedStudents = this.students
          this.selectedClass = ''
          this.$message({
            showClose: true,
            message: '删除成功'
          })
        })
      }
    },
    showStudentsByClass () {
      if (this.selectedClass !== '') {
        this.currentPage = 1
        this.showedStudents = this.students.filter(e => this.selectedClass === e.fields.classes + '')
        this.total = this.showedStudents.length
      } else {
        this.$message.error({
          showClose: true,
          message: '请先选择班级'
        })
      }
    },
    showAllStudents () {
      this.selectedClassInfo = ''
      this.showedStudents = this.students
      this.total = this.showedStudents.length
      this.selectedClass = ''
    },
    cancelSelect () {
      if (this.selectedStudents !== null) {
        if (this.selectedClass === '') {
          this.getClassesInfo()
          this.getStudentsInfo()
        } else {
          this.getClassesInfo()
          this.students = []
          axios.get(this.$store.state.BASEURL + 'information/teacher_students/').then( (res) => {
            this.total = res.data.length
            this.students = res.data
            this.showedStudents = this.students
            this.showStudentsByClass()
          })
        }
      }
    },
    functionInMounted () {
      this.getClassesInfo()
      axios.get(this.$store.state.BASEURL + 'information/teacher_students/').then((res) => {
        this.total = res.data.length
        this.students = res.data
        this.showedStudents = this.students
        if (typeof (this.$route.params.class) !== 'undefined') {
          this.selectedClass = this.$route.params.class + ''
          this.showStudentsByClass()
        }
      })
    }
  },
  mounted () {
    this.functionInMounted()
  },
  watch: {
    selectedClassInfo () {
      if (this.selectedClassInfo === '') {
        this.selectedClass = ''
      } else {
        this.selectedClass = this.selectedClassInfo.split('--')[0].split(':')[1]
      }
    }
  },
  components: {
    TeacherSideBar,
    RegisterCourse,
    NewStudent,
    TeacherTestRecord
  }
}
</script>

<style scoped>
.teacher-students {
  margin: 0;
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  background-color: rgb(244, 244, 244);
}

.top-row {
  height: 30px;
  background: linear-gradient(rgb(199, 211, 225), rgb(185, 198, 215));
}

.right-part {
  margin-top: 1%;
  border: 0 !important;
}

.tip {
  background: linear-gradient(rgb(237, 237, 237), rgb(223, 223, 223));
  height: 25px;
  line-height: 25px;
  font-size: 13px;
  padding-left: 20px;
  margin-left: 10px;
  margin-right: 20px;
  text-align: left;
}

.select-class {
  margin-left: 10px;
  position: relative;
  height: 35px;
}

select {
  width: 18%;
  line-height: 22px;
  height: 22px;
  position: absolute;
  top: 50%;
  margin: -10px 0 0 0;
  left: 3%;
  background-color: white;
}

option {
  line-height: 22px;
  height: 22px;
}

.confirm {
  position: absolute;
  top: 50%;
  margin: -11px 0 0 0;
  left: 25%;
  height: 24px;
  width: 8%;
  font-size: 0.1vw;
  padding: 0;
}

.showAllStudents {
  position: absolute;
  top: 50%;
  margin: -11px 0 0 0;
  left: 35%;
  height: 24px;
  width: 8%;
  font-size: 0.1vw;
  padding: 0;
}

.button-region {
  background: linear-gradient(rgb(215, 224, 239), rgb(172, 187, 208));
  height: 35px;
  margin-left: 10px;
  margin-right: 20px;
}

.el-button, .el-button--text {
  width: 100%;
  height: 30px;
  line-height: 30px;
  padding: 0;
  color: rgb(77, 77, 77);
}

.search {
  width: 60%;
  height: 50%;
  margin: 0;
  padding: 0;
  border: 1px solid;
}

.students-list {
  overflow: hidden;
  margin-left: 10px;
  margin-right: 20px;
}

.students-list /deep/ .even-row {
  background: rgb(255, 255, 255);
}

.students-list /deep/ .odd-row {
  background: rgb(233, 238, 243);
}

.students-list /deep/ tr.current-row>td {
  background-color: #a2a4a7 !important;
}

.turn-page {
  margin-left: 10px;
  margin-right: 20px;
  padding: 0;
  text-align: right;
  margin-top: 30px;
}
</style>
