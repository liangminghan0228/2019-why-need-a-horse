<template>
  <div>
    <el-row class="top-row">
      <el-col :span="24" class="cancel-border"></el-col>
    </el-row>
    <el-row>
      <teacher-side-bar :showCompetition="true"></teacher-side-bar>
      <el-col :span="21" class="right-part">
                <el-row class="right-part-middle">
          <el-col :span="6">
            <el-select v-model="organizerKey" @change="searchByKey" placeholder="请选择组织方:">
              <el-option v-for="(aOrganizer, index) in organizers" :key="index" :value="aOrganizer"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="typeKey" @change="searchByKey" placeholder="请选择分类">
              <el-option v-for="(aType, index) in types" :key="index" :value="aType"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="gradeKey" @change="searchByKey" placeholder="请选择年级:">
              <el-option v-for="(aGrade, index) in grades" :key="index" :value="aGrade"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="statusKey" @change="searchByKey" placeholder="请选择状态">
              <el-option v-for="(aStatus, index) in status" :key="index" :value="aStatus"></el-option>
            </el-select>
          </el-col>
        </el-row>
        <el-row class="right-part-middle">
          <el-col :span="6">
            <el-input placeholder=" 请输入名称:" v-model="nameKey" />
          </el-col>
          <el-col :span="6">
            <el-button class="search-button" @click="searchByKey">搜索比赛</el-button>
          </el-col>
          <el-col :span="6">
            <el-button class="search-button" @click="showAllComepetition">显示全部比赛</el-button>
          </el-col>
          <el-col :span="6">
            <create-competition @regetCompetitionInfo="regetCompetitionInfo"></create-competition>
          </el-col>
        </el-row>
        <div class="right-part-bottom">
          <el-table :data="contextPage()" stripe height="450px" border @current-change="selectRow">
            <el-table-column prop="fields.name" label="名称" align="center"></el-table-column>
            <el-table-column prop="fields.type" label="分类" align="center"></el-table-column>
            <el-table-column prop="fields.organiser" label="组织方" align="center"></el-table-column>
            <el-table-column prop="fields.status" label="状态" align="center"></el-table-column>
            <el-table-column prop="fields.begin_time" label="开始时间" align="center"></el-table-column>
            <el-table-column prop="fields.end_time" label="结束时间" align="center"></el-table-column>
            <el-table-column prop="fields.grade" label="年级" align="center"></el-table-column>
            <el-table-column prop="fields.max_number" label="参与数" align="center"></el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <teacher-competition-rank :home="scope.row"></teacher-competition-rank>
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <teacher-edit-competition :home="scope.row" @regetCompetition="getCompetitionInfo"></teacher-edit-competition>
              </template>
            </el-table-column>
            <el-table-column label="操作" align="center">
              <template slot-scope="scope">
                <el-button @click="prize(scope.row)">奖励</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
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
      </el-col>
    </el-row>
  </div>
</template>

