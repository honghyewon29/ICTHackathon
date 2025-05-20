<template>
  <div class="chatbot-container" :class="{ open: isOpen }">
    <div class="chat-header">
        <div class="title"><img class="icon" src="@/assets/chatbot-icon.png">Suri</div>
        <img class="close" src="@/assets/close.png" @click="$emit('close')">
    </div>

    <div class="chat-body" >
      <div class="messages" ref="messageContainer">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message-bubble', msg.sender]"
          v-html="formatText(msg.text)"
        ></div>

      </div>

      <div class="chat-input">
        <input v-model="input" @keydown.enter="sendMessage" placeholder="메시지를 입력하세요..." />
        <button @click="sendMessage">전송</button>
      </div>
    </div>
  </div>
</template>

<script>
import store from '@/store/store';
import axios from 'axios';
import { nextTick } from 'vue';

export default {
  name: 'ChatBot',
  emits: ['close'],
  
  data() {
    return {
      isOpen: false,
      input: '',
      messages: [
        { sender: 'bot', text: '안녕하세요! 무엇을 도와드릴까요?' }
      ]
    };
  },
  methods: {
    toggleChat() {
      this.isOpen = !this.isOpen;
    },
    sendMessage() {
      if (this.input.trim()) {
        const userText = this.input;
        this.messages.push({ sender: 'user', text: userText });
        this.input = '';
        this.$nextTick(() => {
          this.scrollToBottom();
        });
        this.sendToServer(userText);
      }
    },
    async sendToServer(userMessage) {
      try {
        const response = await axios.post(`${store.state.chatapiBaseUrl}/chat_api`, {
          message: userMessage,
        });

        this.messages.push({ sender: 'bot', text: response.data.answer });
        await nextTick();
        this.scrollToBottom(); // ✅ 메시지 추가 후 스크롤
      } catch (error) {
        this.messages.push({ sender: 'bot', text: '죄송합니다. 오류가 발생했어요.' });
        await nextTick();
        this.scrollToBottom(); // ✅ 오류 메시지도 스크롤
      }
    },
    scrollToBottom() {
      const container = this.$refs.messageContainer;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
    formatText(text) {
      return text
      .replace(/\n/g, "<br>")                        // 줄바꿈
      // .replace(/(\d+)\.\s/g, "<br><strong>$1.</strong> ")  // 번호 매기기 강조
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");   // **굵게** 처리
    },
  }
};
</script>


<style scoped>
* {
  font-family: 'Nanum Gothic', sans-serif;
}

.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 40%;
  font-family: sans-serif;
  z-index: 10;
}
.chat-header {
  display: flex;
  justify-content: space-between; /* 좌우 정렬 */
  align-items: center;
  background-color: #1b1d53;
  color: white;
  padding: 10px;
  border-radius: 10px 10px 0 0;
}

.title {
  display: flex;
  align-items: center;
}

.close {
  width: 30px;
  height: 30px;
  cursor: pointer;
}

.icon {
  width: 40px;
  height: 24px;
  margin-right: 8px;
}
.chat-body {
  background-color: white;
  border: 1px solid #ccc;
  height: 500px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 0 0 10px 10px;
}
.messages {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
  overflow-y: auto;
  max-height: 500px;
}

/* 기본 말풍선 스타일 */
.message-bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 18px;
  line-height: 1.4;
  word-break: break-word;
  display: inline-block;
}

/* 사용자 메시지 (오른쪽 정렬) */
.user {
  align-self: flex-end;
  background-color: #1b1d53;
  color: white;
  border-bottom-right-radius: 0;
}

/* 챗봇 메시지 (왼쪽 정렬) */
.bot {
  align-self: flex-start;
  background-color: #d8d8d8;
  color: #000;
  border-bottom-left-radius: 0;
}

.chat-input {
  display: flex;
  border-top: 1px solid #ccc;
  border-radius: 0 20px 0 20px;
  height: 10%;
}
.chat-input input {
  flex: 1;
  border: none;
  padding: 10px;
  outline: none;
  border-radius: 15px;
}
.chat-input button {
  background-color: #1b1d53;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 0 0 10px 0;
}


</style>
