import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, session, redirect, render_template_string, current_app, jsonify, url_for
from flask_mail import Message as FlaskMessage # Message 객체를 파일 상단에서 임포트
import random
import string
from datetime import datetime, timedelta

# --- 프로젝트 루트 경로 설정 ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# --- 경로 설정 끝 ---

from setting.db_connect import db
from setting.models import User

# --- 기본 스타일 ---
common_style = r"""
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 90vh; }
    .form-container { background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
    h2 { text-align: center; color: #333; margin-bottom: 25px; }
    .form-group { margin-bottom: 20px; }
    .form-group label { display: block; margin-bottom: 8px; color: #555; font-weight: bold; }
    .form-group input[type="text"],
    .form-group input[type="password"],
    .form-group input[type="email"] { width: calc(100% - 22px); padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
    .form-group .email-verify-group { display: flex; align-items: center; }
    .form-group .email-verify-group input[type="email"] { flex-grow: 1; margin-right: 10px; }
    .form-group .email-verify-group button { padding: 10px 15px; background-color: #5cb85c; color: white; border: none; border-radius: 4px; cursor: pointer; white-space: nowrap; font-size:0.9em; }
    .form-group .email-verify-group button:hover { background-color: #4cae4c; }
    .form-group .email-verify-group button:disabled { background-color: #aaa; cursor: not-allowed; }
    .form-group input[type="submit"], .button-link { display: inline-block; width: auto; padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; text-align:center; font-size:1em; }
    .form-group input[type="submit"]:hover, .button-link:hover { background-color: #0056b3; }
    .message { text-align: center; padding: 10px; margin-bottom: 20px; border-radius: 4px; font-size: 0.9em; }
    .message.error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .message.success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .links { text-align: center; margin-top: 20px; font-size: 0.9em; }
    .links a { color: #007bff; text-decoration: none; margin: 0 10px; }
    .links a:hover { text-decoration: underline; }
    #timer { margin-left: 10px; color: #dc3545; font-weight: bold; font-size:0.9em; }
    .verification-code-input { margin-top:10px; }
    .verification-code-input label {font-size:0.9em;}
    .verification-code-input input[type="text"] {width: calc(70% - 22px); margin-right: 10px;}
</style>
"""

# --- HTML 템플릿 문자열 ---
login_form_template = common_style + r'''
<div class="form-container">
  <h2>로그인</h2>
  {% if message %}
    <p class="message {{ message_class | default('error') }}">{{ message }}</p>
  {% endif %}
  <form method="post">
    <div class="form-group">
      <label for="User_id">아이디</label>
      <input type="text" id="User_id" name="User_id" value="{{ request.form.User_id if request and request.form else '' }}" required>
    </div>
    <div class="form-group">
      <label for="User_pw">비밀번호</label>
      <input type="password" id="User_pw" name="User_pw" required>
    </div>
    <div class="form-group" style="text-align:center;">
      <input type="submit" value="로그인">
    </div>
  </form>
  <div class="links">
    <p>계정이 없으신가요? <a href="{{ url_for('register_page') }}">회원가입</a></p>
  </div>
</div>
'''

