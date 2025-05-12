<template>
  <header class="header">
    <div class="logo">
      <img src="https://www.suwon.ac.kr/usr/images/suwon/logo.png" alt="usw logo" />
      <span>수원대학교<br />지능형 SW융합대학</span>
    </div>
    <nav class="nav">
      <a href="#">대학 안내</a>
      <div class="dropdown-wrapper" @mouseover="show = true" @mouseleave="show = false">
        <a href="#">학과 안내</a>
        <div class="dropdown" v-if="show">
          <div class="column">
            <strong>정보통신학부</strong>
            <p>정보보호학과</p>
            <p>정보통신학과</p>
          </div>
          <div class="column">
            <strong>컴퓨터학부</strong>
            <p>컴퓨터SW</p>
            <p>미디어SW</p>
          </div>
          <div class="column">
            <strong>데이터과학부</strong>
            <p>데이터과학부</p>
          </div>
        </div>
      </div>
      <a href="#">정보 광장</a>
      <a href="#">공지</a>
    </nav>
    <div class="sub-nav">
      <a class="small" href="#">register</a>
      <a class="small" href="#">login</a>
      <img class="search-icon" src="https://c2.klipartz.com/pngpicture/341/539/sticker-png-search-icon-search-magnifier-icon-go-shopping-icon-commerce-icon-price-data-sheet-science-transport-truck.png" alt="search" />
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {
      show: false
    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 3rem;
  background-color: #1b1d53;
  color: white;
}
.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
}
.logo img {
  height: 50px;
}
.nav {
  display: flex;
  gap: 60px;
  font-size: 1.1rem;
  align-items: center;
  justify-content: center;
  flex: 1;
}
.nav a {
  color: white;
  text-decoration: none;
  position: relative;
}
.sub-nav {
  display: flex;
  align-items: center;
  gap: 15px;
}
.small {
  font-size: 0.8rem;
  color: #aaa;
}
.search-icon {
  width: 40px;
  height: 40px;
}
.dropdown-wrapper {
  position: relative;
}
.dropdown {
  position: absolute;
  top: 40px;
  left: -100px;
  background-color: white;
  color: black;
  padding: 2rem 3rem;
  display: flex;
  gap: 5rem;
  border: 1px solid #ccc;
  z-index: 10;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  min-width: 700px;
  justify-content: space-around;
}
.dropdown strong {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 1.05rem;
  border-bottom: 2px solid black;
}
.dropdown p {
  margin: 0.3rem 0;
  font-size: 0.95rem;
}
.column {
  display: flex;
  flex-direction: column;
  min-width: 150px;
}
</style>