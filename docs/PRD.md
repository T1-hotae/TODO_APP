# Product Requirements Document (PRD) - Todo App

## 1. 개요

### 1.1 프로젝트 소개
단순하고 직관적인 Todo 웹 애플리케이션입니다.  
**FastAPI** 백엔드 REST API와 **Gradio** 기반 웹 UI로 구성됩니다.

### 1.2 목표
- 할 일을 빠르게 추가·완료·삭제할 수 있는 단일 페이지 앱
- `uvicorn app.main:app --reload` 한 줄로 프론트엔드와 백엔드를 함께 실행

---

## 2. 시스템 아키텍처

```
Gradio UI (Frontend)
    ↕ HTTP (requests)
FastAPI REST API (Backend)
    ↕ SQLModel ORM
SQLite Database
```

| 레이어 | 역할 |
|--------|------|
| Gradio | 사용자 입력 수집, API 호출, HTML 렌더링 |
| FastAPI | CRUD 엔드포인트, 유효성 검사 |
| SQLite | 데이터 영속성 |

---

## 3. 기능 요구사항

### 3.1 Todo CRUD API

| Method | Endpoint | 설명 |
|--------|----------|------|
| `GET` | `/api/todos` | 전체 목록 조회 (생성순 내림차순) |
| `GET` | `/api/todos/{id}` | 단일 항목 조회 |
| `POST` | `/api/todos/` | 새 할 일 추가 (`title` 필수) |
| `PATCH` | `/api/todos/{id}` | 제목 또는 완료 상태 수정 |
| `DELETE` | `/api/todos/{id}` | 삭제 |

### 3.2 UI 기능

- **추가:** 제목 입력 후 추가 버튼 → 목록 즉시 갱신
- **완료 토글:** ID 입력 후 완료 토글 버튼 → 완료된 항목은 취소선 표시
- **삭제:** ID 입력 후 삭제 버튼 → 목록에서 제거

---

## 4. 데이터 모델

```python
class Todo:
    id: int          # PK (자동 생성)
    title: str       # 할 일 제목
    is_completed: bool  # 완료 여부 (기본값: False)
    created_at: datetime  # 생성 시각 (자동 생성)
```

---

## 5. 기술 스택

| 항목 | 기술 |
|------|------|
| Backend | FastAPI + Uvicorn |
| ORM | SQLModel (SQLite) |
| Frontend | Gradio Blocks |
| HTTP Client | requests |

---

## 6. 디렉토리 구조

```
c:/todo-list/
├── app/
│   ├── main.py              # 진입점: FastAPI 초기화, Gradio 마운트
│   ├── todo_list.py         # Gradio UI 컴포넌트
│   ├── api_client.py        # FastAPI 호출 래퍼 (requests)
│   └── api/
│       ├── models.py        # SQLModel ORM 모델
│       ├── schemas.py       # Pydantic 요청/응답 스키마
│       ├── database.py      # DB 엔진 및 세션 관리
│       ├── routes/
│       │   └── todos.py     # Todo CRUD 엔드포인트
│       └── services/
│           └── todo_service.py  # CRUD 비즈니스 로직
├── tests/
│   └── test_api/
│       └── test_todos.py    # API 단위 테스트
└── requirements.txt
```

---

## 7. 검증 계획

- `uvicorn app.main:app --reload` 실행 후 `http://localhost:8000` 접속
- Swagger UI(`/docs`)에서 CRUD 엔드포인트 직접 테스트
- `pytest tests/` 자동화 테스트 실행
