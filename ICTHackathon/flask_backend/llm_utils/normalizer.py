from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY


normalizer_llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)


def normalize_question(user_question):
    system_instruction = """
    주어진 질문에 대해:
    1. 질문의 주요 주제 카테고리를 분류합니다. (예: 연락처, 위치, 학사일정, 서류, 기숙사 등)
    2. 핵심 키워드만 추출합니다. (예: 인물 이름, 시설명, 일정명)
    3. 최종적으로 검색에 적합한 키워드 조합으로 출력합니다.
    
    출력 형식은: 카테고리 | 키워드1 키워드2 ... 키워드N

    예:
    "성적 나누는 기준 알려줘." → 성적 | 기준
    "김대엽 교수님 연구실 어디야?" → 위치 | 김대엽 연구실
    "김대엽 교수님 연락처 어떻게 돼?" → 연락처 | 김대엽 연락처
    "언제까지 학교 나가야 돼?" → 학사일정 | 종강일
    "기숙사 들어가려면 뭐 내야 해?" → 서류 | 기숙사 제출 서류
    """

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_question}
    ]
    return normalizer_llm.invoke(messages).content.strip()