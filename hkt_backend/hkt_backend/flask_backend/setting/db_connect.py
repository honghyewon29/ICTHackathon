# setting/db_connect.py

from flask_sqlalchemy import SQLAlchemy
import os # os 모듈 임포트

db = SQLAlchemy()

def init_db(app):
    """데이터베이스 연결 초기화 (환경 변수 사용)"""
    # .env 파일이나 시스템 환경 변수에서 DB 설정값들을 가져옵니다.
    DB_USER = os.environ.get('DB_USER', 'root') # 기본값 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST', 'localhost') # 기본값 'localhost'
    DB_PORT = os.environ.get('DB_PORT', '3306')     # MySQL 기본 포트
    DB_NAME = os.environ.get('DB_NAME')

    if not DB_PASSWORD or not DB_NAME:
        # 필수 DB 정보가 없으면 경고 또는 에러 처리
        # 여기서는 경고만 출력하고 진행하지만, 실제 운영에서는 더 강력한 처리가 필요할 수 있습니다.
        print("경고: DB_PASSWORD 또는 DB_NAME 환경 변수가 .env 파일이나 환경 변수에 설정되지 않았습니다.")
        if not DB_PASSWORD:
            raise ValueError("DB_PASSWORD가 설정되지 않았습니다!")
        if not DB_NAME:
            raise ValueError("DB_NAME이 설정되지 않았습니다!")


    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)