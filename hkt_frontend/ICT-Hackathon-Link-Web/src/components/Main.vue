<template>
  <div class="main-container">

    <!-- ✅ 2. 스크롤 시 고정되는 헤더 영역 -->
    <header
      :class="['header', { 'visible': isSticky }]"
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
    <section class="hero-section" ref="hero">
      <video autoplay muted loop playsinline class="hero-video" preload="auto">
        <source src="@/assets/uswvideo.mp4" type="video/mp4" />
        브라우저가 비디오를 지원하지 않습니다.
      </video>

      <div class="hero-text">
        <h1>지능형SW융합대학</h1>
        <p>COLLEGE OF INTELLIGENT SOFTWARE CONVERGENCE</p>
      </div>
    </section>
    <div class="cards">
    <div class="card computerSW-card" @click="navigateTo('computerPage')">
      <h2>컴퓨터학부</h2>
      <hr />
      <p>지능형SW융합대학 컴퓨터학부를 안내드립니다.</p>
    </div>
    <div class="card DataScience-card" @click="navigateTo('dataScience')">
      <h2>데이터과학부</h2>
      <hr />
      <p>지능형SW융합대학 데이터과학부를 안내드립니다.</p>
    </div>
    <div
      class="card InfoCommunication-card"
      @click="navigateTo('infoCommunication')"
    >
      <h2>정보통신학부</h2>
      <hr />
      <p>지능형SW융합대학 정보통신학부를 안내드립니다.</p>
    </div>
  </div>
  

    <div class="slider-container">
      <div class="slider-items">
        <div
          v-for="(item, index) in visibleItems"
          :key="index"
          class="slider-item"
        >
          <h3 class="schoolSite" @click="navigateToSite(item.title)" navigateToSite>
            {{ item.title }}
          </h3>
        </div>
      </div>
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
import PrivacyPolicy from '@/components/PrivacyPolicy.vue';
export default {
  name: 'MainPage',
  components: { ChatBot, PrivacyPolicy },
  data() {
    return {
      isLoggedIn: false,
      showPrivacy: false,
      activeDropdown: null,
      navHovered: false,
      showDepartments: false,
      showChat: false,
      isSticky: false,
      departments: [
        { name: '컴퓨터학부', majors: ['컴퓨터SW', '미디어SW'] },
        { name: '정보통신학부', majors: ['정보통신학과', '정보보호학과'] },
        { name: '데이터과학부', majors: [] },
        { name: '클라우드융복합', majors: [] },
      ],
      slideIndex: 0,
      allItems: [
        { title: '홈페이지' },
        { title: '캔버스' },
        { title: '수강신청사이트' },
        { title: '포털' },
      ]
    }
  },
  computed: {
    visibleItems() {
      return this.allItems.slice(this.slideIndex, this.slideIndex + 4);
    },
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    
    handleScroll() {
      const currentScroll = window.scrollY;
      if (currentScroll > 100 && currentScroll > this.lastScrollY) {
        // 아래로 스크롤 중: 헤더 숨김
        this.isSticky = true;
      } else if (currentScroll > 100 && currentScroll < this.lastScrollY) {
        // 위로 스크롤 중: 헤더 표시
        this.isSticky = false;
      }
      this.lastScrollY = currentScroll;
    },

    navigateTo(routeName) {
      this.$router.push({ name: routeName }).catch(err => {
        if (err.name !== 'NavigationDuplicated') throw err;
      });
    },
    navigateToMajor(majorName) {
      const routeMap = {
        컴퓨터학부: 'computerPage',
        컴퓨터SW: 'computerSW',
        미디어SW: 'mediaSW',
        정보통신학부: 'infoCommunication',
        정보통신학과: 'infoCommunicationCollege',
        정보보호학과: 'infoSecurity',
        데이터과학부: 'dataScience',
        클라우드융복합: 'CloudPage',
      };
      const route = routeMap[majorName];
      if (route) this.navigateTo(route);
    },
    hideAllDropdowns() {
      this.activeDropdown = null;
      this.navHovered = false;
    },
    navigateToSite(siteName) {
      const site = {
        홈페이지: 'https://www.suwon.ac.kr/',
        캔버스: 'https://canvas.suwon.ac.kr/',
        수강신청사이트: 'https://sugang.suwon.ac.kr/sugang/login.jsp',
        포털: 'https://portal.suwon.ac.kr/enview/index.html',
      };
      const url = site[siteName];
      if (url) window.open(url, '_blank');
    },
    next() {
      if (this.slideIndex + 4 < this.allItems.length) this.slideIndex++;
    },
    prev() {
      if (this.slideIndex > 0) this.slideIndex--;
    }
  }
}
</script>
<style scoped>
.menu{
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
}
.hero-section {
  position: relative;
  height: 80vh;
  overflow: hidden;
}
.hero-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.hero-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  z-index: 10;
}


.hero-text h1 {
  font-size: 3rem;
}
.hero-text p {
  font-size: 1.2rem;
}
.header.sticky {
  top: 0;
}
.cards {
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
  margin-right: 3rem;
  margin-top: 8rem;
  gap: 2rem;
}
.card {
  position: relative;
  width: 25%;
  height: 220px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  font-size: 2rem;
  font-weight: bold;
  cursor: pointer;
  padding: 1.5rem;
  box-sizing: border-box;
  
}

.computerSW-card {
  background-color: #1b1d53; /* #0070c6 */
  color: white;
  padding-top: 1.5rem;
}

.DataScience-card {
  background-color: #1b1d53; /* #003E94 */
  color: white;
  padding-top: 1.5rem;
}

.InfoCommunication-card {
  background-color: #1b1d53;
  color: white;
  padding-top: 1.5rem;
}

.card h2 {
  font-size: 2rem;
  font-weight: bold;
  margin: 1rem;
  margin-left: 0.2rem;
}

.card hr {
  width: 30px;
  border: 2px solid white;
  margin: 1rem 0;
}

.card p {
  font-size: 1rem;
  margin-bottom: 2rem;
}


.main-container {
 
  background-color: #ffffff;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  min-height: 0;
  overflow-x: hidden;
  height: auto;
  flex: 1;
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 85px;
  transform: translateY(-100%);
  transition: transform 0.3s ease-in-out;
  z-index: 999;
  background-color: #1b1d53;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header.visible {
  transform: translateY(0);
}
.logo {
  height: 40px;
  margin-right: 5rem;
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







.slider-container {
  margin-top: 11rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5rem;
  padding: 1rem;
  padding-left: 0;
  padding-right: 0;
  border-top: 2px solid white;
}

.slider-items {
  display: flex;
  gap: 1rem;
}

.slider-item {
  padding: 1rem;
  color: white;
  border-radius: 8px;
  min-width: 300px;
  text-align: center;
  z-index: 10;
}

.schoolSite {
  cursor: pointer;
}

/*하단창*/
footer {
  background-color: #343539;
  color: #ccc;
  padding: 1rem 0.5rem;
  font-size: 0.9rem;
  line-height: 1
}

footer .container {
  max-width: 100%;
  height: 10rem;
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
