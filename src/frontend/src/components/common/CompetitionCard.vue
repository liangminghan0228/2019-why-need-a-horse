<template>
  <div class="competition-card">
    <img class="top-competition-class" :src="competition.type === 'infinite' ? url2 : url1" alt="x">
    <img class="competition-status" :src="isParticipate ? url3 : url4" alt="x">
    <div class="card-middle">
      <div>
        <div class="dot"></div>
        <h3 class="competition-time-interval">{{competition.timeInterval}}</h3>
      </div>
      <p>{{competition.startTime}} - {{competition.endTime}}</p>
      <span>{{competition.bookName}}</span>
    </div>
    <div class="photo-part">
      <div class="head-image1"></div>
      <div class="head-image2"></div>
      <div class="head-image3"></div>
      <div class="top1-student-name">{{competition.topThree[0].studentName}}</div>
      <div class="top2-student-name">{{competition.topThree[1].studentName}}</div>
      <div class="top3-student-name">{{competition.topThree[2].studentName}}</div>
      <img class="top1" src="../../images/11_little2.png" alt="top1" :style="{'background-image': competition.topThree[0].avatar}">
      <img class="top2" src="../../images/15_little1.png" alt="top2" :style="{'background-image': competition.topThree[1].avatar}">
      <img class="top3" src="../../images/13_little3.png" alt="top3" :style="{'background-image': competition.topThree[2].avatar}">
    </div>
    <div class="card-footer">
      <p class="footer-rank">我的排名：{{competition.rank}}</p>
      <button class="detail-button" @click="goCompetitionDetailPage">详情>></button>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      url1: require('../../images/21_platform pk.png'),
      url2: require('../../images/39_battle.png'),
      url3: require('../../images/participation.png'),
      url4: require('../../images/toparticipate.png'),
      currStudentRank: 999
    }
  },
  methods: {
    goCompetitionDetailPage () {
      this.$store.state.COMPETITIONID = this.competition.pk
      this.$router.push('/competitiondetails')
    }
  },
  props: {
    isParticipate: {
      type: Boolean,
      default: false
    },
    isClick: {
      type: Boolean,
      default: false
    },
    competition: {
      default: {
        timeInterval: '',
        type: '',
        startTime: '',
        endTime: '',
        bookName: '',
        pk: 1,
        rank: 0,
        topThree: [
          {
            studentName: '',
            avatar: ''
          },
          {
            studentName: '',
            avatar: ''
          },
          {
            studentName: '',
            avatar: ''
          }
        ]
      }
    }
  }
}
</script>

<style scoped>
.competition-card:hover {
  width: 250px;
  height: 300px;
  border: 1px solid rgb(74, 199, 103);
  border-top: 3px solid rgb(74, 199, 103);
  box-shadow: 0 0 3px rgb(74, 199, 103);
  position: relative;
  border-radius: 5px;
}

.competition-card {
  width: 250px;
  height: 300px;
  border: 1px solid rgb(240, 240, 240);
  border-top: 3px solid rgb(240, 240, 240);
  box-shadow: 0 0 1px rgb(240, 240, 240);
  position: relative;
  border-radius: 5px;
}

.top-competition-class {
  position: absolute;
  top: -10px;
  left: 0;
}

.competition-status {
  position: absolute;
  top: 5px;
  right: 0;
}

.card-middle {
  width: 100%;
  margin-top: 60px;
  text-align: center;
}

.card-middle span {
  font-size: 12px;
  text-align: center;
  color: rgb(83, 85, 87);
}

.dot {
  height: 10px;
  width: 10px;
  border-radius: 100%;
  background-color: rgb(30, 209, 30);
  display: inline-block;
}

p {
  margin: 8px;
}

.competition-time-interval {
  display: inline-block;
  margin: 5px;
}

.photo-part {
  width: max-content;
  margin: 1.2ex auto 0 auto;
  position: relative;
}

.card-footer {
  width: 100%;
  position: absolute;
  bottom: 5px;
}

.footer-rank {
  display: inline;
  color: rgb(92, 90, 90);
}

.top1-student-name {
  color: white;
  width: 40px;
  height: 30px;
  position: absolute;
  left: 85px;
  bottom: 15px;
}

.top2-student-name {
  color: white;
  width: 40px;
  height: 30px;
  position: absolute;
  left: 15px;
  bottom: 5px;
}

.top3-student-name {
  color: white;
  width: 40px;
  height: 30px;
  position: absolute;
  right: 10px;
  bottom: 5px;
}

.head-image1 {
  width: 40px;
  height: 40px;
  background-image: url('../../images/36_undone.png');
  background-repeat: no-repeat;
  background-size: cover;
  border-radius: 50%;
  position: absolute;
  left: 50%;
  margin-left: -20px;
}

.head-image2 {
  width: 40px;
  height: 40px;
  background-image: url('../../images/36_undone.png');
  background-repeat: no-repeat;
  background-size: cover;
  border-radius: 50%;
  position: absolute;
  left: 10px;
  bottom: 35px;
}

.head-image3 {
  width: 40px;
  height: 40px;
  background-image: url('../../images/36_undone.png');
  background-repeat: no-repeat;
  background-size: cover;
  border-radius: 50%;
  position: absolute;
  left: 150px;
  bottom: 30px;
}

.detail-button {
  background-color: white;
  border: 0;
  float: right;
  margin-right: 15px;
  color: rgb(15, 171, 233);
}
</style>
