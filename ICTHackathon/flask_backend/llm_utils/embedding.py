import os
from glob import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

def load_and_split_documents():
    txt_dir = "/../../LLM/Data"
    txt_files = glob(os.path.join(txt_dir, "*.txt"))
    docs = []
    for path in txt_files:
        loader = TextLoader(path, encoding="utf-8")
        docs.extend(loader.load())

    text_splitter = CharacterTextSplitter(
        separator=r"[.!?]\s+",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=True
    )
    return text_splitter.split_documents(docs)