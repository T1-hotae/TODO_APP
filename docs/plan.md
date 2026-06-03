# Todo App 구현 계획서

## 단계별 로드맵

```
Phase 1: 프로젝트 세팅 & DB
    ↓
Phase 2: FastAPI CRUD API
    ↓
Phase 3: Gradio UI 연동
    ↓
Phase 4: 테스트
```

---

## Phase 1: 프로젝트 세팅 & DB

**목표:** 가상 환경 구성, SQLite DB 연동

**작업:**
- `requirements.txt` 패키지 정의 (`fastapi`, `uvicorn`, `gradio`, `sqlmodel`, `requests`, `pytest`, `httpx`)
- `app/api/database.py` 구현: SQLModel 엔진 + 세션 팩토리
- `app/api/models.py` 구현: `Todo` 테이블 (`id`, `title`, `is_completed`, `created_at`)

**검증:**
- `init_db()` 실행 시 `database.db` 파일 생성 확인

---

## Phase 2: FastAPI CRUD API

**목표:** UI 없이 단독 테스트 가능한 REST API 완성

**작업:**
- `app/api/services/todo_service.py`: CRUD 비즈니스 로직
- `app/api/routes/todos.py`: GET / POST / PATCH / DELETE 엔드포인트
- `app/main.py`: FastAPI 앱 인스턴스 + 라우터 등록

**엔드포인트:**
```
GET    /api/todos        전체 목록
GET    /api/todos/{id}   단일 조회
POST   /api/todos/       새 할 일 추가
PATCH  /api/todos/{id}   완료 토글 / 제목 수정
DELETE /api/todos/{id}   삭제
```

**검증:**
- `uvicorn app.main:app --reload` 후 `/docs` Swagger UI에서 CRUD 동작 확인

---

## Phase 3: Gradio UI 연동

**목표:** 브라우저에서 동작하는 Todo 인터페이스 완성

**작업:**
- `app/api_client.py`: `get_all_todos`, `add_todo`, `toggle_todo`, `delete_todo` 래퍼 함수
- `app/todo_list.py`: Gradio Blocks UI (추가 폼 + HTML 목록 + 토글/삭제 버튼)
- `app/main.py`에 `gr.mount_gradio_app` 마운트

**검증:**
- `http://localhost:8000` 접속 후 추가 → 완료 토글 → 삭제 흐름 확인

---

## Phase 4: 테스트

**목표:** 핵심 API 동작 자동화 검증

**작업:**
- `tests/conftest.py`: 인메모리 SQLite 테스트 DB + TestClient 설정
- `tests/test_api/test_todos.py`:
  - `POST /api/todos/` 성공 케이스
  - `GET /api/todos/` 목록 반환 확인
  - `PATCH /api/todos/{id}` 완료 토글 확인
  - `DELETE /api/todos/{id}` 삭제 확인

**검증:**
- `pytest tests/ -v` 전체 통과

---

## 완료 체크리스트

- [ ] Phase 1: DB 테이블 생성 확인
- [ ] Phase 2: Swagger UI CRUD 테스트 통과
- [ ] Phase 3: 브라우저 UI 동작 확인
- [ ] Phase 4: pytest 전체 통과
