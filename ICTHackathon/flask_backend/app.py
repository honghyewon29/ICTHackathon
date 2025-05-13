# app.py
from flask import Flask
from flask_cors import CORS
from api.chat_api import chat_blueprint
from api.rag_api import rag_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_blueprint, url_prefix="/api/chat")
app.register_blueprint(rag_blueprint, url_prefix="/api/rag")

if __name__ == '__main__':
    app.run(debug=True)