# flask_backend/app.py (또는 프로젝트 루트의 app.py)

import sys
import os
import json
from datetime import timedelta # JWT 만료 시간 설정용

# --- .env 파일 로드 (애플리케이션 설정 전에 가장 먼저 실행) ---
# 이 파일(app.py)이 프로젝트 루트에 있다고 가정합니다.
# 만약 하위 디렉토리(예: api/app.py)에 있다면 PROJECT_ROOT 경로를 조정해야 합니다.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
dotenv_path = os.path.join(PROJECT_ROOT, '.env')
dotenv_loaded = load_dotenv(dotenv_path)
if not dotenv_loaded:
    print(f"WARNING: .env file was NOT loaded from '{dotenv_path}'. Ensure it exists or environment variables are set.")
# --- .env 파일 로드 끝 ---

from flask import Flask, jsonify, request as flask_request
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token, get_jwt
)

# --- 블루프린트 임포트 ---
# 실제 파일 경로에 맞게 수정해주세요
from api.chat_api import chat_blueprint
from api.rag_api import rag_blueprint

# --- DB 및 모델 임포트 ---
from setting.db_connect import init_db, db # init_db 함수와 db 객체
from setting.models import User, Notice    # User, Notice 모델 임포트

# --- API 로직 함수 임포트 ---
# 이전 대화에서 API 스타일로 리팩토링된 함수들을 임포트
# (파일명을 잘 확인하시고)
from api.user_api import (
    request_email_verification_code_api,
    register_user_api,
    login_user_api,  # 이 함수는 내부에서 create_access_token 등을 호출하거나, 인자로 받는게 가능
    logout_user_api,
    delete_user_account_api
)
from api.notice_api import (
    create_notice_api,
    get_all_notices_api,
    get_notice_by_id_api,
    update_notice_api,
    delete_notice_api
)

# --- OpenAI 클라이언트 초기화 (선택 사항: 블루프린트나 다른 모듈에서 관리 가능) ---
# from config import OPENAI_API_KEY # OPENAI_API_KEY는 config.py 또는 .env에서 관리
# import openai
# client = openai.OpenAI(api_key=OPENAI_API_KEY) # OPENAI_API_KEY 환경변수 사용 권장


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) # API 경로에 대해 모든 출처 허용 (개발용)
                                                 # 프로덕션에서는 특정 출처 지정: origins=["http://localhost:3000", "https://suwonn.com"]

# --- Flask 애플리케이션 설정 ---
app.config['PROJECT_ROOT'] = PROJECT_ROOT # notice_api 등에서 사용 가능하도록
app.config['UPLOAD_FOLDER'] = os.path.join(PROJECT_ROOT, 'static', 'uploads') # 첨부파일 업로드 경로

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
if not app.config['SECRET_KEY']:
    print("CRITICAL ERROR: FLASK_SECRET_KEY is not set in .env or environment variables. App cannot start.")
    sys.exit(1)

# JWT Extended 설정
app.config["JWT_SECRET_KEY"] = app.config['SECRET_KEY'] # JWT 서명에도 동일한 시크릿 키 사용 권장
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 1)))
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 30)))
app.config["JWT_BLACKLIST_ENABLED"] = True  # 토큰 블랙리스트 사용 (로그아웃 시)
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"] # access, refresh 토큰 모두 블랙리스트 체크

jwt = JWTManager(app)

# Flask-Mail 설정
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') # Gmail 사용 시 앱 비밀번호
default_sender_name = os.environ.get('MAIL_DEFAULT_SENDER_NAME', '404 Found 팀') # 앱 이름으로 변경
app.config['MAIL_DEFAULT_SENDER'] = (default_sender_name, app.config['MAIL_USERNAME']) if app.config['MAIL_USERNAME'] else default_sender_name
app.config['MAIL_DEFAULT_SENDER_NAME'] = default_sender_name # _send_email_with_code_internal 에서 사용
app.config['VERIFICATION_CODE_VALID_MINUTES'] = int(os.environ.get('VERIFICATION_CODE_VALID_MINUTES', 3)) # 이메일 인증 코드 유효 시간

