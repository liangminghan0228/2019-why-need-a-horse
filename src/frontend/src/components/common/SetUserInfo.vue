<template>
  <div class="dialog-container">
    <el-button type="text" @click="setUserInfo" class="button-set">设置</el-button>
    <el-dialog title="修改个人信息" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="新头像" :label-width="formLabelWidth">
          <el-upload
            class="avatar-uploader"
            ref="upload"
            name="avatar"
            accept="image/png,image/gif,image/jpg,image/jpeg"
            list-type="picture-card"
            :limit=limitNum
            :action="uploadUrl()"
            :on-exceed="handleExceed"
            :before-upload="handleBeforeUpload"
            :on-preview="handlePictureCardPreview"
            :auto-upload="false">
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
          </el-dialog>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="updateInfo">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      dialogFormVisible: false,
      form: {
        name: ''
      },
      dialogImageUrl: '',
      dialogVisible: false,
      disabled: false,
      formLabelWidth: '120px',
      limitNum: 1
    }
  },
  methods: {
    setUserInfo () {
      this.dialogFormVisible = true
    },
    uploadUrl () {
      return this.$store.state.BASEURL + 'information/update_info?student_id=' + sessionStorage.getItem('student') + '&student_name=' + this.form.name
    },
    updateInfo () {
      this.$refs.upload.submit()
      this.dialogFormVisible = false
      this.$message({
        message: '更新成功',
        type: 'success'
      })
    },
    handleBeforeUpload (file){
      if (!(file.type === 'image/png' || file.type === 'image/gif' || file.type === 'image/jpg' || file.type === 'image/jpeg')) {
        this.$notify.warning({
          title: '警告',
          message: '请上传格式为png/gif/jpg/jpeg的图片'
        })
      }
      let size = file.size / 1024 / 1024 / 2
      if (size > 2) {
        this.$notify.warning({
          title: '警告',
          message: '图片大小必须小于2M'
        })
      }
    },
    handleExceed () {
      this.$notify.warning({
        title: '警告',
        message: '请不要选择多于一张图片'
      })
    },
    handlePictureCardPreview (file) {
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    }
  }
}
</script>

<style scoped>
.dialog-container {
  display: inline;
}

.button-set {
  width: auto;
  height: auto;
  color: black;
  margin-left: 25px;
  font-size: 11px;
}

.el-button--text:hover {
  color: #33cc33;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>