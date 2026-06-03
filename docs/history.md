# ZenTodo - Conversation History (대화 기록)

본 문서는 ZenTodo 프로젝트를 진행하며 교환한 사용자와 AI 어시스턴트 간의 전체 대화 및 의사결정 기록입니다.

---

## 💬 대화 타임라인

### 1. 첫 번째 대화 (2026-06-03 20:35:30)
* **사용자 요청:**
  ```text
  todo app에 대한 prd 파일 생성해줘
  ```
* **AI 수행 결과:**
  - ZenTodo의 기획서 초안 [PRD.md](PRD.md) 생성.

---

### 2. 두 번째 대화 (2026-06-03 20:38:19)
* **사용자 요청:**
  ```text
  ref 파일 참고해주고,
  gradio는 ui만 담당하고 계산이 필요한 부분은 전부 fast Api로 구현한 rest api에서 담당하게 해줘.
  prd 수정해줘.
  ```
* **AI 수행 결과:**
  - UI(Gradio)와 백엔드(FastAPI) 관심사를 분리하는 구조로 아키텍처 재설계.
  - [PRD.md](PRD.md) 전면 수정.

---

### 3. 세 번째 대화 (2026-06-03 20:39:33)
* **사용자 요청:**
  ```text
  여러 사람이 개발하기 때문에 기능 모듈 설계가 잘 되어야합니다
  ui부분, fastapi부분, 향후 llm 연동까지 고려해서 project 폴더를 제안해주세요.
  ```
* **AI 수행 결과:**
  - `app/api/`, `app/llm/`, `tests/` 등으로 분할된 모듈형 폴더 구조 설계안 수립.

---

### 4. 네 번째 대화 (2026-06-03 20:40:04)
* **사용자 요청:**
  ```text
  Groq 정도 쓸 생각만있어 방향만 안내해줘.
  ```
* **AI 수행 결과:**
  - 공식 `groq` SDK 직접 연결, `SQLModel` ORM 채택 방향으로 기술 스택 구체화.

---

### 5. 다섯 번째 대화 (2026-06-03 20:40:44)
* **사용자 요청:**
  ```text
  해당 내용 맞아. PRD에 반영해줘.
  ```
* **AI 수행 결과:**
  - 확정된 구조(SQLModel, Groq 직접 연동)를 [PRD.md](PRD.md)에 반영.

---

### 6. 여섯 번째 대화 (2026-06-03 20:41:18)
* **사용자 요청:**
  ```text
  이제 기본적인 todoapp 구현을 진행하는데 단계별 계획서를 작성해주세요.
  ```
* **AI 수행 결과:**
  - Phase 1~5까지의 개발 로드맵 [plan.md](plan.md) 작성.

---

### 7. 일곱 번째 대화 (2026-06-03 20:42:29)
* **사용자 요청:**
  ```text
  지금까지 내가 요청한 대화만 저장해줘.
  ```
* **AI 수행 결과:**
  - 사용자 요청 원본만 필터링한 [user_requests.md](user_requests.md) 생성.

---

### 8. 여덟 번째 대화 (2026-06-03 20:43:24)
* **사용자 요청:**
  ```text
  plan 1단계부터 만들어줘.
  ```
* **AI 수행 결과:**
  - Phase 1 (환경·DB) + Phase 2 (FastAPI CRUD) 동시 구현.
  - `models.py`, `database.py`, `todos.py`, `todo_service.py`, `main.py`, 테스트 코드 생성.

---

### 9. 아홉 번째 대화 (2026-06-03 20:51:18)
* **사용자 요청:**
  ```text
  지금까지 대화내용을 docs/ 에다가 저장해줘.
  ```
* **AI 수행 결과:**
  - `docs/` 디렉토리 생성 및 [history.md](history.md) 작성.

---

