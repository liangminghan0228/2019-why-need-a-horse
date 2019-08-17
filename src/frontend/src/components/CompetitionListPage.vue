<template>
  <div>
    <main-show-top></main-show-top>
    <div class="bg-img">
      <el-row>
        <main-show :showCompetition="true"></main-show>
        <el-col :span="1">&nbsp;</el-col>
        <el-col :span="13">
          <div class="background">
            <h3>我参加的比赛</h3>
            <div class="top-list">
              <div v-for="(item, index) in competitionListBeTaken" :key="index" class="single-box">
                <competition-card :competition="item" :isParticipate="true"></competition-card>
              </div>
            </div>
            <h3>单词比赛</h3>
            <div class="footer-list">
              <div v-for="(item, index) in competitionListNoTaken" :key="index" class="single-box">
                <competition-card :competition="item" :isParticipate="false"></competition-card>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import CompetitionCard from './common/CompetitionCard'
import MainShow from './common/MainShow'
import MainShowTop from './common/MainShowTop'
const axios = require('axios')
export default {
  data: function () {
    return {
      competitionListBeTaken: [],
      competitionListNoTaken: []
    }
  },
  components: {
    CompetitionCard,
    MainShow,
    MainShowTop
  },
  methods: {
    transfer (data) {
      let takenlist = data['takenlist']
      for (let i = 0; i < takenlist.length; i++) {
        let tmp1 = {
          timeInterval: this.timeInterval(takenlist[i].fields['begin_time']),
          type: takenlist[i].fields['type'],
          startTime: takenlist[i].fields['begin_time'],
          endTime: takenlist[i].fields['end_time'],
          bookName: takenlist[i].bookname,
          pk: takenlist[i].pk,
          rank: takenlist[i].rank,
          topThree: takenlist[i].topThree
        }
        this.competitionListBeTaken.push(tmp1)
      }
      let notakenlist = data['notakenlist']
      for (let i = 0; i < notakenlist.length; i++) {
        let tmp2 = {
          timeInterval: this.timeInterval(notakenlist[i].fields['begin_time']),
          type: notakenlist[i].fields['type'],
          startTime: notakenlist[i].fields['begin_time'],
          endTime: notakenlist[i].fields['end_time'],
          bookName: notakenlist[i].bookname,
          pk: notakenlist[i].pk,
          rank: notakenlist[i].rank,
          topThree: notakenlist[i].topThree
        }
        this.competitionListNoTaken.push(tmp2)
      }
    },
    timeInterval (startTime) {
      if (startTime[5] === '1') {
        return '冬季赛段'
      } else if (startTime[6] <= 3) {
        return '春季赛段'
      } else if (startTime[6] <= 6) {
        return '夏季赛段'
      } else {
        return '秋季赛段'
      }
    }
  },
  mounted () {
    let param = sessionStorage.getItem('student')
    const url = this.$store.state.BASEURL + 'competitions/get_competition_list'
    axios.post(url, JSON.stringify(param)).then(res => {
      this.transfer(res.data)
    })
  }
}
</script>

<style scoped>
.bg-img {
  background-image: url('../images/1_bg1.png');
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  z-index: -3;
  background-size: 100%;
  background-repeat: no-repeat;
  background-attachment: fixed;
  overflow: hidden;
}

.background {
  width: 100%;
  height: auto;
  padding-bottom: 50px;
  background-color: #fff;
  margin-top: 50px;
  border-radius: 5px;
  position: relative;
}

.top-list {
  height: 325px;
  margin-top: 50px;
  margin-left: 70px;
  overflow: auto;
}

.footer-list {
  height: 325px;
  margin-top: 50px;
  margin-left: 70px;
  overflow: auto;
}

h3 {
  margin-left: 30px;
  padding-top: 40px;
}

.single-box {
  width: 300px;
  display: inline-block;
  margin: 10px 5px 10px 5px;
}
</style>
