from flask import Flask, request, jsonify
from flask_cors import CORS
from api.chat_api import chat_blueprint
from api.rag_api import rag_blueprint
from config import OPENAI_API_KEY

import openai
from openai import OpenAI

# flask_backend/api/app.py
import sys
import os
import json # delete_notice에서 첨부파일 처리를 위해 추가

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_blueprint, url_prefix="/api/chat")
app.register_blueprint(rag_blueprint, url_prefix="/api/rag")

client = OpenAI(api_key=OPENAI_API_KEY)

# --- 프로젝트 루트 경로 설정 ---
# 이 파일(api/app.py)의 부모 디렉토리(flask_backend)가 PROJECT_ROOT가 됩니다.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
print(f"DEBUG: PROJECT_ROOT set to: {PROJECT_ROOT}")
# --- 경로 설정 끝 ---
print("--- Checking sys.path ---")
for p in sys.path:
    print(p)
print("-------------------------")
# --- .env 파일 로드 (애플리케이션 설정 전에 가장 먼저 실행) ---
from dotenv import load_dotenv
dotenv_path = os.path.join(PROJECT_ROOT, '.env')
print(f"DEBUG: Attempting to load .env file from: {dotenv_path}")
dotenv_loaded = load_dotenv(dotenv_path)
print(f"DEBUG: load_dotenv() successful? {dotenv_loaded}")
if not dotenv_loaded:
    print(f"WARNING: .env file was NOT loaded from '{dotenv_path}'. Using environment variables or defaults.")
# --- .env 파일 로드 끝 ---

# --- Flask 및 기타 모듈 임포트 ---
from flask import Flask, session, jsonify, request as flask_request, redirect, url_for, flash # flash 추가
from flask_mail import Mail
# db_connect.py와 models.py는 PROJECT_ROOT가 sys.path에 추가된 후 임포트
from setting.db_connect import init_db, db # init_db 함수와 db 객체
from setting.models import User, Notice # User, Notice 모델 임포트
# api.user_api에서 로직 함수들 임포트 (user_api.py로 파일명 변경 가정)
from api.user_api import (
    register_logic,
    login_logic,
    logout_logic,
    delete_account_logic,
    send_verification_code_logic
)
# notice_api에서 로직 함수들 임포트
from api.notice_api import (
    show_notice_logic,
    add_notice_logic,
    show_notice_detail_logic,
    get_all_notices_logic,
    get_notice_detail_logic
)

print("DEBUG: All top-level imports successful.")
app.config['PROJECT_ROOT'] = PROJECT_ROOT
print("DEBUG: Flask app object created.")

# --- 환경 변수에서 Flask 설정 로드 ---
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
retrieved_secret_key_for_debug = app.config['SECRET_KEY']
print(f"DEBUG: FLASK_SECRET_KEY from os.environ (used by app): '{retrieved_secret_key_for_debug}'")

if not app.config['SECRET_KEY']:
    print("CRITICAL ERROR: FLASK_SECRET_KEY가 .env 파일 또는 환경 변수에 설정되지 않았습니다! 앱을 시작할 수 없습니다.")
    if dotenv_loaded:
        print("DEBUG: .env 파일은 로드되었으나, 그 안에 FLASK_SECRET_KEY가 없거나 값이 비어있을 수 있습니다. .env 파일 내용을 다시 확인해주세요.")
    else:
        print("DEBUG: .env 파일 자체가 로드되지 않았습니다. 경로와 파일 존재 여부, 권한 등을 확인하세요.")
    sys.exit(1)

# Flask-Mail 설정
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
default_sender_name = os.environ.get('MAIL_DEFAULT_SENDER_NAME', '404 Found 팀')
app.config['MAIL_DEFAULT_SENDER'] = (default_sender_name, app.config['MAIL_USERNAME']) if app.config['MAIL_USERNAME'] else default_sender_name

if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    print("WARNING: MAIL_USERNAME 또는 MAIL_PASSWORD가 .env 파일이나 환경 변수에 설정되지 않았습니다. 이메일 발송 기능이 실패할 수 있습니다.")

