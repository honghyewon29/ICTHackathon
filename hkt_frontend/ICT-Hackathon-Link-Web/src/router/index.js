import { createRouter, createWebHistory } from 'vue-router';
import Main from '@/components/Main.vue';


const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main,
  },
  // {
  //   path: '/login',
  //   name: 'LoginPage',
  //   component: () => import('@/components/LoginPage.vue'),
  // },
  // {
  //   path: '/signup',
  //   name: 'signup',
  //   component: () => import('@/components/SignupPage.vue'),
  // },
  {
    path: '/intro',
    name: 'introCollege',
    component: () => import('@/components/IntroCollege.vue'),
  },
  {
    path: '/announcement',
    name: 'announcePage',
    component: () => import('@/components/AnnouncePage.vue'),
  },
  {
    path: '/announcement-Write',
    name: 'announcementWrite',
    component: () => import('@/components/AnnouncementWrite.vue'),
  },
  {
    path: '/announce_detail',
    name: 'announceDetail',
    component: () => import('@/components/Announce_detail.vue'),
  },
  {
    path: '/club',
    name: 'ClubPage',
    component: () => import('@/components/Information/ClubPage.vue'),
  },
  {
    path: '/lostArticle',
    name: 'lostArticle',
    component: () => import('@/components/Information/LostArticle.vue'),
  },
  {
    path: '/lostArticle',
    name: 'lostArticleDetail',
    component: () => import('@/components/Information/LostArticleDetail.vue'),
  },
  {
    path: '/lostArticle',
    name: 'lostArticleWrite',
    component: () => import('@/components/Information/LostArticleWrite.vue'),
  },
  {
    path: '/schedule',
    name: 'schedulePage',
    component: () => import('@/components/Information/SchedulePage.vue'),
  },
  {
    path: '/computer', //컴퓨터학부
    name: 'computerPage',
    component: () => import('@/components/IntroDepartments/ComputerPage.vue'),
  },
  {
    path: '/dataScience', //데이터과학부
    name: 'dataScience',
    component: () => import('@/components/IntroDepartments/DataScience.vue'),
  },
  {
    path: '/infoCommunication', //정보통신학부
    name: 'infoCommunication',
    component: () =>
      import('@/components/IntroDepartments/InfoCommunication.vue'),
  },
  {
    path: '/mediaSW', //미디어SW
    name: 'mediaSW',
    component: () =>
      import('@/components/IntroDepartments/Computer/MediaSW.vue'),
  },

  {
    path: '/mediaSW-Sub',
    name: 'mediaSWSub',
    component: () =>
      import('@/components/IntroDepartments/Computer/MediaSWSub.vue')
  },

  {
     path: '/computerSW', //컴퓨터SW
    name: 'computerSW',
    component: () =>
      import('@/components/IntroDepartments/Computer/ComputerSW.vue'),
  },
  {
    path: '/computerSW-Sub',
    name: 'computerSWSub',
    component: () =>
      import('@/components/IntroDepartments/Computer/ComputerSWSub'),
  },
  {
    path: '/infoCommunicationCollege', //정보통신학과
    name: 'infoCommunicationCollege',
    component: () =>import('@/components/IntroDepartments/InfoCommunication/InfoCommunicationCollege.vue'),
  },
  {
    path: '/infoCommunicationCollegesub', 
    name: 'infoCommunicationCollegeSub',
    component: () =>import('@/components/IntroDepartments/InfoCommunication/InfoCommunicationCollegeSub.vue'),
  },
  {
    path: '/InfoSecurity',
    name: 'infoSecurity',
    component: () => import('@/components/IntroDepartments/InfoCommunication/InfoSecurity.vue')
  },

 {
    path: '/InfoSecurity/sub',
    name: 'infoSecuritySub',
    component: () => import('@/components/IntroDepartments/InfoCommunication/InfoSecuritySub.vue')
  }, 
  {
    path: '/cloud', //클라우드융복합
    name: 'CloudPage',
    component: () =>import('@/components/IntroDepartments/Cloud/CloudPage.vue'),
  },
  {
    path: '/cloud-sub', //클라우드융복합
    name: 'CloudSub',
    component: () =>import('@/components/IntroDepartments/Cloud/CloudSub.vue'),
  },
  {
    path: '/privacyPolicy',
    name: 'PrivacyPolicy',
    component: () => import('@/components/PrivacyPolicy.vue'),
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
  if (savedPosition) {
    return savedPosition; // 브라우저 '뒤로가기' 시 위치 복원
  } else {
    return { top: 0 }; // 새 페이지 진입 시 스크롤 맨 위로
  }
}
});

export default router;
