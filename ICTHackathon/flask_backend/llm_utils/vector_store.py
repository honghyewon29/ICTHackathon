from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import LANGCHAIN_API_KEY

import os

persist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../LLM/chroma_db"))

embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=LANGCHAIN_API_KEY
)

vectorstore = None

def initialize_vectorstore(split_docs):
    global vectorstore

    if not split_docs or len(split_docs) == 0:
        raise ValueError("❌ 벡터 저장소 초기화 실패: split_docs가 비어 있음")

    print(f"💾 벡터화할 문서 수: {len(split_docs)}")
    
    try:
        vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=embeddings_model,
            collection_name="ict_documents",
            persist_directory=persist_dir,
            collection_metadata={"hnsw:space": "ip"}
        )
        vectorstore.persist()
        print(f"✅ 벡터 저장 완료! 경로: {persist_dir}")
    except Exception as e:
        print("❌ 벡터 저장 중 오류 발생:", str(e))
        raise


def load_vectorstore():
    global vectorstore

    if vectorstore is None:
        print(f"📦 저장된 벡터 DB 불러오기: {persist_dir}")
        vectorstore = Chroma(
            embedding_function=embeddings_model,
            collection_name="ict_documents",
            persist_directory=persist_dir,
        )
    return vectorstore
