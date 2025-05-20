<template>
  <div class="main-container">
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
            <p class="visual_intro"><strong>클라우드융복합전공</strong></p>
            <p class="subtitle a">CloudConvergence</p>
            
          </div>
        </div>
    </section>
    <div class="sub-nav">
  <button
    :class="[$route.name === 'CloudPage' ? 'yellow-button' : 'blue-button']"
    @click="navigateTo('CloudPage')"
  >
    학과소개
  </button>
  <button
    :class="[$route.name === 'CloudSub' ? 'yellow-button' : 'blue-button']"
    @click="navigateTo('CloudSub')"
  >
    교과과정
  </button>
</div>


    <div class="info-box">
  <h2>교과과정</h2>
  <table class="course-table">
  <thead>
    <tr>
      <th>학년</th>
      <th>학기</th>
      <th>학수번호</th>
      <th>이수구분</th>
      <th>교과목명</th>
      <th>학점</th>
      <th>이론</th>
      <th>실습</th>
      <th>과목구분</th>
    </tr>
  </thead>
  <tbody>
    <tr>
  <td rowspan="5">2</td>
  <td>1</td><td>11479</td><td>전핵</td><td>클라우드 컴퓨팅 개론 (Introduction to Cloud Computing)</td><td>3</td><td>3</td><td>0</td><td>이론</td>
  </tr>
  <tr><td>1</td><td>11481</td><td>전핵</td><td>파이썬 프로그래밍 (Python Programming)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
  <tr><td>2</td><td>11480</td><td>전핵</td><td>클라우드 핵심 서비스 (Core Cloud Services)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
  <tr><td>2</td><td>11483</td><td>전핵</td><td>스토리지 구조 (Storage Architecture)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
  <tr><td>2</td><td>11484</td><td>전핵</td><td>No-SQL 구조 (No-SQL Architecture)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
  <tr>
  <td rowspan="5">3</td>
  <td>1</td><td>11482</td><td>전핵</td><td>클라우드 네트워크 (Cloud Network)</td><td>3</td><td>3</td><td>0</td><td>이론</td>
  </tr>
  <tr><td>1</td><td>11486</td><td>전핵</td><td>클라우드 아키텍트 구조 (Cloud Architect Architecture)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
  <tr><td>2</td><td>11485</td><td>전핵</td><td>ICT와 클라우드 컴퓨팅 (ICT and Cloud Computing)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
  <tr><td>2</td><td>11487</td><td>전핵</td><td>클라우드 인프라 운영 (Cloud Infrastructure Operation)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
  <tr><td>2</td><td>11488</td><td>전핵</td><td>클라우드 기반 개발 (Cloud-based Development)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
  <tr>
  <td rowspan="3">4</td>
  <td>1</td><td>11490</td><td>전핵</td><td>클라우드 기반 데이터레이크 및 분석 (Cloud-based Data Lake & Analytics)</td><td>3</td><td>3</td><td>0</td><td>이론</td>
  </tr>
  <tr><td>1</td><td>11491</td><td>전핵</td><td>클라우드 기반 DevOps 자동화 (Cloud-based DevOps Automation)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
  <tr><td>1</td><td>11489</td><td>전핵</td><td>클라우드 인프라 보안 (Cloud Infrastructure Security)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
  </tbody>
</table>
</div>

    
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
  name: 'CloudSub',
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
      this.isIntro = routeName === 'infoSecurityIntro';
      this.$router.push({ name: routeName }).catch((err) => {
        if (err.name !== "NavigationDuplicated") throw err;
      });
    },
    navigateToMajor(majorName) {
      const routeMap = {
        컴퓨터학부: "computer",
        컴퓨터SW: "computerSW",
        미디어SW: "mediaSW",
        정보통신학부: "infoCommunication",
        정보통신학과: "infoCommunicationCollege",
        정보보호학과: "infoSecurity",
        데이터과학부: "dataScience",
        클라우드융복합: "CloudPage",
      };
      const route = routeMap[majorName];
      if (route) this.navigateTo(route);
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
  font-weight: 3px bold;
  text-align: center;
  flex: 1;
  color: white;
}

.subtitle.a {
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  flex: 1;
  color: white;
}
.main-container {
  background-color: white;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  /* 이 두 줄이 핵심 */
  height: auto;         /* 자동으로 콘텐츠에 맞춤 */
  min-height: 0;        /* 필요시 강제 최소 높이 제거 */
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
.chatbot-icon {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 10%; /* ✅ 기존보다 가로폭 확대 */
  height: auto; /* ✅ 높이 자동으로 비율 유지 */
  object-fit: contain; /* ✅ 이미지 전체가 보이도록 조정 */
  z-index: 10; 
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



.menu{
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
}
nav a {
  margin: 0 10px;
  color: white;
  text-decoration: none;
}




.sub-nav {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin: 2rem auto;
}

.sub-nav button {
  padding: 0.7rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.yellow-button {
  background-color: #e6c445; /* 노란색 */
  color: black;
}

.blue-button {
  background-color: #1b1d53; /* 파란색 */
  color: white;
}
/* 선택된 버튼 (노란색) */
.active-button {
  background-color: #e6c445;
  color: white;
}

/* 선택 안 된 버튼 (파란색) */
.inactive-button {
  background-color: #1b1d53;
  color: white;
}
.sub-nav button.active {
  background-color: #e6c445;
  color: black;
}

.info-section {
  padding: 2rem;
  max-width: 1300px;
  margin: 0 auto;
}

.info-box {
  padding: 1.5rem;
  margin-bottom: 2rem;
  color: rgb(0, 0, 0);
  font-weight: bold;
  font-size: 1.1rem;
}

.info-box h2 {
  font-size: 1.6rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.5rem;
}

.info-box p {
  line-height: 1.8;
  margin-bottom: 0.8rem;
}

.course-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background-color: white;
  color: black;
}

.course-table th,
.course-table td {
  border: 1px solid #ccc;
  padding: 0.75rem;
  text-align: center;
  font-size: 0.95rem;
}

.course-table th {
  background-color: #e6e6e6;
  font-weight: bold;
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
