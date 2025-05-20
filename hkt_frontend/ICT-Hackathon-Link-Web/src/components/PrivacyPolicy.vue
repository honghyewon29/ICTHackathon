<!-- PrivacyPolicy.vue -->
<template>
  <div class="privacy-page">
    <img class="close" src="@/assets/close.png" @click="$emit('close')" />
    <div class="privacy-content">
      <section class="privacy-policy">
        <h1 style="text-align: center;">개인정보 처리방침</h1>

        <p>ICT 학부 홈페이지(이하 "본 사이트")는 개인정보 보호법에 따라 사용자(학생)의 개인정보 보호 및 권익을 보호하고, 개인정보와 관련한 사용자의 고충을 원활하게 처리할 수 있도록 다음과 같은 처리방침을 수립·공개합니다.</p>

        <h2>1. 수집하는 개인정보 항목</h2>
        <ul>
            <li>이름</li>
            <li>아이디</li>
            <li>비밀번호</li>
            <li>이메일</li>
        </ul>

        <h2>2. 개인정보의 수집 및 이용 목적</h2>
        <ul>
            <li>회원 식별 및 본인 확인</li>
            <li>공지사항 및 시스템 안내 이메일 발송</li>
            <li>서비스 이용에 따른 본인 인증 및 민원 처리</li>
        </ul>

        <h2>3. 개인정보의 보유 및 이용 기간</h2>
        <p>수집된 개인정보는 회원 탈퇴 시 또는 이용 목적 달성 시 지체 없이 파기됩니다. 다만, 관련 법령에 따라 일정 기간 보관이 필요한 경우에는 예외로 합니다.</p>

        <h2>4. 개인정보의 제3자 제공</h2>
        <p>본 사이트는 원칙적으로 개인정보를 외부에 제공하지 않습니다. 다만 다음의 경우는 예외로 합니다:</p>
        <ul>
            <li>이용자의 사전 동의를 받은 경우</li>
            <li>관련 법령에 따라 제출 의무가 있는 경우</li>
        </ul>

        <h2>5. 개인정보의 파기 절차 및 방법</h2>
        <p>보유 기간이 지난 개인정보는 즉시 파기하며, 파기 절차 및 방법은 다음과 같습니다:</p>
        <ul>
            <li><strong>파기 절차</strong>: 불필요한 개인정보는 즉시 삭제하거나 별도 분리 보관 후 파기합니다.</li>
            <li><strong>파기 방법</strong>: 전자 파일은 복구 불가능한 기술적 방법으로 삭제하며, 출력물은 분쇄하거나 소각합니다.</li>
        </ul>

        <h2>6. 이용자의 권리 및 행사 방법</h2>
        <p>이용자는 언제든지 다음과 같은 권리를 행사할 수 있습니다:</p>
        <ul>
            <li>개인정보 열람 요청</li>
            <li>개인정보 정정 및 삭제 요청</li>
            <li>개인정보 처리 정지 요청</li>
        </ul>
        <p>요청은 이메일(<a class="email" href="mailto:jinbsang@naver.com">jinbsang@naver.com</a>)을 통해 가능하며, 본인 확인 후 처리됩니다.</p>

        <h2>7. 개인정보 보호책임자 및 문의처</h2>
        <p>개인정보 보호에 관한 문의사항은 아래로 연락 주시기 바랍니다.</p>
        <ul>
            <li><strong>담당자</strong>: 반영진</li>
            <li><strong>이메일</strong>: <a class="email" href="mailto:jinbsang@naver.com">jinbsang@naver.com</a></li>
        </ul>

        <h2>8. 개인정보 처리방침의 변경</h2>
        <p>이 개인정보 처리방침은 2025년 5월 17일부터 적용됩니다. 법령 또는 정책 변경 시 수정되어 공지될 수 있습니다.</p>

      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: "PrivacyPolicy",
};
</script>

<style scoped>
* {
  font-family: 'Nanum Gothic', sans-serif;
}

.privacy-page {
  position: fixed;               /* ✅ 화면 위에 고정 */
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow-y: auto;              /* ✅ 내부 스크롤 가능 */
  background-image: url('@/assets/background1.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  background-color: rgba(0, 0, 0, 0.7);
  padding: 60px 20px;
  box-sizing: border-box;
  z-index: 9999;                 /* ✅ 무조건 맨 위에 오게 */
}

.privacy-content {
  max-width: 800px;
  margin: 0 auto;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 40px;
  border-radius: 10px;
  box-sizing: border-box;
}

.close {
  position: fixed;               /* ✅ 항상 우측 상단 고정 */
  top: 20px;
  right: 30px;
  width: 30px;
  height: 30px;
  cursor: pointer;
  z-index: 10000;                /* ✅ 닫기 아이콘은 그 위 */
}


.email {
  color: white;
}

</style>
