# FastAPI 게시판 팀 프로젝트 계획서

## 1. 프로젝트 개요

### 1.1 프로젝트명

**FastAPI Board & Support API**

### 1.2 프로젝트 목표

FastAPI를 이용하여 회원, 게시글, 댓글, 문의사항 기능을 제공하는 게시판 백엔드 API를 구현한다. 추가로 Gemini API를 연동하여 사용자의 질문에 답변하는 독립적인 Chat API를 구현한다.

각 팀원은 자신의 브랜치에서 하나의 기능을 담당하여 `scheme → service → router` 구조로 개발하고, Supabase의 PostgreSQL 테이블을 사용하여 데이터를 저장한다. 팀원별 개인 실행 파일과 테스트 코드는 로컬에서만 사용하고 GitHub에는 업로드하지 않는다.

### 1.3 주요 기능

- User CRUD: 회원가입, 회원 조회, 회원정보 수정, 회원 삭제
- Post CRUD: 게시글 작성, 게시글 조회, 게시글 수정, 게시글 삭제
- Comment CRUD: 댓글 작성, 댓글 조회, 댓글 수정, 댓글 삭제
- Support CRUD: 문의사항 작성, 문의사항 조회, 문의사항 수정, 문의사항 삭제
- Gemini Chat API: 사용자의 질문을 Gemini API에 전달하고 답변 반환

### 1.4 개발 기준

- 참고 저장소: `https://github.com/kiwi248/mini0722.git`
- 참고 폴더: `04_mini_project`
- 참고 구조: `core`, `routers`, `schemas`, `services`, `tests`, `sql` 폴더로 기능을 분리한다.
- 각 CRUD 기능은 다른 팀원의 서비스 코드를 직접 호출하지 않는다.
- 데이터 관계는 `user_id`, `post_id` 등의 공통 ID를 통해 표현한다.
- 팀원은 개인 실행 파일로 자신의 기능을 독립적으로 실행하고 Swagger UI에서 확인한다.
- 최종 통합은 팀장이 `app/main.py`에서 모든 라우터를 등록하여 진행한다.

---

## 2. 기술 스택

| 구분 | 기술 | 용도 |
|---|---|---|
| Language | Python 3.12.7 | 백엔드 개발 언어 |
| Web Framework | FastAPI | REST API 구현 |
| Server | Uvicorn | FastAPI 애플리케이션 실행 |
| Validation | Pydantic | 요청 및 응답 데이터 검증 |
| Database | Supabase PostgreSQL | User, Post, Comment, Support 데이터 저장 |
| Database SDK | Supabase Python SDK | Python에서 Supabase 연결 |
| LLM | Google Gemini API | Chat API 응답 생성 |
| Test | pytest, FastAPI TestClient | API 자동 테스트 |
| Version Control | Git, GitHub | 브랜치 기반 협업 |
| API Document | Swagger UI | API 실행 및 확인 |

---

## 3. 프로젝트 구조

`04_mini_project`의 구조를 참고하여 아래와 같이 구성한다.

```text
04_mini_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── chat_config.py
│   │   └── supabase_client.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat_router.py
│   │   ├── user_router.py
│   │   ├── post_router.py
│   │   ├── comment_router.py
│   │   └── support_router.py
│   │
│   ├── schemes/
│   │   ├── __init__.py
│   │   ├── chat_scheme.py
│   │   ├── user_scheme.py
│   │   ├── post_scheme.py
│   │   ├── comment_scheme.py
│   │   └── support_scheme.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── chat_service.py
│       ├── user_service.py
│       ├── post_service.py
│       ├── comment_service.py
│       └── support_service.py
│
├── sql/
│   ├── users.sql
│   ├── posts.sql
│   ├── comments.sql
│   └── supports.sql
│
├── tests/
│   ├── test_chat_router.py
│   ├── test_user_router.py
│   ├── test_post_router.py
│   ├── test_comment_router.py
│   └── test_support_router.py
│
├── .env
├── .env.example
├── .gitignore
├── PLAN.md
├── README.md
└── requirements.txt
```

### 3.1 폴더 역할

| 폴더 | 역할 |
|---|---|
| `app/core` | Gemini 설정과 Supabase 연결처럼 공통으로 사용하는 설정 관리 |
| `app/routers` | URL 경로와 HTTP 메서드를 정의하고 요청을 받는 계층 |
| `app/schemes` | 요청과 응답에 사용할 Pydantic 모델 정의 |
| `app/services` | 데이터 조회·생성·수정·삭제와 같은 실제 기능 처리 |
| `sql` | Supabase에서 실행할 PostgreSQL 테이블 생성문 관리 |
| `tests` | 각 API가 정상적으로 동작하는지 확인하는 pytest 코드 |

> 참고 저장소의 `04_mini_project`에는 `app`, `sql`, `tests`, `.env.example`, `.gitignore`, `PLAN.md`, `README.md`, `requirements.txt`가 있으며, 애플리케이션 내부는 `core`, `routers`, `schemas`, `services` 형태로 분리되어 있다. 본 프로젝트에서는 팀 규칙에 맞춰 폴더명을 `schemes`로 통일한다.

