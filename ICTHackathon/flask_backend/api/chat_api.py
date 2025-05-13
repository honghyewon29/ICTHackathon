from flask import Blueprint, request, jsonify
from services.rag_service import ask_with_rag

chat_blueprint = Blueprint("chat_api", __name__)

@chat_blueprint.route("/ask", methods=["POST"])
def chat():
    user_input = request.json.get("query", "")
    response = ask_with_rag(user_input)
    return jsonify({"answer": response})