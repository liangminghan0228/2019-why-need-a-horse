<template>
  <div class="calendar" v-show="showCalendar" @click="cardToday">
    <el-calendar>
      <div slot="dateCell" slot-scope="{date, data}">
        <p :class="isStudied(data.day) ? 'has-studied' : ''">
          {{data.day.split('-').slice(1).join('-')}}
          <br />
          {{isStudied(data.day) ? '✔️已打卡' : ''}}
        </p>
      </div>
    </el-calendar>
  </div>
</template>

<script>
const axios = require('axios')
export default {
  data () {
    return {
      cardDays: [],
      studentID: '',
      message: '',
      showCalendar: true
    }
  },
  methods: {
    isStudied: function (day) {
      return this.cardDays.includes(day)
    },
    cardToday () {
      let today = new Date() + ''
      let arr = today.split(' ', 4)
      today = ''
      today += arr[3] + '-'
      switch (arr[1]) {
      case 'Jan':
        today += '01-'
        break
      case 'Feb':
        today += '02-'
        break
      case 'Mar':
        today += '03-'
        break
      case 'Apr':
        today += '04-'
        break
      case 'May':
        today += '05-'
        break
      case 'June':
        today += '06-'
        break
      case 'July':
        today += '07-'
        break
      case 'Aug':
        today += '08-'
        break
      case 'Sep':
        today += '09-'
        break
      case 'Oct':
        today += '10-'
        break
      case 'Nov':
        today += '10-'
        break
      case 'Dec':
        today += '12-'
        break
      }
      today += arr[2]
      if (this.cardDays.includes(today) === false) {
        this.cardDays.push(today)
        this.message.append('today', today)
        this.axios.post(this.$store.state.BASEURL + 'study/card_today', this.message).then((res) => {
          this.$message({
            showClose: true,
            message: res.data
          })
        })
      }
    }
  },
  mounted () {
    this.studentID = sessionStorage.getItem('student')
    this.message = new URLSearchParams()
    this.message.append('studentID', this.studentID)
    axios.post(this.$store.state.BASEURL + 'study/get_study_date', this.message).then((res) => {
      this.cardDays = []
      for (let i = 0; i < res.data.length; i++) {
        this.cardDays.push(res.data[i].fields.study_date)
      }
    })
  }
}
</script>

<style scoped>
.has-studied {
  color: rgb(25, 161, 95);
}

.calendar {
  width: 30%;
  height: 50%;
  position: absolute;
  left: 0;
  top: 0;
}

.calendar /deep/ .el-calendar-table thead th {
  padding: 0;
  font-size: 0.5vw;
}

.calendar /deep/ .el-calendar-day {
  height: 4vh;
  padding: 0;
}

.calendar /deep/ p {
  margin: 0;
  font-size: 0.1vw;
}
</style>