### 3.2 기존 Product 예제 파일 정리 규칙

- `team1_0722` 저장소의 개인 브랜치에서 작업을 시작하기 전에 기존 Product 예제 파일을 모두 삭제한다.
- 예: `product_router.py`, `product_service.py`, `product_schema.py`, Product 관련 SQL·테스트 파일 등
- 각 팀원은 자신이 맡은 기능의 파일만 새로 작성하여 개인 브랜치에 올린다.
- 다른 팀원의 담당 파일과 공통 파일은 특별한 협의 없이 수정하지 않는다.
- 최종 통합 파일인 `app/main.py`는 팀장 윤기화가 `main` 브랜치에서 정리한다.

---

## 4. 역할 분담

| 팀원 | 역할 | 담당 기능 | 담당 파일 | 브랜치 |
|---|---|---|---|---|
| 윤기화 | 팀장 | 공통 구조, Gemini Chat API, 최종 통합 | `chat_config.py`, `supabase_client.py`, `chat_scheme.py`, `chat_service.py`, `chat_router.py`, `main.py`, `README.md` | `feature/ygh` |
| 손영민 | 팀원 | Post CRUD | `post_scheme.py`, `post_service.py`, `post_router.py`, `posts.sql` | `feature/sym` |
| 김인혜 | 팀원 | Support CRUD | `support_scheme.py`, `support_service.py`, `support_router.py`, `supports.sql` | `feature/kih` |
| 장상옥 | 팀원 | User CRUD | `user_scheme.py`, `user_service.py`, `user_router.py`, `users.sql` | `feature/jso` |
| 권오현 | 팀원 | Comment CRUD | `comment_scheme.py`, `comment_service.py`, `comment_router.py`, `comments.sql` | `feature/koh` |

### 4.1 팀장 담당 사항

- GitHub에 기본 프로젝트 구조 업로드
- 공통 `requirements.txt`, `.gitignore`, `.env.example` 작성
- `supabase_client.py` 기본 연결 코드 작성
- Gemini API 연동
- 팀원 코드 확인 및 충돌 해결
- 모든 라우터를 `app/main.py`에 등록
- 최종 Swagger UI 및 pytest 확인
- 최종본을 `main` 브랜치에 정리

### 4.2 팀원 공통 담당 사항

- 본인 기능의 Scheme 작성
- 본인 기능의 Service 작성
- 본인 기능의 Router 작성
- 본인 기능의 SQL 작성
- 개인 실행 파일로 API 실행
- Swagger UI에서 직접 테스트
- `tests` 폴더에 pytest 작성
- 자신의 브랜치에 Commit 및 Push

---

## 5. Git 브랜치 전략

### 5.1 브랜치명

| 팀원 | 브랜치명 |
|---|---|
| 윤기화 | `feature/ygh` |
| 손영민 | `feature/sym` |
| 김인혜 | `feature/kih` |
| 장상옥 | `feature/jso` |
| 권오현 | `feature/koh` |

### 5.2 브랜치 생성

```bash
git switch main
git pull origin main
git switch -c feature/jso
```

각 팀원은 마지막 명령의 브랜치명만 자신의 브랜치명으로 변경한다.

### 5.3 작업 순서

```text
main 최신화
    ↓
개인 feature 브랜치 생성
    ↓
Scheme 작성
    ↓
Service 작성
    ↓
Router 작성
    ↓
개인 실행 파일 작성
    ↓
Swagger UI 테스트
    ↓
pytest 작성 및 실행
    ↓
Commit
    ↓
Push
    ↓
Pull Request 생성 또는 팀장에게 병합 요청
    ↓
팀장이 main 브랜치에 최종 통합
```

### 5.4 Commit 예시

```bash
git add app/schemes/user_scheme.py
git add app/services/user_service.py
git add app/routers/user_router.py
git add sql/users.sql

git commit -m "feat: User CRUD 구현"
git push -u origin feature/jso
```

### 5.5 Git 규칙

- 작업 전 반드시 `main` 브랜치를 최신 상태로 받는다.
- 개인 브랜치에서 기존 Product 관련 파일을 삭제한 뒤 작업한다.
- 각자 맡은 기능의 파일만 작성하고 Commit한다.
- 다른 팀원의 파일은 특별한 이유가 없으면 수정하지 않는다.
- `app/main.py`의 최종 수정은 팀장이 담당한다.
- `.env`, 개인 실행 파일, `tests` 폴더는 Commit하지 않는다.
- API Key와 Supabase Key를 코드에 직접 작성하지 않는다.
- Push 전에 `git status`로 업로드 대상 파일을 확인한다.
- 최종 통합 전 자신의 브랜치에서 API가 정상 작동하는지 확인한다.

---

## 6. `.gitignore`