register_form_template = common_style + r'''
<div class="form-container">
  <h2>회원가입</h2>
  {% if message %}
    <p class="message {{ 'success' if '발송' in message or '성공' in message or '완료' in message else 'error' }}">{{ message }}</p>
  {% endif %}
  <form method="post" id="registerForm">
    <div class="form-group">
      <label for="User_id_reg">아이디</label>
      <input type="text" id="User_id_reg" name="User_id" value="{{ request.form.User_id if request and request.form else '' }}" required>
    </div>
    <div class="form-group">
      <label for="User_pw_reg">비밀번호</label>
      <input type="password" id="User_pw_reg" name="User_pw" required>
    </div>
    <div class="form-group">
      <label for="User_email_reg">이메일</label>
      <div class="email-verify-group">
        <input type="email" id="User_email_reg" name="User_email" value="{{ request.form.User_email if request and request.form else '' }}" required>
        <button type="button" id="sendVerificationCodeBtn">이메일 인증</button> 
      </div>
      <div id="emailVerificationFeedback" style="font-size:0.9em; margin-top:5px;"></div>
      <div id="verificationCodeSection" style="display:none;" class="verification-code-input">
        <label for="verification_code_input">인증 코드</label>
        <div>
          <input type="text" id="verification_code_input" name="verification_code_input" placeholder="4자리 코드" maxlength="4">
          <span id="timer" style="margin-left: 10px;"></span>
        </div>
      </div>
    </div>
    <div class="form-group">
      <label for="User_name_reg">이름</label>
      <input type="text" id="User_name_reg" name="User_name" value="{{ request.form.User_name if request and request.form else '' }}" required>
    </div>
    <div class="form-group" style="text-align:center;">
      <input type="submit" value="가입">
    </div>
  </form>
  <div class="links">
    <p>이미 계정이 있으신가요? <a href="{{ url_for('login_page') }}">로그인</a></p>
  </div>
</div>

<script>
  let timerInterval;
  const VERIFICATION_CODE_TIMER_DURATION = 180; // 3분 (초)

  const sendVerificationCodeBtn = document.getElementById('sendVerificationCodeBtn');
  const emailInput = document.getElementById('User_email_reg');
  const emailFeedback = document.getElementById('emailVerificationFeedback');
  const verificationCodeSection = document.getElementById('verificationCodeSection');
  const timerDisplay = document.getElementById('timer');

  async function requestVerificationCode() {
    const email = emailInput.value.trim();
    if (!email) {
      emailFeedback.textContent = '이메일 주소를 입력해주세요.';
      emailFeedback.className = 'message error';
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        emailFeedback.textContent = '유효한 이메일 주소를 입력해주세요.';
        emailFeedback.className = 'message error';
        return;
    }

    sendVerificationCodeBtn.disabled = true;
    sendVerificationCodeBtn.textContent = '발송중...';
    emailFeedback.textContent = '인증 코드를 발송 중입니다...';
    emailFeedback.className = 'message'; 

    try {
      const response = await fetch("{{ url_for('send_code_route') }}", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email })
      });
      const data = await response.json();
      if (response.ok && data.success) {
        emailFeedback.textContent = data.message || '인증 코드가 이메일로 발송되었습니다. 3분 안에 입력해주세요.';
        emailFeedback.className = 'message success';
        verificationCodeSection.style.display = 'block';
        document.getElementById('verification_code_input').focus();
        startTimer(VERIFICATION_CODE_TIMER_DURATION, timerDisplay);
      } else {
        emailFeedback.textContent = data.message || '인증 코드 발송에 실패했습니다. 잠시 후 다시 시도해주세요.';
        emailFeedback.className = 'message error';
        sendVerificationCodeBtn.disabled = false;
        sendVerificationCodeBtn.textContent = '이메일 인증';
      }
    } catch (error) {
      console.error('Error requesting verification code:', error);
      emailFeedback.textContent = '인증 코드 발송 중 오류가 발생했습니다. 네트워크 연결을 확인해주세요.';
      emailFeedback.className = 'message error';
      sendVerificationCodeBtn.disabled = false;
      sendVerificationCodeBtn.textContent = '이메일 인증';
    }
  }

  function startTimer(duration, displayElement) {
    let timeLeft = duration;
    if (timerInterval) clearInterval(timerInterval);
    displayElement.style.display = 'inline';
    timerInterval = setInterval(() => {
      const minutes = Math.floor(timeLeft / 60);
      let seconds = timeLeft % 60;
      seconds = seconds < 10 ? '0' + seconds : seconds;
      displayElement.textContent = minutes + ":" + seconds;
      if (--timeLeft < 0) {
        clearInterval(timerInterval);
        displayElement.textContent = '시간 만료';
        emailFeedback.textContent = '인증 시간이 만료되었습니다. 다시 시도해주세요.';
        emailFeedback.className = 'message error';
        sendVerificationCodeBtn.disabled = false;
        sendVerificationCodeBtn.textContent = '인증코드 재전송';
      }
    }, 1000);
  }

  if (sendVerificationCodeBtn) {
    sendVerificationCodeBtn.addEventListener('click', requestVerificationCode);
  } else {
    console.error("'sendVerificationCodeBtn' 버튼을 찾을 수 없습니다.");
  }
  
  window.addEventListener('DOMContentLoaded', () => {
      const serverMessage = {% if message %}"{{ message | escapejs }}"{% else %}""{% endif %};
      if (serverMessage && (serverMessage.includes("인증 코드를 입력") || serverMessage.includes("잘못된 인증 코드") || serverMessage.includes("만료된 인증 코드"))) {
          if (emailInput.value) {
            verificationCodeSection.style.display = 'block';
          }
      }
      if (timerDisplay.textContent === '시간 만료') {
          sendVerificationCodeBtn.textContent = '인증코드 재전송';
          sendVerificationCodeBtn.disabled = false;
      }
  });
</script>
'''

