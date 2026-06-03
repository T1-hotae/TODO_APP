# ZenTodo - Conversation History (대화 기록)

본 문서는 ZenTodo 프로젝트를 진행하며 교환한 사용자와 AI 어시스턴트(Antigravity) 간의 전체 대화 및 의사결정 기록입니다.

---

## 💬 대화 타임라인

### 1. 첫 번째 대화 (2026-06-03 20:35:30)
* **사용자 요청:**
  ```text
  todo app에 대한 prd 파일 생성해줘
  ```
* **AI 수행 결과:**
  - 사용자의 할 일 관리뿐만 아니라 몰입과 분석(포모도로, 달성도 잔디 트래커)을 포함하는 프리미엄 투두 애플리케이션 **ZenTodo**의 기획서 초안 [PRD.md](file:///c:/todo-list/PRD.md) 생성.

---

### 2. 두 번째 대화 (2026-06-03 20:38:19)
* **사용자 요청:**
  ```text
  ref 파일 참고해주고,
  gradio는 ui만 담당하고 계산이 필요한 부분은 전부 fast Api로 구현한 rest api에서 담당하게 해줘.
  
  prd 수정해줘.
  ```
* **AI 수행 결과:**
  - `ref/` 폴더 내의 예제를 참조하여 프론트엔드 UI(Gradio)와 백엔드 API(FastAPI)의 관심사를 분리하는 구조로 아키텍처 재설계.
  - UI는 단순 렌더링만 처리하고, 핵심 CRUD 및 연산은 FastAPI REST API가 전담하도록 [PRD.md](file:///c:/todo-list/PRD.md)를 전면 수정.

---

### 3. 세 번째 대화 (2026-06-03 20:39:33)
* **사용자 요청:**
  ```text
  여러 사람이 개발하기 때문에 기능 모듈 설계가 잘 되어야합니다
  ui부분, fastapi부분, 향후 llm 연동까지 고려해서 project 폴더를 제안해주세요.
  ```
* **AI 수행 결과:**
  - 다인 협업 시 충돌을 방지하기 위한 기능성 모듈 분리(클린 아키텍처 스타일)를 제안.
  - `app/api/`, `app/ui/`, `app/llm/`, `tests/` 등으로 분할된 상세 폴더 구조 설계안이 담긴 구현 계획서 수립.

---

### 4. 네 번째 대화 (2026-06-03 20:40:04)
* **사용자 요청:**
  ```text
  Groq 정도 쓸 생각만있어 방향만 안내해줘.
  ```
* **AI 수행 결과:**
  - 무거운 LangChain 대신 공식 `groq` SDK를 직접 연결하여 가볍고 빠르게 자연어 투두 생성 기능을 파싱하는 방향으로 기술 스택 구체화.
  - ORM 기술로 FastAPI와 완벽히 호환되는 `SQLModel` 채택.

---

### 5. 다섯 번째 대화 (2026-06-03 20:40:44)
* **사용자 요청:**
  ```text
  해당 내용 맞아. PRD에 반영해줘.
  ```
* **AI 수행 결과:**
  - 확정된 모듈형 폴더 구조, SQLModel, Groq 직접 연동 구조를 [PRD.md](file:///c:/todo-list/PRD.md)의 기술 스택 및 아키텍처 섹션에 반영.

---

### 6. 여섯 번째 대화 (2026-06-03 20:41:18)
* **사용자 요청:**
  ```text
  이제 기본적인 todoapp 구현을 진행하는데 단계별 계획서를 작성해주세요.
  ```
* **AI 수행 결과:**
  - Phase 1(환경/DB)부터 Phase 5(AI 연동)까지 점진적인 빌드 및 테스트를 할 수 있는 개발 로드맵 작성.
  - 실행 가능한 형태의 단계별 계획서인 [plan.md](file:///c:/todo-list/plan.md) 파일을 워크스페이스에 생성.

---

### 7. 일곱 번째 대화 (2026-06-03 20:42:29)
* **사용자 요청:**
  ```text
  지금까지 내가 요청한 대화만 저장해줘.
  ```
* **AI 수행 결과:**
  - 사용자가 입력한 요청 원본(User Request)만 필터링한 이력 파일 [user_requests.md](file:///c:/todo-list/user_requests.md) 생성.

---

### 8. 여덟 번째 대화 (2026-06-03 20:43:24)
* **사용자 요청:**
  ```text
  plan 1단계부터 만들어줘.
  ```
* **AI 수행 결과:**
  - **Phase 1 및 Phase 2 동시 구현:**
    - `requirements.txt`, `.env.template`, `.env` 등 개발 환경 초기화.
    - `SQLModel` 기반 데이터베이스 모델 선언 및 DB 커넥션 셋업 ([models.py](file:///c:/todo-list/app/api/models.py), [database.py](file:///c:/todo-list/app/api/database.py)).
    - FastAPI 백엔드 CRUD API 구현 ([todos.py](file:///c:/todo-list/app/api/routes/todos.py), [todo_service.py](file:///c:/todo-list/app/api/services/todo_service.py), [main.py](file:///c:/todo-list/app/main.py)).
    - REST API 동작 확인을 위한 Pytest 단위 테스트 코드 작성 ([conftest.py](file:///c:/todo-list/tests/conftest.py), [test_todos.py](file:///c:/todo-list/tests/test_api/test_todos.py)).

---

### 9. 아홉 번째 대화 (2026-06-03 20:51:18 - 현재)
* **사용자 요청:**
  ```text
  지금까지 대화내용을 docs/ 에다가 저장해줘.
  ```
* **AI 수행 결과:**
  - 워크스페이스 내에 `docs/` 디렉토리를 생성하고, 전체 대화 맥락과 이력을 수록한 [history.md](file:///c:/todo-list/docs/history.md) 작성 완료.
