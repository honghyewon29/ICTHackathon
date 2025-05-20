<template>
  <div id="app">
    <router-view /> <!-- 페이지 내용 변경됨 -->
    
    <!-- ✅ 챗봇은 항상 유지 -->
    <img
      class="chatbot-icon"
      src="@/assets/chatbot-icon.png"
      @click="toggleChat"
    />
    <ChatBot v-if="showChat" @close="showChat = false" />
  </div>
</template>

<script>
import ChatBot from '@/components/ChatBot.vue'

export default {
  name: 'App',
  components: {
    ChatBot
  },
  data() {
    return {
      showChat: false,
    }
  },
  methods: {
    toggleChat() {
      this.showChat = !this.showChat
    }
  }
}
</script>

<style>
.chatbot-icon {
  cursor: pointer;
  position: fixed;
  bottom: 30px;
  right: 50px;
  width: 150px; /* ✅ 기존보다 가로폭 확대 */
  height: auto; /* ✅ 높이 자동으로 비율 유지 */
  object-fit: contain; /* ✅ 이미지 전체가 보이도록 조정 */
  z-index: 10; 
  flex-shrink: 0;
}
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
  overflow-x: hidden;
  box-sizing: border-box;
}

</style>


