from llm_utils.vector_store import load_vectorstore
from llm_utils.prompt_template import get_prompt
from llm_utils.gpt_client import generate_response
from llm_utils.retriever import get_multiquery_retriever
from llm_utils.normalizer import normalize_question

context_boilerplate = """
이 챗봇은 수원대학교의 지능형SW융합대학 관련 질문에만 답변합니다.

지능형SW융합대학은 다음과 같은 구조로 되어 있습니다:
- 컴퓨터학부 → 컴퓨터SW학과, 미디어SW학과
- 정보통신학부 → 정보통신학과, 정보보호학과
- 데이터과학부 (단일)
- 클라우드융복합전공 (단일)
즉, "컴퓨터SW학과"는 "컴퓨터학부"에 포함됩니다.

[주요 일정 정보]
- 1학기 종강일: 6월 25일
- 2학기 종강일: 12월 15일

하계방학은 1학기 종강 후 시작되며, 동계방학은 2학기 종강 후 시작됩니다.
"""

def format_docs_with_boilerplate(docs):
    context = "\n\n".join([d.page_content for d in docs])
    return context_boilerplate + "\n\n" + context

def ask_with_rag(user_input):
    normalized = normalize_question(user_input)
    vectorstore = load_vectorstore()
    retriever = get_multiquery_retriever(vectorstore)
    retrieved_docs = retriever.invoke(normalized)

    full_context = format_docs_with_boilerplate(retrieved_docs)
    prompt = get_prompt()
    messages = prompt.format_messages(context=full_context, question=user_input)
    return generate_response(messages).strip()