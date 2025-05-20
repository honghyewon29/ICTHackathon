<template>
  <div class="write-container">
    <h2>공지사항 작성</h2>
    <form @submit.prevent="submitNotice" enctype="multipart/form-data">
      <input v-model="title" type="text" placeholder="제목" required />
      <textarea v-model="content" placeholder="내용" required></textarea>
      <input v-model="publisher" type="text" placeholder="작성자" required />
      <select v-model="category">
        <option value="통합공지">통합공지</option>
        <option value="학과공지">학과공지</option>
      </select>
      <input type="file" @change="handleFileChange" />
      <button type="submit">등록</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AnnouncementWrite',
  data() {
    return {
      title: '',
      content: '',
      publisher: '',
      category: '통합공지',
      file: null,
    };
  },
  methods: {
    handleFileChange(e) {

      this.file = e.target.files[0]; 

      // 허용 확장자 검사 (소문자 처리)
      const validExtensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'];
      const extension = this.file.name.split('.').pop().toLowerCase();

      if (validExtensions.includes(extension)) {
        console.log("업로드된 이미지 파일:", this.file);
      } else {
        alert("이미지 파일만 업로드할 수 있습니다. (.png, .jpg 등)");
        this.file = null; // 기존에 있던 파일도 제거
        e.target.value = ''; // input 초기화
      }
    },

    async submitNotice() {
      const formData = new FormData();
      formData.append('title', this.title);
      formData.append('content', this.content);
      formData.append('publisher', this.publisher);
      formData.append('category', this.category);
      if (this.file) {
        formData.append('attachments', this.file);
  }

      try {
        await axios.post('http://ahnai1.suwon.ac.kr:5052/api/notices', formData);
        alert('공지사항이 등록되었습니다.');
        this.$router.push({ name: 'announcePage' });
      } catch (err) {
        console.error('공지사항 등록 실패:', err);
        alert('공지사항 등록 실패: ' + err.message);
      }
    }
  }
};
</script>

<style scoped>
.write-container {
  max-width: 700px;
  margin: 3rem auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}
h2 {
  margin-bottom: 1rem;
  text-align: center;
}
input, textarea, select {
  display: block;
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}
textarea {
  min-height: 150px;
  resize: vertical;
}
button {
  background-color: #1b1d53;
  color: white;
  padding: 0.7rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}
button:hover {
  background-color: #3a3d80;
}
</style>