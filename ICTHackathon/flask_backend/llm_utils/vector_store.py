from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import OPENAI_API_KEY

persist_dir = "/../../LLM/chroma_db"


embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key="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"   # ← 이게 정확한 인자 이름임
)

vectorstore = None

def initialize_vectorstore(split_docs):
    global vectorstore
    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings_model,
        collection_name="ict_documents",
        persist_directory=persist_dir,
        collection_metadata={"hnsw:space": "ip"}
    )
    vectorstore.persist()


def load_vectorstore():
    global vectorstore
    if vectorstore is None:
        vectorstore = Chroma(
            embedding_function=embeddings_model,
            collection_name="ict_documents",
            persist_directory=persist_dir,
        )
    return vectorstore