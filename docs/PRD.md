# Product Requirements Document (PRD) - ZenTodo

## 1. 개요 (Overview)

### 1.1 프로젝트 소개
**ZenTodo**는 사용자의 몰입과 생산성 향상을 극대화하기 위해 설계된 미니멀하고 프리미엄한 다기능 Todo 애플리케이션입니다. 
본 프로젝트는 **Gradio를 활용한 고품질 웹 UI**와 **FastAPI 기반의 강력한 REST API 백엔드**를 결합하여 구현됩니다. 모든 핵심 연산, 데이터 지속성(Persistence), 비즈니스 로직은 FastAPI 백엔드에서 처리하고, Gradio는 오직 시각적 인터페이스 제공과 사용자 입력 전달(REST API 호출)만을 담당하도록 설계되었습니다.

### 1.2 배경 및 목적
* **UI/UX 개발 생산성:** Gradio를 통해 빠르게 반응형 웹 인터페이스를 구축하되, 커스텀 CSS와 HTML 요소를 결합하여 프리미엄 테마(Glassmorphism 등)를 연출합니다.
* **관심사 분리 (Separation of Concerns):** Gradio UI와 비즈니스 로직을 철저히 분리합니다. 계산, 통계 처리, 정렬, 데이터 CRUD는 전부 FastAPI의 REST API에서 수행되어, 백엔드의 독립적인 테스트 및 확장성을 보장합니다.
* **통합 실행성:** FastAPI 어플리케이션에 Gradio를 마운트하여 단일 명령어(`uvicorn main:app --reload`)로 프론트엔드와 백엔드를 동시에 실행하는 단일 진입점 구조를 가집니다.

---

## 2. 시스템 아키텍처 (System Architecture)

```mermaid
graph TD
    subgraph Gradio UI (Frontend)
        UI[Gradio Blocks Interface]
        Client[API Client: requests]
        UI -->|사용자 이벤트 발생| Client
        Client -->|화면 갱신 (HTML/Data)| UI
    end

    subgraph FastAPI Server (Backend)
        API[FastAPI App]
        Router[API Endpoints]
        Engine[Calculation & Logic Engine]
        DB[(SQLModel / SQLite Database)]
        LLM[Groq SDK Client]
        
        API --> Router
        Router --> Engine
        Engine --> DB
        Engine --> LLM
    end

    Client -->|REST API 요청 (HTTP GET/POST/PUT/DELETE)| Router
    Router -->|JSON 응답| Client
```

### 2.1 Gradio (Frontend) 역할
* 사용자 입력(투두 텍스트 입력, 우선순위/카테고리 선택, 버튼 클릭 등)을 획득합니다.
* Python의 `requests` 라이브러리를 통해 FastAPI의 REST API 엔드포인트를 호출합니다.
* API 응답 데이터를 활용해 Gradio 컴포넌트(Markdown, DataFrame, HTML, Plot 등)를 갱신합니다.
* 로직 계산(예: D-Day 계산, 완료율 계산, 차트 데이터 생성 등)을 **직접 수행하지 않고**, API로부터 계산 완료된 데이터를 받아 단순 렌더링만 처리합니다.

### 2.2 FastAPI (Backend REST API) 역할
* 투두 추가, 수정, 삭제, 조회 등 데이터 입출력 및 유효성 검사(Pydantic/SQLModel 사용)를 처리합니다.
* 데이터베이스(SQLite 및 SQLModel ORM)와의 읽기/쓰기를 전담합니다.
* **연산 및 AI 기능 전담:**
  * 투두 남은 시간 및 D-Day 연산
  * 카테고리별 분배비율 및 주간 완료율 백분위 계산
  * 포모도로 집중 시간 및 일일 달성도 그리드(잔디 심기) 시각화용 데이터 가공
  * 우선순위 및 정렬 로직 처리
  * **Groq API** 연동을 통한 자연어 분석(우선순위 자동 할당, 카테고리 태깅 등) 처리
* 데이터 보존을 담당하는 영속성 계층을 관리합니다.

---

## 3. 기능 요구사항 (Functional Requirements)

### 3.1 투두 관리 (Core Todo Engine)
* **투두 CRUD API:**
  * `GET /api/todos`: 정렬 방식(생성순, 우선순위순, D-Day순) 및 필터(전체, 미완료, 완료)에 따라 정렬 및 필터링된 투두 목록을 반환합니다. (정렬/필터링 계산은 FastAPI가 처리)
  * `POST /api/todos`: 제목, 내용, 기한(Due Date), 우선순위(High/Medium/Low), 카테고리를 포함한 투두를 생성합니다.
  * `PUT /api/todos/{todo_id}`: 완료 여부 변경, 본문 내용 수정 등을 수행합니다.
  * `DELETE /api/todos/{todo_id}`: 투두를 삭제합니다.