delete_account_confirm_form_template = common_style + r'''
<div class="form-container">
  <h2>회원 탈퇴</h2>
  {% if message %}
    <p class="message error">{{ message }}</p>
  {% else %}
    <p><strong>{{ user_id_to_display }}</strong>님, 정말로 회원 탈퇴를 하시겠습니까?</p>
    <p style="color:gray; text-align:center; font-size:0.9em;">이 작업은 되돌릴 수 없습니다.</p>
  {% endif %}
  <form method="post" action="{{ url_for('delete_account_page') }}" style="text-align:center;">
    <div class="form-group" style="margin-bottom:0;">
      <input type="submit" value="예, 탈퇴합니다." style="background-color:#dc3545; margin-right:10px;">
      <a href="{{ url_for('home') }}" class="button-link" style="background-color:#6c757d;">아니요, 취소합니다.</a>
    </div>
  </form>
</div>
'''
# --- HTML 템플릿 문자열 끝 ---


# --- 내부 헬퍼 함수 ---
def generate_verification_code(length=4):
    """4자리 숫자 인증 코드를 생성합니다."""
    return "".join(random.choices(string.digits, k=length))

def _send_email_with_code_internal(user_email, code):
    """실제 이메일 발송 로직. Flask-Mail 설정을 사용합니다."""
    
    # Flask 앱 컨텍스트 및 mail 확장 객체 가져오기
    if not current_app:
        # 이 경우는 일반적으로 요청 컨텍스트 밖에서 호출될 때 발생 (예: 테스트 또는 잘못된 사용)
        print("CRITICAL ERROR (ict_login.py): No active Flask application context found in _send_email_with_code_internal.")
        return False
        
    mail_instance = current_app.extensions.get('mail')

    if not mail_instance:
        print("CRITICAL ERROR (ict_login.py): Flask-Mail (mail) extension not found in current_app. Cannot send email.")
        current_app.logger.critical("Flask-Mail (mail) extension not found in current_app for _send_email_with_code_internal.")
        return False
    
    # Flask 앱 컨피그에서 메일 설정 가져오기
    sender_name = current_app.config.get('MAIL_DEFAULT_SENDER_NAME', '404 Found 팀')
    sender_email = current_app.config.get('MAIL_USERNAME')
    
    if not sender_email:
        print("ERROR (ict_login.py): MAIL_USERNAME is not configured in app.config. Cannot send email.")
        current_app.logger.error("MAIL_USERNAME not configured in app.config for _send_email_with_code_internal.")
        return False

    subject = f"{sender_name} - 회원가입 이메일 인증 코드입니다."
    html_body = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 5px;">
        <h2 style="color: #007bff; text-align: center;">이메일 인증 요청</h2>
        <p>안녕하세요,</p>
        <p>회원가입을 계속하려면 다음 인증 코드를 입력해 주세요. 이 코드는 <strong style="color: #dc3545;">3분 동안</strong> 유효합니다.</p>
        <p style="text-align: center; font-size: 28px; font-weight: bold; color: #28a745; background-color: #f8f9fa; padding: 10px; border-radius: 4px; margin: 20px 0;">{code}</p>
        <p style="text-align: center; font-size: 0.9em; color: #6c757d;">요청하지 않으셨다면 해당 메일을 무시해 주세요.</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
        <p style="text-align: center; font-size: 0.8em; color: #aaa;">{sender_name} 드림</p>
    </div>
    """
    msg = FlaskMessage(subject, sender=(sender_name, sender_email), recipients=[user_email], html=html_body)
    
    try:
        mail_instance.send(msg) 
        current_app.logger.info(f"Verification code email sent to {user_email} via mail_instance from current_app.")
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email to {user_email} using mail_instance: {e} (MAIL_SERVER: {current_app.config.get('MAIL_SERVER')}, PORT: {current_app.config.get('MAIL_PORT')}, USER: {current_app.config.get('MAIL_USERNAME')})")
        return False

# --- 로직 함수들 (app.py에서 임포트하여 사용) ---
def send_verification_code_logic(email):
    if not email or '@' not in email or '.' not in email.split('@')[-1]:
        return False, "유효하지 않은 이메일 주소입니다."
    code = generate_verification_code()
    session['verification_code'] = code
    session['verification_code_time'] = datetime.utcnow().timestamp()
    session['verification_email_for_code'] = email
    if _send_email_with_code_internal(email, code):
        return True, "인증 코드가 이메일로 발송되었습니다. 3분 안에 입력해주세요."
    else:
        session.pop('verification_code', None)
        session.pop('verification_code_time', None)
        session.pop('verification_email_for_code', None)
        return False, "인증 코드 발송에 실패했습니다. 메일 서버 설정을 확인하거나 잠시 후 다시 시도해주세요. (서버 로그 확인 필요)"

def register_logic():
    message = ''
    form_values = request.form if request.method == 'POST' else {}
    if request.method == 'POST':
        user_id_form = request.form.get('User_id', '').strip()
        user_pw_form = request.form.get('User_pw') 
        user_email_form = request.form.get('User_email', '').strip().lower()
        user_name_form = request.form.get('User_name', '').strip()
        verification_code_input = request.form.get('verification_code_input', '').strip()
        if not all([user_id_form, user_pw_form, user_email_form, user_name_form]):
            message = '아이디, 비밀번호, 이메일, 이름은 모두 필수 항목입니다.'
        elif not verification_code_input:
            message = '이메일 인증 코드를 입력해주세요. (먼저 [이메일 인증] 버튼을 눌러 코드를 받아주세요)'
        else:
            stored_code = session.get('verification_code')
            stored_code_time_ts = session.get('verification_code_time')
            stored_email_for_code = session.get('verification_email_for_code', '').lower()
            if not stored_code or not stored_code_time_ts or not stored_email_for_code:
                message = '이메일 인증 세션 정보가 없습니다. [이메일 인증] 버튼을 다시 눌러주세요.'
            elif stored_email_for_code != user_email_form:
                message = '인증을 요청한 이메일과 가입하려는 이메일이 다릅니다. 이메일 확인 후 다시 시도해주세요.'
            elif verification_code_input != stored_code:
                message = '입력하신 인증 코드가 올바르지 않습니다.'
            else:
                try:
                    stored_code_time = datetime.fromtimestamp(float(stored_code_time_ts))
                    if datetime.utcnow() > stored_code_time + timedelta(minutes=3):
                        message = '인증 코드 유효 시간이 만료되었습니다. [이메일 인증] 버튼을 다시 눌러 코드를 받아주세요.'
                    else:
                        existing_user_by_id = User.query.filter_by(User_id=user_id_form).first()
                        existing_user_by_email = User.query.filter_by(User_email=user_email_form).first()
                        if existing_user_by_id:
                            message = '이미 존재하는 아이디입니다.'
                        elif existing_user_by_email:
                            message = '이미 사용 중인 이메일입니다.'
                        else:
                            hashed_password = generate_password_hash(user_pw_form)
                            new_user = User(
                                User_id=user_id_form, User_pw=hashed_password,
                                User_email=user_email_form, User_name=user_name_form
                            )
                            db.session.add(new_user)
                            db.session.commit()
                            session.pop('verification_code', None)
                            session.pop('verification_code_time', None)
                            session.pop('verification_email_for_code', None)
                            return redirect(url_for('login_page', message="회원가입이 완료되었습니다. 로그인해주세요.", message_class="success"))
                except ValueError:
                    message = "인증 코드 시간 정보에 오류가 있습니다. 다시 시도해주세요."
                    current_app.logger.error("Invalid timestamp format for verification_code_time in session.")
                except Exception as e:
                    db.session.rollback()
                    message = f'회원가입 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
                    current_app.logger.error(f"DB ERROR on register commit for {user_id_form}: {e}")
        return render_template_string(register_form_template, message=message, request={'form': form_values})
    return render_template_string(register_form_template, message=message, request={'form': form_values})

from flask_jwt_extended import create_access_token

def login_logic():
    message = request.args.get('message', '') 
    message_class = request.args.get('message_class', 'error')
    form_values = request.form if request.method == 'POST' else {}
    if request.method == 'POST':
        user_id_form = request.json.get("User_id", "").strip()
        user_pw_form = request.json.get("User_pw", "")
        print("id_form:",user_id_form)
        print("pw_form:",user_pw_form)
        if not user_id_form or not user_pw_form:
            message = '아이디와 비밀번호를 모두 입력해주세요.'
            message_class = 'error'

            return jsonify(errorMessage=message), 402
        else:
            user = User.query.filter_by(User_id=user_id_form).first()
            if user and check_password_hash(user.User_pw, user_pw_form):
                session['current_user_id'] = user.User_id

                return jsonify(success=True), 201
            else:
                message = '아이디 또는 비밀번호가 올바르지 않습니다.'
                message_class = 'error'
    return render_template_string(login_form_template, message=message, message_class=message_class, request={'form': form_values})

def logout_logic():
    session.pop('current_user_id', None)
    session.pop('verification_code', None)
    session.pop('verification_code_time', None)
    session.pop('verification_email_for_code', None)
    return redirect(url_for('login_page'))

def delete_account_logic():
    message = ''
    if 'current_user_id' not in session:
        return redirect(url_for('login_page'))
    user_id_to_delete = session['current_user_id']
    if request.method == 'POST':
        user = User.query.filter_by(User_id=user_id_to_delete).first()
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                session.pop('current_user_id', None)
                session.pop('verification_code', None) 
                session.pop('verification_code_time', None)
                session.pop('verification_email_for_code', None)
                return redirect(url_for('login_page', message="회원 탈퇴가 완료되었습니다.", message_class="success"))
            except Exception as e:
                db.session.rollback()
                message = f'회원 탈퇴 처리 중 오류가 발생했습니다.'
                current_app.logger.error(f"DB ERROR on delete account for {user_id_to_delete}: {e}")
        else:
            message = '탈퇴할 사용자 정보를 찾을 수 없습니다.'
            session.pop('current_user_id', None)
            return redirect(url_for('login_page', message=message, message_class="error")) 
    return render_template_string(delete_account_confirm_form_template, message=message, user_id_to_display=user_id_to_delete)