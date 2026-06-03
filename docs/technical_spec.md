# ZenTodo - 세부 기술 명세서

> 작성일: 2026-06-03  
> 버전: 1.1.0

---

## 1. 프로젝트 개요

### 1.1 목적
FastAPI REST API를 백엔드로, Gradio를 프론트엔드 UI로 사용하는 할 일 관리(Todo) 웹 애플리케이션. UI와 비즈니스 로직을 명확히 분리하고, Groq LLM을 통한 Todo 기반 자연어 질의응답 기능을 포함.

### 1.2 기술 스택

| 구분 | 기술 | 버전 | 역할 |
|------|------|------|------|
| 백엔드 프레임워크 | FastAPI | latest | REST API 서버 |
| ASGI 서버 | Uvicorn | latest | 비동기 HTTP 서버 |
| UI 프레임워크 | Gradio | 6.15.2 | 웹 인터페이스 |
| ORM | SQLModel | latest | DB 모델 정의 및 세션 관리 |
| 데이터베이스 | SQLite | 내장 | 로컬 파일 기반 영속 저장소 |
| 데이터 검증 | Pydantic | latest | 요청/응답 스키마 검증 |
| AI 연동 | Groq SDK | latest | LLM 질의응답 (`llama3-8b-8192`) |
| HTTP 클라이언트 | requests | latest | Gradio → FastAPI 내부 통신 |
| 테스트 | pytest | latest | API 단위/통합 테스트 |
| 설정 관리 | python-dotenv | latest | 환경변수 로드 |

---

## 2. 프로젝트 구조

```
todo-list/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI 앱 진입점 + Gradio 마운트
│   ├── api_client.py            # Gradio UI → FastAPI 통신 래퍼
│   ├── todo_list.py             # Gradio UI 컴포넌트 정의 (탭 구성)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── database.py          # DB 엔진, 세션 팩토리
│   │   ├── models.py            # SQLModel 테이블 모델 + 입력 스키마
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── todos.py         # /api/todos CRUD 라우터
│   │   │   ├── ask.py           # /api/ask LLM 질의응답 라우터
│   │   │   └── custom.css       # Gradio 커스텀 스타일
│   │   └── services/
│   │       └── todo_service.py  # CRUD 비즈니스 로직
│   └── llm/
│       ├── __init__.py
│       └── groq_client.py       # Groq SDK 연동, Q&A 함수
├── tests/
│   ├── conftest.py
│   └── test_api/
│       └── test_todos.py
├── docs/                        # 프로젝트 문서
├── ref/                         # 참고 예제
├── .env
├── .env.template
├── requirements.txt
└── database.db                  # SQLite DB 파일 (런타임 생성)
```

---

## 3. 아키텍처 설계

### 3.1 레이어 구조

```
┌──────────────────────────────────────────────┐
│               Gradio UI Layer                 │
│  todo_list.py + api_client.py                │
│  (렌더링만 담당, 비즈니스 로직 없음)            │
└──────────────┬───────────────────────────────┘
               │  HTTP (requests)
               ▼
┌──────────────────────────────────────────────┐
│            FastAPI Route Layer                │
│  routes/todos.py  |  routes/ask.py           │
│  (엔드포인트 정의, 입력 검증, 의존성 주입)      │
└──────────────┬───────────────────────────────┘
               │                    │
               ▼                    ▼
┌─────────────────────┐  ┌──────────────────────┐
│   Service Layer      │  │    LLM Layer          │
│  todo_service.py    │  │  llm/groq_client.py   │
│  (CRUD 로직)         │  │  (Groq SDK 호출)      │
└──────────┬──────────┘  └──────────────────────┘
           │  SQLModel Session
           ▼
┌──────────────────────────────────────────────┐
│           Database Layer                      │
│  app/api/database.py + SQLite                │
└──────────────────────────────────────────────┘
```

