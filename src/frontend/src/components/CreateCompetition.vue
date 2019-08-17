<template>
  <div>
    <el-button @click="createCompetitionVisible = true" class="create-button">新建比赛</el-button>
    <el-dialog :visible.sync="createCompetitionVisible">
      <div class="create-competition">
        <div class="organizer-area">
          <span class="organise-font">组织方:</span>
          <el-input v-model="organiser" placeholder="请输入"></el-input>
        </div>
        <div>
          <div v-if="isBeginOne === true && isFinishOne === true" class="circle-right">√</div>
          <div v-if="isBeginOne === true && isFinishOne === false" class="circle-proceed">1</div>
          <div v-if="isBeginOne === false" class="circle-unsettled">1</div>
          <el-input v-model="competitionName" placeholder="请输入比赛名称"></el-input>
        </div>
        <div class="el-divider el-divider--vertical"></div>
        <div>
          <div v-if="isBeginTwo === true && isFinishTwo === true" class="circle-right">√</div>
          <div v-if="isBeginTwo === true && isFinishTwo === false" class="circle-proceed">2</div>
          <div v-if="isBeginTwo === false" class="circle-unsettled">2</div>
          <p>选择比赛类型:</p>
          <div class="el-divider el-divider--vertical"></div>
          <el-radio-group v-model="competitionType">
            <el-radio-button label="infinite">
              无限模式
              <br />
              <br />
              <label class="small-font">不限次数和题数，总分高者胜</label>
            </el-radio-button>
            <el-radio-button label="pk">
              pk模式
              <br />
              <br />
              <label class="small-font">不限次挑战他人，总积分高者胜</label>
            </el-radio-button>
          </el-radio-group>
        </div>
        <div>
          <div v-if="isBeginThree === true && isFinishThree === true" class="circle-right">√</div>
          <div v-if="isBeginThree === true && isFinishThree === false" class="circle-proceed">3</div>
          <div v-if="isBeginThree === false" class="circle-unsettled">3</div>
          <p>比赛规则设置：</p>
          <div class="rule-area">
            <div class="option-area">
              <label class="option-name">比赛时间：</label>
              <br />
              <br />
              <el-date-picker
                v-model="setTime"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
              ></el-date-picker>
            </div>
            <div class="option-area">
              <label class="option-name">最大参与人数：</label>
              <el-input type="text" v-model.number="maxNumber" placeholder="请输入"></el-input>
            </div>
            <div class="option-area">
              <label class="option-name">比赛门槛：</label>
              <el-radio v-model="limit" label="free">免费</el-radio>
              <el-radio v-model="limit" label="pay">付费</el-radio>
            </div>
            <input
              v-if="limit === 'pay'"
              type="text"
              autocomplete="off"
              placeholder="请输入所需金币数量"
              v-model.number="coinNumber"
              class="coin-input"
            />
            <div class="option-area">
              <label class="option-name">比赛内容：</label>
              <el-radio v-model="content" label="no">不限范围</el-radio>
              <el-radio v-model="content" label="special">设定教材</el-radio>
            </div>
            <input
              v-if="content === 'special'"
              type="text"
              autocomplete="off"
              placeholder="请输入教材ID"
              v-model.number="bookId"
              class="coin-input"
            />
            <div class="option-area">
              <label class="option-name">比赛难度：</label>
              <el-radio v-model="competition.difficulty" label="easy">简单</el-radio>
              <el-radio v-model="competition.difficulty" label="middle">普通</el-radio>
              <el-radio v-model="competition.difficulty" label="difficult">困难</el-radio>
            </div>
            <div class="option-area">
              <label class="option-name">
                <span class="question-type-font">题型：</span>
              </label>
              <el-checkbox v-model="competition.zn_to_en">中译英</el-checkbox>
              <el-checkbox v-model="competition.en_to_zn">英译中</el-checkbox>
              <el-checkbox v-model="competition.listen_to_spelling">拼写</el-checkbox>
              <el-checkbox v-model="competition.listen_to_choose">听选中</el-checkbox>
            </div>
            <div class="option-area">
              <label class="option-name">
                <span class="question-type-font">道具：</span>
              </label>
              <el-switch
                v-model="competition.tool"
                active-color="rgb(24, 144, 255)"
                inactive-color="rgb(166, 166, 166)"
              ></el-switch>
            </div>
            <div class="option-area">
              <label class="option-name">参赛学校：</label>
              <el-input v-model="school" placeholder="请输入学校名称"></el-input>
            </div>
            <div class="option-area">
              <label class="option-name">参赛年级：</label>
              <el-input type="text" v-model.number="grade" placeholder="请输入年级序号"></el-input>
            </div>
            <div class="option-area">
              <label class="option-name">参赛班级：</label>
              <el-input type="text" v-model.number="classes"  placeholder="请输入班级id"></el-input>
            </div>
            <div class="option-area">
              <label class="option-name">奖励数量：</label>
              <el-input type="text" v-model.number="award"  placeholder="请输入奖励金币数量"></el-input>
            </div>
            <div class="option-area">
              <label class="option-name">奖励人数：</label>
              <el-input type="text" v-model.number="topNumber" placeholder="请选择奖励前几名"></el-input>
            </div>
            <input type="button" value="提交" class="submit-button" @click="submit" />
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
const axios = require('axios')
export default {
  data: function () {
    return {
      competition: {
        'name': '',
        'organiser': '',
        'status': 'forbid',
        'set_time': '',
        'max_number': '',
        'type': '',
        'difficulty': 'easy',
        'begin_time': '2019-07-05',
        'end_time': '2019-09-05',
        'tool': true,
        'zn_to_en': false,
        'en_to_zn': false,
        'listen_to_spelling': false,
        'listen_to_choose': false,
        'coin_number': 0,
        'book_id': '',
        'top_number': '',
        'award': '',
        'classes': '',
        'school': '',
        'grade': ''
      },
      limit: 'free',
      content: '',
      coinNumber: '',
      createCompetitionVisible: false,
      topNumber: '',
      maxNumber: '',
      bookId: '',
      award: '',
      classes: '',
      school: '',
      grade: '',
      isBeginOne: false,
      isFinishOne: false,
      isBeginTwo: false,
      isFinishTwo: false,
      isBeginThree: false,
      isFinishThree: false,
      organiser: '',
      competitionName: '',
      competitionType: '',
      setTime: ''
    }
  },
  methods: {
    submit: function () {
      if (this.limit === 'free') {
        this.coinNumber = 0
      }
      if (this.checkIfEmpty()) {
        this.alterValue()
        const url = this.$store.state.BASEURL + 'competitions/new_competition'
        axios.post(url, JSON.stringify(this.competition)).then(res => {
          if (res.data === '所选教材不存在') {
            this.$message(res.data)
          } else {
            this.createCompetitionVisible = false
            this.$emit('regetCompetitionInfo')
            this.$message(res.data)
          }
        })
      }
    },
    checkIfEmpty: function () {
      if (this.content === 'no') {
        this.bookId = 0
      }
      if (
        this.competitionName === '' ||
        this.organiser === '' ||
        this.setTime === '' ||
        this.maxNumber === '' ||
        this.competitionType === '' ||
        this.competition.difficulty === '' ||
        this.coinNumber === '' ||
        this.bookId === '' ||
        this.topNumber === '' ||
        this.award === '' ||
        this.classes === '' ||
        this.school === '' ||
        this.grade === ''
      ) {
        this.$message('输入不能为空')
        return false
      }
      return true
    },
    alterValue: function () {
      this.competition.max_number = this.maxNumber
      this.competition.coin_number = this.coinNumber
      this.competition.top_number = this.topNumber
      this.competition.book_id = this.bookId
      this.competition.award = this.award
      this.competition.classes = this.classes
      this.competition.grade = this.grade
      this.competition.school = this.school
      this.competition.organiser = this.organiser
      this.competition.name = this.competitionName
      this.competition.type = this.competitionType
      this.competition.set_time = this.setTime
    }
  },
  computed: {
    rule () {
      const {
        setTime,
        maxNumber,
        coinNumber,
        topNumber,
        bookId,
        award,
        classes,
        grade,
        school
      } = this
      return {
        setTime,
        maxNumber,
        coinNumber,
        topNumber,
        bookId,
        award,
        classes,
        grade,
        school
      }
    }
  },
  watch: {
    competitionName: function (val) {
      if (val !== '') {
        this.isBeginOne = true
        if (this.isBeginTwo === true) {
          this.isFinishTwo = true
        }
      } else {
        this.isBeginOne = false
      }
    },
    competitionType: function (val) {
      if (val !== '') {
        this.isBeginTwo = true
        if (this.isBeginOne === true) {
          this.isFinishOne = true
        }
      } else {
        this.isBeginTwo = false
      }
    },
    rule: {
      handler: function (val) {
        if (val !== '') {
          this.isBeginThree = true
          if (this.isBeginTwo === true) {
            this.isFinishTwo = true
          }
          if (this.isBeginOne === true) {
            this.isFinishOne = true
          }
        } else {
          this.isBeginThree = false
        }
      },
      deep: true
    },
    grade: function (val) {
      if (val !== '') {
        if (typeof (val) === 'string') {
          this.$message('请输入合法年级')
          this.grade = ''
        }
        if (typeof (val) === 'number') {
          if (val < 1 || val > 12) {
            this.$message('请输入合法年级')
            this.grade = ''
          }
        }
      }
    },
    classes: function (val) {
      if (val !== '') {
        if (typeof (val) === 'string') {
          this.$message('请输入合法班级')
          this.classes = ''
        }
        if (typeof (val) === 'number') {
          if (val < 0){
            this.$message('请输入合法班级')
            this.classes = ''
          }
        }
      }
    },
    coinNumber: function (val) {
      if (val !== '') {
        if (typeof (val) === 'string') {
          this.$message('请输入合法金币数')
          this.coinNumber = ''
        }
        if (typeof (val) === 'number') {
          if (val < 0) {
            this.$message('请输入合法金币数')
            this.coinNumber = ''
          }
        }
      }
    },
    award: function (val) {
      if (val !== '') {
        if (typeof (val) === 'string') {
          this.$message('请输入合法金币数')
          this.award = ''
        }
        if (typeof (val) === 'number') {
          if (val < 0) {
            this.$message('请输入合法金币数')
            this.award = ''
          }
        }
      }
    },
    topNumber: function (val) {
      if (val !== '') {
        if (typeof (val) === 'string') {
          this.$message('请输入合法人数')
          this.topNumber = ''
        }
        if (typeof (val) === 'number') {
          if (val < 0) {
            this.$message('请输入合法人数')
            this.topNumber = ''
          }
        }
      }
    },
    maxNumber: function (val) {
      if (val !== '') {
        if (typeof (val) === 'string') {
          this.$message('请输入合法人数')
          this.maxNumber = ''
        }
        if (typeof (val) === 'number') {
          if (val < 0) {
            this.$message('请输入合法人数')
            this.maxNumber = ''
          }
        }
      }
    },
    bookId: function (val) {
      if (val !== '') {
        if (typeof (val) === 'string') {
          this.$message('请输入合法教材id')
          this.bookId = ''
        }
        if (typeof (val) === 'number') {
          if (val < 0) {
            this.$message('请输入合法教材id')
            this.bookId = ''
          }
        }
      }
    },
    createCompetitionVisible: function (val) {
      if (val === true) {
        this.competition = {
          'name': '',
          'organiser': '',
          'status': 'forbid',
          'set_time': '',
          'max_number': '',
          'type': '',
          'difficulty': 'easy',
          'begin_time': '2019-07-05',
          'end_time': '2019-09-05',
          'tool': true,
          'zn_to_en': false,
          'en_to_zn': false,
          'listen_to_spelling': false,
          'listen_to_choose': false,
          'coin_number': 0,
          'book_id': '',
          'top_number': '',
          'award': '',
          'classes': '',
          'school': '',
          'grade': ''
        }
        this.limit = 'free'
        this.content = ''
        this.coinNumber = ''
        this.topNumber = ''
        this.maxNumber = ''
        this.bookId = ''
        this.award = ''
        this.classes = ''
        this.school = ''
        this.grade = ''
        this.isBeginOne = false
        this.isFinishOne = false
        this.isBeginTwo = false
        this.isFinishTwo = false
        this.isBeginThree = false
        this.isFinishThree = false
        this.organiser = ''
        this.competitionName = ''
        this.competitionType = ''
        this.setTime = ''
      }
    }
  }
}
</script>

