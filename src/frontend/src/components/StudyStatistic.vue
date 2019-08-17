<template>
  <div>
    <main-show-top></main-show-top>
    <div class="bg-img">
      <el-row>
        <main-show :showStatistics="true"></main-show>
        <el-col :span="1">&nbsp;</el-col>
        <el-col :span="13" class="gram-container">
          <span class="title">学习报告</span>
          <div class="line"></div>
          <div class="broadcast">学习报告展现了您最近一周内每天学习的<span class="title-color">单词数量</span>、本月<span class="title-color">学习时间</span>；以及<span class="title-color">测试成绩</span>等数据</div>
          <div id="chart" class="chart"></div>
          <div class="pie"></div>
          <div class="table-title">测试成绩</div>
          <el-table
            :data="tableData"
            border
            stripe
            :cell-style="cellStyle"
            class="table-stripe">
            <el-table-column
              prop="index"
              label="序号"
              width="180"
              align="center">
            </el-table-column>
            <el-table-column
              prop="book"
              label="课本"
              width="180"
              align="center">
            </el-table-column>
            <el-table-column
              prop="testType"
              label="测试类型"
              align="center">
            </el-table-column>
            <el-table-column
              prop="score"
              label="分数"
              align="center">
            </el-table-column>
            <el-table-column
              prop="isPass"
              label="通过"
              align="center">
              <template scope="scope">
                <span v-if="scope.row.isPass">
                  是
                </span>
                <span v-else class="not-pass">
                  否
                </span>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import MainShow from './common/MainShow'
import MainShowTop from './common/MainShowTop'
const axios = require('axios')
export default {
  data: function () {
    return {
      showStatistics: true,
      testTypeObj: {
        'preTest': '学前测试',
        'reviewTest': '巩固测试',
        'afterTest': '学后测试',
        'allTest': '一测到底'
      },
      barOption: {
        title: {
          text: '最近一周内单词学习情况图表',
          left: 'center',
          textStyle: {
            fontSize: 20,
            fontWeight: '400',
            fontFamily: 'monospace'
          }
        },
        grid: {
          show: true,
          borderColor: 'transparent',
          top: 50
        },
        legend: {
          top: -5,
          right: 60,
          orient: 'vertical'
        },
        tooltip: {},
        xAxis: {
          data: [],
          axisLabel: {
            interval: 0
          },
          splitLine: {
            show: true
          }
        },
        yAxis: {
          minInterval: 50
        },
        series: [
          {
            name: '单词数量',
            type: 'bar',
            data: [],
            splitArea: {show: true},
            itemStyle: {
              normal: {
                color: '#6495ED',
                label: {
                  show: true,
                  position: 'top',
                  textStyle: {
                    color: 'black'
                  }
                },
                shadowBlur: 30,
                shadowColor: 'rgba(255, 227, 42, 0.3)',
                shadowOffsetX: -5,
                shadowOffsetY: 5
              }
            }
          },
          {
            name: '趋势曲线',
            type: 'line',
            showSymbol: true,
            symbol: 'circle',
            symbolSize: 10,
            data: [],
            itemStyle: {
              normal: {
                color: '#DAA520',
                width: 1
              }
            }
          }
        ]
      },
      pieOption: {
        title: {
          text: '本月学习时间统计',
          left: 'center',
          textStyle: {
            fontSize: 20,
            fontWeight: '400',
            fontFamily: 'monospace'
          }
        },
        legend: {
          bottom: 10,
          left: 'center',
          data: ['单词拼写', '单词识别']
        },
        color: ['#DAA520', '#6495ED'],
        series: [
          {
            type: 'pie',
            radius: '65%',
            center: ['50%', '50%'],
            selectedMode: 'single',
            data: [
              {value: 548, name: '单词拼写'},
              {value: 1235, name: '单词识别'}
            ],
            label: {
              normal: {
                position: 'inner',
                formatter: '{d}%',
                fontSize: 15,
                color: '#2F4F4F'
              }
            },
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      },
      tableData: []
    }
  },
  methods: {
    draw () {
      let chart = this.$echarts.init(document.getElementById('chart'))
      let pie = this.$echarts.init(document.getElementsByClassName('pie')[0])
      let barOption = this.barOption
      let pieOption = this.pieOption
      window.onresize = chart.resize
      chart.setOption(barOption)
      pie.setOption(pieOption)
    }
  },
  mounted () {
    for (let i = 0; i < 7; i++) {
      let timeNow = new Date()
      timeNow.setTime(timeNow.getTime() - i * 24 * 60 * 60 * 1000)
      this.barOption.xAxis.data.push((timeNow.getMonth() + 1) + '-' + timeNow.getDate())
    }
    axios.get(this.$store.state.BASEURL + 'study/get_bar_statistic?student_id=' + sessionStorage.getItem('student')).then(res => {
      if (res.data) {
        for (let i = 0; i < 7; i++) {
          this.barOption.series[0].data.push(res.data[i])
          this.barOption.series[1].data.push(res.data[i])
        }
        this.draw()
      }
    })
    const url = this.$store.state.BASEURL + 'study/student_statistic?student_id=' + sessionStorage.getItem('student')
    axios.get(url).then(res => {
      if (res.data) {
        let len = res.data.length
        let tableData = []
        for (let i = 0; i < len; i++) {
          let item = {}
          item['index'] = i + 1
          item['book'] = res.data[i].book
          item['testType'] = this.testTypeObj[res.data[i].data.test_type]
          item['score'] = res.data[i].data.test_score
          if (res.data[i].data.is_pass) {
            item['isPass'] = true
          } else {
            item['isPass'] = false
          }
          tableData.push(item)
        }
        this.tableData = tableData
      }
    })
  },
  components: {
    MainShow,
    MainShowTop
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

.chart {
  width: 80%;
  height: 450px;
  margin-top: 50px;
  margin-left: 10%;
}

.pie {
  width: 80%;
  height: 450px;
  margin-top: 20px;
  margin-left: 10%;
}

.title {
  color: #FF6347;
  display: block;
  margin-bottom: 10px;
  padding-top: 20px;
  padding-left: 18px;
}

.title-color {
  color: #FF6347;
}

.line {
  height: 3px;
  background: rgb(204, 200, 200);
  margin-left: 18px;
  margin-right: 18px;
}

.broadcast {
  border: 1px solid rgb(230, 230, 230);
  border-radius: 5px;
  color: rgb(100, 100, 100);
  line-height: 40px;
  font-size: 15px;
  padding-left: 20px;
  margin-top: 20px;
  margin-left: 18px;
  margin-right: 18px;
}

.gram-container {
  margin-top: 20px;
  background-color: #F8F8F8;
  border-radius: 5px;
  margin-top: 50px;
  margin-bottom: 20px;
  z-index: -2;
}

.el-table {
  width: 96%;
  border: 1px solid rgb(230, 230, 230);
  margin-bottom: 40px;
  margin-left: 2%;
}

.table-title {
  font-size: 20px;
  font-family: 'monospace';
  text-align: center;
  margin-top: 30px;
  margin-bottom: 20px;
}

.not-pass {
  color: #FF6347
}
</style>
