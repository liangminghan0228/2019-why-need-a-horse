<template>
<div>
    <el-button type="text" @click="getTestLog" icon="el-icon-document">测试记录</el-button>
    <el-dialog :visible.sync="visible" :close-on-click-modal="false">
      <span>{{title}}的测试成绩</span>
      <div class="test-list">
        <el-table
          :data="testPage()"
          height="300px"
          stripe
          border
          >
          <el-table-column type="index" min-width="5%"></el-table-column>
          <el-table-column prop="test_type" label="测试种类"></el-table-column>
          <el-table-column prop="book_name" label="课本"></el-table-column>
          <el-table-column :formatter="isPass" label="是否通过"></el-table-column>
          <el-table-column prop="test_score" label="测试成绩"></el-table-column>
          <el-table-column prop="test_time" label="测试时间"></el-table-column>
        </el-table>
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
    </el-dialog>
  </div>
</template>

<script>
const axios = require('axios')
export default {
  data () {
    return {
      visible: false,
      testInfo: [],
      total: 0,
      pageSize: 10,
      currentPage: 1,
      title: ''
    }
  },
  props: {
    home: {}
  },
  methods: {
    isPass (row) {
      if (row.is_pass === true) {
        return '通过'
      } else {
        return '未通过'
      }
    },
    getTestLog () {
      if (this.home.selectedStudents === null || this.home.selectedStudents.hasOwnProperty('pk') === false) {
        this.$message.error({
          showClose: true,
          message: '请先选择要查询测试记录的学生'
        })
      } else {
        this.visible = true
        this.title = this.home.selectedStudents.fields.student_name
        let message = new URLSearchParams()
        message.append('student_id', this.home.selectedStudents.pk)
        axios.post(this.$store.state.BASEURL + 'study/teacher_test_record', message).then((res) => {
          this.testInfo = []
          this.total = res.data.length
          for (let i = 0; i < res.data.length; i++) {
            this.testInfo.push(res.data[i])
            this.testInfo[i].test_type = this.switchType(this.testInfo[i].test_type)
          }
        })
      }
    },
    testPage () {
      return this.testInfo.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    },
    handleSizeChange (pageSize) {
      this.pageSize = pageSize
    },
    handleCurrentChange (currentPage) {
      this.currentPage = currentPage
    },
    switchType (type) {
      switch (type) {
      case 'reviewTest':
        return '巩固测试'
      case 'preTest':
        return '学前检测'
      case 'afterTest':
        return '学后检测'
      default:
        return '一测到底'
      }
    }
  }
}
</script>

<style scoped>
.el-button, .el-button--text {
  width: 100%;
  height: 30px;
  line-height: 30px;
  padding: 0;
  color: rgb(77, 77, 77);
}

.el-pagination /deep/ {
  float: right;
}

.turn-page {
  margin-top: 6%;
  margin-bottom: 10%;
}
</style>