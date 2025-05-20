#chat_api.py
from flask import Blueprint, request, jsonify
from services.rag_service import ask_with_rag

chat_blueprint = Blueprint("chat_api", __name__)

@chat_blueprint.route("/ask", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = ask_with_rag(user_input)
    # print("💬 챗봇 요청 수신:", user_input)
    # print("💬 챗봇 응답:", response)
    return jsonify({"answer": response})
# print("📥 API 요청 도착:")