if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    print("WARNING: MAIL_USERNAME or MAIL_PASSWORD is not set. Email functionality may fail.")

mail = Mail(app)
# --- Flask 설정 끝 ---

# --- 데이터베이스 초기화 ---
init_db(app) # DB URI 설정
with app.app_context():
    db.create_all() # 테이블 생성
# --- 데이터베이스 초기화 끝 ---

# --- JWT 토큰 블랙리스트 구현 (간단한 인메모리 방식, 프로덕션에서는 Redis/DB 권장) ---
# 이 set은 app.py가 재시작될 때마다 초기화됩니다.
token_blacklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist_callback(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in token_blacklist
# --- JWT 블랙리스트 끝 ---

# --- 블루프린트 등록 ---
app.register_blueprint(chat_blueprint, url_prefix="/api/chat")
app.register_blueprint(rag_blueprint, url_prefix="/api/rag")
# (선택) 사용자 인증 및 공지사항 API 라우트를 위한 블루프린트 구성 권장
# from api.auth_routes import auth_bp
# app.register_blueprint(auth_bp, url_prefix="/api/auth")
# from api.notice_routes import notice_bp
# app.register_blueprint(notice_bp, url_prefix="/api/notices")

# --- 헬퍼 함수: 사용자 역할 가져오기 ---
def get_user_role_from_db(user_id_from_token):
    user = User.query.filter_by(User_id=user_id_from_token).first()
    return user.User_role if user else 0 # 사용자를 찾을 수 없으면 기본 역할(예: 0) 반환

# --- API 라우트 정의 ---
@app.route('/api/health', methods=['GET'])
def health_check():
    """API 서버 상태 확인 엔드포인트"""
    return jsonify({'status': 'ok', 'message': 'API server is healthy and running.'}), 200

# --- 사용자 인증 API 라우트 ---
# (이하 라우트들은 별도 블루프린트(예: auth_bp)로 관리하는 것이 좋습니다)

@app.route('/api/auth/send-verification-code', methods=['POST'])
def route_send_verification_code():
    # request_email_verification_code_api 함수는 JSON 요청을 받고 JSON 응답을 반환
    return request_email_verification_code_api()

@app.route('/api/auth/register', methods=['POST'])
def route_register():
    # register_user_api 함수는 JSON 요청을 받고 JSON 응답(성공/실패 메시지)을 반환
    return register_user_api()

@app.route('/api/auth/login', methods=['POST'])
def route_login():
    # login_user_api 함수가 사용자 ID를 반환하면, 여기서 토큰 생성
    response_data, status_code = login_user_api() # login_user_api는 (dict, status_code) 반환 가정
    if status_code == 200 and response_data.get('status') == 'success':
        user_id = response_data['data']['user']['user_id'] # login_user_api 응답 구조에 따라 조정
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id) # 리프레시 토큰도 발급
        response_data['data']['access_token'] = access_token
        response_data['data']['refresh_token'] = refresh_token
        return jsonify(response_data), status_code
    return jsonify(response_data), status_code


@app.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True) # 리프레시 토큰으로만 접근 가능
def route_refresh_token():
    current_user_id = get_jwt_identity() # 리프레시 토큰에서 사용자 식별자(identity) 가져오기
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify(access_token=new_access_token), 200

@app.route('/api/auth/logout', methods=['POST'])
@jwt_required() # 액세스 토큰으로 접근
def route_logout():
    access_token_jti = get_jwt()["jti"]
    token_blacklist.add(access_token_jti) # 현재 액세스 토큰을 블랙리스트에 추가

    # (선택) 리프레시 토큰도 무효화하려면 클라이언트가 리프레시 토큰을 함께 보내야 함
    # refresh_token_jti = request.json.get('refresh_token_jti') # 예시
    # if refresh_token_jti:
    #     token_blacklist.add(refresh_token_jti)
    return logout_user_api() # 이 함수는 단순 성공 메시지 반환

