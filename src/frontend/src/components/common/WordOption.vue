<template>
  <div class="option-container">
    <el-button type="primary" class="word-option-index-btn">{{index}}</el-button>
    <input type="button" class="choose-button" @click="chooseOption" :value="option" />
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      selected: 0
    }
  },
  props: ['index', 'option'],
  methods: {
    chooseOption (event) {
      this.selected = event.target.value
      event.target.className += ' choosed-button'
      this.$emit('selectOption', this.selected)
    }
  }
}
</script>

<style scoped>
.option-container {
  margin-bottom: 20px;
}

.word-option-index-btn {
  border-radius: 15px;
  text-align: center;
  width: 50px;
  height: 50px;
  margin-right: 20px;
  background-color: #1E90FF;
}

.option-container /deep/ .choosed-button {
  background-color: #1E90FF;
  color: #FFF;
}

.choose-button {
  width: 84%;
  height: 50px;
  line-height: 5px;
  text-align: center;
  background-color: white;
  border: 1px solid #dcdfe6;
  font-weight: 500;
  font-size: 14px;
  outline: 0;
  color: #606266;
  border-radius: 50px;
}
</style>
