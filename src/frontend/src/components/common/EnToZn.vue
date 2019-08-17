<template>
  <div>
    <div class="en-zn">
      <label class="title-font">{{number}}. {{question.title}}</label>
      <input type="button" :value="'A、' + question.a" :class="optionA" @click="chooseA" />
      <input type="button" :value="'B、' + question.b" :class="optionB" @click="chooseB" />
      <input type="button" :value="'C、' + question.c" :class="optionC" @click="chooseC" />
      <input type="button" :value="'D、' + question.d" :class="optionD" @click="chooseD" />
    </div>
    <input type="button" value="下一个" class="next-button" @click="nextWord" />
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
      isChoose: false,
      question: {
        title: '',
        a: '',
        b: '',
        c: '',
        d: ''
      },
      index: ''
    }
  },
  methods: {
    chooseA: function () {
      this.optionA = 'choosed-button'
      this.optionB = 'choose-button'
      this.optionC = 'choose-button'
      this.optionD = 'choose-button'
      this.chooseAnswer = this.question.a
      this.isChoose = true
    },
    chooseB: function () {
      this.optionA = 'choose-button'
      this.optionB = 'choosed-button'
      this.optionC = 'choose-button'
      this.optionD = 'choose-button'
      this.chooseAnswer = this.question.b
      this.isChoose = true
    },
    chooseC: function () {
      this.optionA = 'choose-button'
      this.optionB = 'choose-button'
      this.optionC = 'choosed-button'
      this.optionD = 'choose-button'
      this.chooseAnswer = this.question.c
      this.isChoose = true
    },
    chooseD: function () {
      this.optionA = 'choose-button'
      this.optionB = 'choose-button'
      this.optionC = 'choose-button'
      this.optionD = 'choosed-button'
      this.chooseAnswer = this.question.d
      this.isChoose = true
    },
    nextWord: function () {
      if (this.isChoose === false) {
        this.$message({
          message: '请选择一个选项',
          type: 'warning'
        })
      } else {
        if (this.chooseAnswer === this.option.correct_option) {
          this.isRight = true
        }
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
  },
  mounted () {
    if (Object.keys(this.option).length !== 0) {
      this.question.title = this.option.question
      this.index = Math.floor(Math.random() * 4)
      //随机数生成为0到3，对于正确选项的顺序为a到d
      if (this.index === 0) {
        this.question.a = this.option.correct_option
        this.question.b = this.option.disturbance_option1
        this.question.c = this.option.disturbance_option2
        this.question.d = this.option.disturbance_option3
      } else if (this.index === 1) {
        this.question.a = this.option.disturbance_option1
        this.question.b = this.option.correct_option
        this.question.c = this.option.disturbance_option2
        this.question.d = this.option.disturbance_option3
      } else if (this.index === 2) {
        this.question.a = this.option.disturbance_option1
        this.question.b = this.option.disturbance_option2
        this.question.c = this.option.correct_option
        this.question.d = this.option.disturbance_option3
      } else if (this.index === 3) {
        this.question.a = this.option.disturbance_option1
        this.question.b = this.option.disturbance_option2
        this.question.c = this.option.disturbance_option3
        this.question.d = this.option.correct_option
      }
    }
  },
  watch: {
    option: function (val) {
      this.question.title = val.question
      this.index = Math.floor(Math.random() * 4)
      if (this.index === 0) {
        this.question.a = val.correct_option
        this.question.b = val.disturbance_option1
        this.question.c = val.disturbance_option2
        this.question.d = val.disturbance_option3
      } else if (this.index === 1) {
        this.question.a = val.disturbance_option1
        this.question.b = val.correct_option
        this.question.c = val.disturbance_option2
        this.question.d = val.disturbance_option3
      } else if (this.index === 2) {
        this.question.a = val.disturbance_option1
        this.question.b = val.disturbance_option2
        this.question.c = val.correct_option
        this.question.d = val.disturbance_option3
      } else if (this.index === 3) {
        this.question.a = val.disturbance_option1
        this.question.b = val.disturbance_option2
        this.question.c = val.disturbance_option3
        this.question.d = val.correct_option
      }
    }
  }
}
</script>

<style scoped>
.title-font {
  font-family: "Microsoft YaHei";
  font-size: 15px;
  font-weight: normal;
}

.en-zn {
  width: 380px;
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