<script>
import CreateCompetition from './CreateCompetition'
import TeacherSideBar from './common/TeacherSideBar'
import TeacherEditCompetition from './TeacherEditCompetition'
import TeacherCompetitionRank from './TeacherCompetitionRank'
const axios = require('axios')
export default {
  data () {
    return {
      searchSpan: '搜索',
      total: 0,
      pageSize: 10,
      currentPage: 1,
      organizerKey: '',
      organizers: [],
      typeKey: '',
      types: [],
      gradeKey: '',
      grades: [],
      statusKey: '',
      status: [],
      nameKey: '',
      competitionInfo: [],
      selectedCompetition: {},
      showedInfo: [],
      tempInfo: [],
      topThree: []
    }
  },
  methods: {
    selectRow (selection) {
      this.selectedCompetition = selection
    },
    contextPage () {
      return this.showedInfo.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    },
    handleSizeChange (pageSize) {
      this.pageSize = pageSize
    },
    handleCurrentChange (currentPage) {
      this.currentPage = currentPage
    },
    getTypes (arr) {
      arr.forEach(element => {
        if (this.types.includes(element.fields.type) === false) {
          this.types.push(element.fields.type)
        }
      })
    },
    getOrganizers (arr) {
      arr.forEach(element => {
        if (this.organizers.includes(element.fields.organiser) === false) {
          this.organizers.push(element.fields.organiser)
        }
      })
    },
    getGrades (arr) {
      arr.forEach(element => {
        if (this.grades.includes(element.fields.grade) === false) {
          this.grades.push(element.fields.grade)
        }
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
    getStatus (arr) {
      arr.forEach(element => {
        if (this.status.includes(element.fields.status) === false) {
          this.status.push(element.fields.status)
        }
      })
    },
    showAllComepetition () {
      this.showedInfo = this.competitionInfo
      this.total = this.competitionInfo.length
      this.statusKey = ''
      this.nameKey = ''
      this.typeKey = ''
      this.organizerKey = ''
      this.gradeKey = ''
    },
    searchByKey () {
      let status = this.statusKey
      let type = this.typeKey
      let grade = this.gradeKey
      let organizer = this.organizerKey
      let name = this.nameKey
      this.tempInfo = this.competitionInfo
      if (status !== '') {
        this.tempInfo = this.tempInfo.filter(e => e.fields.status === status)
      }
      if (type !== '') {
        this.tempInfo = this.tempInfo.filter(e => e.fields.type === type)
      }
      if (grade !== '') {
        this.tempInfo = this.tempInfo.filter(e => e.fields.grade === grade)
      }
      if (organizer !== '') {
        this.tempInfo = this.tempInfo.filter(e => e.fields.organiser === organizer)
      }
      if (name !== '') {
        this.tempInfo = this.tempInfo.filter(e => e.fields.name.indexOf(name) > -1)
      }
      this.total = this.tempInfo.length
      this.showedInfo = this.tempInfo
    },
    regetCompetitionInfo () {
      this.getCompetitionInfo()
    },
    getCompetitionInfo () {
      this.competitionInfo = []
      axios.get(this.$store.state.BASEURL + 'competitions/all_competition_info').then((res) => {
        this.total = res.data.length
        for (let i = 0; i < res.data.length; i++) {
          this.competitionInfo.push(res.data[i])
          this.competitionInfo[i].fields.type = this.switchType(this.competitionInfo[i].fields.type)
          this.competitionInfo[i].fields.status = this.switchStatus(this.competitionInfo[i].fields.status)
        }
        this.showedInfo = this.competitionInfo
        this.getTypes(this.competitionInfo)
        this.getOrganizers(this.competitionInfo)
        this.getGrades(this.competitionInfo)
        this.getStatus(this.competitionInfo)
      })
    },
    prize (row) {
      if (row.fields.status === '进行中' || row.fields.status === '未开始') {
        this.$message({
          showClose: true,
          message: '该比赛还未结束'
        })
      } else if (row.fields.status === '已结束') {
        this.$message({
          showClose: true,
          message: '已经对该比赛颁发了奖励'
        })
      } else {
        axios.get(this.$store.state.BASEURL + 'competitions/prize_top?competition_id=' + row.pk).then((res) => {
          if (res.data === 'prize_top_succeed') {
            this.getCompetitionInfo()
            this.$message({
              showClose: true,
              message: '成功颁发奖励'
            })
          }
        }
        )

      }
    }
  },
  mounted () {
    this.getCompetitionInfo()
  },
  components: {
    CreateCompetition,
    TeacherSideBar,
    TeacherEditCompetition,
    TeacherCompetitionRank
  }
}
</script>

<style scoped>
.cancel-border {
  border: 0 !important;
}

.top-row {
  height: 30px;
  background: linear-gradient(rgb(199, 211, 225), rgb(185, 198, 215));
}

.right-part {
  margin-top: 1%;
}

.right-part-middle /deep/ .el-col {
  border-radius: 4px;
  height: 100%;
  padding-left: 1%;
}

.right-part-middle {
  height: 50px;
  background-color: rgb(244, 244, 244);
  margin-left: 10px;
  margin-right: 20px;
  font-size: 1vw;
}

.right-part-bottom {
  margin-left: 10px;
  margin-right: 20px;
}

.right-part-middle /deep/ .el-button {
  margin-top: 2%;
}

.right-part-middle /deep/ .el-input__inner {
  margin-top: 2%;
}

.turn-page {
  margin-top: 5%;
  margin-right: 20px;
  margin-bottom: 10%;
}

.el-pagination /deep/ {
  float: right;
}

.search-button{
  border-radius: 5px;
  color: #ffffff;
  background-color: rgb(24, 144, 255);
  border: 1px solid rgb(24, 144, 255);
  outline: none;
  margin: 0;
  margin-top: 4%;
}
</style>
