import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
_MODEL = "llama-3.1-8b-instant"

_SYSTEM_PROMPT = """당신은 친절한 Todo 관리 도우미입니다.
사용자의 Todo 목록을 분석하여 질문에 답변해 주세요.
답변은 한국어로 간결하게 작성하세요."""


def _build_todo_context(todos: list[dict]) -> str:
    if not todos:
        return "현재 등록된 Todo가 없습니다."
    lines = []
    for t in todos:
        status = "✅ 완료" if t.get("is_completed") else "⬜ 미완료"
        due = f" | 마감: {t['due_date']}" if t.get("due_date") else ""
        lines.append(f"- [{status}] {t['title']}{due}  (ID: {t['id']}, 생성일: {t['created_at'][:10]})")
    return "\n".join(lines)


def answer_with_todos(question: str, todos: list[dict]) -> str:
    system_msg = f"{_SYSTEM_PROMPT}\n\n## 현재 Todo 목록\n{_build_todo_context(todos)}"
    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": question},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def chat_with_todos(question: str, history: list[dict], todos: list[dict]) -> str:
    system_msg = f"{_SYSTEM_PROMPT}\n\n## 현재 Todo 목록\n{_build_todo_context(todos)}"
    messages = [{"role": "system", "content": system_msg}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": question})
    response = _client.chat.completions.create(
        model=_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content
