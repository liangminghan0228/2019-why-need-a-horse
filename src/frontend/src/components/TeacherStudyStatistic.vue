<template>
  <div>
    <el-row class="top-row">
      <el-col :span="24" class="cancel-border"></el-col>
    </el-row>
    <el-row>
      <teacher-side-bar :showStatistic="true"></teacher-side-bar>
      <el-col :span="21" class="right-part">
        <div class="title">学习统计</div>
        <div class="select-option-bar">
          <select v-model="valueClass" class="select-machine" @change="selectClass">
            <option value="" disabled selected hidden>请选择班级</option>
            <option class="select-option"
              v-for="item in classes"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </option>
          </select>
          <el-button class="select-btn" @click="getSevenDayData('train')">训练量(最近七天)</el-button>
          <el-button class="select-btn" @click="getSevenDayData('vocabulary')">词汇量(最近七天)</el-button>
          <el-button class="select-btn" @click="getSevenDayData('time')">学习时间(最近七天)</el-button>
          <el-button class="select-btn" @click="getSevenDayData('and')">训练&词汇(最近七天)</el-button>
          <select v-model="valueType" class="select-machine" @change="selectType">
            <option value="" disabled selected hidden>请选择统计数据</option>
            <option
              v-for="item in dataTypes"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </option>
          </select>
        </div>
        <div class="title">{{title}}</div>
        <div id="chart" class="chart"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
const axios = require('axios')
import TeacherSideBar from './common/TeacherSideBar'
export default {
  data: function () {
    return {
      classes: [],
      sevenDays: {},
      allDays: {},
      sevenFlag: false,
      allFlag: false,
      titleObj: {
        'train': '[学员单词训练量]',
        'vocabulary': '[学员词汇量]',
        'time': '[学员学习时间]',
        'and': '[学员训练&词汇量]'
      },
      dataTypes: [
        {
          label: '训练总量',
          value: 'train'
        },
        {
          label: '词汇总量',
          value: 'vocabulary'
        },
        {
          label: '学习时间',
          value: 'time'
        },
        {
          label: '训练&词汇总量',
          value: 'and'
        }
      ],
      value: '',
      valueClass: '1',
      valueType: 'train',
      title: '班级学员学习统计',
      option: {
        title: {
          text: '[学员词汇量]',
          left: 'center',
          top: 15
        },
        grid: {
          show: true,
          borderColor: 'transparent',
          top: 60
        },
        tooltip: {},
        xAxis: {
          data: [],
          axisLabel: {
            interval: 0,
            rotate: -50
          },
          splitLine: {
            show: true
          }
        },
        yAxis: {
          maxInterval: 50
        },
        series: [{
          name: '词汇量',
          type: 'bar',
          data: [],
          splitArea: {show: true},
          itemStyle: {
            normal: {
              color: '#FFD700',
              label: {
                show: true,
                position: 'top',
                textStyle: {
                  color: 'black'
                }
              }
            }
          },
          barWidth: 10
        }]
      }
    }
  },
  methods: {
    draw () {
      let chart = this.$echarts.init(document.getElementById('chart'))
      let option = this.option
      window.onresize = chart.resize
      chart.setOption(option)
    },
    getStatistic () {
      let xData = []
      let lData = []
      if (!this.allFlag) {
        let url = this.$store.state.BASEURL + 'study/get_study_statistic?class=' + this.valueClass
        axios.get(url).then(res => {
          if (res.data) {
            this.allDays = res.data
            let length = this.allDays['student'].length
            for (let i = 0; i < length; i++) {
              xData = this.allDays['student']
              lData = this.allDays[this.valueType]
            }
            this.option.xAxis.data = xData
            this.option.series[0].data = lData
            this.option.title.text = this.titleObj[this.valueType]
            this.draw()
            this.allFlag = true
          }
        })
      } else {
        let length = this.allDays['student'].length
        for (let i = 0; i < length; i++) {
          xData = this.allDays['student']
          lData = this.allDays[this.valueType]
        }
        this.option.xAxis.data = xData
        this.option.series[0].data = lData
        this.option.title.text = this.titleObj[this.valueType]
        this.draw()
      }
    },
    selectClass () {
      if (this.valueType !== '') {
        this.allFlag = false
        this.getStatistic()
      }
    },
    selectType () {
      if (this.valueClass !== '') {
        this.allFlag = false
        this.getStatistic()
      }
    },
    getClassesInfo () {
      axios.get(this.$store.state.BASEURL + 'information/teacher_classes/').then((res) => {
        let total = res.data.length
        for (let i = 0; i < total; i++) {
          let tmpObj = {}
          tmpObj['label'] = res.data[i]['fields']['class_name']
          tmpObj['value'] = res.data[i]['pk']
          this.classes.push(tmpObj)
        }
        this.draw()
      })
    },
    getSevenDayData (dataType) {
      let xData = []
      let lData = []
      if (!this.sevenFlag) {
        let url = this.$store.state.BASEURL + 'study/get_study_statistic_seven?class=' + this.valueClass
        axios.get(url).then(res => {
          if (res.data) {
            this.sevenDays = res.data
            let length = this.sevenDays['student'].length
            for (let i = 0; i < length; i++) {
              xData = this.sevenDays['student']
              lData = this.sevenDays[dataType]
            }
            this.option.xAxis.data = xData
            this.option.series[0].data = lData
            this.option.title.text = this.titleObj[dataType]
            this.draw()
            this.sevenFlag = true
          }
        })
      } else {
        let length = this.sevenDays['student'].length
        for (let i = 0; i < length; i++) {
          xData = this.sevenDays['student']
          lData = this.sevenDays[dataType]
        }
        this.option.xAxis.data = xData
        this.option.series[0].data = lData
        this.option.title.text = this.titleObj[dataType]
        this.draw()
      }
    }
  },
  mounted () {
    this.getStatistic()
    this.getClassesInfo()
  },
  components: {
    TeacherSideBar
  }
}
</script>

<style scoped>
.cancel-border {
  border: 0 !important;
}

.top-row {
  height: 30px;
  background: linear-gradient(rgb(199, 211, 225), rgb(185, 198, 215));
}

.right-part {
  margin-top: 1%;
  padding-left: 10px;
}

.border-set {
  border: 1px solid rgb(230, 230, 230);
}

.chart {
  width: 100%;
  height: 480px;
}

.title {
  background-color: rgb(230, 230, 230);
  color: rgb(100, 100, 100);
  line-height: 25px;
  font-size: 15px;
  padding-left: 20px;
  margin-right: 20px;
}

.first-title {
  margin-top: 20px;
}

.select-option-bar {
  height: 45px;
}

.select-machine {
  width: 180px;
  height: 23px;
  margin-top: 12px;
  margin-left: 10px;
  outline: none;
  border: 1px solid rgb(230, 230, 230);
  background-color: white;
  border-radius: 5px;
  color: rgb(100, 100, 100);
}

.select-btn {
  height: 23px;
  width: 160px;
  font-size: 12px;
  margin-left: 10px;
  margin-top: 10px;
  padding: 0;
}
</style>
