import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  BASEURL: 'http://backend.docker.io/',
  userID: '',
  WORD_NOW: {},
  WORDS: [],
  STUDENTID: '',
  TEACHERID: '',
  WORD_COUNT: 7,
  RECALL_COUNT: 0,
  COUNTDOWN: '00:00',
  STUDY_STATUS: false,
  CATEGORY: {'id': 0, 'name': ''},
  TOMATO_COUNT: 0,
  STUDYMINUTE: 24,
  STUDYSECOND: 50,
  WORD_LEVEL: -1,
  IS_KNOW: false,
  IS_RECALL: false,
  ISFOUR: false,
  TOMATO_WORDS: [],
  COMPETITIONID: 0
}

export default new Vuex.Store({
  state
})