<style scoped>
.create-competition {
  height: 450px;
  overflow: auto;
  margin: 0 !important;
}

button {
  height: 26px;
  width: 100px;
  border-radius: 5px;
  color: #ffffff;
  background-color: rgb(24, 144, 255);
  border: 1px solid rgb(24, 144, 255);
  outline: none;
}

p {
  font-size: 18px;
  font-weight: 600;
  line-height: 30px;
}

.rule-area {
  margin-left: 40px;
}

.small-font {
  font-size: 10px;
  color: rgb(166, 166, 166);
}

.create-competition /deep/ .el-input__inner {
  width: 300px;
}

.el-input {
  display: inline;
}

.organizer-area {
  margin-top: 20px;
  font-size: 15px;
  margin-bottom: 20px;
}

.circle-right {
  border-radius: 50%;
  border: 2px solid rgb(24, 144, 225);
  width: 30px;
  height: 30px;
  color: rgb(24, 144, 225);
  font-weight: bold;
  font-size: 20px;
  text-align: center;
  float: left;
  margin-right: 20px;
}

.circle-proceed {
  border-radius: 50%;
  border: 2px solid rgb(24, 144, 225);
  width: 30px;
  height: 30px;
  background-color: rgb(24, 144, 225);
  color: white;
  font-size: 20px;
  text-align: center;
  font-weight: normal;
  margin-right: 20px;
  float: left;
}

