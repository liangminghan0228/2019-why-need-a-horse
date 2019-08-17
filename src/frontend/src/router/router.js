import Login from '../components/Login'
import BeforeStudying from '../components/BeforeStudying'
import BeforeTestPage from '../components/BeforeTestPage'
import Calendar from '../components/Calendar.vue'
import CompetitionDetails from '../components/CompetitionDetails'
import CompetitionListPage from '../components/CompetitionListPage'
import CreateCompetition from '../components/CreateCompetition'
import LeaderBoard from '../components/LeaderBoard'
import NewClass from '../components/NewClass'
import NewStudent from '../components/NewStudent'
import PkCompetition from '../components/PkCompetition'
import QueryCourse from '../components/QueryCourse'
import RegisterCourse from '../components/RegisterCourse'
import SearchContest from '../components/SearchContest'
import SpellingCard from '../components/SpellingCard'
import StudyCardOne from '../components/StudyCardOne'
import StudyCardTwo from '../components/StudyCardTwo'
import StudyCardThree from '../components/StudyCardThree'
import StudyCardFour from '../components/StudyCardFour'
import StudyStatistic from '../components/StudyStatistic'
import TeacherClasses from '../components/TeacherClasses'
import TeacherStudents from '../components/TeacherStudents'
import TeacherStudyStatistic from '../components/TeacherStudyStatistic'
import Test from '../components/Test'
import TestResult from '../components/TestResult'
import UnlimitedChallenge from '../components/UnlimitedChallenge'
import WordList from '../components/WordList'
import ChangePassword from '../components/common/ChangePassword.vue'
import TomatoCard from '../components/TomatoCard'

const routers = [
  {
    path: '/',
    name: 'login',
    component: Login,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/beforestudying',
    name: 'beforestudying',
    component: BeforeStudying,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/beforetestpage',
    name: 'beforetestpage',
    component: BeforeTestPage,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/calendar',
    name: 'calendar',
    component: Calendar,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/competitiondetails',
    name: 'competitiondetails',
    component: CompetitionDetails,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/competitionlistpage',
    name: 'competitionlistpage',
    component: CompetitionListPage,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/createcompetition',
    name: 'createcompetition',
    component: CreateCompetition,
    meta: {
      needLogin: true
    }
  },
  {
    path: '/leaderboard',
    name: 'leaderboard',
    component: LeaderBoard,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/newclass',
    name: 'newclass',
    component: NewClass,
    meta: {
      needLogin: true
    }
  },
  {
    path: '/newstudent',
    name: 'newstudent',
    component: NewStudent,
    meta: {
      needLogin: true
    }
  },
  {
    path: '/pkcompetition',
    name: 'pkcompetition',
    component: PkCompetition,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/querycourse',
    name: 'querycourse',
    component: QueryCourse,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/registercourse',
    name: 'registercourse',
    component: RegisterCourse,
    meta: {
      needLogin: true
    }
  },
  {
    path: '/searchcontest',
    name: 'searchcontest',
    component: SearchContest,
    meta: {
      needLogin: true
    }
  },
  {
    path: '/spellingcard',
    name: 'spellingcard',
    component: SpellingCard,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/studycardone',
    name: 'studycardone',
    component: StudyCardOne,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/studycardtwo',
    name: 'studycardtwo',
    component: StudyCardTwo,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/studycardthree',
    name: 'studycardthree',
    component: StudyCardThree,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/studycardfour',
    name: 'studycardfour',
    component: StudyCardFour,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/studystatistic',
    name: 'studystatistic',
    component: StudyStatistic,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/teacherclasses',
    name: 'teacherclasses',
    component: TeacherClasses,
    meta: {
      needLogin: true
    }
  },
  {
    path: '/teacherstudents',
    name: 'teacherstudents',
    component: TeacherStudents,
    meta: {
      needLogin: true
    }
  },
  {
    path: '/teacherstudystatistic',
    name: 'teacherstudystatistic',
    component: TeacherStudyStatistic,
    meta: {
      needLogin: true
    }
  },
  {
    path: '/test/:type',
    name: 'test',
    component: Test,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/testresult',
    name: 'testresult',
    component: TestResult,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/unlimitedchallenge',
    name: 'unlimitedchallenge',
    component: UnlimitedChallenge,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/wordlist',
    name: 'wordlist',
    component: WordList,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/changepassword',
    name: 'changepassword',
    component: ChangePassword,
    meta: {
      needLogin: true
    }
  },
  {
    path: '/tomatocard',
    name: 'tomatocard',
    component: TomatoCard,
    meta: {
      requireAuth: true
    }
  }
]

export default routers
