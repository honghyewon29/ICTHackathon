# notice_api.py
import hashlib
import os
import json
from flask import request, redirect, render_template_string, session, current_app, flash, url_for
from werkzeug.utils import secure_filename
from setting.models import User, Notice # User, Notice 모델 임포트
# db_connect는 직접 사용하지 않으므로 여기서는 불필요할 수 있으나, User 쿼리를 위해 db 객체가 필요할 수 있습니다.
# from setting.db_connect import db # User 쿼리를 위해 필요하다면 추가

# --- 스타일 ---
common_style = """
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f4f7f6;
        margin: 0;
        padding: 20px;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        min-height: 90vh;
        flex-direction: column; /* 컨테이너들을 세로로 정렬 */
    }
    .container, .detail-wrapper { /* 공통 컨테이너 스타일 */
        background-color: #fff;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 800px; /* 최대 너비 설정 */
        margin: 20px auto; /* 위아래 마진 및 가로 중앙 정렬 */
    }
    h1, h2 {
        color: #333;
        margin-bottom: 25px;
        text-align: center;
    }
    h1 { font-size: 2em; margin-bottom: 30px; }
    h2 { font-size: 1.5em; margin-top: 0; }
    .form-group { margin-bottom: 20px; }
    .form-group label { display: block; margin-bottom: 8px; color: #555; font-weight: bold; }
    .form-group input[type="text"],
    .form-group input[type="password"],
    .form-group input[type="email"],
    .form-group textarea,
    .form-group select {
        width: calc(100% - 22px); /* padding 고려 */
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        box-sizing: border-box;
        font-size: 1em;
    }
    .form-group textarea { min-height: 100px; resize: vertical; }
    .form-group input[type="submit"], .button-link, .button {
        display: inline-block;
        width: auto;
        padding: 10px 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        text-decoration: none;
        text-align:center;
        font-size:1em;
        margin-right: 5px;
    }
    .form-group input[type="submit"]:hover,
    .button-link:hover,
    .button:hover { background-color: #0056b3; }
    .message { /* flash 메시지 스타일 */
        text-align: center;
        padding: 10px;
        margin: 10px auto 20px auto; /* 위아래 마진 및 가로 중앙 정렬 */
        max-width: 800px; /* 다른 컨테이너와 너비 일치 */
        border-radius: 4px;
        font-size: 0.9em;
    }
    .message.error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .message.success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .message.info { background-color: #e7f3fe; color: #31708f; border: 1px solid #bce8f1; }
    /* ... (기존 table, td, th 등 스타일 유지) ... */
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background-color: #e9ecef; color: #495057; font-weight: bold; border-top: 1px solid #ddd;}
    td a { color: #007bff; text-decoration: none; }
    td a:hover { text-decoration: underline; }
    .delete-form { display: inline-block; margin: 0; }
    .delete-form button { padding: 5px 10px; background-color: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.9em; }
    .delete-form button:hover { background-color: #c82333; }
    /* 상세 페이지 스타일 */
    .detail-title { font-size: 28px; font-weight: bold; color: #333; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
    .detail-meta { color: #6c757d; font-size: 0.9em; margin-bottom: 20px; line-height: 1.6; }
    .detail-meta span { margin-right: 20px; }
    .detail-content { white-space: pre-wrap; line-height: 1.8; color: #555; margin-bottom: 30px; }
    .back-link-container { text-align: center; margin-top: 20px; }
</style>
"""

