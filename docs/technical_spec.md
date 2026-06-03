# ZenTodo - 세부 기술 명세서

> 작성일: 2026-06-03  
> 버전: 1.0.0  
> 작성자: ZenTodo 개발팀

---

## 1. 프로젝트 개요

### 1.1 목적
FastAPI REST API를 백엔드로, Gradio를 프론트엔드 UI로 사용하는 할 일 관리(Todo) 웹 애플리케이션 구현. UI와 비즈니스 로직을 명확히 분리하여 다인 협업 및 향후 LLM(Groq) 연동에 대비한 확장성 확보.

### 1.2 기술 스택

| 구분 | 기술 | 버전 | 역할 |
|------|------|------|------|
| 백엔드 프레임워크 | FastAPI | latest | REST API 서버 |
| ASGI 서버 | Uvicorn | latest | 비동기 HTTP 서버 |
| UI 프레임워크 | Gradio | latest | 웹 인터페이스 |
| ORM | SQLModel | latest | DB 모델 정의 및 세션 관리 |
| 데이터베이스 | SQLite | 내장 | 로컬 파일 기반 영속 저장소 |
| 데이터 검증 | Pydantic | latest | 요청/응답 스키마 검증 |
| AI 연동 (예정) | Groq SDK | latest | 자연어 투두 파싱 |
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
│   ├── todo_list.py             # Gradio UI 컴포넌트 정의
│   └── api/
│       ├── __init__.py
│       ├── database.py          # DB 엔진, 세션 팩토리
│       ├── models.py            # SQLModel 테이블 모델 + 입력 스키마
│       ├── schemas.py           # Pydantic 응답 스키마
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── todos.py         # /api/todos CRUD 라우터
│       │   └── custom.css       # Gradio 커스텀 스타일
│       └── services/
│           └── todo_service.py  # CRUD 비즈니스 로직
├── tests/
│   ├── __init__.py (예정)
│   ├── conftest.py              # 테스트 픽스처 (인메모리 DB)
│   └── test_api/
│       └── test_todos.py        # API 엔드포인트 테스트
├── docs/
│   ├── plan.md                  # 단계별 개발 로드맵
│   ├── history.md               # 대화 이력
│   ├── user_requests.md         # 사용자 요청 이력
│   └── technical_spec.md        # 본 문서
├── ref/
│   ├── fastapi_calc.py          # FastAPI 참고 예제
│   └── fastapi_chat.py          # FastAPI + Gradio 참고 예제
├── .env                         # 환경변수 (git 제외)
├── .env.template                # 환경변수 템플릿
├── .gitignore
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
│  app/api/routes/todos.py                     │
│  (엔드포인트 정의, 입력 검증, 의존성 주입)      │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│           Service Layer                       │
│  app/api/services/todo_service.py            │
│  (CRUD 비즈니스 로직)                         │
└──────────────┬───────────────────────────────┘
               │  SQLModel Session
               ▼
┌──────────────────────────────────────────────┐
│           Database Layer                      │
│  app/api/database.py + SQLite                │
│  (데이터 영속화)                               │
└──────────────────────────────────────────────┘
```

### 3.2 서버 단일화 전략
Gradio 앱을 별도 포트로 실행하지 않고, `gr.mount_gradio_app()`으로 FastAPI 앱 내 `/` 경로에 마운트하여 단일 포트(8000)에서 API와 UI를 동시 서빙.

```
http://localhost:8000/         → Gradio UI
http://localhost:8000/api/     → FastAPI REST API
http://localhost:8000/docs     → Swagger UI (자동 생성)
```

---

## 4. 데이터 모델

### 4.1 Todo 테이블 (SQLite)

**파일**: [app/api/models.py](../app/api/models.py)

| 컬럼 | 타입 | 제약 | 설명 |
|------|------|------|------|
| `id` | INTEGER | PK, AUTO INCREMENT | 고유 식별자 |
| `title` | TEXT | NOT NULL | 할 일 제목 |
| `is_completed` | BOOLEAN | DEFAULT false | 완료 여부 |
| `created_at` | DATETIME | DEFAULT utcnow() | 생성 일시 (UTC) |

**SQLModel 정의:**
```python
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 4.2 입력 스키마

**TodoCreate** - 새 할 일 생성 시 요청 바디
```python
class TodoCreate(SQLModel):
    title: str  # 필수
```

**TodoUpdate** - 기존 할 일 수정 시 요청 바디 (PATCH 부분 업데이트)
```python
class TodoUpdate(SQLModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None
```

### 4.3 응답 스키마

**파일**: [app/api/schemas.py](../app/api/schemas.py)

```python
class TodoResponse(BaseModel):
    id: int
    title: str
    is_completed: bool
    created_at: str

    class Config:
        from_attributes = True  # SQLModel 객체 직렬화 허용
```

---

## 5. API 명세

### 5.1 엔드포인트 목록

**파일**: [app/api/routes/todos.py](../app/api/routes/todos.py)  
**Base Path**: `/api/todos`

