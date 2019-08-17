<template>
  <div>
    <el-button type="text" @click="onRegister" class="register-course" icon="el-icon-folder-add">注册课程</el-button>
    <el-dialog title="注册课程" :visible.sync="dialogFormVisible" :close-on-click-modal="false">
      <el-form :model="form" ref="form" :rules="rules">
        <el-form-item label="注册对象:" :label-width="formLabelWidth">
          <p>{{student_name}}<span class="slot"></span>({{student_id}})</p>
        </el-form-item>
        <el-form-item>
          <div class="transfer-block">
            <el-transfer
              v-model="value"
              filterable
              :render-content="renderFunc"
              @change="handleChange"
              :titles="['课程库', '添加课程']"
              :button-texts="['撤回', '添加']"
              :format="{
                noChecked: '${total}',
                hasChecked: '${checked} / ${total}'
              }"
              :data="showList">
              <el-col :span="10"><div class="slot"></div></el-col>
              <el-button class="transfer-footer" slot="left-footer" size="small" @click="dialogFormVisible = false">退 出</el-button>
              <el-button class="transfer-footer" slot="right-footer" size="small" @click="submitByTransfer">注 册</el-button>
            </el-transfer>
          </div>
        </el-form-item>
      </el-form>
      <hr />
      <h4>注册结果</h4>
      <p>已注册课程</p>
      <el-table :data="courseRegisteredList" :row-class-name="tableRowClassName">
        <el-table-column prop="name" label="课程名称"></el-table-column>
        <el-table-column prop="status" label="当前状态"></el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
const axios = require('axios')
export default {
  data: function () {
    return {
      courseRegisteredList: [],
      showList: [],
      courseList: [],
      value: [],
      form: {},
      transfer: [],
      rules: {
        courseId: [
          {
            required: false
          }
        ],
        coursePassword: [
          {
            required: false
          }
        ]
      },
      formLabelWidth: '120px',
      halfFormLabelWidth: '60px',
      dialogFormVisible: false,
      student_id: 'id',
      student_name: 'name'
    }
  },
  methods: {
    tableRowClassName ({row}) {
      if (row.status === '已过期') {
        return 'overdue-row'
      } else {
        return 'subscription-row'
      }
    },
    showClass: function () {
      const url = this.$store.state.BASEURL + 'study/show_register_result?student_id=' + this.student_id
      axios.get(url).then(res => {
        let tmp = []
        for (let i = 0; i < res.data.length; i++) {
          let strStatus = ''
          strStatus = '已注册'
          tmp.push({
            'id': res.data[i]['id'],
            'name': res.data[i]['name'],
            'status': strStatus
          })
        }
        this.courseRegisteredList = tmp
        this.value = []
        for (let i = 0; i < tmp.length; i++) {
          this.value.push(this.courseRegisteredList[i]['id'])
        }
        this.showCourses()
      })
    },
    renderFunc (h, option) {
      return <span>{option.key} - {option.label}</span>
    },
    handleChange (value) {
      this.transfer = value
    },
    submitByTransfer () {
      if (this.transfer.length === 0) {
        this.$message({
          showClose: true,
          type: 'warning',
          message: '没有要添加的课程'
        })
        return false
      }
      this.$confirm('此操作一经执行不支持恢复, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let param = []
        let currStudent = {
          'student_id': this.student_id,
          'student_name': this.student_name
        }
        param.push(currStudent)
        param.push(this.transfer)
        const url = this.$store.state.BASEURL + 'study/register_course'
        axios.post(url, JSON.stringify(param)).then(res => {
          if (res.data === 'SuccessRegister') {
            this.$message({
              showClose: true,
              type: 'success',
              message: '添加成功!'
            })
            this.showClass()
            this.transfer = []
          }
        })
      }).catch(() => {
        this.$message({
          showClose: true,
          type: 'info',
          message: '已取消'
        })
      })
    },
    onRegister () {
      if (this.home.selectedStudents === null || this.home.selectedStudents.hasOwnProperty('pk') === false) {
        this.$message.error({
          showClose: true,
          message: '请先选择要注册的学生'
        })
      } else {
        this.student_name = this.home.selectedStudents.fields.student_name
        this.student_id = this.home.selectedStudents.pk
        this.dialogFormVisible = true
        this.showClass()
      }
    },
    showCourses () {
      const url = this.$store.state.BASEURL + 'books/get_courses'
      axios.get(url).then(res => {
        this.courseList = res.data
        if (res.data) {
          let flag = false
          this.showList = []
          for (let i = 0; i < this.courseList.length; i++) {
            for (let j = 0; j < this.courseRegisteredList.length; j++) {
              if (this.courseList[i].pk === this.courseRegisteredList[j]['id']) {
                flag = true
              }
            }
            if (flag === false) {
              this.showList.push({
                key: this.courseList[i]['pk'],
                label: this.courseList[i]['fields']['category'],
                disabled: false
              })
            } else {
              this.showList.push({
                key: this.courseList[i]['pk'],
                label: this.courseList[i]['fields']['category'],
                disabled: true
              })
            }
            flag = false
          }
        }
      })
    }
  },
  props: {
    home: {}
  },
  mounted () {
  },
  watch: {
    dialogFormVisible: function () {
      if (this.dialogFormVisible === false) {
        this.value = []
        this.showList = []
      }
    }
  }
}
</script>

<style scoped>
.el-form-item__content p {
  width: 100%;
  margin: 0;
}

.el-transfer {
  text-align: left;
  display: inline-block;
}

.transfer-block {
  text-align: center;
}

.el-form-item__content .el-input {
  width: 45%;
}

.register-button {
  width: 180px;
  margin: 10px auto;
}

.el-transfer-panel__footer button {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-left: -28px;
  margin-top: -16px;
}

.el-button {
  border-radius: 5px !important;
}

.slot {
  display: inline-block;
  width: 1px;
  height: 1px;
}

.register-course {
  width: 100%;
  height: 30px;
  line-height: 30px;
  padding: 0;
  color: rgb(77, 77, 77);
}

h4 {
  width: 60px;
  margin-left: 10px;
}

p {
  width: 70px;
  margin-left: 10px;
}

.el-table {
  font-size: 12px;
  width: 100%;
}

.el-table /deep/ .subscription-row {
  color: rgb(8, 184, 52);
}
</style>
