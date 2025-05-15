import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, session, current_app, jsonify # redirect, url_for, render_template_string 제거
from flask_mail import Message as FlaskMessage
import random
import string
from datetime import datetime, timedelta
import jwt

# --- 프로젝트 루트 경로 설정 ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# --- 경로 설정 끝 ---

from setting.db_connect import db 
from setting.models import User   

# --- JWT 액세스 토큰 생성 함수 ---
def generate_access_token(user_id):
    """
    사용자 ID를 기반으로 JWT 액세스 토큰을 생성합니다.
    Flask 앱 설정에서 SECRET_KEY와 TOKEN_EXPIRE_HOURS를 사용합니다.
    """
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=current_app.config.get('TOKEN_EXPIRE_HOURS', 1)), # 기본 1시간
            'iat': datetime.utcnow() # 토큰 발급 시간
        }
        # SECRET_KEY는 Flask 앱 설정에 반드시 있어야 합니다.
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
    except KeyError as e:
        current_app.logger.critical(f"Configuration missing: {e}. SECRET_KEY must be set in app.config.")
        return None
    except Exception as e:
        current_app.logger.error(f"Error generating access token for user_id {user_id}: {e}")
        return None

# --- 내부 헬퍼 함수 ---
def _generate_numeric_verification_code(length=4):
    """지정된 길이의 숫자 인증 코드를 생성합니다."""
    return "".join(random.choices(string.digits, k=length))

