<template>
  <div>
    <main-show-top></main-show-top>
    <img src="../images/1_bg1.png" />
    <el-row>
      <el-col offset="3" :span="6">
        <div class="title-left">
          每日金币榜
          <span>努力努力努力</span>
        </div>
        <div class="bg-board-left">
          <el-row>
            <el-col class="ranking-number" :span="24">
              <div class="ranking second">
                <img class="second-img ranking-img" src="../images/avatar1.png" />
                <div class="second-username username">{{coinTop[1].name}}</div>
                <div class="second-number number">{{coinTop[1].coin_number}}</div>
              </div>
              <div class="ranking first">
                <img class="first-img ranking-img" src="../images/avatar2.jpg" />
                <div class="first-username username">{{coinTop[0].name}}</div>
                <div class="first-number number">{{coinTop[0].coin_number}}</div>
              </div>
              <div class="ranking third">
                <img class="third-img ranking-img" src="../images/avatar3.jpg" />
                <div class="third-username username">{{coinTop[2].name}}</div>
                <div class="third-number number">{{coinTop[2].coin_number}}</div>
              </div>
            </el-col>
            <el-col class="ranking-people" :span="24">
              <div class="people">
                <table class="person" v-for="(aCoin, index) in coin" :key="index">
                  <td><div class="person-ranking">{{index + 4}}</div></td>
                  <img class="person-img" src="../images/avatar4.jpg" />
                  <td><div class="per-username">{{aCoin.name}}</div></td>
                  <img class="alarm-clock" src="../images/22_alarm clock.png" />
                  <td><div class="per-goldnum">{{aCoin.coin_number}}</div></td>
                </table>
              </div>
              <div class="information">
                <div class="self-ranking">{{coinRank}}</div>
                <img class="self-img" src="../images/avatar5.jpg" />
                <div class="self-username">{{user}}</div>
                <img class="self-clock" src="../images/22_alarm clock.png" />
                <div class="self-goldnum">{{coinNumber}}</div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="title-middle">
          总计勤奋榜
          <span>勤奋也是一种能力</span>
        </div>
        <div class="bg-board-middle">
          <el-row>
            <el-col class="ranking-number" :span="24">
              <div class="ranking second">
                <img class="second-img ranking-img" src="../images/avatar1.png" />
                <div class="second-username username">{{allTop[1].fields.student_name}}</div>
                <div class="second-number number">{{allTop[1].fields.cumulative_study_duration}}</div>
              </div>
              <div class="ranking first">
                <img class="first-img ranking-img" src="../images/avatar2.jpg" />
                <div class="first-username username">{{allTop[0].fields.student_name}}</div>
                <div class="first-number number">{{allTop[0].fields.cumulative_study_duration}}</div>
              </div>
              <div class="ranking third">
                <img class="third-img ranking-img" src="../images/avatar3.jpg" />
                <div class="third-username username">{{allTop[2].fields.student_name}}</div>
                <div class="third-number number">{{allTop[2].fields.cumulative_study_duration}}</div>
              </div>
            </el-col>
            <el-col class="ranking-people" :span="24">
              <div class="people">
                <table v-for="(aAll, index) in all" :key="index" class="person">
                  <td><div class="person-ranking">{{index + 4}}</div></td>
                  <img class="person-img" src="../images/avatar5.jpg" />
                  <td><div class="per-username">{{aAll.fields.student_name}}</div></td>
                  <img class="alarm-clock" src="../images/22_alarm clock.png" />
                  <td><div class="per-goldnum">{{aAll.fields.cumulative_study_duration}}</div></td>
                </table>
              </div>
              <div class="information">
                <div class="self-ranking">{{allRank}}</div>
                <img class="self-img" src="../images/avatar4.jpg" />
                <div class="self-username">{{user}}</div>
                <img class="self-clock" src="../images/22_alarm clock.png" />
                <div class="self-goldnum">{{allDuration}}</div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="title-right">
          今日勤奋榜
          <span>一日之际在于晨</span>
        </div>
        <div class="bg-board-right">
          <el-row>
            <el-col class="ranking-number" :span="24">
              <div class="ranking second">
                <img class="second-img ranking-img" src="../images/avatar1.png" />
                <div class="second-username username">{{todayTop[1].name}}</div>
                <div class="second-number number">{{todayTop[1].study_duration}}</div>
              </div>
              <div class="ranking first">
                <img class="first-img ranking-img" src="../images/avatar2.jpg" />
                <div class="first-username username">{{todayTop[0].name}}</div>
                <div class="first-number number">{{todayTop[0].study_duration}}</div>
              </div>
              <div class="ranking third">
                <img class="third-img ranking-img" src="../images/avatar3.jpg" />
                <div class="third-username username">{{todayTop[2].name}}</div>
                <div class="third-number number">{{todayTop[2].study_duration}}</div>
              </div>
            </el-col>
            <el-col class="ranking-people" :span="24">
              <div class="people">
                <div v-for="(aToday, index) in today" :key="index" class="person">
                  <td><div class="person-ranking">{{index + 4}}</div></td>
                  <img class="person-img" src="../images/avatar5.jpg" />
                  <td><div class="per-username">{{aToday.name}}</div></td>
                  <img class="alarm-clock" src="../images/22_alarm clock.png" />
                  <td><div class="per-goldnum">{{aToday.study_duration}}</div></td>
                </div>
              </div>
              <div class="information">
                <div class="self-ranking">{{todayRank}}</div>
                <img class="self-img" src="../images/avatar4.jpg" />
                <div class="self-username">{{user}}</div>
                <img class="self-clock" src="../images/22_alarm clock.png" />
                <div class="self-goldnum">{{todayDuration}}</div>
              </div>
              <button class="back" @click="backHome">返回主界面</button>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import MainShowTop from './common/MainShowTop'