```gitignore
# 환경 변수
.env

# 개인 실행 파일
app/ygh.py
app/sym.py
app/kih.py
app/jso.py
app/koh.py

# 개인 테스트 코드
tests/

# Python 캐시
__pycache__/
*.pyc
*.pyo
*.pyd

# 가상환경
.venv/
venv/

# pytest 캐시
.pytest_cache/

# IDE 설정
.vscode/
.idea/

# 운영체제 파일
.DS_Store
Thumbs.db
```

### 6.1 주의사항

`tests/` 전체를 `.gitignore`에 등록하면 팀원들의 테스트 코드는 GitHub에서 공유되지 않는다. 따라서 각 팀원은 로컬에서 자신의 테스트 코드를 관리하고, 팀장은 최종 통합 후 필요한 경우 별도의 통합 테스트를 직접 작성한다.

---

## 7. `.env` 예시

각 팀원은 프로젝트 루트에 자신의 `.env` 파일을 생성한다.

```env
GEMINI_API_KEY=각자의_Gemini_API_Key
GEMINI_MODEL=gemini-3.5-flash
PYTHON_VERSION=3.12.7

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=각자의_Supabase_Key
```

공개 가능한 `.env.example`은 실제 값을 넣지 않고 다음과 같이 작성한다.

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash
PYTHON_VERSION=3.12.7

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
```

### 7.1 환경변수 사용 원칙

- `.env`는 절대 GitHub에 올리지 않는다.
- `.env.example`만 GitHub에 올린다.
- Gemini API Key와 Supabase Key를 Python 코드에 직접 작성하지 않는다.
- 팀원이 같은 Supabase 프로젝트를 사용할 경우 팀장이 테이블 이름과 컬럼명을 먼저 확정한다.
- `SUPABASE_SERVICE_ROLE_KEY`를 사용할 경우 관리자 수준 권한이 있으므로 외부에 노출하지 않는다.

### 7.2 Python 버전 고정

팀원 전원이 Python `3.12.7`을 사용한다. 설치된 버전은 아래 명령어로 확인한다.

```bash
python --version
```

예상 출력:

```text
Python 3.12.7
```

프로젝트 루트에 `.python-version` 파일을 사용할 경우 다음 한 줄을 작성한다.

```text
3.12.7
```

---

## 8. API 설계

### 8.1 공통 경로

| 기능 | 기본 경로 | 담당자 |
|---|---|---|
| 회원 | `/users` | 장상옥 |
| 게시글 | `/posts` | 손영민 |
| 댓글 | `/comments` | 권오현 |
| 문의사항 | `/supports` | 김인혜 |
| Gemini Chat | `/chat/gemini` | 윤기화 |

### 8.2 전체 API 목록

| 기능 | Method | 경로 | 설명 |
|---|---|---|---|
| 회원가입 | `POST` | `/users` | 새로운 회원 생성 |
| 전체 회원 조회 | `GET` | `/users` | 회원 목록 조회 |
| 회원 한 명 조회 | `GET` | `/users/{user_id}` | 회원 ID로 상세 조회 |
| 회원정보 수정 | `PUT` | `/users/{user_id}` | 회원정보 전체 수정 |
| 회원 삭제 | `DELETE` | `/users/{user_id}` | 회원 삭제 |
| 게시글 작성 | `POST` | `/posts` | 게시글 생성 |
| 전체 게시글 조회 | `GET` | `/posts` | 게시글 목록 조회 |
| 게시글 한 개 조회 | `GET` | `/posts/{post_id}` | 게시글 상세 조회 |
| 게시글 수정 | `PUT` | `/posts/{post_id}` | 게시글 수정 |
| 게시글 삭제 | `DELETE` | `/posts/{post_id}` | 게시글 삭제 |
| 댓글 작성 | `POST` | `/posts/{post_id}/comments` | 특정 게시글에 댓글 생성 |
| 전체 댓글 조회 | `GET` | `/comments` | 전체 댓글 목록 조회 |
| 게시글별 댓글 조회 | `GET` | `/posts/{post_id}/comments` | 특정 게시글 댓글 조회 |
| 댓글 한 개 조회 | `GET` | `/comments/{comment_id}` | 댓글 상세 조회 |
| 댓글 수정 | `PUT` | `/comments/{comment_id}` | 댓글 내용 수정 |
| 댓글 삭제 | `DELETE` | `/comments/{comment_id}` | 댓글 삭제 |
| 문의 작성 | `POST` | `/supports` | 문의사항 생성 |
| 전체 문의 조회 | `GET` | `/supports` | 문의사항 목록 조회 |
| 문의 한 개 조회 | `GET` | `/supports/{support_id}` | 문의사항 상세 조회 |
| 문의 수정 | `PUT` | `/supports/{support_id}` | 문의사항 수정 |
| 문의 삭제 | `DELETE` | `/supports/{support_id}` | 문의사항 삭제 |
| Gemini 질문 | `POST` | `/chat/gemini` | 질문을 Gemini에 전달하고 답변 반환 |

### 8.3 공통 응답 원칙

- 생성 성공: `201 Created`
- 조회·수정 성공: `200 OK`
- 삭제 성공: `200 OK` 또는 `204 No Content`
- 요청값 검증 실패: `422 Unprocessable Entity`
- 데이터 없음: `404 Not Found`
- 중복 이메일: `409 Conflict`
- 서버 또는 외부 API 오류: `500 Internal Server Error`

---

## 9. User CRUD

### 9.1 기능 설명

회원가입, 회원 목록 조회, 회원 상세 조회, 회원정보 수정, 회원 삭제 기능을 제공한다.

비밀번호는 입력받아 저장하지만 API 응답에는 포함하지 않는다. 실제 서비스에서는 비밀번호를 평문으로 저장하면 안 되지만, 본 미니 프로젝트에서는 수업 범위에 따라 구현한다. 가능하면 추후 해시 처리한다.

### 9.2 담당 파일

```text
app/schemes/user_scheme.py
app/services/user_service.py
app/routers/user_router.py
sql/users.sql
```

### 9.3 Scheme 예시

```python
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)
    nickname: str = Field(min_length=2, max_length=30)


