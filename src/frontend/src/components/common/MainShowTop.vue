<template>
  <el-row>
    <el-col :span="3">&nbsp;</el-col>
    <el-col :span="4">
      <img class="bird" src="../../images/add_bird.png" alt="bird"/>
    </el-col>
    <el-col :span="1">&nbsp;</el-col>
    <el-col :span="13">
      <div class="head-nav">
        <img class="trophy" src="../../images/17_trophy.png" alt="trophy"/>
        <img class="new-tips" src="../../images/new.png" alt="newTips"/>
        <el-button type="text" :class="showRankList?show:init" @click.native="changeToRankList">排行榜</el-button>
        <set-user-info></set-user-info>
        <el-button type="text" @click.native="changeToLogin">退出</el-button>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import * as Cookies from 'js-cookie'
import SetUserInfo from './SetUserInfo'
export default {
  data: function () {
    return {
      init: 'button-init',
      show: 'button-focus'
    }
  },
  props: {
    showRankList: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    changeToRankList () {
      this.showRankList = true
      this.$router.push('/leaderboard')
    },
    changeToLogin () {
      Cookies.remove('student')
      sessionStorage.removeItem('student')
      this.$router.push('/login')
    },
    setUserInfo () {
      this.dialogFormVisible = true
    }
  },
  components: {
    SetUserInfo
  }
}
</script>

<style scoped>
* {
  margin: 0;
}

.el-row {
  line-height: 100%;
}

.trophy {
  width: 30px;
  position: absolute;
  left: -1em;
  top: 10px;
}

.bird {
  height: 50px;
}

.new-tips {
  position: absolute;
  left: 3.5em;
  top: 0.3em;
}

.head-nav {
  float: right;
  position: relative;
  height: 45px;
  line-height: 45px;
}

.el-button, .el-button--text {
  width: auto;
  height: auto;
  color: black;
  margin-left: 25px;
  font-size: 11px;
}

.el-button--text:hover {
  color: #33cc33;
}

.button-focus {
  color: #33cc33;
}
</style>
