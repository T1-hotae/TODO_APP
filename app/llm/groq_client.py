import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

_SYSTEM_PROMPT = """당신은 친절한 Todo 관리 도우미입니다.
사용자의 Todo 목록을 분석하여 질문에 답변해 주세요.
답변은 한국어로 간결하게 작성하세요."""


def answer_with_todos(question: str, todos: list[dict]) -> str:
    if not todos:
        todo_context = "현재 등록된 Todo가 없습니다."
    else:
        lines = []
        for t in todos:
            status = "✅ 완료" if t.get("is_completed") else "⬜ 미완료"
            due = f" | 마감: {t['due_date']}" if t.get("due_date") else ""
            lines.append(f"- [{status}] {t['title']}{due}  (ID: {t['id']}, 생성일: {t['created_at'][:10]})")
        todo_context = "\n".join(lines)

    system_msg = f"{_SYSTEM_PROMPT}\n\n## 현재 Todo 목록\n{todo_context}"

    response = _client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": question},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content
