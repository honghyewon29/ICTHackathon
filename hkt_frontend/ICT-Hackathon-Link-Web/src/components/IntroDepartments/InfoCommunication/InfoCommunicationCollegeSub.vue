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
            <p class="visual_intro"><strong>정보통신학과</strong></p>
            <p class="subtitle a">InformationCommunication</p>
            
          </div>
        </div>
    </section>
    <div class="sub-nav">
    <button
      :class="[$route.name === 'infoCommunicationCollege' ? 'yellow-button' : 'blue-button']"
      @click="navigateTo('infoCommunicationCollege')"
    >
      학과소개
    </button>
    <button
      :class="[$route.name === 'infoCommunicationCollegeSub' ? 'yellow-button' : 'blue-button']"
      @click="navigateTo('infoCommunicationCollegeSub')"
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
      <td rowspan="15">2</td>
      <td>1</td><td>02053</td><td>전선</td><td>디지털논리설계 (Digital Logic Design)</td><td>3</td><td>3</td><td>0</td><td>이론</td>
    </tr>
    <tr><td>1</td><td>07697</td><td>전핵</td><td>회로이론 (Electric Circuit Theory)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>07892</td><td>전선</td><td>웹프로그래밍 (Web Programming)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>08366</td><td>전핵</td><td>신호및시스템 (Signals and Systems)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>08880</td><td>전선</td><td>기초전자회로실험 (Basic Circuit Experiment)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>1</td><td>10627</td><td>전선</td><td>임베디드시스템기초실습 (Introduction to Embedded Systems Design)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>1</td><td>10628</td><td>전선</td><td>공학수학1 (Engineering Mathematics 1)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>10629</td><td>전선</td><td>디지털논리설계실험 (Digital Logic Circuit Lab)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>2</td><td>10469</td><td>전선</td><td>전산해석컴퓨팅 (Computational Analysis of Computing)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>09655</td><td>전선</td><td>객체지향프로그래밍 (Object Oriented Programming)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>08894</td><td>전선</td><td>알고리즘 (Algorithm)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>07695</td><td>전선</td><td>회로및시스템 (Circuits and System)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>05630</td><td>전선</td><td>전자기학 (Electromagnetics)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>10630</td><td>전선</td><td>공학수학2 (Engineering Mathematics 2)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>02049</td><td>전선</td><td>디지털신호처리 (Digital Signal Processing)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr>
      <td rowspan="17">3</td>
    <td>1</td><td>09365</td><td>전선</td><td>공업교육론 (Industrial Education)</td><td>3</td><td>3</td><td>0</td><td>이론</td>
    </tr>
    <tr><td>1</td><td>08656</td><td>전선</td><td>전자회로1 (Electronic Circuits(1))</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>06754</td><td>전선</td><td>통신이론 (Communication Theory)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>06547</td><td>전선</td><td>컴퓨터네트워크 (Computer Network)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>03099</td><td>전선</td><td>비주얼프로그래밍 (Visual Programming)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>02240</td><td>전선</td><td>멀티미디어신호처리 (Multimedia Signal Processing)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>02168</td><td>전선</td><td>마이크로프로세서 (Microprocessor)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>10631</td><td>전선</td><td>전자통신실험 (Electronic Communication Lab)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>2</td><td>02059</td><td>전선</td><td>디지털통신 (Digital Communication)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>02239</td><td>전선</td><td>멀티미디어시스템 (Multimedia System)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>08150</td><td>전선</td><td>마이크로컴퓨터실험 (Microcomputer Lab.)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>2</td><td>08657</td><td>전선</td><td>전자회로2 (Electronic Circuits(2))</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>10632</td><td>전선</td><td>네트워크설계및실습 (Network Design and Practice)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>09657</td><td>전선</td><td>시스템프로그래밍 (System Programming)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>10576</td><td>전선</td><td>캡스톤디자인1 (Capstone Design 1)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>10584</td><td>전선</td><td>패턴인식 (Pattern Recognition)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>09366</td><td>전선</td><td>공업교과교재연구및지도법 (Study of Teaching Methods for Industrial Curriculum)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr>
      <td rowspan="13">4</td>
      <td>1</td><td>06219</td><td>전선</td><td>집적회로 (Integrated Circuits)</td><td>3</td><td>3</td><td>0</td><td>이론</td>
    </tr>
    <tr><td>1</td><td>08884</td><td>전선</td><td>창의적공학설계1 (Capstone Design 1)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>1</td><td>10634</td><td>전선</td><td>네트워크응용및프로그래밍 (Network Programming)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>10633</td><td>전선</td><td>로봇비젼 (Robot Vision)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>10616</td><td>전선</td><td>캡스톤설계1 (Capstone Design 1)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>1</td><td>10577</td><td>전선</td><td>캡스톤디자인2 (Capstone Design 2)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>1</td><td>08885</td><td>전선</td><td>임베디드시스템프로그래밍 (Embedded System Programming)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>10636</td><td>전선</td><td>지식재산의보호와관리 (Intellectual Property Protection)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>10635</td><td>전선</td><td>VLSI 설계 (VLSI Design)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
    <tr><td>2</td><td>10617</td><td>전선</td><td>캡스톤설계2 (Capstone Design 2)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>2</td><td>09367</td><td>전선</td><td>공업교과논리및논술 (Text Logics for Industrial Education and Essay)</td><td>2</td><td>2</td><td>--</td><td>--</td></tr>
    <tr><td>2</td><td>08886</td><td>전선</td><td>창의적공학설계2 (Capstone Design 2)</td><td>3</td><td>2</td><td>2</td><td>이론/실습</td></tr>
    <tr><td>2</td><td>10637</td><td>전선</td><td>정보통신특강 (Information Communication Prospect)</td><td>3</td><td>3</td><td>0</td><td>이론</td></tr>
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
                  <a  @click="showPrivacy = true" style="cursor: pointer" target="_blank">개인정보처리방침</a>
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
      this.$router.push({ name: routeName }).catch((err) => {
        if (err.name !== 'NavigationDuplicated') throw err;
      });
    },
    getButtonClass(targetRoute) {
        return this.$route.name === targetRoute ? 'active-button' : 'inactive-button';
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
  background-color: white;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  min-height: 0;
  height: auto;
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
  background-color: white;
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
