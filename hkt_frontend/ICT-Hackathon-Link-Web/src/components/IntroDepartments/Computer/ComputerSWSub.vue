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
            <p class="visual_intro"><strong>컴퓨터SW학과</strong></p>
            <p class="subtitle a">ComputerSoftware</p>
            
          </div>
        </div>
    </section>
    <div class="sub-nav">
  <button
    :class="[$route.name === 'computerSW' ? 'yellow-button' : 'blue-button']"
    @click="navigateTo('computerSW')"
  >
    학과소개
  </button>
  <button
    :class="[$route.name === 'computerSWSub' ? 'yellow-button' : 'blue-button']"
    @click="navigateTo('computerSWSub')"
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
  <td rowspan="10">2</td>
  <td>1</td><td>01765</td><td>전선</td><td>데이터통신 (Data Communication)</td><td>3</td><td>3</td><td>0</td><td>이론</td>
    </tr>
    <tr><td>1</td><td>02048</td><td>전선</td><td>디지털시스템응용및실험 (Digital System Application & Experiment)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>1</td><td>03498</td><td>전선</td><td>선형대수학 (Linear Algebra)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>06994</td><td>전선</td><td>프로그래밍언어및실습 (Programming Languaue and Practice)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>1</td><td>09040</td><td>전선</td><td>디지털영상처리 (Digital Image Processing)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>09657</td><td>전선</td><td>시스템프로그래밍 (System Programming)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>04152</td><td>전선</td><td>어셈블리어 (Assembly Language)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>03098</td><td>전선</td><td>비주얼언어및실습 (Visual Language and Practice)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>2</td><td>08683</td><td>전선</td><td>리눅스시스템 (Linux Systems)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>09372</td><td>전선</td><td>컴퓨터교과교재연구및지도법 (Advanced Introduction Method in Computer Education)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr>
  <td rowspan="16">3</td>
  <td>1</td><td>00191</td><td>전선</td><td>JAVA (JAVA)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td>
</tr>
    <tr><td>1</td><td>02176</td><td>전선</td><td>마이크로프로세서응용 (Microprocessor Applications)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>03650</td><td>전선</td><td>소프트웨어공학 (Software Engineering)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>06993</td><td>전선</td><td>프로그래밍언어론 (Programming Language)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>08870</td><td>전선</td><td>임베디드하드웨어설계 (Embedded Hardware Design)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>1</td><td>09371</td><td>전선</td><td>컴퓨터교육론 (Education Theory of Computer)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>10612</td><td>전선</td><td>임베디드소프트웨어실습 (Embedded Software Design and Experiment)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>2</td><td>04115</td><td>전선</td><td>알고리즘분석 (Analysis of Algorithms)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>01762</td><td>전선</td><td>데이터베이스 (Database)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>04963</td><td>전선</td><td>인터넷컴퓨팅 (Internet Computing)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>10615</td><td>전선</td><td>IOT 설계실습 (IOT Design and Experiment)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>2</td><td>10614</td><td>전선</td><td>창업실무 (Entrepreneurship and Practice)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>10613</td><td>전선</td><td>오토마타 (Automata)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>10576</td><td>전선</td><td>캡스톤디자인1 (Capstone Design 1)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>09373</td><td>전선</td><td>컴퓨터교과논리및논술 (Computer Logic and Writing Skill)</td><td>2</td><td>2</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>05778</td><td>전선</td><td>정보처리기술 (Information Processing)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr>
  <td rowspan="13">4</td>
  <td>1</td><td>10577</td><td>전선</td><td>캡스톤디자인2 (Capstone Design 2)</td><td>3</td><td>3</td><td>0</td><td>이론</td>
    </tr>
    <tr><td>1</td><td>10616</td><td>전선</td><td>캡스톤설계1 (Capstone Design 1)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>1</td><td>07922</td><td>전선</td><td>분산컴퓨팅 (Distributed Computing)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>06522</td><td>전선</td><td>컴파일러구성 (Compiler Construction)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>08872</td><td>전선</td><td>네트워크컴퓨팅 (Network Computing)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>09633</td><td>전선</td><td>졸업프로젝트 (Graduation Project)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>03855</td><td>전선</td><td>시스템분석및설계 (System Analysis and Design)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>04931</td><td>전선</td><td>인공지능 (Artificial Intelligence)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>06532</td><td>전선</td><td>컴퓨터과학특강 (Special Topics in Computer Science)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>08866</td><td>전선</td><td>자유전공 (Special Topics in Chemical and Biochemical Engineering)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>08877</td><td>전선</td><td>모바일소프트웨어설계 (Mobile Software Design)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>2</td><td>10617</td><td>전선</td><td>캡스톤설계2 (Capstone Design 2)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>2</td><td>10468</td><td>전선</td><td>빅데이터정보검색 (Information Retrieval)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
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
  name: 'InfoSecurityIntro',
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
  background: white;
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
