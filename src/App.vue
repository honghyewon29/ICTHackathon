<template>
  <div id="app">
    <HeaderBar />
    <Home />
    <ChatbotIcon />
  </div>
</template>

<script>
import HeaderBar from './components/HeaderBar.vue';
import Home from './views/HomePage.vue';
import ChatbotIcon from './components/ChatbotIcon.vue';

export default {
  name: 'App',
  components: {
    HeaderBar,
    Home,
    ChatbotIcon
  }
}
</script>