| 메서드 | 경로 | 설명 | 응답 코드 |
|--------|------|------|-----------|
| `GET` | `/api/todos/` | 전체 목록 조회 (생성일 내림차순) | 200 |
| `GET` | `/api/todos/{todo_id}` | 단건 조회 | 200 / 404 |
| `POST` | `/api/todos/` | 새 할 일 생성 | 200 |
| `PATCH` | `/api/todos/{todo_id}` | 제목/완료 여부 수정 | 200 / 404 |
| `DELETE` | `/api/todos/{todo_id}` | 삭제 | 200 / 404 |
| `GET` | `/api/health` | 헬스 체크 | 200 |

### 5.2 엔드포인트 상세

#### GET /api/todos/
```
Response 200:
[
  {
    "id": 1,
    "title": "장보기",
    "is_completed": false,
    "created_at": "2026-06-03T11:00:00"
  },
  ...
]
```

#### POST /api/todos/
```
Request Body:
{
  "title": "장보기"
}

Response 200:
{
  "id": 1,
  "title": "장보기",
  "is_completed": false,
  "created_at": "2026-06-03T11:00:00"
}
```

#### PATCH /api/todos/{todo_id}
```
Request Body (부분 업데이트 가능):
{
  "is_completed": true
}

Response 200: (업데이트된 Todo 객체)
Response 404: {"detail": "Todo not found"}
```

#### DELETE /api/todos/{todo_id}
```
Response 200: {"ok": true}
Response 404: {"detail": "Todo not found"}
```

#### GET /api/health
```
Response 200: {"status": "healthy"}
```

### 5.3 의존성 주입 (DB 세션)
FastAPI `Depends`를 통해 각 라우터에 DB 세션을 주입. 세션은 요청마다 새로 생성되고, 컨텍스트 매니저로 자동 종료.

```python
def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=List[Todo])
def read_todos(session: Session = Depends(get_session)):
    ...
```

---

## 6. 데이터베이스 설정

**파일**: [app/api/database.py](../app/api/database.py)

| 항목 | 값 |
|------|-----|
| DB 종류 | SQLite |
| 파일 경로 | `./database.db` (실행 디렉토리 기준) |
| 연결 옵션 | `check_same_thread=False` (FastAPI 다중 스레드 대응) |
| SQL 로깅 | `echo=True` (개발 환경 - 운영 시 비활성화 권장) |
| 테이블 초기화 | `lifespan` 이벤트에서 `init_db()` 호출 (앱 시작 시 1회) |

```python
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)  # 테이블 없으면 생성 (있으면 스킵)
```

---

## 7. 서비스 레이어

**파일**: [app/api/services/todo_service.py](../app/api/services/todo_service.py)

모든 메서드는 `@staticmethod`로 정의. 라우터에서 세션을 받아 처리.

| 메서드 | 시그니처 | 동작 |
|--------|----------|------|
| `create_todo` | `(session, todo_data) → Todo` | `model_validate`로 ORM 객체 생성 후 저장 |
| `get_todos` | `(session) → List[Todo]` | `created_at` 내림차순 정렬 전체 조회 |
| `update_todo` | `(session, todo_id, todo_data) → Todo \| None` | `exclude_unset=True`로 변경된 필드만 업데이트 |
| `delete_todo` | `(session, todo_id) → Todo \| None` | 삭제 후 삭제된 객체 반환 (404 판단용) |

**부분 업데이트 처리 방식:**
```python
todo_dict = todo_data.model_dump(exclude_unset=True)  # 전달된 필드만 추출
for key, value in todo_dict.items():
    setattr(db_todo, key, value)
```

---

## 8. Gradio UI

### 8.1 UI 컴포넌트 구조

**파일**: [app/todo_list.py](../app/todo_list.py)

```
gr.Blocks
├── gr.Markdown("## 📝 Todo List")
├── gr.Row
│   ├── gr.Textbox (title_input) - 할 일 입력
│   └── gr.Button (add_btn) - 추가 버튼
├── gr.HTML (todo_display) - 동적 Todo 목록 테이블
├── gr.Row
│   ├── gr.Number (todo_id_input) - ID 입력
│   ├── gr.Button (toggle_btn) - 완료 토글
│   └── gr.Button (delete_btn) - 삭제
└── gr.Markdown (msg) - 상태 메시지
```

### 8.2 이벤트 핸들러

| 이벤트 | 핸들러 | 입력 | 출력 |
|--------|--------|------|------|
| add_btn.click | `handle_add` | title_input | todo_display, title_input(초기화), msg |
| toggle_btn.click | `handle_toggle` | todo_id_input | todo_display, msg |
| delete_btn.click | `handle_delete` | todo_id_input | todo_display, msg |

### 8.3 HTML 렌더링 (`format_todo_html`)
- 완료 항목: 텍스트에 `line-through` 스타일 + `✅` 아이콘
- 미완료 항목: 기본 스타일 + `⬜` 아이콘
- 빈 목록: 안내 메시지 출력

