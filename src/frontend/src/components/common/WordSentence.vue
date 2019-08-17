<template>
  <div class="sentence-container">
    <div class="pron-div">
      <img src="../../images/42_voice2.png" class="pron-img">
      <span class="pron-span-en">{{sentence.example_sentence_en}}</span>
      <span class="pron-span-zh">{{sentence.example_sentence_ch}}</span>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {}
  },
  props: ['sentence']
}
</script>

<style scoped>
.sentence-container {
  background-color: #F0F0F0;
  border-radius: 10px;
}

.pron-div {
  position: relative;
  color: #606266;
  height: 70px;
  width: 100%;
  margin-bottom: 5px;
}

.pron-img {
  position: absolute;
  margin-left: 20px;
  top: 15px;
}

.pron-span-en {
  position: absolute;
  top: 11px;
  left: 65px;
}

.pron-span-zh {
  position: absolute;
  top: 38px;
  left: 65px;
}
</style>