mail = Mail(app)
print("DEBUG: Flask-Mail (mail object) initialized.")
# --- Flask 설정 끝 ---

# --- 데이터베이스 초기화 ---
init_db(app)
print("DEBUG: init_db(app) called to configure database URI.")

with app.app_context():
    print("DEBUG: Entered app_context for db.create_all().")
    try:
        db.create_all()
        print("DEBUG: db.create_all() finished successfully.")
    except Exception as e:
        print(f"ERROR: db.create_all() failed: {e}")
# --- 데이터베이스 초기화 끝 ---


# --- 기본 라우트 ---
@app.route('/')
def home():
    if 'current_user_id' in session:
        user_id = session['current_user_id']
        return (
            f"""
            <div style="padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center;">
                <h2>{user_id}님, 환영합니다!</h2>
                <p>
                    <a href='{url_for('logout_page')}' style="text-decoration: none; color: #007bff; margin: 0 10px; padding: 8px 15px; border: 1px solid #007bff; border-radius: 4px;">로그아웃</a>
                    <a href='{url_for('delete_account_page')}' style="text-decoration: none; color: #dc3545; margin: 0 10px; padding: 8px 15px; border: 1px solid #dc3545; border-radius: 4px;">회원탈퇴</a>
                    <a href='{url_for('show_notice_page')}' style="text-decoration: none; color: #17a2b8; margin: 0 10px; padding: 8px 15px; border: 1px solid #17a2b8; border-radius: 4px;">공지사항</a>
                </p>
            </div>
            """
        )
    return (
        """
        <div style="padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center;">
            <h2>로그인이 필요합니다.</h2>
            <p>
                <a href='""" + url_for('login_page') + """' style="text-decoration: none; color: #007bff; margin: 0 10px; padding: 8px 15px; border: 1px solid #007bff; border-radius: 4px;">로그인</a>
                <a href='""" + url_for('register_page') + """' style="text-decoration: none; color: #28a745; margin: 0 10px; padding: 8px 15px; border: 1px solid #28a745; border-radius: 4px;">회원가입</a>
                <a href='""" + url_for('show_notice_page') + """' style="text-decoration: none; color: #17a2b8; margin: 0 10px; padding: 8px 15px; border: 1px solid #17a2b8; border-radius: 4px;">공지사항 보기</a>
            </p>
        </div>
        """
    )

# --- 사용자 인증 관련 라우트 ---
@app.route('/send_verification_code', methods=['POST'])
def send_code_route():
    email = flask_request.json.get('email')
    if not email:
        return jsonify({'success': False, 'message': '이메일 주소가 필요합니다.'}), 400
    success, message = send_verification_code_logic(email)
    if success:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message}), 500 if "실패" in message else 400

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return register_logic()

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return login_logic()

@app.route('/logout')
def logout_page():
    return logout_logic()

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account_page():
    return delete_account_logic()

print("DEBUG: User auth routes defined.")

# --- 공지사항 관련 라우트 ---
@app.route('/notice', methods=['GET'])
def show_notice_page():
    return show_notice_logic()

@app.route('/api/notices', methods=['POST']) # 공지 추가 API (add_notice_logic에서 권한 처리)
def add_notice():
    return add_notice_logic()

