import os
import json
from flask import request, jsonify, current_app # render_template_string, session, flash, url_for, redirect 제거
from werkzeug.utils import secure_filename
from setting.db_connect import db # db 객체 직접 임포트
from setting.models import User, Notice # User, Notice 모델 임포트
from datetime import datetime # 날짜/시간 처리를 위해


# --- 첨부파일 관련 헬퍼 함수 (선택 사항) ---
def _get_upload_folder():
    """설정에서 업로드 폴더 경로를 가져오거나 기본값을 반환합니다."""
    upload_dir = current_app.config.get('UPLOAD_FOLDER')
    if not upload_dir:
        project_root_from_config = current_app.config.get('PROJECT_ROOT', current_app.root_path)
        upload_dir = os.path.join(project_root_from_config, 'static', 'uploads')
        current_app.logger.warning(f"UPLOAD_FOLDER not configured, using default: {upload_dir}")

    if not os.path.exists(upload_dir):
        try:
            os.makedirs(upload_dir, exist_ok=True)
        except Exception as e:
            current_app.logger.error(f"Failed to create upload directory: {upload_dir}, Error: {e}")
            return None # 디렉토리 생성 실패 시 None 반환
    return upload_dir
 
def _delete_attachment_files(attachment_paths_json_str):
    """JSON 문자열로 저장된 첨부파일 경로들을 받아 실제 파일들을 삭제합니다."""
    if not attachment_paths_json_str:
        return

    try:
        attachment_urls = json.loads(attachment_paths_json_str)
    except json.JSONDecodeError:
        # 단일 파일 경로가 문자열로 직접 저장된 경우 (레거시 데이터 호환)
        if isinstance(attachment_paths_json_str, str) and attachment_paths_json_str.startswith('/static/uploads/'):
            attachment_urls = [attachment_paths_json_str]
        else:
            current_app.logger.error(f"Failed to parse attachment JSON: {attachment_paths_json_str}")
            return

    if not isinstance(attachment_urls, list):
        current_app.logger.warning(f"Attachments are not a list after parsing: {attachment_urls}")
        return

    project_root = current_app.config.get('PROJECT_ROOT', current_app.root_path)

    for file_url in attachment_urls:
        if not isinstance(file_url, str) or not file_url.startswith('/static/uploads/'):
            current_app.logger.warning(f"Invalid or unexpected attachment URL path: {file_url}")
            continue
        
        # url경로 (/static/uploads/filename.ext) 에서 실제 파일 시스템 경로로 변환
        # ex) /static/uploads/image.png -> PROJECT_ROOT/static/uploads/image.png
        relative_path = file_url.lstrip('/') # "static/uploads/filename.ext"
        actual_file_path = os.path.join(project_root, relative_path)
        
        try:
            if os.path.exists(actual_file_path):
                os.remove(actual_file_path)
                current_app.logger.info(f"Deleted attachment file: {actual_file_path}")
            else:
                current_app.logger.warning(f"Attachment file not found, skipping deletion: {actual_file_path}")
        except OSError as e:
            current_app.logger.error(f"Could not delete attachment file {actual_file_path}: {e}")


# --- API 로직 함수들 ---

