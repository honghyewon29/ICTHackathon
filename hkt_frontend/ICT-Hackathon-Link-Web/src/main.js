import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
// import store from '@/store/store';

createApp(App).mount('#app');

createApp(App).use(router).mount('#app');
