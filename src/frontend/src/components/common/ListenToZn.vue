<template>
  <div>
    <div class="listen-zn">
      {{number}}.
      <img src="../../images/41_voice1.png" class="image-voice" />
      <div class="progress">
        <el-progress :percentage="50"></el-progress>
      </div>
      <br />
      <input type="button" :value="'A、' + option.a" :class="optionA" @click="chooseA" />
      <input type="button" :value="'B、' + option.b" :class="optionB" @click="chooseB" />
      <input type="button" :value="'C、' + option.c" :class="optionC" @click="chooseC" />
      <input type="button" :value="'D、' + option.d" :class="optionD" @click="chooseD" />
    </div>
    <input type="button" value="下一个" class="next-button" @click="nextWord"/>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      time: '00:00',
      optionA: 'choose-button',
      optionB: 'choose-button',
      optionC: 'choose-button',
      optionD: 'choose-button',
      isRight: false,
      isChoose: false
    }
  },
  methods: {
    chooseA: function () {
      this.optionA = 'choosed-button'
      this.optionB = 'choose-button'
      this.optionC = 'choose-button'
      this.optionD = 'choose-button'
    },
    chooseB: function () {
      this.optionA = 'choose-button'
      this.optionB = 'choosed-button'
      this.optionC = 'choose-button'
      this.optionD = 'choose-button'
    },
    chooseC: function () {
      this.optionA = 'choose-button'
      this.optionB = 'choose-button'
      this.optionC = 'choosed-button'
      this.optionD = 'choose-button'
    },
    chooseD: function () {
      this.optionA = 'choose-button'
      this.optionB = 'choose-button'
      this.optionC = 'choose-button'
      this.optionD = 'choosed-button'
    },
    nextWord: function () {
      if (this.isChoose === false){
        this.$message({
          message: '请选择一个选项',
          type: 'warning'
        })
      } else {
        this.isChoose = false
        this.optionA = 'choose-button'
        this.optionB = 'choose-button'
        this.optionC = 'choose-button'
        this.optionD = 'choose-button'
        this.$emit('sendAnswer', this.isRight)
        this.isRight = false
      }
    }
  },
  props: {
    option: {
      type: Object,
      default: () => []
    },
    number: {
      type: Number,
      default: 1
    }
  }
}
</script>

<style scoped>
.listen-zn {
  margin-top: 10px;
}

.choose-button {
  display: block;
  width: 300px;
  height: 40px;
  margin: 20px;
  line-height: 5px;
  text-align: left;
  background-color: white;
  border: 1px solid #dcdfe6;
  font-weight: 500;
  font-size: 14px;
  outline: 0;
  color: #606266;
  border-radius: 20px;
  padding-left: 20px;
}

.choosed-button {
  display: block;
  width: 300px;
  height: 40px;
  margin: 20px;
  line-height: 5px;
  text-align: left;
  font-weight: 500;
  font-size: 14px;
  outline: 0;
  border-radius: 20px;
  padding-left: 20px;
  background-color: rgb(236, 245, 255);
  color: rgb(67, 146, 236);
  border: 1px solid rgb(79, 152, 236);
}

.choose-button:hover {
  background-color: rgb(236, 245, 255);
  color: rgb(67, 146, 236);
  cursor: pointer;
  border: 1px solid rgb(79, 152, 236);
  transition-duration: 0.2s;
}

.image-voice {
  float: left;
  height: 20px;
  width: 20px;
  position: inherit;
  padding-right: 5px;
  margin-left: 20px;
}

.progress {
  width: 300px;
  float: left;
  margin-top: 4px;
  margin-bottom: 20px;
}

.progress /deep/ .el-progress-bar__inner {
  background-color: rgb(255, 177, 40);
}

.next-button {
  display: block;
  width: 100px;
  height: 40px;
  margin-top: 60px;
  margin-left: 250px;
  background-color: rgb(74, 199, 73);
  border: 0;
  font-weight: 500;
  font-size: 14px;
  outline: 0;
  color: white;
  border-radius: 10px;
  text-align: center;
  box-shadow: 1px 1px 1px 1px rgb(74, 199, 73);
  cursor: pointer;
}

.next-button:hover {
  background-color: rgb(123, 199, 123);
}
</style>