### 8.4 API 클라이언트

**파일**: [app/api_client.py](../app/api_client.py)

Gradio UI에서 FastAPI를 HTTP로 호출하는 래퍼 함수 모음. 모든 연산은 FastAPI가 처리.

| 함수 | HTTP 요청 | 설명 |
|------|-----------|------|
| `get_all_todos()` | `GET /api/todos` | 전체 목록 반환 |
| `add_todo(title)` | `POST /api/todos/` | 새 항목 추가 |
| `toggle_todo(todo_id)` | `GET` + `PATCH /api/todos/{id}` | 현재 상태 반전 후 업데이트 |
| `delete_todo(todo_id)` | `DELETE /api/todos/{id}` | 항목 삭제 |

---

## 9. 애플리케이션 진입점

**파일**: [app/main.py](../app/main.py)

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()   # 앱 시작 시 DB 테이블 초기화
    yield

app = FastAPI(title="Todo REST API", version="1.0.0", lifespan=lifespan)

# CORS 미들웨어 (전체 오리진 허용 - 개발 환경)
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)

# REST API 라우터 등록
app.include_router(todos.router, prefix="/api")

# Gradio UI를 / 경로에 마운트
app = gr.mount_gradio_app(app, demo, path="/")
```

---

## 10. 환경 설정

**파일**: [.env.template](../.env.template)

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `PORT` | `8000` | FastAPI 서버 포트 |
| `DATABASE_URL` | `sqlite:///database.db` | DB 연결 문자열 |
| `GROQ_API_KEY` | - | Groq LLM API 키 (Phase 4 예정) |

---

## 11. 테스트

### 11.1 테스트 전략
- 인메모리 SQLite DB(`sqlite:///:memory:`)를 사용해 실제 DB에 영향 없이 격리된 테스트 실행
- FastAPI `dependency_overrides`로 운영 세션을 테스트 세션으로 교체
- 각 테스트 케이스 전후 `create_all` / `drop_all`로 테이블 생성/삭제하여 테스트 간 독립성 보장

### 11.2 픽스처 구조

**파일**: [tests/conftest.py](../tests/conftest.py)

```python
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

### 11.3 테스트 케이스

**파일**: [tests/test_api/test_todos.py](../tests/test_api/test_todos.py)

| 테스트 함수 | 검증 내용 | 기대 상태코드 |
|-------------|-----------|---------------|
| `test_health_check` | `/api/health` 정상 응답 | 200 |
| `test_create_todo` | POST 생성 후 필드 검증 | 201 |
| `test_read_todos` | 목록 조회 + 우선순위 정렬 | 200 |
| `test_update_todo` | 제목/완료 여부 수정 | 200 |
| `test_delete_todo` | 삭제 후 404 확인 | 204 → 404 |

> **주의**: 현재 테스트 케이스는 `priority`, `content`, `category`, `due_date`, `d_day` 등 확장 필드를 검증하고 있으나, 현재 `Todo` 모델에는 해당 필드가 미구현 상태입니다. Phase 4에서 모델 확장 시 함께 구현 예정.

### 11.4 테스트 실행
```bash
pytest tests/ -v
```

---

## 12. 실행 방법

### 12.1 개발 서버 시작
```bash
# 가상환경 활성화
.venv\Scripts\activate  # Windows

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.template .env
# .env 파일에 GROQ_API_KEY 입력

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

### 12.2 접속 URL
| 주소 | 내용 |
|------|------|
| `http://localhost:8000/` | Gradio Todo UI |
| `http://localhost:8000/docs` | Swagger API 문서 |
| `http://localhost:8000/redoc` | ReDoc API 문서 |

---

## 13. 향후 개발 계획 (미구현)

### Phase 4: 모델 확장 (예정)
현재 테스트에서 참조하는 확장 필드를 `Todo` 모델에 추가:

| 필드 | 타입 | 설명 |
|------|------|------|
| `content` | `Optional[str]` | 상세 내용 |
| `priority` | `str` | 우선순위 (High / Medium / Low) |
| `category` | `Optional[str]` | 카테고리 (Work, Personal 등) |
| `due_date` | `Optional[date]` | 마감일 |
| `d_day` | `Optional[int]` | D-day 계산 (computed field) |

API 응답에도 이를 반영하여 `PUT /api/todos/{id}` (전체 업데이트), 우선순위 정렬 쿼리 파라미터 `?sort_by=priority` 지원.

### Phase 5: Groq LLM 연동 (예정)
- `app/llm/` 디렉토리에 Groq 클라이언트 및 파싱 로직 추가
- 자연어 입력 → 구조화된 TodoCreate 객체 변환
- 예: `"내일까지 보고서 써야함"` → `{"title": "보고서 작성", "due_date": "2026-06-04", "priority": "High"}`

---

*본 문서는 구현 진행에 따라 지속적으로 업데이트됩니다.*