notice_form_template = common_style + '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>📢 공지사항</title>
</head>
<body>
    {# 플래시 메시지 표시 영역 #}
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="message {{ category }}">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    {# 관리자(user_role == 1)에게만 새 공지 등록 폼 표시 #}
    {% if user_role == 1 %}
    <div class="container notice-form-container"> {# notice-form-container 클래스명 유지 #}
        <h2>새 공지 등록</h2>
        <form method="POST" action="{{ url_for('add_notice') }}" enctype="multipart/form-data">
            <div class="form-group">
                <label for="title">제목:</label>
                <input type="text" id="title" name="title" required>
            </div>
            <div class="form-group">
                <label for="content">내용:</label>
                <textarea id="content" name="content" required></textarea>
            </div>
            <div class="form-group">
                <label for="publisher">작성자:</label>
                {# current_user 객체가 있다면 User_name을 기본값으로 사용 #}
                <input type="text" id="publisher" name="publisher" value="{{ current_user.User_name if current_user else '' }}" required>
            </div>
            <div class="form-group">
                <label for="category">분류:</label>
                <input type="text" id="category" name="category" required>
            </div>
            <div class="form-group">
                <label for="attachments">첨부파일:</label>
                <input type="file" id="attachments" name="attachments" multiple>
            </div>
            <div class="form-group" style="text-align:center;">
                <input type="submit" value="등록">
            </div>
        </form>
    </div>
    {% endif %}

    <div class="container notice-table-container"> {# notice-table-container 클래스명 유지 #}
        <h1>📢 공지사항 목록</h1>
        <table>
            <thead>
                <tr>
                    <th>번호</th>
                    <th>제목</th>
                    <th>작성자</th>
                    <th>작성일</th>
                    {# 관리자(user_role == 1)에게만 삭제 컬럼 표시 #}
                    {% if user_role == 1 %}
                    <th>삭제</th>
                    {% endif %}
                </tr>
            </thead>
            <tbody>
            {% for n in notices %}
                <tr>
                    <td>{{ n.notice_id }}</td>
                    <td><a href="{{ url_for('notice_detail_page', notice_id=n.notice_id) }}">{{ n.title }}</a></td>
                    <td>{{ n.publisher }}</td>
                    <td>{{ n.created_at.strftime('%Y.%m.%d') }}</td>
                    {# 관리자(user_role == 1)에게만 삭제 버튼 표시 #}
                    {% if user_role == 1 %}
                    <td>
                        <form method="POST" action="{{ url_for('delete_notice', notice_id=n.notice_id) }}" class="delete-form" onsubmit="return confirm('정말로 이 공지를 삭제하시겠습니까?');">
                            <button type="submit">삭제</button>
                        </form>
                    </td>
                    {% endif %}
                </tr>
            {% else %}
                <tr>
                    <td colspan="{{ 5 if user_role == 1 else 4 }}" style="text-align:center;">등록된 공지사항이 없습니다.</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
'''

notice_detail_template = common_style + '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>{{ notice.title }} - 공지사항</title> {# 페이지 타이틀에 공지사항 명시 #}
</head>
<body>
    {# 플래시 메시지 표시 영역 (상세 페이지에도 필요할 수 있음) #}
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="message {{ category }}">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <div class="detail-wrapper"> {# detail-wrapper 클래스명 유지 #}
        <div class="detail-title">{{ notice.title }}</div>
        <div class="detail-meta">
            <span>분류: {{ notice.category }}</span> 
            <span>작성자: {{ notice.publisher }} ({% if notice.created_by %}ID: {{ notice.created_by }}{% else %}정보 없음{% endif %})</span><br>
            <span>작성일: {{ notice.created_at.strftime('%Y.%m.%d %H:%M') }}</span>
        </div>
        <div class="detail-content">{{ notice.content }}</div>

        {% if notice.attachments and notice.attachments|length > 0 %}
            <div class="detail-meta">
                📎 첨부파일:
                <ul>
                {% for file_path in notice.attachments %}
                    {# file_path가 문자열인지 확인하고, 문자열인 경우에만 split 사용 #}
                    <li><a href="{{ file_path }}" download>{{ file_path.split('/')[-1] if file_path is string else file_path }}</a></li>
                {% endfor %}
                </ul>
            </div>
        {% endif %}

        <div class="back-link-container">
            {# 관리자(user_role == 1)에게만 수정/삭제 버튼 예시 (실제 라우트 및 로직 필요) #}
            {% if user_role == 1 %}
                {# <a href="{{ url_for('edit_notice_page', notice_id=notice.notice_id) }}" class="button">수정</a> #}
                {# <form method="POST" action="{{ url_for('delete_notice', notice_id=notice.notice_id) }}" style="display:inline;" onsubmit="return confirm('정말로 이 공지를 삭제하시겠습니까?');">
                    <button type="submit" class="button" style="background-color:#dc3545;">삭제</button>
                </form> #}
            {% endif %}
            <a href="{{ url_for('show_notice_page') }}" class="button-link">🔙 목록으로</a>
        </div>
    </div>
</body>
</html>
'''

def show_notice_logic():
    # from setting.models import Notice # app.py에서 이미 임포트 되었으므로 중복 피할 수 있으나, 가독성을 위해 유지 가능
    # from setting.models import User   # User 모델도 필요

    user_role = 0 # 기본값: 비로그인 또는 일반 사용자 (읽기 전용)
    current_user_obj = None # 템플릿에서 사용자 이름 등을 사용하기 위함

    if 'current_user_id' in session:
        user_id = session['current_user_id']
        # User 모델을 사용하여 User_role 조회
        user = User.query.filter_by(User_id=user_id).first()
        if user:
            user_role = user.User_role
            current_user_obj = user
        else:
            # 세션에 ID는 있지만 DB에 해당 유저가 없는 경우 (예: 탈퇴 후 세션이 남은 경우)
            session.pop('current_user_id', None) # 세션 정리
            flash("사용자 정보를 찾을 수 없습니다. 다시 로그인해주세요.", "error")
            # 이 경우 로그인 페이지로 리디렉션할 수도 있으나, 일단 공지 목록은 보여주되 권한은 0으로 처리
            
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    # user_role과 현재 사용자 객체(current_user)를 템플릿에 전달
    return render_template_string(notice_form_template, notices=notices, user_role=user_role, current_user=current_user_obj)

def askPassword():
    # 비밀번호 확인 로직 (예시)
    if request.method == 'POST':
        password = request.json.get('password')
        # 비밀번호 검증 로직 (예: DB에서 확인)
        if generate_sha256(password) == "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4":  # 예시 비밀번호
            return {"status": "success"}, 200
        else:
            return {"status": "error"}, 401

def generate_sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()        

def add_notice_logic():
    # from setting.models import Notice, User # User 모델 임포트
    # from setting.db_connect import db       # db 객체 임포트

    # 1. 로그인 상태 확인
    if 'current_user_id' not in session:
        flash('공지를 등록하려면 로그인이 필요합니다.', 'error')
        return redirect(url_for('login_page')) # 로그인 페이지로 리디렉션

    current_user_id_from_session = session['current_user_id']
    user = User.query.filter_by(User_id=current_user_id_from_session).first()

    # 2. 사용자 존재 여부 및 권한(User_role == 1) 확인
    if not user: # DB에 해당 사용자가 없는 경우 (비정상적 상황)
        flash('사용자 정보를 찾을 수 없습니다. 다시 로그인해주세요.', 'error')
        session.pop('current_user_id', None) # 세션 정리
        return redirect(url_for('login_page'))
        
    if user.User_role != 1: # 관리자가 아닌 경우
        flash('공지 등록 권한이 없습니다.', 'error')
        return redirect(url_for('show_notice_page')) # 공지 목록 페이지로 리디렉션

    # --- 이하 로직은 User_role == 1 (관리자)인 경우에만 실행됨 ---
    # POST 요청일 때만 공지 추가 로직 실행
    if request.method == 'POST':
        title = request.json.get('title')
        content = request.json.get('content')
        # 'publisher'는 관리자가 직접 입력하거나, 현재 로그인한 관리자 이름으로 자동 설정
        publisher = request.json.get('publisher', user.User_name) # 기본값으로 로그인한 관리자 이름 사용
        created_by = current_user_id_from_session # 공지를 생성한 시스템 사용자 ID
        category = request.json.get('category')

        # 필수 필드 검증
        if not all([title, content, publisher, category]): # created_by는 자동이므로 제외
            flash('제목, 내용, 작성자, 분류는 모두 필수 항목입니다.', 'error')
            # GET 요청으로 되돌아가 폼을 다시 보여주거나, 공지 목록으로 리디렉션
            # 현재는 POST만 처리하므로, 오류 시 공지 목록으로 보냄 (폼 값 유지는 추가 구현 필요)
            return redirect(url_for('show_notice_page'))

        saved_files = []
        uploaded_files = request.files.getlist("attachments")

        if uploaded_files:
            # PROJECT_ROOT는 app.py에서 설정된 경로를 사용한다고 가정
            # app.py가 flask_backend/api/에 있다면, static은 flask_backend/static/ 에 있어야 함
            # current_app.root_path는 /api 폴더를 가리킴
            upload_dir = os.path.join(current_app.config.get('PROJECT_ROOT', current_app.root_path), 'static', 'uploads')

            if not os.path.exists(upload_dir):
                try:
                    os.makedirs(upload_dir, exist_ok=True)
                except Exception as e:
                    current_app.logger.error(f"첨부파일 저장 디렉토리 생성 실패: {upload_dir}, 오류: {e}")
                    flash(f'첨부파일 저장 디렉토리 생성에 실패했습니다.', 'error')
                    return redirect(url_for('show_notice_page'))
            
            for file in uploaded_files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(upload_dir, filename)
                    try:
                        file.save(filepath)
                        # 웹 접근 가능 URL 경로 (app.py의 PROJECT_ROOT 설정에 따라 static 경로가 달라질 수 있음)
                        # 일반적으로 /static/uploads/filename 형태
                        saved_files.append(f'/static/uploads/{filename}')
                    except Exception as e:
                        current_app.logger.error(f"첨부파일 저장 실패: {filepath}, 오류: {e}")
                        flash(f'첨부파일 "{filename}" 저장에 실패했습니다.', 'error')
                        # 하나라도 실패하면 전체 롤백 또는 부분 성공 처리 결정 필요. 여기서는 일단 계속 진행.

        new_notice = Notice(
            title=title,
            content=content,
            publisher=publisher,
            created_by=created_by,
            category=category,
            attachments=json.dumps(saved_files) if saved_files else None
        )
        # db는 app.py에서 초기화되어 전역적으로 사용 가능해야 함.
        # from setting.db_connect import db 를 통해 가져오거나, current_app.extensions['sqlalchemy'].db 사용
        from setting.db_connect import db # 명시적 임포트
        db.session.add(new_notice)
        db.session.commit()
        flash('새 공지가 성공적으로 등록되었습니다.', 'success')
        return redirect(url_for('show_notice_page')) # 성공 후 공지 목록으로 리디렉션
    
    # GET 요청으로 이 함수가 직접 호출되는 경우는 없어야 함 (폼은 show_notice_logic에서 관리자에게만 표시)
    # 만약 GET으로 접근 시, 권한 오류 또는 공지 목록으로 리디렉션
    flash('잘못된 접근입니다.', 'error')
    return redirect(url_for('show_notice_page'))


def show_notice_detail_logic(notice_id):
    # from setting.models import Notice, User

    current_user_obj = None
    if 'current_user_id' in session:
        user_id = session['current_user_id']
        user = User.query.filter_by(User_id=user_id).first()
        if user:
            user_role = user.User_role
            current_user_obj = user # 상세 페이지에서도 current_user 정보 사용 가능
        else:
            session.pop('current_user_id', None)
            # flash("사용자 정보를 찾을 수 없습니다. (상세 페이지)", "error") # 필요시 메시지

    notice = Notice.query.get(notice_id)
    if not notice:
        flash("해당 공지를 찾을 수 없습니다.", 'error')
        return redirect(url_for('show_notice_page'))

    attachments_list = []
    if notice.attachments:
        try:
            loaded_attachments = json.loads(notice.attachments)
            if isinstance(loaded_attachments, list):
                attachments_list = loaded_attachments
            elif isinstance(loaded_attachments, str):
                attachments_list = [loaded_attachments] if loaded_attachments else []
        except (json.JSONDecodeError, TypeError):
            attachments_list = [notice.attachments] if isinstance(notice.attachments, str) and notice.attachments else []
            current_app.logger.warning(f"공지 ID {notice_id}의 첨부파일 JSON 파싱 실패 또는 타입 오류. 원본 데이터: {notice.attachments}")


    # 템플릿에 전달할 공지 객체 (attachments를 파싱된 리스트로 교체)
    class NoticeViewModel:
        def __init__(self, notice_model, parsed_attachments):
            self.notice_id = notice_model.notice_id
            self.title = notice_model.title
            self.content = notice_model.content
            self.created_at = notice_model.created_at
            self.publisher = notice_model.publisher
            self.created_by = notice_model.created_by
            self.category = notice_model.category
            self.attachments = parsed_attachments # 파싱된 리스트

    notice_for_template = NoticeViewModel(notice, attachments_list)

    return render_template_string(notice_detail_template, notice=notice_for_template, user_role=user_role, current_user=current_user_obj)

# get_all_notices_logic, get_notice_detail_logic (JSON API용)은
# 현재 요구사항(웹 페이지 접근 제어)과 직접적 관련은 없으므로 일단 그대로 둡니다.
# 만약 이 API들에 대한 접근 제어도 필요하다면 알려주세요.

def get_all_notices_logic():
    # from setting.models import Notice
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return [
        {
            "notice_id": n.notice_id,
            "title": n.title,
            # "content": n.content, # 목록에서는 내용 제외 가능
            "created_at": n.created_at.isoformat(),
            "publisher": n.publisher,
            "created_by": n.created_by,
            "category": n.category,
            "attachments": json.loads(n.attachments) if n.attachments else []
        }
        for n in notices
    ]


def get_notice_detail_logic(notice_id):
    # from setting.models import Notice
    notice = Notice.query.get(notice_id)
    if not notice:
        return None
    
    attachments_list = []
    if notice.attachments:
        try:
            loaded_attachments = json.loads(notice.attachments)
            if isinstance(loaded_attachments, list):
                attachments_list = loaded_attachments
            elif isinstance(loaded_attachments, str): # 문자열 하나만 저장된 경우
                 attachments_list = [loaded_attachments] if loaded_attachments else []
        except (json.JSONDecodeError, TypeError): # 파싱 실패 또는 이미 리스트가 아닌 경우
            attachments_list = [notice.attachments] if isinstance(notice.attachments, str) and notice.attachments else []


    return {
        "notice_id": notice.notice_id,
        "title": notice.title,
        "content": notice.content,
        "created_at": notice.created_at.isoformat(),
        "publisher": notice.publisher,
        "created_by": notice.created_by,
        "category": notice.category,
        "attachments": attachments_list
    }