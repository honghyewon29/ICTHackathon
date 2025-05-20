# vector_store.py
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import OPENAI_API_KEY

import os

persist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../LLM/chroma_db"))

embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=OPENAI_API_KEY
)

vectorstore = None

def initialize_vectorstore(split_docs):
    raise RuntimeError("❌ 현재 모드에서는 벡터 저장이 비활성화되어 있습니다. 저장 금지!")

def load_vectorstore():
    global vectorstore

    if vectorstore is None:
        # print(f"📦 기존 벡터 DB 불러오는 중... 경로: {persist_dir}")
        vectorstore = Chroma(
            embedding_function=embeddings_model,
            collection_name="ict_documents",
            persist_directory=persist_dir,
        )
    return vectorstore