class UserUpdate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)
    nickname: str = Field(min_length=2, max_length=30)


class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    nickname: str
    created_at: str
```

### 9.4 API 경로

| 기능 | Method | 경로 |
|---|---|---|
| 회원가입 | `POST` | `/users` |
| 전체 회원 조회 | `GET` | `/users` |
| 회원 한 명 조회 | `GET` | `/users/{user_id}` |
| 회원정보 수정 | `PUT` | `/users/{user_id}` |
| 회원 삭제 | `DELETE` | `/users/{user_id}` |

### 9.5 회원가입 Request

```json
{
  "email": "user1@example.com",
  "password": "1234",
  "nickname": "상옥"
}
```

### 9.6 회원가입 Response

```json
{
  "user_id": 1,
  "email": "user1@example.com",
  "nickname": "상옥",
  "created_at": "2026-07-22T10:00:00+09:00"
}
```

### 9.7 회원 목록 Response

```json
[
  {
    "user_id": 1,
    "email": "user1@example.com",
    "nickname": "상옥",
    "created_at": "2026-07-22T10:00:00+09:00"
  }
]
```

### 9.8 회원정보 수정 Request

```json
{
  "email": "updated@example.com",
  "password": "5678",
  "nickname": "상옥수정"
}
```

### 9.9 회원 삭제 Response

```json
{
  "message": "회원이 삭제되었습니다.",
  "user_id": 1
}
```

### 9.10 User 테이블 컬럼

| 컬럼 | 자료형 | PK | FK | NOT NULL | DEFAULT | 설명 |
|---|---|---|---|---|---|---|
| `user_id` | `BIGINT` | O | X | O | 자동 증가 | 회원 번호 |
| `email` | `VARCHAR(255)` | X | X | O | 없음 | 로그인 이메일, 중복 불가 |
| `password` | `VARCHAR(255)` | X | X | O | 없음 | 비밀번호 |
| `nickname` | `VARCHAR(30)` | X | X | O | 없음 | 사용자 닉네임 |
| `created_at` | `TIMESTAMPTZ` | X | X | O | `NOW()` | 가입일 |
| `updated_at` | `TIMESTAMPTZ` | X | X | O | `NOW()` | 수정일 |

---

## 10. Post CRUD

### 10.1 기능 설명

게시글 작성, 전체 게시글 조회, 게시글 상세 조회, 게시글 수정, 게시글 삭제 기능을 제공한다.

### 10.2 담당 파일

```text
app/schemes/post_scheme.py
app/services/post_service.py
app/routers/post_router.py
sql/posts.sql
```

### 10.3 Scheme 예시

```python
from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    user_id: int
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostResponse(BaseModel):
    post_id: int
    user_id: int
    title: str
    content: str
    created_at: str
    updated_at: str