def create_notice_api(authenticated_user_id, user_role):
    """
    새 공지사항을 생성하는 API 로직.
    인증된 사용자 ID와 역할을 인자로 받습니다.
    """
    if user_role != 1: # 관리자(User_role == 1)만 공지 등록 가능
        return jsonify({'status': 'error', 'message': '공지 등록 권한이 없습니다.'}), 403 # Forbidden

    if request.method != 'POST': # 이 체크는 Flask 라우트에서 하는 것이 더 적절
        return jsonify({'status': 'error', 'message': 'POST 요청만 허용됩니다.'}), 405

    # form-data로 제목, 내용 등을 받는다(파일 업로드 때문에)
    # 만약 JSON과 파일을 함께 받으려면 클라이언트에서 multipart/form-data로 보내되,
    # JSON 부분은 별도의 필드로 문자열화해서 보내고 서버에서 파싱해야 할 수 있습니다.
    # 여기서는 request.form 사용.
    title = request.form.get('title')
    content = request.form.get('content')
    publisher_name_input = request.form.get('publisher') # 관리자가 지정한 작성자명
    category = request.form.get('category')

    if not all([title, content, category]):
        return jsonify({'status': 'error', 'message': '제목, 내용, 분류는 필수 항목입니다.'}), 400

    user = User.query.filter_by(User_id=authenticated_user_id).first()
    if not user: # 인증된 ID로 사용자를 찾을 수 없는 매우 드문 경우
        current_app.logger.error(f"Authenticated user ID {authenticated_user_id} not found in DB for creating notice.")
        return jsonify({'status': 'error', 'message': '인증 오류: 사용자 정보를 찾을 수 없습니다.'}), 401
    
    # 실제 공지 게시자 이름: 관리자가 입력한 값을 우선, 없으면 로그인한 관리자 이름
    final_publisher_name = publisher_name_input if publisher_name_input else user.User_name

    saved_file_urls = []
    uploaded_files = request.files.getlist("attachments") # "attachments"는 form 필드 이름
    
    upload_dir = _get_upload_folder()
    if not upload_dir and uploaded_files: # 업로드 폴더가 없고 파일이 있다면 에러
        return jsonify({'status': 'error', 'message': '파일 업로드 설정을 확인해주세요. (폴더 생성 실패)'}), 500

    if uploaded_files and upload_dir:
        for file_obj in uploaded_files:
            if file_obj and file_obj.filename:
                filename = secure_filename(file_obj.filename)
                # 파일명 중복 방지를 위해 UUID나 타임스탬프 추가 권장 알아서 필요하면 추가하세요
                # timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                # unique_filename = f"{timestamp}_{filename}"
                # filepath = os.path.join(upload_dir, unique_filename)
                filepath = os.path.join(upload_dir, filename) # 단순 저장
                try:
                    file_obj.save(filepath)
                    # 웹에서 접근 가능한 URL (static 경로는 앱 설정에 따라 달라질 수 있음)
                    saved_file_urls.append(f'/static/uploads/{filename}') # unique_filename 사용 시 그것으로 변경
                except Exception as e:
                    current_app.logger.error(f"Failed to save attachment: {filename}, Error: {e}")
                    # 여기서는 일단 에러 반환
                    return jsonify({'status': 'error', 'message': f'첨부파일 "{filename}" 저장에 실패했습니다.'}), 500
    
    try:
        new_notice = Notice(
            title=title,
            content=content,
            publisher=final_publisher_name,
            created_by=authenticated_user_id, # 공지 생성자 시스템 ID
            category=category,
            attachments=json.dumps(saved_file_urls) if saved_file_urls else None
        )
        db.session.add(new_notice)
        db.session.commit()
        
        # 생성된 공지 정보 반환 (id 포함)
        return jsonify({
            'status': 'success',
            'message': '새 공지가 성공적으로 등록되었습니다.',
            'data': {
                'notice_id': new_notice.notice_id,
                'title': new_notice.title,
                'publisher': new_notice.publisher,
                'category': new_notice.category,
                'created_at': new_notice.created_at.isoformat(),
                'attachments': saved_file_urls
            }
        }), 201 # \생성
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating notice by {authenticated_user_id}: {e}")
        # 저장 시도했던 파일들 삭제 로직 추가 가능
        for url in saved_file_urls:
            _delete_attachment_files(json.dumps([url])) # 단일 파일 삭제 헬퍼 사용 예시
        return jsonify({'status': 'error', 'message': '공지 등록 중 서버 오류가 발생했습니다.'}), 500


