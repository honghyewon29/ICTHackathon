from langchain_openai import ChatOpenAI


normalizer_llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key="sk-여기에_당신의_API_KEY"
)


def normalize_question(user_question):
    system_instruction = """
    사용자의 질문을 수원대학교 ICT 단대 기준으로 검색하기 쉽게 바꿔줘.
    의미는 유지하되, 키워드 중심으로 간결하게 정형화해.
    예시:
    - "학교 언제까지 나가야 ?" → "종강일"
    - "졸업하려면 뭘 해야 돼?" → "졸업 요건"
    - "여름방학 언제야?" → "하계방학 시작일"
    - "기숙사 서류 뭐 필요해?" → "기숙사 제출 서류"
    """

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_question}
    ]
    return normalizer_llm.invoke(messages).content.strip()