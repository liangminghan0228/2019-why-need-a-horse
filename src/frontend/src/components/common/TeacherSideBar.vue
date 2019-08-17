<template>
  <el-col :span="3" class="cancel-border">
    <div>
      <div class="side-navigation">
        <div class="sub-menu">我的信息</div>
        <div class="menu-item">
          <change-password></change-password>
        </div>
        <div class="sub-menu">学习管理</div>
        <div class="menu-item">
          <button @click="goTeacherClasses" :class="showClasses ? show : init">班级列表</button>
        </div>
        <div class="menu-item">
          <button type="text" @click="goTeacherStudents" :class="showStudents ? show : init">学生名册</button>
        </div>
        <div class="menu-item">
          <button @click="goTeacherStudyStatistic" :class="showStatistic ? show : init">学习统计</button>
        </div>
        <div class="menu-item">
          <button @click="goSearchContest" :class="showCompetition ? show : init">单词比赛</button>
        </div>
        <div class="sub-menu">系统设置</div>
        <div class="menu-item">
          <button class="button-type-init" @click="logOut">退出</button>
        </div>
      </div>
    </div>
  </el-col>
</template>

<script>
import ChangePassword from './ChangePassword'
import * as Cookies from 'js-cookie'
export default {
  data () {
    return {
      show: 'button-type-focus',
      init: 'button-type-init'
    }
  },
  props: {
    showClasses: {
      type: Boolean,
      default: false
    },
    showStudents: {
      type: Boolean,
      default: false
    },
    showCompetition: {
      type: Boolean,
      default: false
    },
    showStatistic: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    goTeacherClasses () {
      this.$router.push('/teacherclasses')
    },
    goTeacherStudents () {
      this.$router.push('/teacherstudents')
    },
    goTeacherStudyStatistic () {
      this.$router.push('/teacherstudystatistic')
    },
    goSearchContest () {
      this.$router.push('/searchcontest')
    },
    logOut () {
      Cookies.remove('teacher')
      sessionStorage.removeItem('teacher')
      this.$router.push('/login')
    }
  },
  components: {
    ChangePassword
  }
}
</script>

<style scoped>
.cancel-border {
  border: 0 !important;
}

.sub-menu {
  padding-left: 5px;
  text-align: left;
  font-size: 16px;
  height: 35px;
  line-height: 35px;
  color: rgb(77, 77, 77);
  background: linear-gradient(rgb(204, 214, 226), rgb(184, 196, 218));
}

.menu-item {
  position: relative;
  text-align: center;
  height: 30px;
  margin: 0;
  padding: 0;
  background-color: rgb(219, 226, 235);
}

.button-type-init {
  border: 0;
  background-color: rgb(219, 226, 235);
  width: 100%;
  height: 100%;
}

.button-type-init:hover {
  border: 0;
  background: rgb(200, 200, 240);
  width: 100%;
  height: 100%;
}

.button-type-focus {
  border: 0;
  background: rgb(200, 200, 240);
  width: 100%;
  height: 100%;
}
</style>
