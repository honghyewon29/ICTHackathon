# gpt_client.py
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY



llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    max_tokens=300,
    api_key=OPENAI_API_KEY
)


def generate_response(messages):
    response = llm.invoke(messages)
    print("🧠 GPT 응답 원본:", response)
    return llm.invoke(messages)
