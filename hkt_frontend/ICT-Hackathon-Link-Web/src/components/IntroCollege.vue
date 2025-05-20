<template>
  <div class="main-container">
    <!-- ✅ 헤더 -->
    <header
      class="header"
      @mouseleave="hideAllDropdowns"
      @mouseenter="navHovered = true"
    >
      <img
        src="https://www.suwon.ac.kr/usr/images/suwon/logo.png"
        class="logo"
        @click="navigateTo('Main')"
        style="padding: 1.3rem 2rem"
      />

       <div class="menu">
        <nav>
          <!-- 대학 안내 -->
          <div class="center-menu">
            <a class="intro" @click="navigateTo('introCollege')" style="cursor: pointer">대학 안내</a>
            <div class="divider"></div>
            <div class="department-wrapper" @mouseenter="activeDropdown = 'department'">
              <a class="department" style="cursor: default">학과 안내</a>
              <div
                class="dropdown"
                v-show="activeDropdown === 'department'"
                @mouseenter="navHovered = true"
                @mouseleave="hideAllDropdowns"
              >
                <div
                  class="department-block"
                  v-for="(dept, index) in departments"
                  :key="index"
                >
                  <h4 @click="navigateToMajor(dept.name)" style="cursor: pointer">
                    {{ dept.name }}
                  </h4>
                  <ul v-if="dept.majors.length">
                    <li
                      v-for="(major, idx) in dept.majors"
                      :key="idx"
                      @click="navigateToMajor(major)"
                      style="cursor: pointer"
                    >
                      {{ major }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="divider"></div>
            <div class="department-wrapper" @mouseenter="activeDropdown = 'info'">
              <a class="information" style="cursor: default">정보 광장</a>
              <div
                class="dropdown dropdown-info"
                v-show="activeDropdown === 'info'"
                @mouseenter="navHovered = true"
                @mouseleave="hideAllDropdowns"
              >
                <div class="department-block">
                  <ul>
                    <li @click="navigateTo('schedulePage')">학사일정</li>
                    <li @click="navigateTo('ClubPage')">동아리</li>
                    <li @click="navigateTo('lostArticle')">분실물</li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="divider"></div>
            <a class="announcememt" @click="navigateTo('announcePage')" style="cursor: pointer">공지</a>
          </div>
        </nav>
      </div>
      
    </header>
    <section class="title-section">
        <div class="wrap_sub_visual">
          <div class="container center-only">
            <p class="visual_intro"><strong>지능형SW융합대학</strong></p>
            <p class="subtitle a">COLLEGE OF INTELLIGENT SOFTWARE CONVERGENCE</p>
            <p class="subtitle b">제4차 산업혁명, 수원대학교 지능형SW융합대학이 주도합니다.</p>
          </div>
        </div>
    </section>

    <section class="main-section">
      <div class="intro">
        <h2>지능형SW융합대학 소개</h2>
        <p class="intro-text">
          ICT 융합대학은 4차 산업혁명 시대, 사물인터넷 시대를 선도할 정보보안, 사물인터넷, 빅데이터, 스마트 제조 등 ICT 분야의 하드웨어 및 소프트웨어, ICT 융합 분야의 전문가가 될 수 있도록 관련 이론과 현장에서 요구하는 기술, 협업 능력을 첨단 실습 기자재를 통해 배양함과 동시에 ICT 관련 분야를 주도할 글로벌 ICT 인재 양성을 목표로 하고 있다. 이를 위해 HW·SW융합 STEAM 교육, 코딩, 3D모델링, 컴퓨터가공, 빅데이터/머신러닝 등의 실습 환경을 제공하고 Digital Fabrication Center(DFC), 3D Printer Center, Smart Factory Center, VR/AR Center 등을 통한 최첨단 교육/실습 환경을 제공하고 있다. ICT 융합대학은 단순 ICT 융합 교육이 아닌 학생 개개인의 성취 능력 향상과 실무 교육을 바탕으로 언제 어디서나 실무에 참여하여 핵심 인재로서 발돋움할 수 있는 교육에 중점을 두고 있다.
        </p>
      </div>
      <div class="stats">
        <div class="stat">
          <div class="stat-value">31</div>
          <div class="stat-label">교수진 수(전임 포함)</div>
        </div>
        <div class="stat">
          <div class="stat-value">1,539</div>
          <div class="stat-label">학생 수</div>
          <div class="stat-label">(2020.07 재학생 및 휴학생)</div>
        </div>
      </div>
      <section>
        <h2 class="section-title">학장 소개</h2>
        <div class="profile">
          <div>
            <p><strong>성명:</strong> 김대엽</p>
            <p><strong>위치:</strong> 지능형SW융합대학 525호실</p>
          </div>
          <div>
            <p><strong>소속:</strong> 정보통신학부 정보보호</p>
            <p><strong>연락처:</strong> 031-229-8352</p>
            <p><strong>Email:</strong> daeyoub69@suwon.ac.kr</p>
          </div>
        </div>
      </section>
      <div class="informbox">   
        <div class="majors">
          <div class="major">
            <a  @click="navigateTo('infoCommunication')" style="cursor: pointer">정보통신학부</a>
            <a  @click="navigateTo('infoCommunicationCollege')" style="cursor: pointer">정보통신학과</a>
            <a  @click="navigateTo('infoSecurity')" style="cursor: pointer">정보보호학과</a>
          </div>
          <div class="major">
            <a  @click="navigateTo('computerPage')" style="cursor: pointer">컴퓨터학부</a>
            <a  @click="navigateTo('computerSW')" style="cursor: pointer">컴퓨터SW</a>
            <a  @click="navigateTo('mediaSW')" style="cursor: pointer">미디어SW</a>
          </div>
          <div class="major">
            <a  @click="navigateTo('dataScience')" style="cursor: pointer">데이터과학부</a>
          </div>
          <div class="major a">
            <a  @click="navigateTo('CloudPage')" style="cursor: pointer">클라우드융복합전공</a>
          </div>   
        </div>
      </div>
    </section>

    <img class="chatbot-icon"  src="@/assets/chatbot-icon.png" alt="chatbot" @click="showChat = !showChat"/>

    <ChatBot v-if="showChat" @close="showChat = false" />
    <footer>
      <div class="container">
        <div class="wrap">
          <div class="foot_info">
            <div class="fnb">
              <ul class="inGuideFnb">
                <li>
                  <a @click="showPrivacy = true" style="cursor: pointer">개인정보처리방침</a>
                </li>
              </ul>
            </div>
            <address>
              18323 경기도 화성시 봉담읍 와우안길 17
              <span>Tel : 031-220-2114</span>
            </address>
            <p>
              <span>Copyright (C) THE UNIVERSITY OF SUWON.</span>
              All rights reserved.
            </p>
          </div>
          <div class="foot_sns">
            <ul>
              <li class="n_blog">
                <a title="수원대학교 블로그" href="https://blog.naver.com/usw1982" target="_blank">
                  <img src="@/assets/blog.png" />
                </a>
              </li>
              <li class="facebook">
                <a title="수원대학교 페이스북" href="https://www.facebook.com/SuwonUniv/" target="_blank">
                  <img src="@/assets/facebook.png" />
                </a>
              </li>
              <li class="instagram">
                <a title="수원대학교 인스타그램" href="https://www.instagram.com/usw1982/" target="_blank">
                  <img src="@/assets/insta.png" />
                </a>
              </li>
              <li class="youtube">
                <a title="수원대학교 유튜브" href="https://www.youtube.com/channel/UC4JfyRGKu5AfBjvaFMCj3cg" target="_blank">
                  <img src="@/assets/youtube.png" />
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
  </footer>
  <PrivacyPolicy v-if="showPrivacy" @close="showPrivacy = false" />
  </div>
</template>

<script>
import ChatBot from '@/components/ChatBot.vue'
import PrivacyPolicy from '@/components/PrivacyPolicy.vue'
export default {
  name: 'introCollege',
  components: {
    ChatBot,
    PrivacyPolicy
  },
   data() {
    return {
      isLoggedIn: false,
      showPrivacy: false,
      showChat: false,
      activeDropdown: null,
      navHovered: false,
      departments: [
        { name: '컴퓨터학부', majors: ['컴퓨터SW', '미디어SW'] },
        { name: '정보통신학부', majors: ['정보통신학과', '정보보호학과'] },
        { name: '데이터과학부', majors: [] },
        { name: '클라우드융복합', majors: [] },
      ],
    };
  },
  methods: {
    
    
    navigateTo(routeName) {
      this.$router.push({ name: routeName }).catch((err) => {
        if (err.name !== 'NavigationDuplicated') {
          //동일한 경로일x 때, 오류 무시하기
          throw err;
        }
      });
    },
    navigateToMajor(majorName) {
      const routeMap = {
        컴퓨터학부: "computerPage",
        컴퓨터SW: "computerSW",
        미디어SW: "mediaSW",
        정보통신학부: "infoCommunication",
        정보통신학과: "infoCommunicationCollege",
        정보보호학과: "infoSecurity",
        데이터과학부: "dataScience",
        클라우드융복합: "CloudPage",

      };
      const route = routeMap[majorName];
      if (route) {
        this.navigateTo(route);
      } else {
        console.warn(`No route found for major: ${majorName}`);
      }
    },

    hideAllDropdowns() {
      this.activeDropdown = null;
      this.navHovered = false;
    },
  },
};
</script>

<style scoped>
* {
  font-family: 'Nanum Gothic', sans-serif;
}
.menu{
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
}
.main-container {
  background-color: white;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  min-height: 0;
  height: auto;
  overflow-x: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1b1d53;
  color: white;
  height: 85px;
  position: relative;
}

.logo {
  height: 40px;
  margin-right: 2rem;
  cursor: pointer;
}

nav {
  /* position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  justify-content: center; */
  display: flex;
  justify-content: center;
  margin: 0 auto;
}

.center-menu {
  display: flex;
  gap: 50px;
}

.center-menu a {
  color: white;
  padding: 0 10px;
  position: relative;
  text-decoration: none;
}

.right-menu {
  display: flex;
  text-decoration: none;
  align-items: center;
  gap: 10px;
  color: white;
  margin-left: auto;
  margin-right: 2rem;
}

.intro:hover .announcement:hover {
  cursor: pointer;
}

.announcement {
  margin-right: 5rem;
}
.divider {
  height: 20px;
  width: 1px;
  background-color: white;
  opacity: 0.6;
}

.dropdown {
  position: absolute;
  justify-content: center;
  left: 0;
  /* transform: translateX(-50%); */
  top: 100%;
  width: 100vw;
  background-color: #2c2d4fee;
  display: flex;
  gap: 3rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  color: white;
  
  border-radius: 4px;
  z-index: 1000;
  height: 120px;
  
}

.dropdown-info {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 3rem;
  width: 100vw;
  height: 120px;
}

.dropdown-info .department-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.department {
  position: relative;
  color: white;
  text-decoration: none;
}

.department-block {
  min-width: 150px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* padding-left: 90px; */
}

.department-block h4 {
  margin-bottom: 0.5rem;
  border-bottom: 1px solid #666;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  white-space: nowrap;
}

.department-block ul {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
}

.department-block li {
  margin-bottom: 0.3rem;
  cursor: pointer;
  font-size: 0.9rem;
  color: #ddd;
  white-space: nowrap;
}

.department-block li:hover {
  text-decoration: underline;
  color: #fff;
}





nav a {
  margin: 0 10px;
  color: white;
  text-decoration: none;
}





/* 서브 비주얼 */
.wrap_sub_visual {
  background-image: url('@/assets/background1.png');
  background-size: cover;
  background-position: center;
  height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.wrap_sub_visual .container.center-only {
  justify-content: center;
}

.visual_intro {
  font-size: 2.2rem;
  font-weight: bold;
  text-align: center;
  flex: 1;
  color: white;
}
.subtitle.a{
  font-size: 1rem;
  font-weight: bold;
  text-align: center;
  flex: 1;
  color: white;
}

.subtitle.b{
  font-size: 0.8rem;
  font-weight: bold;
  text-align: center;
  flex: 1;
  color: white;
}

.content {
  color: white;
}

.main-section {
  min-height: 100vh;
  
  padding: 2rem 2rem;
  z-index: 1;
  position: relative;
  
}

.intro h2 {
  font-size: 1.5rem;
  margin-left: 1rem ;
  margin-bottom: 2rem;
  font-weight: bold;
  color: rgb(0, 0, 0);
}

.intro-text {
  font-size: 20px;
  font-weight: bold;
  color: rgb(0, 0, 0);
  padding: 1rem;
  font-weight: 500;
  line-height: 2rem;
}

.profile {
  display: flex;
  justify-content: space-between;
  background-color: #f9f9f9;
  padding: 1rem;
  margin: 1rem 0;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1.1rem;
}

.profile div {
  width: 48%;
}

.stats {
  display: flex;
  justify-content: center;
  gap: 5rem;
  margin-top: 4rem;
}

.stat {
  text-align: center;
  padding: 1rem 2rem;
}

.stat-value {
  font-size: 3rem;
  font-weight: bold;
  color: rgb(0, 0, 0);
}

.stat-label {
  font-size: 0.9rem;
  margin-top: 0.5rem;
  color: rgb(0, 0, 0);
}
/* ✅ 공통 컨테이너 */
.informbox {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 auto;
  max-width: 100%;
}

/* ✅ 학장 소개 박스 */
.info-box {
  background-color: rgba(0, 0, 0, 0.6); 
  padding: 1.5rem;
  margin-bottom: 2rem;
  color: white;
  font-weight: bold; /* 매우 중요한 코드 */
  font-size: 1.1rem;
  border-radius: 10px;
  width: 82%;
  margin: 3rem;
}
.chair-card {
  border: 2px solid #ddd;
  padding: 1rem 1.5rem;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  row-gap: 0.8rem;
  column-gap: 1.5rem;
  border-radius: 10px;
}

.chair-item {
  display: flex;
  align-items: center;
  font-size: 1rem;
}

/* ✅ 전공 전체 묶음 */
.majors {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 3.5rem;
  width: 100%;
  margin-top: 3rem;
}

/* ✅ 각 전공 박스 */
.major {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgb(4, 13, 62);
  padding: 2rem 1rem;
  border-radius: 10px;
  width: 20%;
  height: 240px;
  box-sizing: border-box;
}

.major.a {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgb(4, 13, 62);
  padding: 2rem 1rem;
  border-radius: 10px;
  width: 300px;
  height: 240px;
  box-sizing: border-box;
}

.major a:first-child {
  font-size: 30px; /* 학부 */
  color: white;
  font-weight: bold;
  margin-bottom: 1rem;
  text-decoration: none;
  
}

.major a:not(:first-child) {
  font-size: 20px; /* 학과 */
  color: white;
  margin-bottom: 0.5rem;
  text-decoration: none;
}

.major-a {
  font-size: 30px;
  color: white;
  font-weight: bold;
  text-align: center;
}

.dy-title{
  color: white;
  font-size: 35px;
}

.inform {
  color: white;
  font-size: 30px;
}



/*하단창*/
footer {
  background-color: #343539;
  color: #ccc;
  padding: 1rem 0.5rem;
  font-size: 0.9rem;
  line-height: 1.6
}

footer .container {
  max-width: 100%;
  margin: 0 auto;
}

footer .wrap {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  align-items: center;
  gap: 2rem;
}

footer .foot_info address {
  font-style: normal;
  color: #ccc;
}

footer .foot_info span {
  margin-left: 0.5rem;
}

footer .foot_info p {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #999;
}



footer .foot_sns ul {
  list-style: none;
  padding: 0.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 100px;
}

footer .foot_sns li a {
  color: #ccc;
  text-decoration: none;
  font-size: 0.85rem;
}

footer .foot_sns li a:hover {
  text-decoration: underline;
}
footer .inGuideFnb{
  margin-bottom: 40px;
  color: white;
}
</style>
