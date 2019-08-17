<template>
  <div class="rank">
    <el-button @click="rank">排名</el-button>
    <el-dialog :visible.sync="visible" :close-on-click-modal="false">
      {{title}}的排名
      <br />
      <br />
      <el-table :data="rankPage()" height="300px" stripe border>
        <el-table-column type="index" label="排名" align="center" min-width="20%"></el-table-column>
        <el-table-column prop="id" label="学生ID" align="center" min-width="25%"></el-table-column>
        <el-table-column prop="name" label="学生姓名" align="center" min-width="30%"></el-table-column>
        <el-table-column prop="score" label="学生分数" align="center" min-width="25%"></el-table-column>
      </el-table>
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
      title: '',
      visible: false,
      clickNum: 0,
      total: 0,
      pageSize: 10,
      currentPage: 1,
      rankInfo: []
    }
  },
  props: {
    home: {}
  },
  methods: {
    rank () {
      this.title = this.home.fields.name
      this.visible = true
      this.getRank()
    },
    getRank () {
      this.rankInfo = []
      axios.get(this.$store.state.BASEURL + 'competitions/get_competition_rank?competition_id=' + this.home.pk).then((res) =>{
        this.total = res.data.length
        for (let i = 0; i < res.data.length ; i++) {
          this.rankInfo.push(res.data[i])
        }
      })
    },
    rankPage () {
      return this.rankInfo.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    },
    handleSizeChange (pageSize) {
      this.pageSize = pageSize
    },
    handleCurrentChange (currentPage) {
      this.currentPage = currentPage
    }
  }
}
</script>

<style scoped>
.rank /deep/ .el-dialog__body {
  font-size: 2vh;
  text-align: center;
}

.turn-page {
  margin-top: 5%;
  margin-bottom: 10%;
}

.el-pagination /deep/ {
  float: right;
}

span {
  position: absolute;
  top: 5%;
  font-size: 2vh;
  left: 40%;
  text-align: center;
}
</style>