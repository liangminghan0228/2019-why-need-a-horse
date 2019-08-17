<template>
  <div class="span-container">
    <span class="word-span">{{explain}}</span>
  </div>
</template>

<script>
export default {
  data: function () {
    return {}
  },
  props: ['explain']
}
</script>

<style scoped>
.span-container {
  font-size: 14px;
  margin-bottom: 30px;
}

.word-span {
  display: block;
  height: 18px;
  margin-bottom: 5px;
  color: #787878;
}
</style>
