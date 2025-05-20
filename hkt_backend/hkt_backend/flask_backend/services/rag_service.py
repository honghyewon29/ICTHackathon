# rag_service.py
from llm_utils.vector_store import load_vectorstore
from llm_utils.prompt_template import get_prompt
from llm_utils.gpt_client import generate_response
from llm_utils.retriever import get_multiquery_retriever
from llm_utils.normalizer import normalize_question
# from googletrans import Translator
from deep_translator import GoogleTranslator
import langid

def detect_language(text):
    lang, _ = langid.classify(text)
    return lang


context_boilerplate = """
이 챗봇은 수원대학교의 지능형SW융합대학 관련 질문에만 답변합니다.

지능형SW융합대학은 다음과 같은 구조로 되어 있습니다:
- 컴퓨터학부 → 컴퓨터SW학과, 미디어SW학과
- 정보통신학부 → 정보통신학과, 정보보호학과
- 데이터과학부 (단일)
- 클라우드융복합전공 (단일)
즉, "컴퓨터SW학과"는 "컴퓨터학부"에 포함됩니다.

컴퓨터sw 학과 교수진 정보

장성태 교수는 컴퓨터SW학과 소속으로, 전공은 컴퓨터구조, 차세대 Mobile Embedded System, 보안감시 기술이며, 이메일은 stjhang@suwon.ac.kr, 연구실은 ICT 융합대학 510호, 연락처는 031-220-2126입니다.

한성일 교수는 컴퓨터SW학과 소속이며, 전공은 Applied Machine Learning입니다. 이메일은 seongil.han@suwon.ac.kr, 연구실은 ICT 융합대학 521호, 연락처는 031-229-8218입니다.

준웨이푸 교수는 컴퓨터SW학과 소속이며, 전공과 연락처 정보는 없으며, 이메일도 없습니다. 연구실은 IT대학 405호입니다.

김장영 교수는 컴퓨터SW학과 소속이며, 전공은 빅데이터, 네트워크, 인공지능, 보안입니다. 이메일은 jykim77@suwon.ac.kr, 연구실은 지능형SW융합대학 522호, 연락처는 031-229-8345입니다.

구창진 교수는 컴퓨터SW학과 소속이며, 전공은 운영체제와 정보보호입니다. 이메일은 ycjkoo@suwon.ac.kr, 연구실은 미래혁신관 712호, 연락처는 031-229-8595입니다.

허성민 교수는 컴퓨터SW학과 소속이며, 전공, 이메일, 연구실, 연락처 정보가 제공되지 않았습니다.


하계방학은 1학기 종강 후 시작되며, 동계방학은 2학기 종강 후 시작됩니다.

사용자의 질문이 셔틀버스에 대한 내용이면, 셔틀버스 데이터만 사용하여 답변하세요.
셔틀이 아닌 대중교통(시내/광역/마을버스 등) 관련이면, 대중교통 버스 데이터만 사용하세요.
어떤 종류인지 구분이 어렵다면, 먼저 어떤 정보를 원하는지 물어보세요.
s
"""



def format_docs_with_boilerplate(docs):
    context_from_docs = "\n\n".join([d.page_content for d in docs])
    return context_boilerplate + "\n\n" + context_from_docs

translator = GoogleTranslator()
from openai import OpenAI
import langid
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)  # 환경변수에서 불러오면 더 안전해

def detect_language_with_gpt(text):
    system_prompt = (
        "너는 언어 감지 전문가야. 다음 문장의 언어를 ISO 639-1 코드 형식으로만 응답해. "
        "예: 한국어는 'ko', 영어는 'en', 일본어는 'ja', 아랍어는 'ar'"
    )
    user_prompt = f"문장: {text}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=5
        )
        lang = response.choices[0].message.content.strip().lower()
        print(f"🌐 GPT 감지 언어: {lang}")
        return lang
    except Exception as e:
        print(f"❌ GPT 언어 감지 실패: {e} → langid fallback")
        lang, _ = langid.classify(text)
        return lang

def ask_with_rag(user_input):
    # 1. 언어 감지 (단어가 너무 짧으면 영어로 간주)
    lang = detect_language_with_gpt(user_input)
    print(f"🌐 감지된 언어: {lang}")

    # 2. 검색용 번역 (비한국어 → 한국어)
    if lang != "ko":
        translated = translator.translate(user_input, src=lang, dest="ko")
        print(f"🔁 번역된 질문 (검색용): {translated}")
    else:
        translated = user_input

    # 3. 정형화
    normalized = normalize_question(translated)
    print(f"📌 정형화된 질문: {normalized}")

    # 4. 검색
    vectorstore = load_vectorstore()
    retriever = get_multiquery_retriever(vectorstore)
    retrieved_docs = retriever.invoke(normalized)

    # 5. context 생성
    from services.rag_service import format_docs_with_boilerplate  # 재귀 import 피하기 위해 이렇게 가능
    full_context = format_docs_with_boilerplate(retrieved_docs)

    # 6. 프롬프트 생성 (질문은 원문, 언어는 감지된 값)
    prompt = get_prompt()
    messages = prompt.format_messages(
        context=full_context,
        question=user_input,
        language=lang
    )

    # 7. 응답 생성
    response = generate_response(messages)
    return response.content.strip()