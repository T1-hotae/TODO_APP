# ZenTodo - 변경 이력

> 작성일: 2026-06-03
> 버전: 1.1.0

---

## v1.1.0 — UI 개선 + 날짜 지원 + AI 질의응답

### 1. UI 개선 (체크박스 · 카드 스타일 · 수정·삭제 버튼)

**배경**
기존 UI는 테이블 형태로 렌더링되고, 완료 토글과 삭제가 별도의 ID 입력 필드를 통해서만 동작하여 사용성이 낮았음.

**변경 파일**

| 파일 | 변경 내용 |
|------|-----------|
| `app/todo_list.py` | 전체 재작성 |
| `app/api_client.py` | `update_todo_title()` 추가 |
| `app/main.py` | `gr.Blocks(js=PAGE_JS)` 적용 |

**상세 변경**

- **테이블 제거 → 카드 리스트**: `<table>` 구조를 제거하고 `<div>` 기반 카드 스타일로 전환
- **체크박스**: 각 항목에 `<input type="checkbox">` 추가. 클릭 시 완료 상태 즉시 토글
- **인라인 수정 버튼**: 클릭 시 상단에 편집 행(텍스트박스 + 저장/취소) 표시
- **인라인 삭제 버튼**: 클릭 시 해당 항목 즉시 삭제
- **JS 브릿지**: `gr.HTML` 내부 스크립트는 브라우저 보안 정책상 직접 실행 불가 → `gr.Blocks(js=PAGE_JS)`로 페이지 로드 시 전역 함수 등록, HTML 버튼의 `onclick`에서 참조
- **Enter 키 제출**: `title_input.submit` 이벤트 연결

---

### 2. Feature 1 — 날짜(due_date) 지원

**변경 파일**

| 파일 | 변경 내용 |
|------|-----------|
| `app/api/models.py` | `due_date: Optional[date]` 필드 추가 |
| `app/api_client.py` | `add_todo(title, due_date=None)` 시그니처 변경 |
| `app/todo_list.py` | 날짜 입력 Textbox 추가, D-day 뱃지 렌더링 |

**상세 변경**

- **모델 확장**
  ```python
  # app/api/models.py
  class Todo(SQLModel, table=True):
      due_date: Optional[date] = Field(default=None)   # 추가

  class TodoCreate(SQLModel):
      due_date: Optional[date] = None                  # 추가

  class TodoUpdate(SQLModel):
      due_date: Optional[date] = None                  # 추가
  ```

- **입력 UI**: 할 일 입력 옆에 `마감일 (YYYY-MM-DD)` Textbox 추가 (선택 입력)

- **D-day 뱃지**: 마감일이 있는 항목에 색상 뱃지 자동 표시
  - `D-N` (미래) → 보라색 `#6366f1`
  - `D-Day` (당일) → 주황색 `#f59e0b`
  - `D+N` (지난 날) → 빨간색 `#ef4444`

- **DB 마이그레이션**: SQLite auto-migrate 미지원으로 `database.db` 삭제 후 서버 재시작 필요

---

### 3. Feature 2 — AI 질의응답 (Groq LLM)

**변경 파일**

| 파일 | 변경 내용 |
|------|-----------|
| `app/llm/__init__.py` | 신규 패키지 |
| `app/llm/groq_client.py` | Groq SDK Q&A 로직 |
| `app/api/routes/ask.py` | `POST /api/ask` 엔드포인트 |
| `app/main.py` | ask 라우터 등록 |
| `app/api_client.py` | `ask_question()` 추가 |
| `app/todo_list.py` | `gr.Tabs` 분리 + AI 탭 추가 |
| `.env` | `GROQ_API_KEY` 설정 |

**아키텍처**

```
User 질문 (Gradio AI 탭)
  └─ POST /api/ask
       └─ DB에서 전체 Todo 목록 조회
       └─ Groq API 호출 (llama3-8b-8192)
            System: Todo 목록 컨텍스트 포함
            User: 질문
       └─ 답변 반환 → Gradio Markdown 표시
```

**Groq 연동 상세**

```python
# app/llm/groq_client.py
model = "llama3-8b-8192"
temperature = 0.3
max_tokens = 1024
```

- 시스템 프롬프트에 전체 Todo 목록(ID, 제목, 완료 여부, 마감일, 생성일)을 컨텍스트로 주입
- 한국어 응답 지시

**새 API 엔드포인트**

```
POST /api/ask
Request:  { "question": "오늘 마감인 일이 있어?" }
Response: { "answer": "..." }
```

**UI 변경**

- `gr.Tabs`로 두 탭 분리
  - **📝 Todo**: 기존 기능 (날짜 입력 포함)
  - **🤖 AI 질의응답**: 질문 입력 + 답변 출력

---

## 재시작 절차

```powershell
# 서버 종료 후
Remove-Item c:\todo-list\database.db
uvicorn app.main:app --reload --port 8000
```
