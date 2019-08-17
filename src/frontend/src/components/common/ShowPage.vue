<template>
  <div class="pager">
    <a href="javascript:void(0);" @click="firstPage">首页</a>
    <a href="javascript:void(0);" @click="prevPage">上一页</a>
    <span>{{curPage}}/{{total}}</span>
    <a href="javascript:void(0);" @click="nextPage">下一页</a>
    <a href="javascript:void(0);" @click="lastPage">尾页</a>
  </div>
</template>

<script>
export default {
  mounted () {
    this.$nextTick(() => {
      this.initPager()
    })
  },
  name: 'showpage',
  data () {},
  methods: {
    nextPage () {
      this.$emit('setPage', this.curPage + 1)
    },
    prevPage () {
      this.$emit('setPage', this.curPage - 1)
    },
    firstPage () {
      this.$emit('setPage', 1)
    },
    lastPage () {
      this.$emit('setPage', this.total)
    }
  },
  props: ['curPage', 'total']
}
</script>

<style scoped>
.pager > span,
.pager > a,
.pager > div {
  float: left;
  margin-left: 10px;
  font-size: 14px;
  color: rgb(53, 138, 97);
}

.pager {
  width: 600px;
  margin: 0 auto;
  height: 48px;
  line-height: 48px;
  margin-bottom: 40px;
}

.pager a {
  font-weight: bold;
  text-decoration: none;
}

.pager a:hover {
  color: #000;
}
</style>