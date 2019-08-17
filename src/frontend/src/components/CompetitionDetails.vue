<template>
  <div v-if="isShow">
    <img src="../images/1_bg1.png" />
    <main-show-top></main-show-top>
    <el-row>
      <main-show :showCompetition="true"></main-show>
      <el-col :span="1">&nbsp;</el-col>
      <el-col :span="13">
        <div class="white-box">
          <p>{{competitionInfo[0].fields.name}}</p>
          <el-row>
            <el-col :span="15">
              <div class="competition-info">
                <img src="../images/29_time2.png" class="image-class" />
                <label class="p6">比赛时间</label>
                <br />
                <label class="p7">{{competitionInfo[0].fields.begin_time}}-{{competitionInfo[0].fields.end_time}}</label>
              </div>
              <div class="competition-info">
                <img src="../images/35_statistical range.png" class="image-class" />
                <label class="p6">参赛范围</label>
                <br />
                <label class="p7">学校：{{competitionInfo[0].fields.school}}</label>
                <label class="p7">年级：{{competitionInfo[0].fields.grade}}</label>
                <label class="p7">班级：{{competitionInfo[0].fields.classes}}</label>
              </div>
              <div class="competition-info">
                <img src="../images/23_content.png" class="image-class" />
                <label class="p6">比赛内容</label>
                <br />
                <label class="p7">{{book[0].fields.category}}</label>
              </div>
              <div class="competition-info">
                <img src="../images/18_reward.png" class="image-class" />
                <label class="p6">奖励内容</label>
                <br />
                <label class="p7">金币：{{competitionInfo[0].fields.award}}</label>
              </div>
              <div class="competition-info">
                <img src="../images/16_rule.png" class="image-class" />
                <label class="p6">比赛规则</label>
                <br />
                <label class="p7">{{rule}}</label>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="9">&nbsp;</el-col>
            <el-col :span="12">
              <input type="button" value="开始挑战" class="start-button" @click="goCompetition" />
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import MainShow from './common/MainShow'
import MainShowTop from './common/MainShowTop'
const axios = require('axios')
export default {
  data: function () {
    return {
      competitionName: '',
      time: '2018.7.12-2019.3.6',
      limit: '全体学生',
      content: '人教版 初一上册',
      award: '奖励前10名，每人10000金币',
      rule:
        '系统挑选已参赛学员进行两两PK，胜者获得10积分，输者获得2积分，平手各获5积分，比赛截止日根据排名获得奖励。',
      competitionInfo: [],
      competitionId: 1,
      bookId: '',
      book: [],
      competitionType: '',
      isShow: false
    }
  },
  components: {
    MainShow,
    MainShowTop
  },
  methods: {
    goCompetition: function () {
      setTimeout(() => {
        if (this.competitionType === 'infinite') {
          this.$router.push('/unlimitedchallenge')
        } else {
          this.$router.push('/pkcompetition')
        }
      }, 1000)
    }
  },
  mounted () {
    this.competitionId = this.$store.state.COMPETITIONID
    axios
      .get(
        this.$store.state.BASEURL +
          'competitions/get_competition_info?competition_id=' +
          this.competitionId
      )
      .then(res => {
        this.competitionInfo = res.data
        if (this.competitionInfo.length > 0) {
          this.bookId = this.competitionInfo[0].fields.book_id
          this.competitionType = res.data[0].fields.type
          if (res.data[0].fields.type === 'infinite') {
            this.rule =
              '参赛选手连续答题，如果答错三次则不能继续作答，比赛截止日根据连续答题数排名获得奖励。'
          }
          axios
            .get(
              this.$store.state.BASEURL +
                'books/get_book_name?books_id=' +
                this.bookId
            )
            .then(res => {
              this.book = res.data
              this.isShow = true
            })
        } else {
          this.$router.push('/competitionlistpage')
        }
      })
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  top: 0;
  left: 0;
}

.p6 {
  font-size: 14px;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  font-weight: boldlabel
}

.p7 {
  font-size: 14px;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  color: rgb(167, 167, 167);
  margin-left: 30px;
}

img {
  position: absolute;
  top: 50px;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: -10;
  margin: 0;
  padding: 0;
}

.white-box {
  background-color: white;
  margin-top: 50px;
  border-radius: 5px;
  height: 465px;
  padding: 20px;
  box-shadow: 1px 1px 1px 1px rgb(188, 221, 221);
}

p {
  font-size: 18px;
  font-weight: bolder;
  margin-top: 20px;
  color: rgb(51, 51, 51);
  margin-left: 20px;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}

.image-class {
  height: 20px;
  width: 20px;
  position: inherit;
  padding-right: 5px;
  vertical-align: text-bottom;
}

.competition-info {
  margin: 20px;
}

.start-button {
  background-color: rgb(255, 177, 40);
  width: 100px;
  height: 30px;
  border-radius: 5px;
  outline: none;
  border: 0;
  color: white;
  box-shadow: 1px 1px 1px 1px rgb(255, 177, 40);
  cursor: pointer;
}

input.start-button:hover {
  background-color: rgb(253, 196, 98);
}
</style>