const axios = require('axios')
export default {
  data: function () {
    return {
      coinTop: [{'name': '', 'coin_number': 0}, 
      {'name': '', 'coin_number': 0}, 
      {'name': '', 'coin_number': 0}],
      coin: [],
      todayTop: [{'name': '', 'study_duration': 0}, 
      {'name': '', 'study_duration': 0}, 
      {'name': '', 'study_duration': 0}, ],
      today: [],
      allTop: [{'fields': {'student_name': '', 'cumulative_study_duration': 0}}, 
      {'fields': {'student_name': '', 'cumulative_study_duration': 0}}, 
      {'fields': {'student_name': '', 'cumulative_study_duration': 0}}, ],
      all: [],
      allDuration: 0,
      allRank: 0,
      coinNumber: 0,
      coinRank: 0,
      todayDuration: 0,
      todayRank: 0,
      user: '',
    }
  },
  methods: {
    backHome () {
      this.$router.push('/beforestudying')
    },
    getRank () {
      let message = new URLSearchParams()
      message.append('student_id', sessionStorage.getItem('student'))
      axios.post(this.$store.state.BASEURL + 'study/leader_board', message).
        then((res) => {
          this.allDuration = res.data.all_duration
          this.allRank = res.data.all_rank
          this.coinNumber = res.data.coin_number
          this.coinRank = res.data.coin_rank
          this.todayDuration = res.data.today_duration
          this.todayRank = res.data.today_rank
        })
    },
    getCoinRank () {
      axios.get(this.$store.state.BASEURL + 'study/leader_coin_board').then((res) => {
        if (res.data.length > 0) {
          this.coinTop[0] = res.data[0]
        }
        if (res.data.length > 1) {
          this.coinTop[1] = res.data[1]
        }
        if (res.data.length > 2) {
          this.coinTop[2] = res.data[2]
        }
        if (res.data.length > 3)
        for (let i = 3; i < 10 && i < res.data.length; i++) {
          this.coin.push(res.data[i])
        }
      })
    },
    getTodayRank () {
      axios.get(this.$store.state.BASEURL + 'study/leader_today_board').then((res) => {
        if (res.data.length > 0) {
          this.todayTop[0] = res.data[0]
        }
        if (res.data.length > 1) {
          this.todayTop[1] = res.data[1]
        }
        if (res.data.length > 2) {
          this.todayTop[2] = res.data[2]
        }
        if (res.data.length > 3)
        for (let i = 3; i < 10 && i < res.data.length; i++) {
          this.today.push(res.data[i])
        }
      })
    },
    getAllRank () {
      axios.get(this.$store.state.BASEURL + 'study/leader_all_board').then((res) => {
        if (res.data.length > 0) {
          this.allTop[0] = res.data[0]
        }
        if (res.data.length > 1) {
          this.allTop[1] = res.data[1]
        }
        if (res.data.length > 2) {
          this.allTop[2] = res.data[2]
        }
        if (res.data.length > 3)
        for (let i = 3; i < 10 && i < res.data.length; i++) {
          this.all.push(res.data[i])
        }
      })
    }
  },
  mounted () {
    this.user = sessionStorage.getItem('student')
    this.getRank()
    this.getCoinRank()
    this.getTodayRank()
    this.getAllRank()
  },
  components: {
    MainShowTop
  }
}
</script>

