// 📄 src/store/store.js
import { createStore } from 'vuex';

const store = createStore({
  state: {
    apiBaseUrl: 'http://ahnai1.suwon.ac.kr:5052', // 여기에 백엔드 주소 넣기
    accessToken: null,
    chatapiBaseUrl: 'http://ahnai1.suwon.ac.kr:5052',
  },
  mutations: {
    setAccessToken(state, token) {
      state.accessToken = token;
    },
  },
  actions: {
    setAuthData({ commit }, { accessToken }) {
      commit('setAccessToken', accessToken);
    },
  },
});

export default store;