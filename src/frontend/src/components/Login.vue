<template>
<div class="background-img">
  <el-row type="flex" justify="center" class="head-row">
    <el-col :span="7">
      <img class="logo-img" src="../images/50_icon.png"/>
      <p class="title">单词赢</p>
      <p class="slogan">三天背完小升初 七天背完中高考</p>
    </el-col>
  </el-row>
  <el-row type="flex" justify="center">
    <el-col :span="7">
      <el-tabs v-model="activeName">
        <el-tab-pane label="学生端登录" name="student">
          <el-form :label-position="labelPosition" label-width="80px" :model="loginForm" :rules="rules">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="loginForm.username" placeholder="请输入学生用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-checkbox v-model="loginForm.checked">自动登录</el-checkbox>
            <el-link :underline="false" class="form-link" @click="forgetStudent">忘记密码</el-link>
            <el-button class="submit-btn" type="primary" @click="submitStudent">登录</el-button>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="教师端登录" name="teacher">
          <el-form :label-position="labelPosition" label-width="80px" :model="loginForm" :rules="rules">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="loginForm.username" placeholder="请输入教师用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-checkbox v-model="loginForm.checked">自动登录</el-checkbox>
            <el-link :underline="false" class="form-link" @click="forgetTeacher">忘记密码</el-link>
            <el-button type="primary" class="submit-btn" @click="submitTeacher">登录</el-button>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-col>
  </el-row>
</div>
</template>

<script>
const axios = require('axios')
import * as Cookies from 'js-cookie'
export default {
  data: function () {
    return {
      activeName: 'student',
      labelPosition: 'left',
      loginForm: {
        username: '',
        password: '',
        checked: false
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitStudent () {
      let urlStr = 'information/login_student'
      this.submitFunc(urlStr)
    },
    submitTeacher () {
      let urlStr = 'information/login_teacher'
      this.submitFunc(urlStr)
    },
    submitFunc (urlStr) {
      let param = new URLSearchParams()
      param.append('username', this.loginForm.username)
      param.append('password', this.loginForm.password)
      let url = this.$store.state.BASEURL + urlStr
      axios.post(url, param)
        .then(res => {
          if (res.data === 'loginStudentSuccess') {
            this.$message({
              message: '登录成功',
              type: 'success'
            })
            if (urlStr === 'information/login_student') {
              sessionStorage.setItem('student', this.loginForm.username)
              if (this.loginForm.checked) {
                Cookies.set('student', this.loginForm.username, {expires: 3})
              }
              this.$router.push('/beforestudying')
            }
          }
          else if (res.data === 'loginTeacherSuccess') {
            this.$message({
              message: '登录成功',
              type: 'success'
            })
            if (urlStr === 'information/login_teacher') {
              sessionStorage.setItem('teacher', this.loginForm.username)
              if (this.loginForm.checked) {
                Cookies.set('teacher', this.loginForm.username, {expires: 3})
              }
              this.$router.push('/teacherclasses')
            }
          } else {
            this.$message.error('用户名或密码错误，登录失败')
          }
        })
    },
    forgetStudent () {
      this.$message({
        message: '忘记密码的话，快去找老师吧',
        type: 'warning'
      })
    },
    forgetTeacher () {
      this.$message({
        message: '忘记密码的话，快去找管理员吧',
        type: 'warning'
      })
    }
  }
}
</script>

<style scoped>
.head-row {
  margin-bottom: 20px;
  margin-top: 120px;
  text-align: center;
}

.logo-img {
  height: 45px;
  width: 55px;
}

.title {
  display: inline;
  font-size: 32px;
  font-weight: bold;
  margin-left: 20px;
}

.slogan {
  color: #888;
  font-size: 15px;
}

.submit-btn {
  display: block;
  width: 100%;
  margin-top: 20px;
}

.form-link {
  float: right;
}

.background-img {
  background: url('../images/48_login bg.jpg');
  background-size: cover;
  border-width: 0;
  height: 100%;
  left: 0;
  position: fixed;
  top: 0;
  width: 100%;
}
</style>
