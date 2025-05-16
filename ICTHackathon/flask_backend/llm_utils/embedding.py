import os
from glob import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


def load_and_split_documents():
    txt_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../LLM/Data"))
    print("📂 불러오는 폴더:", txt_dir)

    txt_files = glob(os.path.join(txt_dir, "*.txt"))
    print("📄 찾은 파일 개수:", len(txt_files))

    docs = []
    for path in txt_files:
        print("📄 로드 중:", path)
        loader = TextLoader(path, encoding="utf-8")
        docs.extend(loader.load())

    print("📄 로딩 완료, 문서 수:", len(docs))

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", "!", "?", " ", ""],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=True
    )

    chunks = text_splitter.split_documents(docs)
    print("🧩 분할된 청크 수:", len(chunks))

    return chunks

# embedding.py
from langchain_huggingface import HuggingFaceEmbeddings

# ✅ 앱 시작 시 단 한 번만 로딩됨
print("🧠 한국어 특화 KoSimCSE 임베딩 모델 로드 중...")
embedding_model = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")

def get_korean_embedding_model():
    return embedding_model
