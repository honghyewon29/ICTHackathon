<!-- 컴퓨터SW학과 -->
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
    :class="[$route.name === 'computerSW-Sub' ? 'yellow-button' : 'blue-button']"
    @click="navigateTo('computerSWSub')"
  >
    교과과정
  </button>
</div>

    <!-- 본문 영역 -->
    <section class="info-section">
      <div class="info-box">
        <h2>학과소개</h2>
        <p>학과위치: 지능형SW융합대학 3층(304호)</p>
        <p>대표전화: 031-220-2516</p>
        <p>업무시간: 오전 9시 ~ 오후 5:30</p>
      </div>

      <div class="info-box">
        <h2>전공소개</h2>
          <p>현대 사회는 컴퓨터 및 통신기술 등에 의해 정보의 수집, 가공 분배를 수행하는 능력이 사회의 발전을 주도해 가는 정보화 사회이다.</p>
          <p>따라서 컴퓨터SW 전공은 컴퓨터 및 정보 통신의 기본적인 이론을 바탕으로, 컴퓨터 시스템의 이론 및 실습 교육을 통해 전문 분야 지식을 배양함으로써, 정보화 사회를 이끌어갈 고급 인력을 양성하는데 역점을 두고 있다.</p>
          <p>또한 이들의 효율적인 응용 및 관리를 담당할 컴퓨터 과학자, 컴퓨터 기술자, 컴퓨터 관리자 등의 유능한 인재를 육성하는데 목표를 둔다.</p>
      </div>

      <div class="info-box">
        <h2>관련자격 및 시험</h2>
        <p>정보처리기사, 중등교사 정교사 2급 자격증 (컴퓨터), CCNA( Cisco Certified NetworkAssociate), 네트워크 관리 자격 인증, LPIC (Linux Professional Institute Certification), 리눅스 국제 인증, OCP (Oracle Certified Professional), 오라클 데이터베이스 관리 능력 인증</p>

      </div>
      <div class="info-box">
  <h2>학과시설</h2>
  <table class="facility-table">
    <thead>
      <tr>
        <th>구분</th>
        <th>위치 및 설명</th>
      </tr>
    </thead>
    <tbody>
            <tr>
        <td><strong>학과사무실</strong></td>
        <td>지능형SW융합대학 304호</td>
      </tr>
      <tr>
        <td><strong>강의실</strong></td>
        <td>지능형SW융합대학 108호, 415호</td>
      </tr>
      <tr>
        <td><strong>실습실</strong></td>
        <td>지능형SW융합대학 308호, 310호, 406호, 409호, 411호</td>
      </tr>
      <tr>
        <td><strong>학생회실</strong></td>
        <td>지능형SW융합대학 518호</td>
      </tr>
      <tr>
        <td><strong>교수연구실</strong></td>
        <td>지능형SW융합대학 507호, 508호, 509호, 510호, 522호</td>
      </tr>
      <tr>
        <td><strong>대학원생 연구실</strong></td>
        <td>지능형SW융합대학 207호, 513호</td>
      </tr>

    </tbody>
  </table>
</div>

      <div class="info-box">
        <h2>교수 소개</h2>
        <div class="professor-grid">
          <div class="professor-card" v-for="(prof, index) in professors" :key="index">
            <h3>
                <a :href="prof.link" target="_blank" rel="noopener noreferrer">{{ prof.name }}</a>
            </h3>
            <p class="dept">{{ prof.dept }}</p>
            <p><strong>전공 : </strong> {{ prof.major }}</p>
            <p><strong>이메일 : </strong> {{ prof.email }}</p>
            <p><strong>연구실 : </strong> {{ prof.lab }}</p>
            <p><strong>연락처 : </strong> {{ prof.phone }}</p>
          </div>
        </div>
      </div>
    </section>
   
    
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
      isIntro: true,
      showChat: false,
      activeDropdown: null,
      navHovered: false,
      departments: [
        { name: '컴퓨터학부', majors: ['컴퓨터SW', '미디어SW'] },
        { name: '정보통신학부', majors: ['정보통신학과', '정보보호학과'] },
        { name: '데이터과학부', majors: [] },
        { name: '클라우드융복합', majors: [] },
      ],
            professors: [
        { name: '장성태', dept: '컴퓨터SW', major: '컴퓨터구조, 차세대 Mobile Embedded System, 보안감시 기술', email: 'stjhang@suwon.ac.kr', lab: '지능형SW융합대학 510호', phone: '031-220-2126', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1941508' },
        { name: '준웨이푸', dept: '컴퓨터SW', major: '-', email: '없음', lab: 'IT대학405', phone: '없음', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1164040' },
        { name: '김장영', dept: '컴퓨터SW', major: '빅데이터,네트워크,인공지능,보안', email: 'jykim77@suwon.ac.kr', lab: '지능형SW융합대학 522호', phone: '031-229-8345', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1143596' },
        { name: '구창진', dept: '컴퓨터SW', major: '운영체제,정보보호', email: 'ycjkoo@suwon.ac.kr', lab: '미래혁신관 712호', phone: '031-229-8595', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1244953' },
        { name: '한성일', dept: '컴퓨터SW', major: 'Applied Machine Learning', email: 'seongil.han@suwon.ac.kr', lab: '지능형SW융합대학 521호', phone: '031-229-8218', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1255128' },
        { name: '허성민', dept: '컴퓨터SW', major: '-', email: '없음', lab: '-', phone: '없음', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1090047' }
]


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

.sub-nav button.active {
  background-color: #1b1d53;
  color: white;
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
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.462);
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

.facility-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  color: black;
  background-color: rgba(255, 255, 255);
}

.facility-table th,
.facility-table td {
  border: 1px solid black;
  padding: 1rem;
  text-align: left;
  vertical-align: top;
  font-size: 1rem;
}

.facility-table th {
  background-color: #c9c9c9;
  font-size: 1rem;
  font-weight: bold;
}

.professor-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3개씩 배치 */
  gap: 2rem; /* 카드 간 간격 */
  padding: 1rem;
}

.professor-card a {
    color: white;
    text-decoration: underline;
    text-underline-offset: 4px;
}

.professor-card {
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 1rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  color: white;
}

.professor-card h3 {
  margin: 0;
  font-size: 1.7rem;
  color: white;
}

.professor-card .dept {
  font-size: 0.9rem;
  color: white;
  margin-bottom: 0.5rem;
}

.chair-card {
  border: 2px solid #ddd;
  padding: 1rem 1.5rem;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  row-gap: 0.8rem;
  column-gap: 1.5rem;
}

.chair-item {
  display: flex;
  align-items: center;
  font-size: 1rem;
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