### 10. 열 번째 대화 (2026-06-03)
* **사용자 요청:**
  ```text
  두가지 기능을 개선하려고 함.
  1. todo 데이터 입력시 날짜 지원
  2. llm 호출해서 저장된 todo 데이터를 기반으로 질의응답.
  GROQ_API_KEY=... API 는 이거 사용. 계획해줘
  ```
* **AI 수행 결과:**
  - Feature 1 (due_date), Feature 2 (LLM Q&A) 구현 계획 수립 및 제안.

---

### 11. 열한 번째 대화 (2026-06-03)
* **사용자 요청:**
  ```text
  그전에 투두의 완료 표시를 체크박스로 하고,
  표 그림은 삭제하고
  수정 삭제 버튼을 추가해줘
  ```
* **AI 수행 결과:**
  - `app/todo_list.py` 전체 재작성: 테이블 → 카드 스타일, 인라인 체크박스·수정·삭제 버튼 추가.
  - `gr.Blocks(js=PAGE_JS)` 패턴으로 HTML 버튼 ↔ Python 핸들러 JS 브릿지 구현.
  - `app/api_client.py`에 `update_todo_title()` 추가.

---

### 12. 열두 번째 대화 (2026-06-03)
* **사용자 요청:**
  ```text
  (구현 계획 확인 후) 구현해줘.
  ```
* **AI 수행 결과:**
  - **Feature 1 — due_date 지원:**
    - `app/api/models.py`: `due_date: Optional[date]` 추가.
    - `app/api_client.py`: `add_todo(title, due_date)` 시그니처 변경.
    - `app/todo_list.py`: 날짜 Textbox 및 D-day 뱃지 추가.
  - **Feature 2 — AI 질의응답:**
    - `app/llm/groq_client.py` 신규 생성: Groq `llama3-8b-8192` 연동, Todo 컨텍스트 주입.
    - `app/api/routes/ask.py` 신규 생성: `POST /api/ask` 엔드포인트.
    - `app/main.py`: ask 라우터 등록.
    - `app/api_client.py`: `ask_question()` 추가.
    - `app/todo_list.py`: `gr.Tabs`로 분리 — 📝 Todo 탭 + 🤖 AI 질의응답 탭.
    - `.env`: `GROQ_API_KEY` 설정.
  - 변경 이력 문서 [changelog.md](changelog.md) 생성.

---

### 13. 열세 번째 대화 (2026-06-03)
* **사용자 요청:**
  ```text
  FO: 127.0.0.1:55196 - "POST /api/ask HTTP/1.1" 404 Not Found
  ```
* **AI 수행 결과:**
  - 원인 분석: `@router.post("/")` → 등록 경로 `/api/ask/`, 클라이언트 요청 경로 `/api/ask` 불일치.
  - `ask.py`의 데코레이터를 `@router.post("")`로 수정하여 trailing slash 제거.

---

### 14. 열네 번째 대화 (2026-06-03)
* **사용자 요청:**
  ```text
  web에서 날짜ui를 접근하는 방법을 충분히 검색하고, version 고려해서 코드를 수정해줘.
  ```
* **AI 수행 결과:**
  - Gradio 6.15.2 설치 버전 확인.
  - `venv/Lib/site-packages/gradio/components/datetime.py` 소스 직접 분석.
  - `gr.DateTime(include_time=False, type="string")`: 캘린더 팝업 UI, `"YYYY-MM-DD"` 문자열 또는 `None` 반환 확인.
  - `app/todo_list.py`의 날짜 `gr.Textbox` → `gr.DateTime` 컴포넌트로 교체.

---

### 15. 열다섯 번째 대화 (2026-06-03)
* **사용자 요청:**
  ```text
  @docs 폴더 전체적으로 업데이트 해줘
  ```
* **AI 수행 결과:**
  - `PRD.md`, `plan.md`, `history.md`, `user_requests.md`, `technical_spec.md` 전체 업데이트.
  - v1.1.0 기준 최신 기능(due_date, LLM Q&A, UI 개선) 반영.