@app.route('/api/notices/<int:notice_id>/delete', methods=['POST']) # 공지 삭제 API
def delete_notice(notice_id):
    current_user_id = session.get('current_user_id')
    if not current_user_id:
        flash('삭제 권한이 없습니다. 로그인이 필요합니다.', 'error')
        return redirect(url_for('login_page'))

    user = User.query.filter_by(User_id=current_user_id).first()
    if not user or user.User_role != 1: # 관리자(User_role == 1)만 삭제 가능
        flash('삭제 권한이 없습니다.', 'error')
        return redirect(url_for('show_notice_page'))

    notice_to_delete = Notice.query.filter_by(notice_id=notice_id).first()
    if notice_to_delete:
        try:
            # 첨부파일 삭제 로직
            if notice_to_delete.attachments:
                attachments_list = []
                try:
                    loaded_attachments = json.loads(notice_to_delete.attachments)
                    if isinstance(loaded_attachments, list):
                        attachments_list = loaded_attachments
                    elif isinstance(loaded_attachments, str) and loaded_attachments: # 단일 파일 경로 문자열
                        attachments_list = [loaded_attachments]
                except json.JSONDecodeError:
                    if isinstance(notice_to_delete.attachments, str) and notice_to_delete.attachments: # 파싱 실패 시 단일 파일 경로로 간주
                        attachments_list = [notice_to_delete.attachments]
                
                print(f"DEBUG: Attachments to delete for notice {notice_id}: {attachments_list}")

                for file_url_path in attachments_list:
                    if not file_url_path or not file_url_path.startswith('/static/uploads/'):
                        print(f"WARNING: Invalid or unexpected attachment path: {file_url_path}")
                        continue
                    
                    # URL 경로 (/static/uploads/filename.ext) 에서 실제 파일 시스템 경로로 변환
                    # PROJECT_ROOT/static/uploads/filename.ext
                    # app.py는 PROJECT_ROOT/api/ 에 있으므로, PROJECT_ROOT를 사용
                    relative_path = file_url_path.lstrip('/') # "static/uploads/filename.ext"
                    actual_file_path = os.path.join(PROJECT_ROOT, relative_path)
                    
                    print(f"DEBUG: Attempting to delete attachment file: {actual_file_path}")
                    if os.path.exists(actual_file_path):
                        try:
                            os.remove(actual_file_path)
                            print(f"INFO: Deleted attachment file: {actual_file_path}")
                        except OSError as e:
                            print(f"ERROR: Could not delete attachment file {actual_file_path}: {e}")
                            # 파일 삭제 실패 시 flash 메시지를 추가하거나 로깅할 수 있습니다.
                            # flash(f'첨부파일 "{os.path.basename(actual_file_path)}" 삭제 실패.', 'warning')
                    else:
                        print(f"WARNING: Attachment file not found, skipping deletion: {actual_file_path}")
            
            db.session.delete(notice_to_delete)
            db.session.commit()
            flash('공지가 성공적으로 삭제되었습니다.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'공지 삭제 중 오류가 발생했습니다: {str(e)}', 'error')
            app.logger.error(f"Error deleting notice {notice_id}: {e}")
    else:
        flash('삭제할 공지를 찾을 수 없습니다.', 'error')
    
    return redirect(url_for('show_notice_page'))

@app.route('/api/notices') # 모든 공지사항 JSON으로 가져오기 (현재는 권한 X)
def get_all_notices():
    return jsonify(get_all_notices_logic())

@app.route('/api/notices/<int:notice_id>') # 특정 공지사항 JSON으로 가져오기 (현재는 권한 X)
def get_one_notice(notice_id):
    result = get_notice_detail_logic(notice_id)
    if result is None:
        return jsonify({'error': '공지 없음'}), 404
    return jsonify(result)

@app.route('/notice/<int:notice_id>', methods=['GET']) # 공지사항 상세 페이지
def notice_detail_page(notice_id):
    return show_notice_detail_logic(notice_id)

print("DEBUG: Notice routes defined.")




@app.route('/chat_api', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 수원대학교 지능형SW융합대학 안내 챗봇입니다."},
                {"role": "user", "content": user_message}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"response": f"⚠️ GPT 오류: {str(e)}"}), 500


# ✅ 실행: 여기서만 학습시키기
if __name__ == '__main__':

    from llm_utils.embedding import load_and_split_documents
    from llm_utils.vector_store import initialize_vectorstore

    docs = load_and_split_documents()
    initialize_vectorstore(docs)
    

    print("DEBUG: Entering `if __name__ == '__main__'` block to start development server.")
    # 로그 레벨 설정 (선택 사항, 더 자세한 로그를 보고 싶을 경우)
    # import logging
    # logging.basicConfig(level=logging.INFO)
    # app.logger.setLevel(logging.INFO)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
