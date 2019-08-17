<template>
  <div class="test-result">
    <button @click="dialogVisible = true" :class="showClasses ? 'button-type-focus' : 'button-type-init'">修改密码</button>
    <div class="inner">
      <el-dialog :visible.sync="dialogVisible">
        <el-form :close-on-click-modal="false"
            :model="ruleForm"
            status-icon
            :rules="rules"
            ref="ruleForm"
            label-width="100px"
            >
            <el-form-item label="原密码" prop="oldPass">
              <el-input type="password" v-model="ruleForm.oldPass" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="新密码" prop="newPass">
              <el-input type="password" v-model="ruleForm.newPass" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="checkPass">
              <el-input type="password" v-model="ruleForm.checkPass"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button class="submit-button" type="primary" @click="submitForm('ruleForm')">提交</el-button>
              <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form-item>
        </el-form>
      </el-dialog>
    </div>
  </div>
</template>

<script>
const information = {
  PASSWORD_IS_SIMPLE: '密码太简单了，请输入3位以上密码',
  PASSWORD_IS_LONG: '密码太长了，请设置小于20位的密码',
  PASSWORD_IS_SAME: '新密码不应与原密码相同'
}
const axios = require('axios')
export default {
  data: function () {
    let validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.ruleForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass')
        }
        callback()
      }
    }
    let validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.ruleForm.newPass) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }

    return {
      dialogVisible: false,
      teacher_username: '',
      ruleForm: {
        checkPass: '',
        oldPass: '',
        newPass: ''
      },
      rules: {
        oldPass: [{ required: true, message: '请输入原始密码', trigger: 'blur' }],
        newPass: [
          {
            validator: validatePass,
            required: true,
            message: '请输入新密码',
            trigger: 'blur'
          }
        ],
        checkPass: [
          {
            validator: validatePass2,
            required: true,
            message: '两次输入密码不一致',
            trigger: 'blur'
          }
        ]
      }
    }
  },
  methods: {
    submitForm (formName) {
      if (this.ruleForm.newPass.length < 4) {
        this.$message(information.PASSWORD_IS_SIMPLE)
      }
      else if (this.ruleForm.newPass.length > 20) {
        this.$message(information.PASSWORD_IS_LONG)
      }
      else if (this.ruleForm.oldPass === this.ruleForm.newPass) {
        this.$message(information.PASSWORD_IS_SAME)
      }
      else {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.teacher_username = sessionStorage.getItem('teacher')
            let param = new URLSearchParams()
            param.append('username', this.teacher_username)
            param.append('oldpass', this.ruleForm.oldPass)
            param.append('newpass', this.ruleForm.newPass)
            axios.post(this.$store.state.BASEURL + 'teachers/change_password', param).then((res) => {
              if (res.data === 'modifyPasswordSuccess') {
                this.$message({
                  message: '修改成功',
                  type: 'success'
                })
                this.dialogVisible = false
                this.ruleForm.oldPass = ''
                this.ruleForm.newPass = ''
                this.ruleForm.checkPass = ''
              }
              else {
                this.$message({
                  message: '原密码输入错误',
                  type: 'error'
                })
              }
            })
          }
          return false
        })}
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>


<style scoped>
.test-result {
  position: absolute;
  width: 100%;
  height: 100%;
}

.button-type-init {
  border: 0;
  background-color: rgb(219, 226, 235);
  width: 100%;
  height: 100%;
}

.button-type-init:hover {
  border: 0;
  background: rgb(200, 200, 240);
  width: 100%;
  height: 100%;
}

.button-type-focus {
  border: 0;
  background: rgb(200, 200, 240);
  width: 100%;
  height: 100%;
}

.inner {
  position: absolute;
  left: 200%;
  width: 200%;
  height: 1100%;
  overflow: hidden;
}

.inner /deep/ .el-dialog__wrapper {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.inner /deep/ .el-dialog {
  padding: 0;
  width: 100%;
  height: 100%;
  margin: 0 !important;
}

.form /deep/ .demo-ruleForm {
  margin-top: 50px;
}

.form /deep/ .submit-button {
  margin-left: 60px;
  margin-right: 30px;
}
</style>
