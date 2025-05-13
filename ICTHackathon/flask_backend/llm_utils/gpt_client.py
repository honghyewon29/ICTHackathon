from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    max_tokens=300,
    api_key="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"
)


def generate_response(messages):
    return llm.invoke(messages)