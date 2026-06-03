# ZenTodo 구현 계획서

> 최종 수정: 2026-06-03  
> 버전: 1.1.0

---

## 단계별 로드맵

```
Phase 1: 프로젝트 세팅 & DB          ✅ 완료
    ↓
Phase 2: FastAPI CRUD API            ✅ 완료
    ↓
Phase 3: Gradio UI 연동              ✅ 완료
    ↓
Phase 4: 테스트                       ✅ 완료
    ↓
Phase 5: UI 개선                      ✅ 완료
    ↓
Phase 6: 날짜 지원 (due_date)         ✅ 완료
    ↓
Phase 7: AI 질의응답 (Groq LLM)      ✅ 완료
```

---

## Phase 1: 프로젝트 세팅 & DB ✅

**목표:** 가상 환경 구성, SQLite DB 연동

**완료 작업:**
- `requirements.txt` 패키지 정의
- `app/api/database.py`: SQLModel 엔진 + 세션 팩토리
- `app/api/models.py`: `Todo` 테이블 (`id`, `title`, `is_completed`, `created_at`)
- `.env`, `.env.template` 환경변수 파일 생성

---

## Phase 2: FastAPI CRUD API ✅

**목표:** UI 없이 단독 테스트 가능한 REST API 완성

**완료 작업:**
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
GET    /api/health       헬스 체크
```

---

## Phase 3: Gradio UI 연동 ✅

**목표:** 브라우저에서 동작하는 Todo 인터페이스 완성

**완료 작업:**
- `app/api_client.py`: FastAPI 호출 래퍼 함수
- `app/todo_list.py`: Gradio Blocks UI
- `app/main.py`에 `gr.mount_gradio_app` 마운트

---

## Phase 4: 테스트 ✅

**목표:** 핵심 API 동작 자동화 검증

**완료 작업:**
- `tests/conftest.py`: 인메모리 SQLite 테스트 DB + TestClient 설정
- `tests/test_api/test_todos.py`: CRUD 전체 케이스 테스트

---

## Phase 5: UI 개선 ✅

**목표:** 사용성 향상 — 테이블 제거, 인라인 인터랙션 추가

**완료 작업:**
- 테이블 → 카드 스타일 리스트 전환
- 각 항목에 인라인 체크박스(완료 토글), 수정 버튼, 삭제 버튼 추가
- `gr.Blocks(js=PAGE_JS)`: 페이지 로드 시 전역 JS 함수 등록 (HTML 버튼 이벤트 브릿지)
- Enter 키 제출 지원

---

## Phase 6: 날짜 지원 (due_date) ✅

**목표:** 마감일 입력 및 D-day 자동 계산

**완료 작업:**
- `app/api/models.py`: `due_date: Optional[date]` 필드 추가
- `app/api_client.py`: `add_todo(title, due_date=None)` 시그니처 변경
- `app/todo_list.py`: `gr.DateTime(include_time=False, type="string")` 컴포넌트 적용
- D-day 뱃지 렌더링 (미래: 보라, 당일: 주황, 초과: 빨강)
- DB 재생성 필요 (`database.db` 삭제 후 재시작)

---

## Phase 7: AI 질의응답 (Groq LLM) ✅

**목표:** 저장된 Todo 데이터 기반 자연어 질의응답

**완료 작업:**
- `app/llm/groq_client.py`: Groq SDK 연동, 시스템 프롬프트에 Todo 컨텍스트 주입
- `app/api/routes/ask.py`: `POST /api/ask` 엔드포인트
- `app/main.py`: ask 라우터 등록
- `app/api_client.py`: `ask_question(question)` 추가
- `app/todo_list.py`: `gr.Tabs` 분리 — 📝 Todo 탭 + 🤖 AI 질의응답 탭
- `.env`: `GROQ_API_KEY` 설정
- 모델: `llama3-8b-8192`, temperature 0.3

---

## 완료 체크리스트

- [x] Phase 1: DB 테이블 생성 확인
- [x] Phase 2: Swagger UI CRUD 테스트 통과
- [x] Phase 3: 브라우저 UI 동작 확인
- [x] Phase 4: pytest 전체 통과
- [x] Phase 5: 카드 UI + 인라인 버튼 동작 확인
- [x] Phase 6: 날짜 입력 + D-day 뱃지 표시 확인
- [x] Phase 7: AI 탭에서 질의응답 동작 확인
