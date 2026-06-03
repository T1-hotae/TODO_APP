# Product Requirements Document (PRD) - ZenTodo

> 버전: 1.1.0  
> 최종 수정: 2026-06-03

---

## 1. 개요

### 1.1 프로젝트 소개
단순하고 직관적인 Todo 웹 애플리케이션입니다.  
**FastAPI** 백엔드 REST API와 **Gradio** 기반 웹 UI로 구성되며, **Groq LLM**을 통해 저장된 Todo 데이터에 대한 자연어 질의응답을 지원합니다.

### 1.2 목표
- 할 일을 빠르게 추가·완료·수정·삭제할 수 있는 단일 페이지 앱
- 마감일(due_date) 입력 및 D-day 자동 계산
- 저장된 Todo 목록 기반 AI 질의응답
- `uvicorn app.main:app --reload` 한 줄로 프론트엔드와 백엔드를 함께 실행

---

## 2. 시스템 아키텍처

```
Gradio UI (Frontend)
    ↕ HTTP (requests)
FastAPI REST API (Backend)
    ↕ SQLModel ORM          ↕ Groq SDK
SQLite Database           Groq LLM (llama3-8b)
```

| 레이어 | 역할 |
|--------|------|
| Gradio | 사용자 입력 수집, API 호출, HTML 렌더링 |
| FastAPI | CRUD 엔드포인트, AI 질의 라우팅, 유효성 검사 |
| SQLite | 데이터 영속성 |
| Groq | Todo 컨텍스트 기반 자연어 Q&A |

---

## 3. 기능 요구사항

### 3.1 Todo CRUD API

| Method | Endpoint | 설명 |
|--------|----------|------|
| `GET` | `/api/todos` | 전체 목록 조회 (생성순 내림차순) |
| `GET` | `/api/todos/{id}` | 단일 항목 조회 |
| `POST` | `/api/todos/` | 새 할 일 추가 (`title` 필수, `due_date` 선택) |
| `PATCH` | `/api/todos/{id}` | 제목·완료 상태·마감일 수정 |
| `DELETE` | `/api/todos/{id}` | 삭제 |
| `POST` | `/api/ask` | AI 질의응답 |

### 3.2 UI 기능

- **추가:** 제목 + 마감일(캘린더 피커) 입력 후 추가 → 목록 즉시 갱신
- **완료 체크박스:** 각 항목의 인라인 체크박스 클릭으로 완료 토글, 완료된 항목은 취소선 표시
- **인라인 수정:** 항목별 수정 버튼 클릭 → 편집 행 표시 → 저장/취소
- **인라인 삭제:** 항목별 삭제 버튼으로 즉시 제거
- **D-day 뱃지:** 마감일이 있는 항목에 자동 계산된 D-day 표시
- **AI 질의응답:** 별도 탭에서 저장된 Todo 데이터를 기반으로 자연어로 질문

### 3.3 AI 질의응답

- 전체 Todo 목록(제목, 완료 여부, 마감일)을 Groq LLM 컨텍스트로 제공
- 예시 질문: "오늘 마감인 일이 있어?", "아직 못 끝낸 일 요약해줘"
- 모델: `llama3-8b-8192`

---

## 4. 데이터 모델

```python
class Todo:
    id: int                     # PK (자동 생성)
    title: str                  # 할 일 제목
    is_completed: bool          # 완료 여부 (기본값: False)
    due_date: Optional[date]    # 마감일 (선택)
    created_at: datetime        # 생성 시각 (자동 생성)
```

---

## 5. 기술 스택

| 항목 | 기술 | 비고 |
|------|------|------|
| Backend | FastAPI + Uvicorn | REST API 서버 |
| ORM | SQLModel (SQLite) | DB 모델 및 세션 |
| Frontend | Gradio 6.x Blocks | `gr.DateTime` 컴포넌트 포함 |
| HTTP Client | requests | Gradio → FastAPI 내부 통신 |
| LLM | Groq SDK (`llama3-8b-8192`) | AI 질의응답 |
| 환경변수 | python-dotenv | GROQ_API_KEY 관리 |

---

## 6. 디렉토리 구조

```
c:/todo-list/
├── app/
│   ├── main.py              # 진입점: FastAPI 초기화, Gradio 마운트
│   ├── todo_list.py         # Gradio UI 컴포넌트 (탭 구성)
│   ├── api_client.py        # FastAPI 호출 래퍼 (requests)
│   ├── api/
│   │   ├── models.py        # SQLModel ORM 모델
│   │   ├── database.py      # DB 엔진 및 세션 관리
│   │   ├── routes/
│   │   │   ├── todos.py     # Todo CRUD 엔드포인트
│   │   │   └── ask.py       # AI 질의응답 엔드포인트
│   │   └── services/
│   │       └── todo_service.py  # CRUD 비즈니스 로직
│   └── llm/
│       └── groq_client.py   # Groq SDK 연동, Q&A 로직
├── tests/
│   └── test_api/
│       └── test_todos.py    # API 단위 테스트
├── docs/                    # 프로젝트 문서
├── .env                     # GROQ_API_KEY 등 환경변수
└── requirements.txt
```

---

## 7. 검증 계획

- `uvicorn app.main:app --reload` 실행 후 `http://localhost:8000` 접속
- Swagger UI(`/docs`)에서 CRUD 및 `/api/ask` 엔드포인트 직접 테스트
- `pytest tests/` 자동화 테스트 실행