def _send_email_with_verification_code(user_email, code):
    """
    Flask-Mail을 사용하여 인증 코드를 이메일로 발송합니다.
    Flask 앱 컨텍스트 및 설정(MAIL_USERNAME 등)이 필요합니다.
    """
    if not current_app:
        # 이 로그는 일반적으로 테스트 환경이나 잘못된 호출 시 발생할 수 있습니다.
        print("CRITICAL: No active Flask application context found for sending email.")
        return False
        
    mail_instance = current_app.extensions.get('mail')
    if not mail_instance:
        current_app.logger.critical("Flask-Mail (mail) extension not found in current_app. Cannot send email.")
        return False
    
    sender_name = current_app.config.get('MAIL_DEFAULT_SENDER_NAME', 'Your Application Name') # 앱 이름으로 변경
    sender_email_address = current_app.config.get('MAIL_USERNAME')
    
    if not sender_email_address:
        current_app.logger.error("MAIL_USERNAME is not configured in app.config. Cannot send email.")
        return False

    subject = f"{sender_name} - 이메일 인증 코드 안내"
    # VERIFICATION_CODE_VALID_MINUTES는 Flask 앱 설정에서 가져옵니다.
    valid_minutes = current_app.config.get('VERIFICATION_CODE_VALID_MINUTES', 3)
    html_body = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 5px;">
        <h2 style="color: #007bff; text-align: center;">이메일 인증 요청</h2>
        <p>안녕하세요,</p>
        <p>요청하신 인증 코드는 다음과 같습니다. 이 코드는 <strong style="color: #dc3545;">{valid_minutes}분 동안</strong> 유효합니다.</p>
        <p style="text-align: center; font-size: 28px; font-weight: bold; color: #28a745; background-color: #f8f9fa; padding: 10px; border-radius: 4px; margin: 20px 0;">{code}</p>
        <p style="text-align: center; font-size: 0.9em; color: #6c757d;">본인이 요청하지 않으셨다면 이 메일을 무시해 주세요.</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
        <p style="text-align: center; font-size: 0.8em; color: #aaa;">{sender_name} 드림</p>
    </div>
    """
    msg = FlaskMessage(subject, sender=(sender_name, sender_email_address), recipients=[user_email], html=html_body)
    
    try:
        mail_instance.send(msg) 
        current_app.logger.info(f"Verification code email sent to {user_email} successfully.")
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email to {user_email} using mail_instance. Error: {e}. Mail Server: {current_app.config.get('MAIL_SERVER')}, Port: {current_app.config.get('MAIL_PORT')}, User: {current_app.config.get('MAIL_USERNAME')}")
        return False

# --- API 로직 함수들 ---

def request_email_verification_code_api():
    """
    프론트엔드에서 사용자가 이메일을 입력하고 '인증 코드 발송' 버튼을 누르면 호출됩니다.
    """
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'status': 'error', 'message': '이메일 주소가 필요합니다.'}), 400
    
    email_to_verify = data['email'].strip().lower()
    if not email_to_verify or '@' not in email_to_verify or '.' not in email_to_verify.split('@')[-1]:
        return jsonify({'status': 'error', 'message': '유효한 이메일 주소를 입력해주세요.'}), 400
    
    # 선택: 이미 가입된 이메일인지 확인 (회원가입 시나리오)
    if User.query.filter_by(User_email=email_to_verify).first():
         return jsonify({'status': 'error', 'message': '이미 사용 중인 이메일입니다.'}), 409 # Conflict

    verification_code = _generate_numeric_verification_code()
    
    # 세션에 인증 코드, 발송 시간, 대상 이메일 저장
    session['verification_code'] = verification_code
    session['verification_code_timestamp'] = datetime.utcnow().timestamp()
    session['verification_target_email'] = email_to_verify # 어떤 이메일에 대한 코드인지 명시

    if _send_email_with_verification_code(email_to_verify, verification_code):
        valid_minutes = current_app.config.get('VERIFICATION_CODE_VALID_MINUTES', 3)
        return jsonify({'status': 'success', 'message': f'인증 코드가 {email_to_verify}(으)로 발송되었습니다. {valid_minutes}분 안에 입력해주세요.'}), 200
    else:
        # 실패 시 세션 정보 즉시 삭제
        session.pop('verification_code', None)
        session.pop('verification_code_timestamp', None)
        session.pop('verification_target_email', None)
        return jsonify({'status': 'error', 'message': '인증 코드 이메일 발송에 실패했습니다. 서버 로그를 확인하거나 관리자에게 문의해주세요.'}), 500

def register_user_api():
    """
    사용자 회원가입 API 엔드포인트 로직.
    """
    if request.method != 'POST': # 이 체크는 보통 Flask 라우트에서 처리
        return jsonify({'status': 'error', 'message': 'POST 요청만 허용됩니다.'}), 405

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': '요청 본문이 비어있거나 JSON 형식이 아닙니다.'}), 400

    # 필수 필드 검사
    required_fields = ['User_id', 'User_pw', 'User_email', 'User_name', 'verification_code_input']
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({'status': 'error', 'message': f"필수 항목이 누락되었습니다: {', '.join(missing_fields)}"}), 400

    user_id = data['User_id'].strip()
    user_pw = data['User_pw'] # 비밀번호는 스트립하지 않음 (공백도 비밀번호의 일부일 수 있음)
    user_email = data['User_email'].strip().lower()
    user_name = data['User_name'].strip()
    verification_code_input = data['verification_code_input'].strip()

    # 세션에서 인증 정보 가져오기
    stored_code = session.get('verification_code')
    stored_code_timestamp = session.get('verification_code_timestamp')
    stored_target_email = session.get('verification_target_email', '').lower()

    if not stored_code or not stored_code_timestamp or not stored_target_email:
        return jsonify({'status': 'error', 'message': '이메일 인증 세션 정보가 유효하지 않습니다. 인증 코드를 다시 요청해주세요.'}), 400
    
    if stored_target_email != user_email:
        return jsonify({'status': 'error', 'message': '인증 코드를 받은 이메일 주소와 가입하려는 이메일 주소가 일치하지 않습니다.'}), 400

    if verification_code_input != stored_code:
        return jsonify({'status': 'error', 'message': '입력하신 인증 코드가 올바르지 않습니다.'}), 400

    try:
        code_issue_time = datetime.fromtimestamp(float(stored_code_timestamp))
        valid_duration = timedelta(minutes=current_app.config.get('VERIFICATION_CODE_VALID_MINUTES', 3))
        if datetime.utcnow() > code_issue_time + valid_duration:
            # 만료 시 세션 정보 정리
            session.pop('verification_code', None)
            session.pop('verification_code_timestamp', None)
            session.pop('verification_target_email', None)
            return jsonify({'status': 'error', 'message': '인증 코드의 유효 시간이 만료되었습니다. 인증 코드를 다시 요청해주세요.'}), 400
    except ValueError:
        current_app.logger.error("Invalid timestamp format for 'verification_code_timestamp' in session during registration.")
        return jsonify({'status': 'error', 'message': '인증 코드 시간 정보 처리 중 오류가 발생했습니다. 다시 시도해주세요.'}), 500

    # 사용자 중복 검사 (아이디 및 이메일)
    if User.query.filter_by(User_id=user_id).first():
        return jsonify({'status': 'error', 'message': '이미 사용 중인 아이디입니다.'}), 409 # Conflict
    if User.query.filter_by(User_email=user_email).first():
        return jsonify({'status': 'error', 'message': '이미 가입된 이메일 주소입니다.'}), 409 # Conflict

    try:
        hashed_password = generate_password_hash(user_pw)
        new_user = User(
            User_id=user_id, 
            User_pw=hashed_password,
            User_email=user_email, 
            User_name=user_name
        )
        db.session.add(new_user)
        db.session.commit()

        # 회원가입 성공 후 인증 관련 세션 정보 정리
        session.pop('verification_code', None)
        session.pop('verification_code_timestamp', None)
        session.pop('verification_target_email', None)
        
        current_app.logger.info(f"New user registered successfully: User ID '{user_id}', Email '{user_email}'.")
        return jsonify({'status': 'success', 'message': '회원가입이 성공적으로 완료되었습니다. 이제 로그인할 수 있습니다.'}), 201 # Created
    except Exception as e:
        db.session.rollback() # 오류 발생 시 롤백
        current_app.logger.error(f"Database error during registration for User ID '{user_id}': {e}")
        return jsonify({'status': 'error', 'message': '회원가입 처리 중 서버 내부 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'}), 500

def login_user_api():
    """
    사용자 로그인 API 엔드포인트 로직.
    성공 시 JWT 액세스 토큰을 발급합니다.
    """
    if request.method != 'POST':
        return jsonify({'status': 'error', 'message': 'POST 요청만 허용됩니다.'}), 405

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': '요청 본문이 비어있거나 JSON 형식이 아닙니다.'}), 400

    user_id_input = data.get('User_id', '').strip()
    password_input = data.get('User_pw') # 비밀번호는 스트립하지 않음

    if not user_id_input or not password_input:
        return jsonify({'status': 'error', 'message': '아이디와 비밀번호를 모두 입력해주세요.'}), 400

    user = User.query.filter_by(User_id=user_id_input).first()

    if user and check_password_hash(user.User_pw, password_input):
        access_token = generate_access_token(user.User_id) # 모델의 User_id 필드명 사용
        if access_token:
            current_app.logger.info(f"User '{user.User_id}' logged in successfully.")
            # 로그인 성공 시 세션에 사용자 정보 저장 (선택 사항, API에서는 토큰으로 충분)
            # session['current_user_id'] = user.User_id # 만약 서버측 세션도 필요하다면
            return jsonify({
                'status': 'success',
                'message': '로그인에 성공했습니다.',
                'access_token': access_token,
                'user': { # 프론트엔드에서 활용할 수 있는 사용자 정보
                    'user_id': user.User_id,
                    'user_name': user.User_name,
                    'user_email': user.User_email 
                }
            }), 200
        else:
            # 토큰 생성 실패는 심각한 내부 오류일 가능성이 높음
            current_app.logger.error(f"Access token generation failed for user '{user.User_id}' during login.")
            return jsonify({'status': 'error', 'message': '로그인 처리 중 내부 서버 오류가 발생했습니다. (토큰 생성 실패)'}), 500
    else:
        current_app.logger.warning(f"Failed login attempt for User ID: '{user_id_input}'. Invalid credentials.")
        return jsonify({'status': 401}) # Unauthorized

def logout_user_api():
    """
    사용자 로그아웃 API 엔드포인트 로직.
    API 기반 로그아웃은 주로 클라이언트 측에서 토큰을 삭제하는 방식으로 이루어집니다.
    서버 측에서는 토큰 블랙리스트를 구현하거나, 관련 세션을 정리할 수 있습니다.
    """
    # 이메일 인증 관련 세션 정보가 있다면 정리 (선택 사항)
    session.pop('verification_code', None)
    session.pop('verification_code_timestamp', None)
    session.pop('verification_target_email', None)
    
    # 만약 Flask-Login 같은 라이브러리로 세션 기반 로그인을 병행한다면 여기서 logout_user() 호출
    # session.pop('current_user_id', None) # 만약 로그인 시 세션에 사용자 ID를 저장했다면

    # Flask-JWT-Extended 사용 시, 여기에 토큰을 블랙리스트에 추가하는 로직이 들어갈 수 있습니다.
    # 예: from flask_jwt_extended import get_jti
    # jti = get_jti(encoded_token=request.headers.get("Authorization").split()[1]) # 헤더에서 토큰 가져와 jti 추출
    # add_token_to_blacklist(jti, current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    
    current_app.logger.info("Logout API called. Client should discard the token.")
    return jsonify({'status': 'success', 'message': '로그아웃 요청이 처리되었습니다. 클라이언트 측에서 토큰을 안전하게 삭제해주세요.'}), 200

def delete_user_account_api(authenticated_user_id): # 인증된 사용자의 ID를 인자로 받아야 함
    """
    사용자 계정 삭제 API 엔드포인트 로직.
    반드시 인증된 사용자만 이 기능을 호출할 수 있도록 보호되어야 합니다 (예: @jwt_required).
    """
    if request.method != 'DELETE': # RESTful API에서는 DELETE 메소드 사용
        return jsonify({'status': 'error', 'message': 'DELETE 요청만 허용됩니다.'}), 405

    user_to_delete = User.query.filter_by(User_id=authenticated_user_id).first()

    if not user_to_delete:
        # 토큰은 유효하지만 해당 사용자가 DB에 없는 매우 드문 경우.
        current_app.logger.warning(f"Attempt to delete a non-existent user account with User ID: '{authenticated_user_id}' (possibly already deleted or data inconsistency).")
        return jsonify({'status': 'error', 'message': '삭제할 사용자 계정을 찾을 수 없습니다.'}), 404 # Not Found
    
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        current_app.logger.info(f"User account for User ID '{authenticated_user_id}' has been successfully deleted.")
        
        # 계정 삭제 후 관련 세션 정보가 있다면 모두 정리
        session.clear() 

        # 해당 사용자의 모든 활성 토큰을 무효화(블랙리스트)하는 로직 추가 필요 (Flask-JWT-Extended 등 사용)
        return jsonify({'status': 'success', 'message': '회원 탈퇴가 성공적으로 처리되었습니다.'}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Database error during account deletion for User ID '{authenticated_user_id}': {e}")
        return jsonify({'status': 'error', 'message': '계정 삭제 처리 중 서버 내부 오류가 발생했습니다.'}), 500