### 3.2 포모도로 타이머 및 몰입 (Pomodoro Focus Timer)
* **포모도로 타이머 상태 연산 API:**
  * `POST /api/pomodoro/start`: 타이머 세션 시작 기록.
  * `POST /api/pomodoro/complete`: 25분 집중 세션 완료 시, 특정 투두와 연동하여 집중 기록을 데이터베이스에 저장합니다.
* **Gradio 타이머 UI:**
  * Gradio의 `gr.Timer` 또는 브라우저의 HTML/JS 타이머 컴포넌트를 마운트하여 화면상에서 부드러운 카운트다운을 제공하되, 최종 완료 기록은 백엔드 API를 호출해 연산 및 기록을 수행합니다.

### 3.3 대시보드 및 달성도 분석 (Analytics & Calculation)
* **대시보드 통계 API:**
  * `GET /api/analytics`: 다음 계산 항목들을 종합적으로 연산하여 Gradio에 반환합니다.
    1. **일일 달성도 잔디 데이터:** 최근 30일/365일 동안의 일자별 완료 개수 배열 (깃허브 잔디 심기 렌더링용 HTML 데이터).
    2. **주간 완료 추이:** 최근 7일간 요일별 완료된 할 일 개수.
    3. **카테고리 비율:** 전체 할 일 대비 카테고리별 비중 백분율.
    4. **전체 달성률:** (완료된 할 일 / 전체 할 일) * 100 계산 값.
* **오늘의 명언 및 메시지 API:**
  * `GET /api/quote`: 사용자의 기분을 환기할 수 있는 오늘의 동기부여 명언을 백엔드 목록에서 매칭하여 제공합니다.

### 3.4 인공지능 (AI / LLM) 부가 기능
* **투두 자동 태깅 및 일정 파싱:**
  * 사용자가 자연어로 투두를 생성할 때 (예: "오늘 밤 10시까지 레포트 쓰기"), **Groq API**를 사용해 자연어를 해석한 후 마감 기한(`오늘`), 카테고리(`업무`), 우선순위(`High`)를 자동으로 파싱하여 JSON 형태로 응답하고 반영합니다.

---

## 4. UI/UX 디자인 철학 (Visual Design System)

Gradio의 기본 컴포넌트 레이아웃 위에 **Custom CSS**를 주입하여 프리미엄 감성의 현대적인 UI를 연출합니다.

### 4.1 비주얼 스타일 가이드
* **Glassmorphism:** 컴포넌트 배경에 투명도와 블러 효과를 주어 배경 레이어와 융합시킵니다.
  ```css
  .glass-card {
      background: rgba(20, 26, 40, 0.6);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
  }
  ```
* **Color Palette:**
  * **Primary background:** `hsl(224, 25%, 10%)` (매우 깊은 차콜 네이비)
  * **Accent Color:** `hsl(263, 70%, 55%)` (몽환적인 일렉트릭 바이올렛)
  * **Card Hover:** `hsl(224, 25%, 15%)` (미세하게 밝아지며 깊이감을 극대화)
* **Micro-interactions:** Gradio 버튼 hover, 투두 체크박스 클릭 시의 미세한 스케일 애니메이션 및 투명도 변경 효과 적용.

### 4.2 Gradio UI 레이아웃 구조 (Blocks)
* **상단 바 (Header):** 앱 로고("ZenTodo"), 오늘의 명언, 현재 포모도로 목표.
* **메인 영역 (Split Layout):**
  * **좌측 열 (Input & List):** 
    - 신규 투두 입력 폼 (텍스트 박스, 기한 선택기, 우선순위 드롭다운).
    - 투두 리스트 렌더링 영역 (HTML 컴포넌트를 사용하여 이쁜 체크박스 리스트와 D-Day 배지 렌더링).
  * **우측 열 (Focus & Analytics):**
    - 포모도로 타이머 위젯 (Zen Mode 진입용 버튼 포함).
    - 달성도 통계 차트 (Plot/HTML로 렌더링되는 꺾은선/원 차트 및 잔디 심기 그리드).

---

## 5. 기술 스택 (Technology Stack)

* **Backend API Framework:** FastAPI
* **Database ORM:** SQLModel (SQLite 연동)
* **Frontend UI Framework:** Gradio (Blocks 기반 웹 인터페이스)
* **AI/LLM Engine:** Groq SDK (직접 API 연동)
* **Communication Client:** `requests` (Gradio UI와 백엔드 간 REST API 통신)
* **ASGI Server:** Uvicorn