def get_all_notices_api():
    """모든 공지사항 목록을 JSON으로 반환하는 API 로직."""
    try:
        notices = Notice.query.order_by(Notice.created_at.desc()).all()
        result = []
        for n in notices:
            attachments_list = []
            if n.attachments:
                try:
                    loaded_attachments = json.loads(n.attachments)
                    if isinstance(loaded_attachments, list):
                        attachments_list = loaded_attachments
                    elif isinstance(loaded_attachments, str): # 단일 경로 문자열
                        attachments_list = [loaded_attachments] if loaded_attachments else []
                except (json.JSONDecodeError, TypeError):
                     attachments_list = [n.attachments] if isinstance(n.attachments, str) and n.attachments else []

            result.append({
                "notice_id": n.notice_id,
                "title": n.title,
                "publisher": n.publisher,
                "category": n.category,
                "created_at": n.created_at.isoformat(),
                "view_count": n.view_count, # 조회수 필드가 있다면 추가
                # "content": n.content, # 목록에서는 보통 내용 제외
                "attachments_count": len(attachments_list) # 첨부파일 개수
            })
        return jsonify({'status': 'success', 'data': result}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching all notices: {e}")
        return jsonify({'status': 'error', 'message': '공지사항 목록을 가져오는 중 오류가 발생했습니다.'}), 500


def get_notice_by_id_api(notice_id):
    """특정 ID의 공지사항 상세 정보를 JSON으로 반환하는 API 로직."""
    try:
        notice = Notice.query.get(notice_id)
        if not notice:
            return jsonify({'status': 'error', 'message': '해당 ID의 공지를 찾을 수 없습니다.'}), 404

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
                current_app.logger.warning(f"Notice ID {notice_id} attachments JSON parsing failed or type error. Raw data: {notice.attachments}")
        
        return jsonify({
            'status': 'success',
            'data': {
                "notice_id": notice.notice_id,
                "title": notice.title,
                "content": notice.content,
                "publisher": notice.publisher,
                "category": notice.category,
                "created_at": notice.created_at.isoformat(),
                "created_by": notice.created_by, # 작성자 시스템 ID
                "attachments": attachments_list,
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching notice ID {notice_id}: {e}")
        return jsonify({'status': 'error', 'message': '공지사항 상세 정보를 가져오는 중 오류가 발생했습니다.'}), 500

def update_notice_api(notice_id, authenticated_user_id, user_role):
    """
    특정 ID의 공지사항을 수정하는 API 로직.
    PUT 또는 PATCH 요청으로 처리. 여기서는 PUT (전체 교체) 기준으로 작성.
    """
    if user_role != 1:
        return jsonify({'status': 'error', 'message': '공지 수정 권한이 없습니다.'}), 403

    notice = Notice.query.get(notice_id)
    if not notice:
        return jsonify({'status': 'error', 'message': '수정할 공지를 찾을 수 없습니다.'}), 404

    # 공지 작성자 또는 관리자만 수정 가능
    if notice.created_by != authenticated_user_id and user_role != 1:
         return jsonify({'status': 'error', 'message': '이 공지를 수정할 권한이 없습니다.'}), 403

    data = request.form # 파일 수정을 고려하여 form-data 사용 가정
    
    # 변경하려는 필드만 업데이트 (PATCH 방식에 더 적합하나, PUT에서도 선택적 업데이트 가능)
    notice.title = data.get('title', notice.title)
    notice.content = data.get('content', notice.content)
    notice.category = data.get('category', notice.category)
    notice.publisher = data.get('publisher', notice.publisher) # 관리자가 게시자명 변경 가능

    # 첨부파일 처리: 기존 파일 삭제 후 새 파일 추가 또는 기존 파일 유지/부분 수정 등 복잡한 로직 가능
    # 여기서는 단순화하여, 새 첨부파일이 있다면 기존것을 대체하는 방식 (기존 파일 삭제 로직 필요)
    new_uploaded_files = request.files.getlist("attachments")
    
    if new_uploaded_files: # 새 첨부파일이 있는 경우
        _delete_attachment_files(notice.attachments) # 기존 첨부파일 삭제
        
        saved_new_file_urls = []
        upload_dir = _get_upload_folder()
        if not upload_dir:
             return jsonify({'status': 'error', 'message': '파일 업로드 설정을 확인해주세요. (폴더 접근 불가)'}), 500

        for file_obj in new_uploaded_files:
            if file_obj and file_obj.filename:
                filename = secure_filename(file_obj.filename)
                filepath = os.path.join(upload_dir, filename)
                try:
                    file_obj.save(filepath)
                    saved_new_file_urls.append(f'/static/uploads/{filename}')
                except Exception as e:
                    current_app.logger.error(f"Failed to save new attachment during update: {filename}, Error: {e}")
                    return jsonify({'status': 'error', 'message': f'새 첨부파일 "{filename}" 저장에 실패했습니다.'}), 500
        notice.attachments = json.dumps(saved_new_file_urls) if saved_new_file_urls else None
    # 새 첨부파일이 없고, 기존 첨부파일을 삭제하라는 요청이 있다면 (예: 'remove_attachments' 필드) 해당 로직 추가

    try:
        db.session.commit()
        # 수정된 공지 정보 반환
        updated_attachments = json.loads(notice.attachments) if notice.attachments else []
        return jsonify({
            'status': 'success',
            'message': '공지가 성공적으로 수정되었습니다.',
            'data': {
                'notice_id': notice.notice_id,
                'title': notice.title,
                'content': notice.content,
                'publisher': notice.publisher,
                'category': notice.category,
                'created_at': notice.created_at.isoformat(), # 수정일 필드가 있다면 그것도 반환
                'attachments': updated_attachments
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating notice ID {notice_id}: {e}")
        return jsonify({'status': 'error', 'message': '공지 수정 중 서버 오류가 발생했습니다.'}), 500


def delete_notice_api(notice_id, authenticated_user_id, user_role):
    """
    특정 ID의 공지사항을 삭제하는 API 로직.
    """
    if user_role != 1:
        return jsonify({'status': 'error', 'message': '공지 삭제 권한이 없습니다.'}), 403

    notice_to_delete = Notice.query.get(notice_id)
    if not notice_to_delete:
        return jsonify({'status': 'error', 'message': '삭제할 공지를 찾을 수 없습니다.'}), 404

    # 공지 작성자 또는 관리자만 삭제 가능하도록 
    if notice_to_delete.created_by != authenticated_user_id and user_role != 1:
         return jsonify({'status': 'error', 'message': '이 공지를 삭제할 권한이 없습니다.'}), 403
        
    try:
        # 첨부파일 먼저 삭제
        _delete_attachment_files(notice_to_delete.attachments)
        
        db.session.delete(notice_to_delete)
        db.session.commit()
        current_app.logger.info(f"Notice ID {notice_id} deleted by user ID {authenticated_user_id}.")
        return jsonify({'status': 'success', 'message': '공지가 성공적으로 삭제되었습니다.'}), 200 # 또는 204 No Content
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting notice ID {notice_id} by user {authenticated_user_id}: {e}")
        return jsonify({'status': 'error', 'message': '공지 삭제 중 서버 오류가 발생했습니다.'}), 500