<!-- 분실물 -->
<template>
  <div class="lost-container">
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
    <!-- ✅ 서브 비주얼 영역 -->
    <section class="title-section">
        <div class="wrap_sub_visual">
          <div class="container center-only">
            <p class="visual_intro"><strong>분실물 게시판</strong></p>
          </div>
        </div>
    </section>

    <div style="text-align: right; margin: 1rem 2rem 0 0">
      <button @click="navigateToWrite" class="write-button">분실물 등록</button>
    </div>

    <section class="lost-section">
      <div class="lost-header">
        <p>총 <strong>{{ items.length }}</strong>개의 분실물 기록이 있습니다.</p>
      </div>

      <table class="lost-table">
        <thead>
          <tr>
            <th>번호</th>
            <th>제목</th>
            <th>작성자</th>
            <th>작성일</th>
            <th>첨부</th>
            <th>습득 여부</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="6">분실물이 없습니다.</td>
          </tr>
          <tr v-for="item in items" :key="item.id" @click="navigateToDetail(item.id)" style="cursor: pointer">
            <td>{{ item.id }}</td>
            <td>{{ item.title }}</td>
            <td>{{ item.publisher }}</td>
            <td>{{ formatDate(item.created_at) }}</td>
            <td><span v-if="item.has_file">📎</span></td>
            <td><span :style="{ color: item.is_found ? 'green' : 'red' }">{{ item.is_found ? '습득 완료' : '미습득' }}</span></td>
          </tr>
        </tbody>
      </table>
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
import axios from 'axios';
import ChatBot from '@/components/ChatBot.vue'
import PrivacyPolicy from '@/components/PrivacyPolicy.vue'

export default {
  name: "lostArticle",
  components: {
    ChatBot,
    PrivacyPolicy
  },
  data() {
    return {
       isLoggedIn: false,
      items: [],
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
    
    async fetchLostItems() {
      try {
        const res = await axios.get('http://ahnai1.suwon.ac.kr:5052/api/lost-item');
        this.items = res.data;
      } catch (err) {
        console.error("분실물 목록 불러오기 실패:", err);
      }
    },
    formatDate(datetimeStr) {
      const date = new Date(datetimeStr);
      return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
    },
    navigateToWrite() {
      this.$router.push({ name: 'lostWrite' });
    },
    navigateToDetail(id) {
      this.$router.push({ name: 'lostDetail', params: { id } });
    },
    navigateTo(routeName) {
      this.$router.push({ name: routeName }).catch(err => {
        if (err.name !== 'NavigationDuplicated') throw err;
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

  mounted() {
    this.fetchLostItems();
  }
};
</script>

<style scoped>
.lost-container {
  display: flex;
  flex-direction: column;
  background-color: #f7f7f7;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  /* 이 두 줄이 핵심 */
  height: auto;         /* 자동으로 콘텐츠에 맞춤 */
  min-height: 100vh;        /* 필요시 강제 최소 높이 제거 */
}

* {
  font-family: 'Nanum Gothic', sans-serif;
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

.right-menu a {
  font-size: 0.8rem;
  text-decoration: none;
}



nav a {
  margin: 0 10px;
  color: white;
  text-decoration: none;
}

.menu{
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
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

.content {
  color: white;
}

.write-button {
  padding: 0.5rem 1rem;
  background-color: #1b1d53;
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
}
.write-button:hover {
  background-color: #3a3d80;
}

.lost-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}
.lost-table th,
.lost-table td {
  border: 1px solid #ccc;
  padding: 0.6rem;
  text-align: center;
}
.lost-table th {
  background-color: #f4f4f4;
  color: #1b1d53;
}
.notice-table td a {
  color: #1b1d53;
  text-decoration: none;
}
.lost-section {
  width: 60%; /* 원하는 너비 (예: 700px) */
  margin: 3rem auto;
  padding: 1rem;
  background-color: rgb(255, 255, 255);
  border-radius: 8px;
  flex: 1;
}

footer {
  background-color: #343539;
  color: #ccc;
  padding: 1rem 0.5rem;
  font-size: 0.9rem;
  line-height: 1.6;
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