---

## 6. 프로젝트 디렉토리 구조 (Project Structure)

```
c:/todo-list/
├── app/
│   ├── __init__.py
│   ├── main.py                  # 진입점 (FastAPI 초기화, Gradio 마운트 및 CORS 설정)
│   │
│   ├── api/                     # 1. FastAPI 백엔드 (REST API)
│   │   ├── __init__.py
│   │   ├── routes/              # API 엔드포인트 라우터 (각 엔드포인트 기능 분리)
│   │   │   ├── __init__.py
│   │   │   ├── todos.py         # Todo CRUD 엔드포인트
│   │   │   ├── pomodoro.py      # 포모도로 타이머 상태/완료 API
│   │   │   ├── analytics.py     # 잔디 심기 및 백분율 통계 API
│   │   │   └── llm.py           # LLM 기반 AI 기능 위임 API (FastAPI 엔드포인트)
│   │   ├── schemas.py           # Pydantic 데이터 검증 모델 (Request / Response Body)
│   │   ├── database.py          # DB 연결 관리 및 Session 주입 (SQLModel 기반)
│   │   ├── models.py            # DB 테이블 선언 (SQLModel ORM 모델)
│   │   └── services/            # 비즈니스 로직 & 연산 계층 (엔드포인트에서 호출)
│   │       ├── __init__.py
│   │       ├── todo_service.py  # D-Day 연산, 정렬 로직, CRUD 연산 처리
│   │       ├── focus_service.py # 포모도로 세션 비즈니스 로직
│   │       └── stats_service.py # Github 스타일 잔디 HTML 생성 및 통계 수학적 계산
│   │
│   ├── ui/                      # 2. Gradio 프론트엔드 (UI 계층)
│   │   ├── __init__.py
│   │   ├── dashboard.py         # Gradio 메인 Blocks 레이아웃 통합 파일
│   │   ├── api_client.py        # 백엔드 API를 호출하는 REST API 래퍼 모듈 (requests 활용)
│   │   ├── styles/
│   │   │   └── custom.css       # 프리미엄 Glassmorphism, 다크모드 테마 CSS 파일
│   │   └── components/          # Gradio 컴포넌트 모듈화
│   │       ├── __init__.py
│   │       ├── header.py        # 로고, 오늘의 명언 영역
│   │       ├── todo_list.py     # 투두 작성 폼, HTML 렌더링 목록 테이블
│   │       ├── pomodoro.py      # 포모도로 카운트다운 컴포넌트
│   │       └── stats_panel.py   # 잔디 심기 그리드, SVG/Plot 차트 컴포넌트
│   │
│   └── llm/                     # 3. Groq SDK 연동 모듈 (비동기 처리)
│       ├── __init__.py
│       ├── client.py            # Groq 클라이언트 인스턴스 초기화 (groq SDK 활용)
│       ├── prompts.py           # 프롬프트 템플릿 관리
│       └── services/
│           ├── __init__.py
│           ├── tagger.py        # 투두 자연어 입력 시 AI 기반 속성(기한, 카테고리 등) 자동 파싱 서비스
│           └── assistant.py     # 사용자 학습 패턴/할 일 분석 피드백 리포트 작성 서비스
│
├── tests/                       # 4. 테스트 자동화 스위트
│   ├── __init__.py
│   ├── conftest.py              # Pytest DB 세션 및 클라이언트 Mock 설정
│   ├── test_api/                # API 라우터 단위 테스트
│   └── test_services/           # 서비스(연산) 로직 단위 테스트
│
├── .env.template                # 환경 변수 템플릿 (GROQ_API_KEY 포함)
├── requirements.txt             # 의존성 패키지 목록
└── README.md                    # 빌드 및 실행 가이드 문서
```

---

## 7. 개발 및 검증 계획 (Verification & API Test)

### 7.1 백엔드 API 테스트
* FastAPI의 Swagger UI (`/docs`)를 활용해 독립적으로 CRUD API 및 Analytics API의 반환 데이터가 정확한 연산 값인지 검증합니다.
* `pytest` 및 `httpx`를 사용하여 API 엔드포인트 단위의 자동화 테스트를 수행합니다.

### 7.2 프론트엔드 연동 테스트
* Gradio UI에서 각 컴포넌트 조작 시 콘솔 로그 및 FastAPI 액세스 로그를 체크하여, UI 단에서의 독자적인 비즈니스 로직 연산이 발생하지 않고 **전부 API 통신을 경유**하는지 모니터링합니다.