```

### 10.4 API 경로

| 기능 | Method | 경로 |
|---|---|---|
| 게시글 작성 | `POST` | `/posts` |
| 전체 게시글 조회 | `GET` | `/posts` |
| 게시글 한 개 조회 | `GET` | `/posts/{post_id}` |
| 게시글 수정 | `PUT` | `/posts/{post_id}` |
| 게시글 삭제 | `DELETE` | `/posts/{post_id}` |

### 10.5 게시글 작성 Request

```json
{
  "user_id": 1,
  "title": "FastAPI 팀 프로젝트 시작",
  "content": "오늘부터 게시판 API를 구현합니다."
}
```

### 10.6 게시글 작성 Response

```json
{
  "post_id": 1,
  "user_id": 1,
  "title": "FastAPI 팀 프로젝트 시작",
  "content": "오늘부터 게시판 API를 구현합니다.",
  "created_at": "2026-07-22T10:10:00+09:00",
  "updated_at": "2026-07-22T10:10:00+09:00"
}
```

### 10.7 게시글 수정 Request

```json
{
  "title": "FastAPI 팀 프로젝트 진행 중",
  "content": "게시글 CRUD를 구현하고 있습니다."
}
```

### 10.8 게시글 삭제 Response

```json
{
  "message": "게시글이 삭제되었습니다.",
  "post_id": 1
}
```

### 10.9 Post 테이블 컬럼

| 컬럼 | 자료형 | PK | FK | NOT NULL | DEFAULT | 설명 |
|---|---|---|---|---|---|---|
| `post_id` | `BIGINT` | O | X | O | 자동 증가 | 게시글 번호 |
| `user_id` | `BIGINT` | X | `users.user_id` | O | 없음 | 게시글 작성자 |
| `title` | `VARCHAR(200)` | X | X | O | 없음 | 게시글 제목 |
| `content` | `TEXT` | X | X | O | 없음 | 게시글 내용 |
| `created_at` | `TIMESTAMPTZ` | X | X | O | `NOW()` | 작성일 |
| `updated_at` | `TIMESTAMPTZ` | X | X | O | `NOW()` | 수정일 |

---

## 11. Comment CRUD

### 11.1 기능 설명

특정 게시글에 댓글을 작성하고, 전체 또는 게시글별 댓글을 조회하며, 댓글 내용 수정 및 삭제 기능을 제공한다.

### 11.2 담당 파일

```text
app/schemes/comment_scheme.py
app/services/comment_service.py
app/routers/comment_router.py
sql/comments.sql
```

### 11.3 Scheme 예시

```python
from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    user_id: int
    content: str = Field(min_length=1, max_length=1000)


class CommentUpdate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)


class CommentResponse(BaseModel):
    comment_id: int
    post_id: int
    user_id: int
    content: str
    created_at: str
    updated_at: str
```

### 11.4 API 경로

| 기능 | Method | 경로 |
|---|---|---|
| 댓글 작성 | `POST` | `/posts/{post_id}/comments` |
| 전체 댓글 조회 | `GET` | `/comments` |
| 게시글별 댓글 조회 | `GET` | `/posts/{post_id}/comments` |
| 댓글 한 개 조회 | `GET` | `/comments/{comment_id}` |
| 댓글 수정 | `PUT` | `/comments/{comment_id}` |
| 댓글 삭제 | `DELETE` | `/comments/{comment_id}` |

### 11.5 댓글 작성 Request

`post_id`는 URL에서 받고, `user_id`와 `content`는 요청 본문에서 받는다.

```json
{
  "user_id": 2,
  "content": "좋은 게시글입니다."
}
```

### 11.6 댓글 작성 Response

```json
{
  "comment_id": 1,
  "post_id": 1,
  "user_id": 2,
  "content": "좋은 게시글입니다.",
  "created_at": "2026-07-22T10:20:00+09:00",
  "updated_at": "2026-07-22T10:20:00+09:00"
}
```

### 11.7 댓글 수정 Request

```json
{
  "content": "내용이 이해하기 쉽게 정리되어 있습니다."
}
```

### 11.8 댓글 삭제 Response

```json
{
  "message": "댓글이 삭제되었습니다.",
  "comment_id": 1
}
```

### 11.9 Comment 테이블 컬럼

| 컬럼 | 자료형 | PK | FK | NOT NULL | DEFAULT | 설명 |
|---|---|---|---|---|---|---|
| `comment_id` | `BIGINT` | O | X | O | 자동 증가 | 댓글 번호 |
| `post_id` | `BIGINT` | X | `posts.post_id` | O | 없음 | 댓글이 작성된 게시글 |
| `user_id` | `BIGINT` | X | `users.user_id` | O | 없음 | 댓글 작성자 |
| `content` | `TEXT` | X | X | O | 없음 | 댓글 내용 |
| `created_at` | `TIMESTAMPTZ` | X | X | O | `NOW()` | 작성일 |
| `updated_at` | `TIMESTAMPTZ` | X | X | O | `NOW()` | 수정일 |

---

## 12. Support CRUD

### 12.1 기능 설명

사용자가 서비스 이용 중 발생한 문제나 요청사항을 문의로 등록하고, 문의 내용을 조회·수정·삭제할 수 있는 기능을 제공한다.

본 프로젝트에서는 `support`를 하나의 문의사항 데이터로 사용한다. `status`는 문의 처리 상태를 나타낸다.

### 12.2 담당 파일

```text
app/schemes/support_scheme.py
app/services/support_service.py
app/routers/support_router.py
sql/supports.sql
```

### 12.3 Scheme 예시

```python
from typing import Literal

from pydantic import BaseModel, Field


class SupportCreate(BaseModel):
    user_id: int
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class SupportUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    status: Literal["pending", "answered", "closed"]


class SupportResponse(BaseModel):
    support_id: int
    user_id: int
    title: str
    content: str
    status: str
    created_at: str
    updated_at: str