.circle-unsettled {
  border-radius: 50%;
  border: 2px solid rgb(204, 204, 204);
  width: 30px;
  height: 30px;
  color: rgb(204, 204, 204);
  font-weight: normal;
  font-size: 20px;
  text-align: center;
  margin-right: 20px;
  float: left;
}

.el-divider--vertical {
  display: inline-block;
  width: 2px;
  height: 5em;
  margin: 10px 15px;
  vertical-align: middle;
  position: relative;
}

.el-button {
  margin-left: 50px;
  height: 80px;
}

.option-name {
  color: rgb(49, 49, 49);
}

.option-area {
  margin: 40px;
}

.el-select {
  margin: 20px;
  margin-left: 60px;
}

.coin-input {
  -webkit-appearance: none;
  background-color: #fff;
  background-image: none;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  color: #606266;
  display: inline-block;
  font-size: 13px;
  height: 40px;
  line-height: 40px;
  outline: 0;
  padding: 0 15px;
  -webkit-transition: border-color 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
  transition: border-color 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
  width: 200px;
  margin-left: 40px;
}

.submit-button {
  outline: none;
  color: #606266;
  width: 100px;
  height: 35px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background-color: white;
  margin-left: 200px;
}

.submit-button:hover {
  background-color: rgb(24, 144, 225);
  color: white;
}

.el-radio-button__orig-radio:checked + .el-radio-button__inner {
  color: #606266;
  background-color: white;
  border-color: #409eff;
  -webkit-box-shadow: -1px 0 0 0 #409eff;
  box-shadow: -1px 0 0 0 #409eff;
}

.el-radio-button__inner {
  height: 80px;
  width: 200px;
}

.create-button {
  height: 50%;
  width: 30%;
  border-radius: 5px;
  color: #ffffff;
  background-color: rgb(24, 144, 255);
  border: 1px solid rgb(24, 144, 255);
  outline: none;
  margin: 0;
  margin-top: 4%;
}

.organise-font {
  margin-right: 3px;
}

.question-type-font {
  margin-left: 28px;
}
</style>
