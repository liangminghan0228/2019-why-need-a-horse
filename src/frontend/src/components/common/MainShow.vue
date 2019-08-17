<template>
  <div>
    <el-col :span="3">&nbsp;</el-col>
    <el-col :span="4">
      <aside>
        <div class="card">
          <div class="card-top">
            <img src="../../images/62_card.png" class="head-img" />
            <div class="name">{{username}}</div>
            <br />
            <br />
            <div class="coin">
              <img src="../../images/47_diamond.png" class="coin-img" />
              {{coinNumber}}
            </div>
          </div>
          <input type="button" v-model="cardMessage" class="card-button" @click="changeCalendar" />
          <calendar class="calendar-area" v-show="isShowedCalendar" ref="calendar"></calendar>
        </div>
        <div class="button-area">
          <input type="button" value="正在学习" :class="showStudying ? show : init" @click="goStudying" />
          <input type="button" value="学习统计" :class="showStatistics ? show : init" @click="goStatistic" />
          <input type="button" value="单词本" :class="showList ? show : init" @click="goWordList"/>
          <input type="button" value="单词比赛" :class="showCompetition ? show : init" @click="goCompetition"/>
        </div>
      </aside>
    </el-col>
  </div>
</template>

<script>
import Calendar from '../Calendar'
const axios = require('axios')
export default {
  data: function () {
    return {
      init: 'button-type-init',
      show: 'button-type-focus',
      isShowedCalendar: false,
      cardMessage: '打卡',
      username: '',
      coinNumber: 0
    }
  },
  props: {
    showStudying: {
      type: Boolean,
      default: false
    },
    showStatistics: {
      type: Boolean,
      default: false
    },
    showList: {
      type: Boolean,
      default: false
    },
    showCompetition: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    goStudying () {
      this.$router.push('/beforestudying')
    },
    goStatistic () {
      this.$router.push('/studystatistic')
    },
    goWordList () {
      this.$router.push('/wordlist')
    },
    goCompetition () {
      this.$router.push('/competitionlistpage')
    },
    changeCalendar () {
      if (this.isShowedCalendar === true) {
        this.isShowedCalendar = false
        this.cardMessage = '打卡'
      }
      else if (this.isShowedCalendar === false) {
        this.isShowedCalendar = true
        this.cardMessage = '关闭'
        this.$refs.calendar.cardToday()
      }
    }
  },
  mounted () {
    let url = this.$store.state.BASEURL + 'information/get_user_info?student_id=' + sessionStorage.getItem('student')
    axios.get(url).then(res => {
      if (res.data) {
        this.username = res.data[0]['fields']['student_name']
        this.coinNumber = res.data[0]['fields']['coin_total']
      }
    })
  },
  components: {
    Calendar
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

aside {
  padding: 10px;
  margin-top: 40px;
}

.button-area {
  background-color: white;
  border-radius: 0 0 5px 5px;
  box-shadow: 1px 1px 1px 1px rgb(188, 221, 221);
  padding: 10px 0 10px 0;
}

.button-type-init {
  width: 80%;
  height: 50px;
  background-color: #f8f8f8;
  margin: 15px auto 15px auto;
}

input.button-type-init {
  border-radius: 5px;
  border: 0;
  padding: 9px;
  font-family: PingFangSC-Regular;
  color: black;
  font-size: 14px;
  outline: none;
  display: list-item;
}

input.button-type-init:hover {
  color: white;
  background-color: rgb(74, 199, 103);
  transition-duration: 0.2s;
}

.button-type-focus {
  width: 80%;
  height: 50px;
  background-color: rgb(74, 199, 103);
  margin: 15px auto 15px auto;
}

input.button-type-focus {
  color: white;
  border-radius: 5px;
  border: 0;
  padding: 9px;
  font-family: PingFangSC-Regular;
  font-size: 14px;
  outline: none;
  display: list-item;
}

.card {
  background: url("../../images/1_bg1.png");
  background-size: 230px;
  height: 100px;
  padding-top: 10px;
  padding-left: 20px;
  padding-bottom: 20px;
  border-radius: 5px 5px 0 0;
  box-shadow: 1px 1px 1px 1px rgb(188, 221, 221);
}

.card-top {
  height: 60px;
}

.head-img {
  height: 60px;
  width: 60px;
  border-radius: 50%;
  -webkit-border-radius: 50%;
  -moz-border-radius: 50%;
  margin-top: 15px;
  position: inherit;
  float: left;
  margin-right: 10px;
}

.name {
  margin-top: 10px;
  float: left;
  text-align: center;
  line-height: 40px;
  vertical-align: text-bottom;
  font-size: 15px;
  font-weight: bold;
}

.coin {
  float: left;
  text-align: center;
  line-height: 10px;
  vertical-align: text-bottom;
  margin-left: 10px;
}

.coin-img {
  height: 15px;
  width: 15px;
  position: inherit;
}

.card-button {
  float: right;
  background-color: white;
  margin-right: 10px;
  margin-top: 15px;
  margin-bottom: 10px;
}

input.card-button {
  color: #ff9900;
  border-radius: 20px;
  border: 0;
  font-size: 13px;
  outline: none;
  height: 25px;
  width: 70px;
}

input.card-button:hover {
  background-color: #ff9900;
  color: white;
  transition-duration: 0.2s;
}

input.card-button:active {
  background-color: #ff9900;
  color: white;
  transition-duration: 0.2s;
}

input.card-button:focus {
  background-color: #ff9900;
  color: white;
  transition-duration: 0.2s;
}

.calendar-area {
  z-index: 10;
  position: absolute;
  left: 30%;
  top: 9%;
}
</style>