```

### 12.4 API 경로

| 기능 | Method | 경로 |
|---|---|---|
| 문의 작성 | `POST` | `/supports` |
| 전체 문의 조회 | `GET` | `/supports` |
| 문의 한 개 조회 | `GET` | `/supports/{support_id}` |
| 문의 수정 | `PUT` | `/supports/{support_id}` |
| 문의 삭제 | `DELETE` | `/supports/{support_id}` |

### 12.5 문의 작성 Request

```json
{
  "user_id": 3,
  "title": "게시글 삭제 문의",
  "content": "제가 작성한 게시글이 삭제되지 않습니다."
}
```

### 12.6 문의 작성 Response

```json
{
  "support_id": 1,
  "user_id": 3,
  "title": "게시글 삭제 문의",
  "content": "제가 작성한 게시글이 삭제되지 않습니다.",
  "status": "pending",
  "created_at": "2026-07-22T10:30:00+09:00",
  "updated_at": "2026-07-22T10:30:00+09:00"
}
```

### 12.7 문의 수정 Request

```json
{
  "title": "게시글 삭제 오류 문의",
  "content": "삭제 버튼을 눌러도 게시글이 남아 있습니다.",
  "status": "answered"
}
```

### 12.8 문의 삭제 Response

```json
{
  "message": "문의사항이 삭제되었습니다.",
  "support_id": 1
}
```

### 12.9 Support 테이블 컬럼

| 컬럼 | 자료형 | PK | FK | NOT NULL | DEFAULT | 설명 |
|---|---|---|---|---|---|---|
| `support_id` | `BIGINT` | O | X | O | 자동 증가 | 문의 번호 |
| `user_id` | `BIGINT` | X | `users.user_id` | O | 없음 | 문의 작성자 |
| `title` | `VARCHAR(200)` | X | X | O | 없음 | 문의 제목 |
| `content` | `TEXT` | X | X | O | 없음 | 문의 내용 |
| `status` | `VARCHAR(20)` | X | X | O | `'pending'` | 문의 처리 상태 |
| `created_at` | `TIMESTAMPTZ` | X | X | O | `NOW()` | 작성일 |
| `updated_at` | `TIMESTAMPTZ` | X | X | O | `NOW()` | 수정일 |

---

## 13. Gemini Chat API

> 이 프로젝트에서 사용하는 Gemini 모델은 `gemini-3.5-flash`로 통일한다. 모델명은 코드에 직접 작성하지 않고 `.env`의 `GEMINI_MODEL`에서 읽는다.

### 13.1 기능 설명

사용자가 입력한 질문을 Gemini API에 전달하고, 생성된 답변을 반환한다. 게시글, 회원, 댓글, 문의사항 데이터와 직접 연결하지 않는 독립적인 API로 구현한다.

### 13.2 담당 파일

```text
app/core/chat_config.py
app/schemes/chat_scheme.py
app/services/chat_service.py
app/routers/chat_router.py
```

### 13.3 Scheme 예시

```python
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str
    prompt: str = Field(min_length=1)


class ChatResponse(BaseModel):
    user_id: str
    answer: str
```

### 13.4 API 경로

| 기능 | Method | 경로 |
|---|---|---|
| Gemini 질문 | `POST` | `/chat/gemini` |

### 13.5 Request

```json
{
  "user_id": "user-1",
  "prompt": "FastAPI의 장점을 쉽게 설명해줘."
}
```

### 13.6 Response

```json
{
  "user_id": "user-1",
  "answer": "FastAPI는 빠르고 사용하기 쉬운 Python 웹 프레임워크입니다."
}
```

### 13.7 오류 응답 예시

```json
{
  "detail": "Gemini API 호출 중 오류가 발생했습니다."
}
```

---

## 14. SQL 테이블 설계

### 14.1 테이블 관계

```text
users
 ├── posts
 ├── comments
 └── supports

posts
 └── comments
```

- 회원 한 명은 여러 게시글을 작성할 수 있다.
- 회원 한 명은 여러 댓글을 작성할 수 있다.
- 회원 한 명은 여러 문의사항을 작성할 수 있다.
- 게시글 한 개에는 여러 댓글이 작성될 수 있다.

### 14.2 `users.sql`

```sql
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 14.3 `posts.sql`

```sql
CREATE TABLE IF NOT EXISTS posts (
    post_id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_posts_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);
```

### 14.4 `comments.sql`

```sql
CREATE TABLE IF NOT EXISTS comments (
    comment_id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_comments_post
        FOREIGN KEY (post_id)
        REFERENCES posts(post_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_comments_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);
```

### 14.5 `supports.sql`

```sql
CREATE TABLE IF NOT EXISTS supports (
    support_id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_support_status
        CHECK (status IN ('pending', 'answered', 'closed')),
    CONSTRAINT fk_supports_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);
```

### 14.6 SQL 실행 순서

외래키 관계 때문에 다음 순서대로 실행한다.

```text
1. users.sql
2. posts.sql
3. comments.sql
4. supports.sql
```

`supports`는 `users`만 참조하므로 `users.sql` 실행 후에는 언제든 생성할 수 있다.

### 14.7 Supabase 사용 시 주의사항