<style scoped>
img {
  top: 0;
  left: 0;
  position: absolute;
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  z-index: -3;
}

.el-row {
  margin-bottom: 20px;
}

.el-col {
  border-radius: 4px;
  height: 90px;
  text-align: center;
  font-weight: bold;
}

.title-left,
.title-middle,
.title-right {
  position: absolute;
  height: 65px;
  width: 250px;
  z-index: 0;
  color: #fff;
  font-size: 14px;
  font-weight: bold;
  margin-left: 15px;
  padding-left: 10px;
}

span {
  display: block;
  font-size: 10px;
  margin-top: 5px;
}

.title-left {
  padding-top: 27px;
  background: url("../images/38_learning time.png") no-repeat;
  background-size: 250px 65px;
}

.title-middle {
  padding-top: 18px;
  margin-top: 9px;
  background: url("../images/24_diligent list.png") no-repeat;
  background-size: 250px 55px;
}

.title-right {
  padding-top: 28px;
  background: url("../images/20_gold.png") no-repeat;
  background-size: 250px 65px;
}

.bg-board-left,
.bg-board-middle,
.bg-board-right {
  margin-top: 44px;
  position: relative;
  z-index: -2;
  width: 280px;
  height: 400px;
  background: #fff;
  border-radius: 5px;
}

.ranking {
  display: inline-block;
  height: 100px;
  width: 80px;
  margin-right: 10px;
  margin-top: 40px;
  padding-top: 45px;
  color: #fff;
  font-size: 12px;
  z-index: -1;
  position: relative;
}

.first {
  background: url("../images/14_big1.png") no-repeat;
  background-size: 75px 80px;
}

.second {
  margin-left: 10px;
  background: url("../images/10_big2.png") no-repeat;
  background-size: 75px 80px;
}

.third {
  background: url("../images/12_big3.png") no-repeat;
  background-size: 75px 80px;
}

.number {
  margin-top: 3px;
}

.ranking-img {
  height: 30px;
  width: 30px;
  position: absolute;
  z-index: 0;
  background: transparent;
  border-radius: 50%;
}

.first-img {
  border: 2px solid rgb(253, 182, 43);
}

.second-img {
  margin-top: 5px;
  border: 2px solid rgb(177, 187, 253);
}

.third-img {
  margin-top: 5px;
  border: 2px solid rgb(99, 204, 123);
}

.people {
  height: 230px;
  overflow: auto;
}

.person {
  /* 让一个div块在另外一个div块水平居中 */
  text-align: left;
  margin: auto;
  height: 30px;
  width: 250px;
  line-height: 30px;
  border-radius: 5px;
  position: relative;
  font-size: 12px;
  z-index: -2;
  background-color: rgb(238, 249, 255);
}

td {
  width: 30px;
}

.alarm-clock {
  z-index: 0;
  margin-top: 3px;
  margin-left: 180px;
  position: absolute;
  height: 20px;
  width: 20px;
  border-radius: 50%;
}

.ranking-people {
  margin-top: 40px;
}

.person-ranking {
  display: inline;
  color: rgb(67, 188, 255);
}

.person-img {
  margin-top: 3px;
  margin-left: 20px;
  height: 20px;
  width: 20px;
  position: absolute;
  z-index: 0;
  background: transparent;
  border-radius: 50%;
  border: 1px solid rgb(67, 188, 255);
}

.per-username {
  display: inline;
}

.per-goldnum {
  display: inline;
}

.information {
  text-align: left;
  background-color: rgb(46, 180, 255);
  height: 40px;
  line-height: 40px;
  border-radius: 0 0 5px 5px;
  z-index: -2;
  color: #fff;
  position: relative;
  font-size: 12px;
}

.self-ranking {
  display: inline;
  margin-left: 10px;
}

.self-img {
  margin-top: 10px;
  margin-left: 25px;
  height: 20px;
  width: 20px;
  position: absolute;
  z-index: 0;
  background: transparent;
  border-radius: 50%;
  border: 1px solid rgb(67, 188, 255);
}

.self-username {
  display: inline;
  margin-left: 40px;
}

.self-clock {
  z-index: 0;
  margin-top: 10px;
  margin-left: 205px;
  position: absolute;
  height: 20px;
  width: 20px;
  border-radius: 50%;
}

.self-goldnum {
  display: inline;
  margin-left: 160px;
}

.back {
  margin-top: 20px;
  float: right;
  background-color: rgb(211, 242, 243);
  height: 30px;
  border-radius: 5px;
  border: 1px solid #000;
}
</style>