### 3.2 서버 단일화 전략
`gr.mount_gradio_app()`으로 FastAPI 앱 내 `/` 경로에 Gradio를 마운트하여 단일 포트(8000)에서 API와 UI를 동시 서빙.

```
http://localhost:8000/         → Gradio UI
http://localhost:8000/api/     → FastAPI REST API
http://localhost:8000/docs     → Swagger UI
```

---

## 4. 데이터 모델

### 4.1 Todo 테이블 (SQLite)

| 컬럼 | 타입 | 제약 | 설명 |
|------|------|------|------|
| `id` | INTEGER | PK, AUTO INCREMENT | 고유 식별자 |
| `title` | TEXT | NOT NULL | 할 일 제목 |
| `is_completed` | BOOLEAN | DEFAULT false | 완료 여부 |
| `due_date` | DATE | NULL 허용 | 마감일 |
| `created_at` | DATETIME | DEFAULT utcnow() | 생성 일시 (UTC) |

```python
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    is_completed: bool = Field(default=False)
    due_date: Optional[date] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 4.2 입력 스키마

```python
class TodoCreate(SQLModel):
    title: str
    due_date: Optional[date] = None

class TodoUpdate(SQLModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[date] = None
```

### 4.3 LLM 요청/응답 스키마

```python
class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
```

---

## 5. API 명세

### 5.1 엔드포인트 목록

| 메서드 | 경로 | 설명 | 응답 코드 |
|--------|------|------|-----------|
| `GET` | `/api/todos/` | 전체 목록 조회 (생성일 내림차순) | 200 |
| `GET` | `/api/todos/{todo_id}` | 단건 조회 | 200 / 404 |
| `POST` | `/api/todos/` | 새 할 일 생성 | 200 |
| `PATCH` | `/api/todos/{todo_id}` | 제목/완료/마감일 수정 | 200 / 404 |
| `DELETE` | `/api/todos/{todo_id}` | 삭제 | 200 / 404 |
| `POST` | `/api/ask` | AI 질의응답 | 200 / 400 |
| `GET` | `/api/health` | 헬스 체크 | 200 |

### 5.2 POST /api/todos/ 예시

```
Request:  { "title": "보고서 작성", "due_date": "2026-06-10" }
Response: { "id": 1, "title": "보고서 작성", "is_completed": false,
            "due_date": "2026-06-10", "created_at": "2026-06-03T11:00:00" }
```

### 5.3 POST /api/ask 예시

```
Request:  { "question": "오늘 마감인 일이 있어?" }
Response: { "answer": "네, '보고서 작성' 항목의 마감일이 오늘입니다." }
```

---

## 6. 데이터베이스 설정

| 항목 | 값 |
|------|-----|
| DB 종류 | SQLite |
| 파일 경로 | `./database.db` |
| 연결 옵션 | `check_same_thread=False` |
| 테이블 초기화 | `lifespan` 이벤트에서 `init_db()` 호출 |

> **주의:** `due_date` 컬럼 추가 후에는 기존 `database.db` 삭제 후 재시작 필요 (SQLite auto-migrate 미지원).

---

## 7. 서비스 레이어

**파일:** `app/api/services/todo_service.py`

| 메서드 | 동작 |
|--------|------|
| `create_todo(session, todo_data)` | ORM 객체 생성 후 저장 |
| `get_todos(session)` | `created_at` 내림차순 전체 조회 |
| `update_todo(session, todo_id, todo_data)` | `exclude_unset=True`로 변경 필드만 업데이트 |
| `delete_todo(session, todo_id)` | 삭제 후 객체 반환 |

---

## 8. LLM 레이어

**파일:** `app/llm/groq_client.py`

| 항목 | 값 |
|------|-----|
| 모델 | `llama3-8b-8192` |
| temperature | `0.3` |
| max_tokens | `1024` |
| 시스템 프롬프트 | 전체 Todo 목록(ID, 제목, 완료 여부, 마감일) 컨텍스트 포함 |

```python
def answer_with_todos(question: str, todos: list[dict]) -> str:
    # todos → 시스템 프롬프트에 포맷팅하여 주입
    # question → user 메시지
    # Groq API 호출 후 answer 반환
```

---

## 9. Gradio UI

### 9.1 탭 구조

```
gr.Blocks(js=PAGE_JS)
└── gr.Tabs
    ├── gr.TabItem("📝 Todo")
    │   ├── gr.Row
    │   │   ├── gr.Textbox (title_input)
    │   │   ├── gr.DateTime (due_input, include_time=False, type="string")
    │   │   └── gr.Button (add_btn)
    │   ├── gr.Row (edit_row, visible=False)
    │   │   ├── gr.Textbox (edit_input)
    │   │   ├── gr.Button (save_btn)
    │   │   └── gr.Button (cancel_btn)
    │   ├── gr.HTML (todo_display)
    │   ├── gr.Markdown (msg)
    │   ├── gr.Textbox (hidden_action, visible=False, elem_id="_todo_action")
    │   └── gr.Button (hidden_action_btn, visible=False, elem_id="_todo_action_btn")
    └── gr.TabItem("🤖 AI 질의응답")
        ├── gr.Textbox (question_input)
        ├── gr.Button (ask_btn)
        └── gr.Markdown (answer_output)
```

### 9.2 JS 브릿지

`gr.HTML` 내부 `<script>` 태그는 브라우저 보안 정책상 실행 불가 → `gr.Blocks(js=PAGE_JS)`로 페이지 로드 시 전역 함수를 등록하고, HTML 버튼의 `onclick`에서 참조.

```
HTML 버튼 onclick
  └─ window._todoDispatch({action, id, ...})
       └─ 숨겨진 textarea 값 업데이트 + dispatchEvent('input')
       └─ setTimeout → 숨겨진 Button 클릭
            └─ Gradio Python 핸들러 실행
```

### 9.3 gr.DateTime 컴포넌트

| 파라미터 | 값 | 설명 |
|----------|-----|------|
| `include_time` | `False` | 날짜만 선택 (시간 제외) |
| `type` | `"string"` | `"YYYY-MM-DD"` 포맷 문자열 반환 |
| `value` | `None` | 기본값 없음 |

반환값: `"YYYY-MM-DD"` 문자열 또는 미선택 시 `None` → FastAPI `Optional[date]` Pydantic 파싱과 호환.

### 9.4 D-day 뱃지

| 상태 | 색상 | 표시 |
|------|------|------|
| 미래 | 보라 `#6366f1` | `D-N` |
| 당일 | 주황 `#f59e0b` | `D-Day` |
| 초과 | 빨강 `#ef4444` | `D+N` |

---

## 10. 애플리케이션 진입점

**파일:** `app/main.py`

```python
app.include_router(todos.router, prefix="/api")   # /api/todos/*
app.include_router(ask.router, prefix="/api")     # /api/ask

with gr.Blocks(title="Todo App", js=PAGE_JS) as demo:
    create_todo_ui()

app = gr.mount_gradio_app(app, demo, path="/")
```

---

## 11. 환경 설정

| 변수명 | 설명 |
|--------|------|
| `PORT` | FastAPI 서버 포트 (기본: 8000) |
| `DATABASE_URL` | DB 연결 문자열 |
| `GROQ_API_KEY` | Groq LLM API 키 |

---

## 12. 테스트

### 12.1 테스트 전략
- 인메모리 SQLite DB로 격리된 테스트 실행
- FastAPI `dependency_overrides`로 운영 세션을 테스트 세션으로 교체

### 12.2 테스트 실행
```bash
pytest tests/ -v
```

---

## 13. 실행 방법

```bash
# 가상환경 활성화 (Windows)
.venv\Scripts\activate

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

| 주소 | 내용 |
|------|------|
| `http://localhost:8000/` | Gradio Todo UI |
| `http://localhost:8000/docs` | Swagger API 문서 |

---

*본 문서는 구현 진행에 따라 지속적으로 업데이트됩니다.*
