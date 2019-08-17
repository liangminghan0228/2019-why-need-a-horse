<template>
  <div>
    <el-button type="text" @click="newStudent" icon="el-icon-circle-plus-outline" class="new-student">添加学员</el-button>
    <el-dialog title="添加学员" :visible.sync="dialogFormVisible" :close-on-click-modal="false">
      <p> 添加到班级：{{classId}}</p>
      <el-form :model="form" :rules="rules" ref="form">
        <el-form-item label="请输入学生姓名" :label-width="formLabelWidth" prop="name">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item
        prop="email"
        label="请输入学生邮箱"
        :label-width="formLabelWidth"
        >
        <el-input v-model="form.email"></el-input>
        </el-form-item>
        <el-form-item label="请输入学生ID" :label-width="formLabelWidth" prop="id">
          <el-input v-model="form.id" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="请输入学生密码" :label-width="formLabelWidth" prop="password">
          <el-input v-model="form.password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="请选择学生年级" :label-width="formLabelWidth" prop="grade">
          <el-select v-model="form.grade" placeholder="请选择状态">
            <el-option label="小学一年级" :value="1"></el-option>
            <el-option label="小学二年级" :value="2"></el-option>
            <el-option label="小学三年级" :value="3"></el-option>
            <el-option label="小学四年级" :value="4"></el-option>
            <el-option label="小学五年级" :value="5"></el-option>
            <el-option label="小学六年级" :value="6"></el-option>
            <el-option label="初中一年级" :value="7"></el-option>
            <el-option label="初中二年级" :value="8"></el-option>
            <el-option label="初中三年级" :value="9"></el-option>
            <el-option label="高中一年级" :value="10"></el-option>
            <el-option label="高中二年级" :value="11"></el-option>
            <el-option label="高中三年级" :value="12"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="请输入学生学校" :label-width="formLabelWidth" prop="school">
          <el-input v-model="form.school" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="请选择付费状态" :label-width="formLabelWidth" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态">
            <el-option label="已付费" :value="true"></el-option>
            <el-option label="未付费" :value="false"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancel">取 消</el-button>
        <el-button type="primary" @click="submit('form')">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
const axios = require('axios')
export default {
  data: function () {
    return {
      dialogFormVisible: false,
      form: {
        name: '',
        email: '',
        id: '',
        status: false,
        password: '',
        grade: '',
        school: ''
      },
      rules: {
        name: [
          {
            required: true
          }
        ],
        id: [
          {
            required: true
          }
        ],
        email: [
          { required: true, message: '请输入学生邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ],
        status: [
          {
            required: true
          }
        ],
        password: [
          {
            required: true
          }
        ]
      },
      formLabelWidth: '200px'
    }
  },
  methods: {
    submit (form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          if (this.form.name === 'name' || this.form.id === 'id') {
            this.$message({
              message: '学生用户名与ID不符合规范，请重新输入',
              type: 'warning'
            })
            return false
          }
          const url = this.$store.state.BASEURL + 'information/add_new_student'
          let param = []
          param.push({'currClass': this.classId})
          param.push({'studentInfo': this.form})
          axios.post(url, JSON.stringify(param)).then(res => {
            if (res.data !== 'SuccessCreateStudent') {
              this.$message({
                message: '添加学员失败，该ID已存在！',
                type: 'warning'
              })
            } else {
              this.$message({
                message: '添加学员成功！',
                type: 'success'
              })
              this.dialogFormVisible = false
              this.$emit('regetStudentsInfo')
              this.form = {name: ' ', email: '', id: ' ', status: false, password: ' ', grade: ' ', school: ' '}
            }
          })
          return true
        } else {
          this.$message({
            message: '填写不符合规范！',
            type: 'warning'
          })
          return false
        }
      })
    },
    newStudent () {
      if (this.classId.length === 0) {
        this.$message({
          message: '请先选择所要添加到的班级',
          type: 'warning'
        })
      } else {
        this.dialogFormVisible = true
      }
    },
    cancel () {
      this.dialogFormVisible = false
      this.form = {name: ' ', email: '', id: ' ', status: false, password: ' ', grade: ' ', school: ' '}
    }
  },
  props: {
    classId: {
      type: String,
      default: '1'
    }
  }
}
</script>

<style scoped>
p {
  font-weight: 600;
  font-size: 20px;
  margin-top: 0;
}

.el-input {
  width: 70%;
}

.new-student {
  width: 100%;
  height: 30px;
  line-height: 30px;
  padding: 0;
  color: rgb(77, 77, 77);
}

.el-dialog__wrapper /deep/  .el-dialog__headerbtn {
  display: none;
}
</style>
