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

      <nav>
        <!-- 대학 안내 -->
        <div class="center-menu">
          <a class="intro" @click="navigateTo('introCollege')" style="cursor: pointer"
            >대학 안내</a
          >
          <div class="divider"></div>

          <!-- 학과 안내 -->
          <div
            class="department-wrapper"
            @mouseenter="activeDropdown = 'department'"
          >
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

          <!-- 정보 광장 -->
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

          <a
            class="announcememt"
            @click="navigateTo('announcePage')"
            style="cursor: pointer"
            >공지</a
          >
        </div>
      </nav>
      
    </header>

    <!-- ✅ 상세내용 -->
    <div class="detail-container">
      <h2>{{ notice.title }}</h2>
      <p><strong>작성자:</strong> {{ notice.publisher }}</p>
      <p><strong>작성일:</strong> {{ formatDate(notice.created_at) }}</p>
      <div class="content">{{ notice.content }}</div>
      <div v-if="notice.attachments">
        <a :href="`http://ahnai1.suwon.ac.kr:5052/api/notices/${notice.notice_id}/file`" download>📎 첨부파일 다운로드</a>
      </div>
    </div>
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
import axios from 'axios';
import ChatBot from '@/components/ChatBot.vue'
import PrivacyPolicy from '@/components/PrivacyPolicy.vue'
export default {
  name: "announceDetail",
  components: {
    ChatBot,
    PrivacyPolicy
  },
  data() {
    return {
      isLoggedIn: false,
      notice: {},
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
    
        filteredNotices() {
      return this.notices
        .filter((n) => this.selectCategory === "all_annonce" || n.category === this.selectCategory)
        .filter((n) => {
          const field = this.searchColumn;
          return n[field].toLowerCase().includes(this.searchTerm.toLowerCase());
        });
    },
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

    async fetchNotice() {
      try {
        const id = this.$route.params.id;
        const res = await axios.get(`http://ahnai1.suwon.ac.kr:5052/api/notices/${id}`);
        this.notice = res.data;
      } catch (err) {
        console.error("공지 상세 불러오기 실패:", err);
      }
    },
    formatDate(str) {
      const d = new Date(str);
      return d.toLocaleDateString('ko-KR');
    },
  },
  mounted() {
    this.fetchNotice();
  }
};
</script>

<style scoped>
* {
  font-family: 'Nanum Gothic', sans-serif;
}

.main-container {
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  background-color: #f7f7f7;
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

.detail-container {
  max-width: 800px;
  margin: 3rem auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}
h2 {
  margin-bottom: 1rem;
}
.content {
  margin-top: 1.5rem;
  white-space: pre-wrap;
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