@app.route('/api/auth/account', methods=['DELETE'])
@jwt_required()
def route_delete_account():
    current_user_id = get_jwt_identity()
    # delete_user_account_api 함수는 current_user_id를 받아 계정 삭제 처리
    # 성공적으로 삭제되면, 관련된 모든 토큰 (access, refresh)무효화
    # 이 부분은 delete_user_account_api 내부, 여기서 처리
    response_data, status_code = delete_user_account_api(current_user_id)
    if status_code == 200: # 성공 시 현재 사용 중인 토큰들을 블랙리스트에 추가 (선택적)
        # access_jti = get_jwt()["jti"]
        # token_blacklist.add(access_jti)
        # (만약 리프레시 토큰도 있다면)
        pass
    return jsonify(response_data), status_code

@app.route('/api/users/me', methods=['GET'])
@jwt_required()
def route_get_current_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(User_id=current_user_id).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found or token invalid."}), 404
    return jsonify({
        "status": "success",
        "data": {
            "user_id": user.User_id,
            "user_name": user.User_name,
            "user_email": user.User_email,
            "user_role": user.User_role # 역할 정보도 반환
        }
    }), 200

# --- 공지사항 API 라우트 ---
@app.route('/api/notices', methods=['POST'])
@jwt_required()
def route_create_notice():
    current_user_id = get_jwt_identity()
    user_role = get_user_role_from_db(current_user_id) # DB에서 역할 조회
    return create_notice_api(current_user_id, user_role)

@app.route('/api/notices', methods=['GET'])
def route_get_all_notices():
    return get_all_notices_api()

@app.route('/api/notices/<int:notice_id>', methods=['GET'])
def route_get_notice_by_id(notice_id):
    return get_notice_by_id_api(notice_id)

@app.route('/api/notices/<int:notice_id>', methods=['PUT'])
@jwt_required()
def route_update_notice(notice_id):
    current_user_id = get_jwt_identity()
    user_role = get_user_role_from_db(current_user_id)
    return update_notice_api(notice_id, current_user_id, user_role)

@app.route('/api/notices/<int:notice_id>', methods=['DELETE'])
@jwt_required()
def route_delete_notice(notice_id):
    current_user_id = get_jwt_identity()
    user_role = get_user_role_from_db(current_user_id)
    return delete_notice_api(notice_id, current_user_id, user_role)

# --- 선택 전역 에러 핸들러 ---
@app.errorhandler(400) # Bad Request
def bad_request_error(error):
    return jsonify(status="error", message=str(error.description if hasattr(error, 'description') else "Bad request")), 400

@app.errorhandler(401) # Unauthorized
def unauthorized_error(error):
    return jsonify(status="error", message=str(error.description if hasattr(error, 'description') else "Unauthorized")), 401

@app.errorhandler(403) # Forbidden
def forbidden_error(error):
    return jsonify(status="error", message=str(error.description if hasattr(error, 'description') else "Forbidden")), 403

@app.errorhandler(404) # Not Found
def not_found_error(error):
    return jsonify(status="error", message=str(error.description if hasattr(error, 'description') else "Resource not found")), 404

@app.errorhandler(500) # Internal Server Error
def internal_server_error(error):
    app.logger.error(f"Internal Server Error: {error}") # 서버 로그에 상세 에러 기록
    return jsonify(status="error", message="Internal server error. Please try again later."), 500


# --- 애플리케이션 실행 ---
if __name__ == '__main__':
    # RAG 관련 초기화 (필요시, 앱 시작 시 한 번만 실행)
    from llm_utils.embedding import load_and_split_documents
    from llm_utils.vector_store import initialize_vectorstore
    with app.app_context():
         docs = load_and_split_documents()
         initialize_vectorstore(docs)
         print("INFO: RAG vector store initialized.")

    print("INFO: Starting Flask development server...")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))