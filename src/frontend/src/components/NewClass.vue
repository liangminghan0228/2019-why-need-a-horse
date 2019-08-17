<template>
  <div>
    <el-button
      class="new-class-button"
      type="text"
      @click="dialogFormVisible = true"
      icon="el-icon-circle-plus">
      新增班级
    </el-button>
    <el-dialog title="新增班级" :visible.sync="dialogFormVisible" :close-on-click-modal="false">
      <el-form :model="form" :rules="rules" ref="form">
        <el-form-item label="请输入班级名称:" :label-width="formLabelWidth" prop="className">
          <el-input class="class-input" v-model="form.className"></el-input>
        </el-form-item>
        <el-form-item label="请输入班级说明:" :label-width="formLabelWidth" prop="introduce">
          <el-input class="class-input" v-model="form.introduce" type="textarea" :rows="3"></el-input>
        </el-form-item>
        <el-form-item label="请选择班级状态:" :label-width="formLabelWidth" prop="status">
          <el-select class="class-input" v-model="form.status" placeholder="正常" :disabled="true">
            <el-option label="正常" :value="true"></el-option>
            <el-option label="异常" :value="false"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button class="class-button" @click="dialogFormVisible = false">取 消</el-button>
        <el-button class="class-button" type="primary" @click="submit('form')">确 定</el-button>
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
        className: '',
        introduce: '',
        status: ''
      },
      formLabelWidth: '130px',
      rules: {
        className: [
          {
            required: true
          }
        ]
      }
    }
  },
  methods: {
    submit (form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          const url = this.$store.state.BASEURL + 'information/add_new_class'
          axios.post(url, JSON.stringify(this.form)).then(res => {
            if (res.data !== 'SuccessCreateClass') {
              this.$message({
                message: '注册失败',
                type: 'warning'
              })
            } else {
              this.$message({
                message: '注册成功',
                type: 'success'
              })
            }
            this.dialogFormVisible = false
            this.form.className = ''
            this.form.introduce = ''
            this.form.status = ''
            this.$emit('regetClassesInfo')
          })
          return true
        } else {
          this.$message({
            message: '填写不符合规范',
            type: 'warning'
          })
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.new-class-button {
  color: rgb(77, 77, 77);
}

.class-input {
  margin-left: 20px;
  width: 70%;
  float: left;
}

.class-button {
  margin-right: 20px;
  margin-bottom: 20px;
}

.el-form-item {
  margin-left: 10%;
}
</style>
