from flask import Flask, request, jsonify
from flask_cors import CORS
from api.chat_api import chat_blueprint
from api.rag_api import rag_blueprint
from config import OPENAI_API_KEY

import openai
from openai import OpenAI

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_blueprint, url_prefix="/api/chat")
app.register_blueprint(rag_blueprint, url_prefix="/api/rag")

client = OpenAI(api_key=OPENAI_API_KEY)


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

    app.run(debug=True)