- Supabase SQL Editor에서 테이블 생성문을 실행한다.
- 팀원 모두 동일한 테이블명과 컬럼명을 사용한다.
- `user_id`, `post_id`, `comment_id`, `support_id`의 자료형을 통일한다.
- PostgreSQL 테이블은 기본적으로 Row Level Security 설정을 확인해야 한다.
- 서버에서 Service Role Key를 사용할 경우 외부에 노출되지 않도록 한다.
- 미니 프로젝트에서는 인증 기능을 별도로 구현하지 않으므로 RLS 정책을 단순화하거나 수업에서 안내한 방법을 따른다.

---

## 15. 테스트 계획

### 15.1 테스트 파일

| 담당 기능 | 테스트 파일 | 담당자 |
|---|---|---|
| Chat API | `tests/test_chat_router.py` | 윤기화 |
| User CRUD | `tests/test_user_router.py` | 장상옥 |
| Post CRUD | `tests/test_post_router.py` | 손영민 |
| Comment CRUD | `tests/test_comment_router.py` | 권오현 |
| Support CRUD | `tests/test_support_router.py` | 김인혜 |

### 15.2 개인 실행 파일

각 팀원은 `app/main.py`를 수정하지 않고 개인 실행 파일을 만든다.

| 팀원 | 개인 실행 파일 | 실행 명령어 |
|---|---|---|
| 윤기화 | `app/ygh.py` | `uvicorn app.ygh:app --reload` |
| 손영민 | `app/sym.py` | `uvicorn app.sym:app --reload` |
| 김인혜 | `app/kih.py` | `uvicorn app.kih:app --reload` |
| 장상옥 | `app/jso.py` | `uvicorn app.jso:app --reload` |
| 권오현 | `app/koh.py` | `uvicorn app.koh:app --reload` |

### 15.3 개인 실행 파일 예시

`app/jso.py`

```python
from fastapi import FastAPI

from app.routers.user_router import user_router


app = FastAPI(title="User CRUD Test")
app.include_router(user_router)
```

### 15.4 pytest 예시

```python
from fastapi.testclient import TestClient

from app.jso import app


client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": "1234",
            "nickname": "테스트",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "password" not in response.json()
```

### 15.5 User 테스트 항목

- 회원가입 성공
- 전체 회원 조회 성공
- 회원 한 명 조회 성공
- 회원정보 수정 성공
- 회원 삭제 성공
- 중복 이메일 가입 시 오류
- 존재하지 않는 회원 조회 시 `404`
- 이메일 형식이 잘못된 경우 `422`
- 비밀번호 또는 닉네임 누락 시 `422`
- 응답에 비밀번호가 포함되지 않는지 확인

### 15.6 Post 테스트 항목

- 게시글 작성 성공
- 전체 게시글 조회 성공
- 게시글 한 개 조회 성공
- 게시글 수정 성공
- 게시글 삭제 성공
- 제목 누락 시 `422`
- 내용 누락 시 `422`
- 존재하지 않는 게시글 조회·수정·삭제 시 `404`

### 15.7 Comment 테스트 항목

- 댓글 작성 성공
- 전체 댓글 조회 성공
- 게시글별 댓글 조회 성공
- 댓글 한 개 조회 성공
- 댓글 수정 성공
- 댓글 삭제 성공
- 댓글 내용 누락 시 `422`
- 존재하지 않는 댓글 조회·수정·삭제 시 `404`

### 15.8 Support 테스트 항목

- 문의사항 작성 성공
- 전체 문의사항 조회 성공
- 문의사항 한 개 조회 성공
- 문의사항 수정 성공
- 문의사항 삭제 성공
- 문의 제목 또는 내용 누락 시 `422`
- 잘못된 `status` 입력 시 `422`
- 존재하지 않는 문의 조회·수정·삭제 시 `404`

### 15.9 Chat 테스트 항목

- 정상 질문 요청 성공
- 빈 질문 입력 시 `422`
- Gemini API 응답 반환 확인
- API Key가 없을 때 오류 처리 확인
- 외부 API 호출 실패 시 오류 응답 확인

### 15.10 테스트 실행

전체 테스트:

```bash
pytest
```

특정 파일만 테스트:

```bash
pytest tests/test_user_router.py
```

상세 결과 확인:

```bash
pytest -v
```

> `tests/` 폴더는 `.gitignore`에 포함되므로 테스트 코드는 각자의 컴퓨터에만 저장된다.

---

## 16. README 작성 예시

아래 내용을 `README.md`의 기본 구조로 사용한다.

````markdown
# FastAPI Board & Support API

FastAPI, Supabase, Gemini API를 이용하여 구현한 게시판 팀 프로젝트입니다.

## 프로젝트 소개

다음 기능을 제공합니다.

- 회원 CRUD
- 게시글 CRUD
- 댓글 CRUD
- 문의사항 CRUD
- Gemini Chat API

## 기술 스택

- Python 3.12.7
- FastAPI
- Pydantic
- Uvicorn
- Supabase PostgreSQL
- Google Gemini API
- pytest

## 프로젝트 구조

```text
app/
  main.py
  core/
  routers/
  schemes/
  services/
sql/
tests/
```

## 설치 방법

```bash
python -m venv .venv
```

Windows 가상환경 활성화:

```bash
.venv\Scripts\activate
```

의존성 설치:

```bash
pip install -r requirements.txt
```

## 환경변수

프로젝트 루트에 `.env` 파일을 생성합니다.

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash
PYTHON_VERSION=3.12.7
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
```

## 서버 실행

최종 통합 서버:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## API 목록

| 기능 | Method | 경로 |
|---|---|---|
| 회원가입 | POST | `/users` |
| 회원 조회 | GET | `/users` |
| 게시글 작성 | POST | `/posts` |
| 게시글 조회 | GET | `/posts` |
| 댓글 작성 | POST | `/posts/{post_id}/comments` |
| 문의 작성 | POST | `/supports` |
| Gemini 질문 | POST | `/chat/gemini` |

## 역할 분담

| 팀원 | 담당 |
|---|---|
| 윤기화 | 팀장, 프로젝트 구조, Gemini API, 최종 통합 |
| 손영민 | Post CRUD |
| 김인혜 | Support CRUD |
| 장상옥 | User CRUD |
| 권오현 | Comment CRUD |

## 브랜치 전략

- `feature/ygh`
- `feature/sym`
- `feature/kih`
- `feature/jso`
- `feature/koh`

각 팀원은 개인 브랜치에서 작업한 뒤 Push하고, 팀장이 `main` 브랜치에 최종 통합합니다.

## Git 규칙

- `.env`는 업로드하지 않습니다.
- 개인 실행 파일은 업로드하지 않습니다.
- `tests/` 폴더는 업로드하지 않습니다.
- API Key는 코드에 직접 작성하지 않습니다.
- 작업 전 `main` 브랜치를 최신화합니다.
````

---

## 17. 완료 기준

### 17.1 공통 완료 기준

- [ ] 프로젝트 기본 폴더 구조가 생성되어 있다.
- [ ] `requirements.txt`로 필요한 라이브러리를 설치할 수 있다.
- [ ] `.env.example`이 작성되어 있다.
- [ ] `.env`와 개인 파일이 `.gitignore`에 등록되어 있다.
- [ ] Supabase 테이블이 정상적으로 생성되어 있다.
- [ ] 각 기능이 `scheme`, `service`, `router`로 분리되어 있다.
- [ ] 각 팀원이 개인 실행 파일로 자신의 API를 실행할 수 있다.
- [ ] Swagger UI에서 각 API를 직접 호출할 수 있다.
- [ ] 각 팀원이 본인 기능의 pytest를 로컬에서 통과했다.
- [ ] 각 팀원이 자신의 브랜치에 코드를 Push했다.
- [ ] 팀장이 각 브랜치를 확인하고 `main`에 통합했다.

### 17.2 User 완료 기준

- [ ] 회원가입이 가능하다.
- [ ] 전체 회원과 특정 회원을 조회할 수 있다.
- [ ] 회원정보를 수정할 수 있다.
- [ ] 회원을 삭제할 수 있다.
- [ ] 비밀번호가 응답에 포함되지 않는다.

### 17.3 Post 완료 기준

- [ ] 게시글을 작성할 수 있다.
- [ ] 전체 게시글과 특정 게시글을 조회할 수 있다.
- [ ] 게시글 제목과 내용을 수정할 수 있다.
- [ ] 게시글을 삭제할 수 있다.

### 17.4 Comment 완료 기준

- [ ] 특정 게시글에 댓글을 작성할 수 있다.
- [ ] 전체 댓글, 게시글별 댓글, 특정 댓글을 조회할 수 있다.
- [ ] 댓글 내용을 수정할 수 있다.
- [ ] 댓글을 삭제할 수 있다.

### 17.5 Support 완료 기준

- [ ] 문의사항을 작성할 수 있다.
- [ ] 전체 문의사항과 특정 문의사항을 조회할 수 있다.
- [ ] 문의 제목, 내용, 상태를 수정할 수 있다.
- [ ] 문의사항을 삭제할 수 있다.

### 17.6 Gemini Chat 완료 기준

- [ ] `.env`의 API Key를 이용하여 Gemini에 연결할 수 있다.
- [ ] 사용자의 질문을 Gemini API에 전달할 수 있다.
- [ ] Gemini의 답변을 JSON으로 반환할 수 있다.
- [ ] API 오류를 적절한 HTTP 오류로 처리할 수 있다.

### 17.7 최종 통합 기준

팀장은 모든 라우터를 `app/main.py`에 등록한다.

```python
from fastapi import FastAPI

from app.routers.chat_router import chat_router
from app.routers.comment_router import comment_router
from app.routers.post_router import post_router
from app.routers.support_router import support_router
from app.routers.user_router import user_router


app = FastAPI(title="FastAPI Board & Support API")

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(support_router)
app.include_router(chat_router)
```

최종 실행 명령어:

```bash
uvicorn app.main:app --reload
```

최종 확인 주소:

```text
http://127.0.0.1:8000/docs
```

모든 API가 Swagger UI에서 정상적으로 나타나고 요청·응답이 동작하면 프로젝트를 완료한다.
