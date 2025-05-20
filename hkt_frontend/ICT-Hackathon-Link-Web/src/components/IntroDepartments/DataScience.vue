<!-- 데이터과학부 -->
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
            <p class="visual_intro"><strong>데이터과학부</strong></p>
            <p class="subtitle a">DataScience</p>
            
          </div>
        </div>
    </section>
     <section class="info-section">
      <section class="info-box">
        <h2 class="section-title">학부 소개</h2>
        <p>데이터과학부는 제4차 산업혁명의 필요한 전문인 양성을 적합한 교육과정을 제공한다. 이에 따라 데이터 분석에서부터 인공지능 알고리즘 개발 및 실행에 필요한 전문 지식을 익히도록 한다.</p>
        <p>데이터과학 전공에서는 데이터 처리를 위한 IT 기술과 데이터의 분석 및 의사결정, 빅데이터 처리 및 응용력 습득, 머신러닝을 위한 알고리즘, 딥러닝의 구조와 원리 및 인공지능의 알고리즘 구현 등을 가능하도록 하며, 이에 필요한 수학, 통계학 이론 및 소프트웨어 교육과정을 제공하며, 캡스톤 디자인을 통하여 사회 및 산업계에 필요한 지식 등을 학습하여 데이터 과학자로 성장할 수 있도록 한다.</p>
        <p>본 학부에서는 R과 Python 등 다양한 프로그램 언어를 실습할 수 있는 컴퓨터실을 제공하며, 머신러닝 랩을 활용할 수 있도록 하고, 산업계와의 협업으로 현장에 필요한 교육을 제공하여, 학생 스스로 데이터분석 전문가로서 비전을 설계하고 만들어 가도록 협력을 한다.</p>
        <p>본 학부의 교과과정은 새로운 문제를 도출하고 해결 능력을 갖춘 창의적 데이터 과학자를 양성하는 것이다.</p>
      </section>

      <section>
        <h2 class="section-title">학과장 소개</h2>
        <div class="profile">
          <div>
            <p><strong>성명:</strong> 정진명</p>
            <p><strong>위치:</strong> 경상대학 918호</p>
          </div>
          <div>
            <p><strong>소속:</strong> 데이터과학부 데이터과학</p>
            <p><strong>연락처:</strong> 031-220-2521</p>
            <p><strong>Email:</strong> jmjung@suwon.ac.kr</p>
          </div>
        </div>
      </section>

      <section class="degree-table">
        <h2 class="section-title">전공 및 학위 과정</h2>
        <table>
          <thead>
            <tr>
              <th>전공</th>
              <th>학사과정</th>
              <th>석사과정</th>
              <th>박사과정</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>데이터과학</td>
              <td>○</td>
              <td>○</td>
              <td>○</td>
            </tr>
          </tbody>
        </table>
      </section>

      <div class="infobox">
        <h2 class="section-title">교수 소개</h2>
        <div class="professor-grid">
          <div class="professor-card" v-for="(prof, index) in professors" :key="index">
            <h3><a :href="prof.link" target="_blank" rel="noopener noreferrer">{{ prof.name }}</a></h3>
            <p class="dept">{{ prof.dept }}</p>
            <p><strong>전공 : </strong> {{ prof.major }}</p>
            <p><strong>이메일 : </strong> {{ prof.email }}</p>
            <p><strong>연구실 : </strong> {{ prof.lab }}</p>
            <p><strong>연락처 : </strong> {{ prof.phone }}</p>
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
  name: 'dataScience',
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
      professors: [
        { name: '박진우', dept: '데이터과학부', major: '통계학(표본이론)', email: 'jwpark@suwon.ac.kr', lab: '글로벌경상관 908호', phone: '-', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1931463' },
        { name: '고영미', dept: '데이터과학부', major: '수학', email: 'ymkoh@suwon.ac.kr', lab: '글로벌경상관 913호', phone: '031-220-2166', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1931467' },
        { name: '김진흠', dept: '데이터과학부', major: '다변량통계학 / 생물통계학', email: 'jkimdt65@gmail.com', lab: '글로벌경상관 904호', phone: '031-220-2394', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1961566' },
        { name: '정형철', dept: '데이터과학부', major: '통계학', email: 'jeong.hc@suwon.ac.kr', lab: '글로벌경상관 912호', phone: '031-229-8153', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1050009' },
        { name: '한경훈', dept: '데이터과학부', major: '수학', email: 'kyunghoon.han@gmail.com', lab: '글로벌경상관 917호', phone: '031-229-8156', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1110243' },
        { name: '정진명', dept: '데이터과학부', major: '생물정보학', email: 'jmjung@suwon.ac.kr', lab: '글로벌경상관 918호', phone: '031-229-8671', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1174107' },
        { name: '김남국', dept: '데이터과학부', major: '클라우드 컴퓨팅', email: 'ngkim@suwon.ac.kr', lab: '미래혁신관 414호', phone: '031-229-8655', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1174073' },
        { name: '황용득', dept: '데이터과학부', major: '생물정보학', email: 'ydhwang@suwon.ac.kr', lab: '글로벌경상관 911호', phone: '031-220-2301', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1174108' },
        { name: '안홍렬', dept: '데이터과학부', major: '바이오·의료 인공지능', email: 'hrahn@suwon.ac.kr', lab: '글로벌경상관 1012호', phone: '031-229-8762', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1200091' },
        { name: '염희란', dept: '데이터과학부', major: '생물정보학', email: 'huiran.yeom@gmail.com', lab: '글로벌경상관 1018호', phone: '031-220-8833', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1234816' },
        { name: '김진현', dept: '데이터과학부', major: '바이오·의료 인공지능', email: 'jinhyun.kim@suwon.ac.kr', lab: '글로벌경상관 914호', phone: '031-220-2472', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1240102' },
        { name: '김순찬', dept: '데이터과학부', major: '바이오·의료 인공지능', email: 'soonchan.kim@suwon.ac.kr', lab: '글로벌경상관 901호', phone: '031-220-2479', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1255130' },
        { name: '김인환', dept: '데이터과학부', major: 'Computer Science', email: '-', lab: '미래혁신관 508', phone: '010-2328-8055', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1255129' },
        { name: '방효은', dept: '데이터과학부', major: '생물정보학', email: 'hebang@suwon.ac.kr', lab: '글로벌경상관 1011호', phone: '031-229-8763', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1255125' },
        { name: '안주희', dept: '데이터과학부', major: '보건빅데이터통계', email: 'jhahn@suwon.ac.kr', lab: '글로벌경상관 1017호', phone: '031-220-8831', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1255126' },
        { name: '이상욱', dept: '데이터과학부', major: 'Combinatorics', email: 'swree@suwon.ac.kr', lab: '글로벌경상관 914호', phone: '031-220-2472', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1961562' },
        { name: '정문자', dept: '데이터과학부', major: '수학', email: 'mjeong@suwon.ac.kr', lab: '-', phone: '--', link: 'https://www.suwon.ac.kr/mainHp/prointro/detail.html?eno=1941507' }
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
  min-height: 100vh;
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





.info-section {
  background-color: transparent;
  padding: 4% 10% ;
  border-radius: 5px;
  line-height: 1.8;
  font-weight: 500;

}

.section-title {
  font-size: 1.5rem;
  margin-top: 3rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid #1b1d53;
  display: inline-block;
}


.info-box {
  background-color: #f5f5f5;
  padding: 1rem;
  border-left: 5px solid #1b1d53;
  margin: 1rem 0;
}
.infobox{
  background-color: #f5f5f5;
  padding: 1rem;
  
  margin: 1rem 0;

}
.professor-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3개씩 배치 */
  gap: 2rem; /* 카드 간 간격 */
  
}

.professor-card a {
  color: white;
  text-decoration: underline;
  text-underline-offset: 7px;
}

.professor-card {
  background: rgba(0, 0, 0, 0.596);
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

.programs {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}

.programs button {
  flex: 1;
  margin: 0 0.5rem;
  padding: 1rem;
  background-color: #1b1d53;
  color: white;
  border: none;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.2s;
}

.programs button:hover {
  background-color: #3a3c7d;
}

.icon {
  background-color: #e9b93e;
  color: #333;
  border-radius: 50%;
  padding: 0.2rem 0.5rem;
  margin-right: 0.6rem;
  font-size: 0.9rem;
}
.degree-table {
  margin-top: 2rem;
}

.degree-table h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid #14213d;
  padding-bottom: 0.5rem;
  color: #14213d;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);

}

th,
td {
  padding: 0.8rem;
  text-align: center;
  border: 1px solid #ddd;
  font-size: 1rem;
}

th {
  background-color: #14213d;
  color: white;
}


@media (max-width: 1000px) {
  .professor-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .professor-grid {
    grid-template-columns: 1fr;
  }
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
