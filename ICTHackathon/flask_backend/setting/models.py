# flask_backend/setting/models.py

from setting.db_connect import db  # ✅ 여기서만 db import
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    Num_idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    User_id = db.Column(db.String(80), unique=True, nullable=False)
    User_pw = db.Column(db.String(200), nullable=False)
    User_email = db.Column(db.String(120), unique=True, nullable=False)
    User_name = db.Column(db.String(80), nullable=True)
    User_role = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<User {self.User_id}>'

class Notice(db.Model):
    __tablename__ = 'notice'

    notice_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    publisher = db.Column(db.String(100))  
    created_by = db.Column(db.String(100)) 
    category = db.Column(db.String(100))
    attachments = db.Column((db.Text), nullable=True)