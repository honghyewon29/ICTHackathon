from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

def get_multiquery_retriever(vectorstore):
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    gpt35 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    return MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=gpt35,
        include_original=True
    )