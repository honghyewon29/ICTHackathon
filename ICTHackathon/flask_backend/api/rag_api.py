# rag_api.py
from flask import Blueprint, jsonify
from llm_utils.vector_store import initialize_vectorstore
from llm_utils.embedding import load_and_split_documents

rag_blueprint = Blueprint("rag_api", __name__)

@rag_blueprint.route("/init", methods=["GET"])
def initialize():
    docs = load_and_split_documents()
    initialize_vectorstore(docs)
    return jsonify({"status": "initialized"})