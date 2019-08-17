<template>
  <div class="classes">
    <el-row class="top-row">
      <el-col :span="24" class="cancel-border">
        <div class="cap"></div>
      </el-col>
    </el-row>
    <el-row>
      <teacher-side-bar :showClasses="true"></teacher-side-bar>
      <el-col :span="21" class="cancel-border">
        <div class="right-part">
          <el-row class="button-region">
            <el-col :span="2" :offset="1" class="top-button">
              <new-class @regetClassesInfo="getClassesInfo"></new-class>
            </el-col>
            <el-col :span="2" :offset="1" class="top-button">
              <el-button type="text" icon="el-icon-circle-close" @click="deleteClasses">删除班级</el-button>
            </el-col>
            <el-col :span="2" :offset="1" class="top-button">
              <el-button type="text" icon="el-icon-document-remove" @click="cancelSelect">取消选择</el-button>
            </el-col>
          </el-row>
          <el-table
            :data="classesPage()"
            :row-class-name="rowClassName"
            :header-cell-style="headerCellStyle"
            highlight-current-row
            @current-change="selectClasses"
            height="450px"
            border
          >
            <el-table-column prop="pk" label="班级id" min-width="10%" align="center"></el-table-column>
            <el-table-column prop="fields.class_name" label="班级名称" min-width="20%" align="center"></el-table-column>
            <el-table-column
              prop="fields.student_number"
              label="学生人数"
              min-width="10%"
              align="center"
            ></el-table-column>
            <el-table-column
              prop="fields.classes_description"
              label="班级说明"
              min-width="30%"
              align="center"
            ></el-table-column>
            <el-table-column label="操作" min-width="20%" align="center">
              <template slot-scope="scope">
                <el-button @click="handleToStudents(scope.row)" type="text">添加/删除学员</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="turn-page">
            <el-pagination
              background
              layout="total, sizes, prev, pager, next"
              :total="total"
              :page-size="pageSize"
              :current-page="currentPage"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            ></el-pagination>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import TeacherSideBar from './common/TeacherSideBar'
import NewClass from './NewClass'
const axios = require('axios')
export default {
  components: {
    TeacherSideBar,
    NewClass
  },
  data: function () {
    return {
      number: 1,
      even: 'even-row',
      odd: 'odd-row',
      classesInfo: [],
      showedClasses: [],
      total: 0,
      pageSize: 10,
      currentPage: 1,
      selectedClasses: {}
    }
  },
  methods: {
    classesPage () {
      return this.showedClasses.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    },
    handleSizeChange (pageSize) {
      this.pageSize = pageSize
    },
    handleCurrentChange (currentPage) {
      this.currentPage = currentPage
    },
    rowClassName ({row, rowIndex}) {
      row.index = rowIndex
      if (rowIndex % 2 === 0) {
        return 'even-row'
      }
      else {
        return 'odd-row'
      }
    },
    headerCellStyle () {
      return 'background: linear-gradient(rgb(213, 223, 236), rgb(190, 204, 224));'
    },
    handleToStudents (row) {
      this.$router.push({
        name: 'teacherstudents',
        params: {
          class: row.pk
        }
      })
    },
    getClassesInfo () {
      this.classesInfo = []
      axios.get(this.$store.state.BASEURL + 'information/teacher_classes/').then((res) => {
        this.total = res.data.length
        for (let i = 0; i < res.data.length; i++) {
          this.classesInfo.push(res.data[i])
        }
        this.showedClasses = this.classesInfo
      })
    },
    selectClasses (selection) {
      this.selectedClasses = selection
    },
    deleteClasses () {
      if (this.selectedClasses === null || this.selectedClasses.hasOwnProperty('pk') === false) {
        this.$message.error({
          showClose: true,
          message: '请先选择要删除的班级'
        })
      }
      else {
        axios.post(this.$store.state.BASEURL + 'information/teacher_delete_classes/', JSON.stringify(this.selectedClasses)).then((res) => {
          this.classesInfo = []
          for (let i = 0; i < res.data.length; i++) {
            this.classesInfo.push(res.data[i])
          }
          this.total = this.classesInfo.length
          this.showedClasses = this.classesInfo
          this.$message({
            showClose: true,
            type: 'success',
            message: '删除成功'
          })
        })
      }
    },
    cancelSelect () {
      this.getClassesInfo()
    }
  },
  mounted () {
    this.getClassesInfo()
  }
}
</script>

<style scoped>
* {
  top: 0;
  left: 0;
  padding: 0;
  margin: 0;
}

.top-row {
  height: 30px;
  background: linear-gradient(rgb(199, 211, 225), rgb(185, 198, 215));
}

.classes {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 100%;
  background-color: rgb(244, 244, 244);
  overflow: hidden;
}

.cap {
  height: 100%;
  width: 100%;
  background: linear-gradient(rgb(199, 211, 225), rgb(185, 198, 215));
}

.cancel-border {
  border: 0 !important;
}

.right-part {
  padding-left: 10px;
  margin-right: 20px;
}

.button-region {
  background: linear-gradient(rgb(215, 224, 239), rgb(172, 187, 208));
  margin-top: 1%;
}

.el-button, .el-button--text {
  width: 80%;
  height: 40px;
  line-height: 40px;
  padding: 0;
  color: rgb(77, 77, 77);
}

.top-button {
  border: 0 !important;
}

.el-col {
  border: 1px solid rgb(188, 197, 210);
  text-align: center;
  color: rgb(77, 77, 77);
}

.right-part /deep/ .table-row-style {
  height: 10px;
}

.right-part /deep/ .table-cell-style {
  padding: 0;
}

.right-part /deep/ .even-row {
  background-color: rgb(255, 255, 255);
}

.right-part /deep/ .odd-row {
  background-color: rgb(233, 238, 243);
}

.classes /deep/ tr.current-row>td {
  background-color: #a2a4a7 !important;
}

.el-pagination /deep/ {
  float: right;
}

.turn-page {
  margin-top: 6%;
  margin-bottom: 10%;
}
</style>



