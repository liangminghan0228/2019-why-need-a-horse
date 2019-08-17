<template>
  <div class="edit">
    <el-button @click="edit">编辑</el-button>
    <el-dialog :visible.sync="visible" :close-on-click-modal="false">
      编辑比赛
      <br />
      <el-row>
        <el-col :span="8">比赛种类</el-col>
        <el-col :span="16">
          <el-select v-model="type">
            <el-option :value="'pk比赛'"></el-option>
            <el-option :value="'无限挑战'"></el-option>
          </el-select>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">比赛名称</el-col>
        <el-col :span="16">
          <el-input v-model="name" />
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">组织单位</el-col>
        <el-col :span="16">
          <el-input v-model="organizer" />
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">比赛状态</el-col>
        <el-col :span="16">
          <el-select v-model="status">
            <el-option :value="'未开始'"></el-option>
            <el-option :value="'进行中'"></el-option>
            <el-option :value="'已截止'"></el-option>
            <el-option :value="'已结束'"></el-option>
          </el-select>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">参与年级</el-col>
        <el-col :span="16">
          <el-select v-model="grade">
            <el-option :value="7"></el-option>
            <el-option :value="8"></el-option>
            <el-option :value="9"></el-option>
            <el-option :value="10"></el-option>
            <el-option :value="11"></el-option>
          </el-select>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">最大人数</el-col>
        <el-col :span="16">
          <el-select v-model="maxNumber">
            <el-option :value="500"></el-option>
            <el-option :value="1000"></el-option>
            <el-option :value="2000"></el-option>
            <el-option :value="3000"></el-option>
            <el-option :value="5000"></el-option>
          </el-select>
        </el-col>
      </el-row>
      <el-button @click="cancelEdit">取消</el-button>
      <el-button type="primary" @click="submitEdit">确定</el-button>
    </el-dialog>
  </div>
</template>

<script>
const axios = require('axios')
export default {
  data () {
    return {
      visible: false,
      clickNum: 0,
      info: {},
      type: '',
      name: '',
      organizer: '',
      status: '',
      grade: 0,
      maxNumber: 0
    }
  },
  props: {
    home: {}
  },
  methods: {
    edit () {
      this.visible = true
      this.getComepetition()
    },
    cancelEdit () {
      this.visible = false
      this.info = {}
      this.type = ''
      this.name = ''
      this.organizer = ''
      this.status = ''
      this.grade = 0
      this.maxNumber = 0
    },
    submitEdit () {
      this.visible = false
      this.editCompetition()
    },
    getComepetition () {
      axios.get(this.$store.state.BASEURL + 'competitions/get_competition_info?competition_id=' + this.home.pk).then((res) => {
        this.info = res.data[0]
        this.type = this.switchType(this.info.fields.type)
        this.name = this.info.fields.name
        this.organizer = this.info.fields.organiser
        this.status = this.switchStatus(this.info.fields.status)
        this.grade = this.info.fields.grade
        this.maxNumber = this.info.fields.max_number
      })
    },
    switchType (type) {
      switch (type) {
      case 'pk':
        return 'pk比赛'
      default:
        return '无限挑战'
      }
    },
    switchTypeOver (type) {
      switch (type) {
      case 'pk比赛':
        return 'pk'
      default:
        return 'infinite'
      }
    },
    switchStatus (status) {
      switch (status) {
      case 'forbid':
        return '未开始'
      case 'proceeding':
        return '进行中'
      case 'abort':
        return '已截止'
      default:
        return '已结束'
      }
    },
    switchStatusOver (status) {
      switch (status) {
      case '未开始':
        return 'forbid'
      case '进行中':
        return 'proceeding'
      case '已截止':
        return 'abort'
      default:
        return 'finish'
      }
    },
    editCompetition () {
      //修改信息
      this.info.fields.type = this.switchTypeOver(this.type)
      this.info.fields.name = this.name
      this.info.fields.organiser = this.organizer
      this.info.fields.status = this.switchStatusOver(this.status)
      this.info.fields.grade = this.grade
      this.info.fields.max_number = this.maxNumber
      axios.post(this.$store.state.BASEURL + 'competitions/edit_competition', this.info).then((res) => {
        if (res.data === 'edit_competition_success') {
          this.$message({
            showClose: true,
            message: '修改比赛信息成功'
          })
          this.$emit('regetCompetition')
        }
      })
    }
  }
}
</script>

<style scoped>
.el-row {
  width: 100%;
  height: 80%;
  margin-top: 6%;
  margin-bottom: 6%;
  text-align: left;
}

.el-col {
  text-align: center;
  font-size: 2vh;
  height: 3vh;
  line-height: 3vh;
}

.edit /deep/ .el-select /deep/ .el-input {
  height: 3vh;
  line-height: 3vh;
  font-size: 2vh;
  width: 100%;
}

.edit /deep/ .el-input {
  height: 3vh;
  line-height: 3vh;
  font-size: 2vh;
  width: 60%;
}

.edit /deep/ .el-select {
  height: 3vh;
  line-height: 3vh;
  font-size: 2vh;
  width: 60%;
}

.edit /deep/ .el-dialog__body {
  font-size: 5vh;
  text-align: center;
}
</style>