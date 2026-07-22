# 02 Mini Project

FastAPI 기반의 간단한 백엔드 프로젝트입니다. Gemini API를 이용한 챗봇형 엔드포인트와 상품 관련 API를 제공하며, 테스트 코드도 포함되어 있습니다.

## 프로젝트 개요

이 프로젝트는 다음 기능을 포함합니다.

- Gemini 기반 챗봇 응답 API
- Supabase 기반 상품 생성·조회·수정·삭제 API
- FastAPI 라우터 구조 분리
- pytest 기반 테스트 코드

## 기술 스택

- Python 3.11+
- FastAPI
- Pydantic
- Uvicorn
- pytest
- Google GenAI SDK
- Supabase Python SDK

## 프로젝트 구조

```text
app/
  main.py
  core/
    chat_config.py
    supabase_client.py
  routers/
    chat_router.py
    product_router.py
  schemas/
    chat_schema.py
    product_schema.py
  services/
    chat_service.py
    product_service.py
tests/
  test_chat_router.py
  test_product_router.py
sql/
  product.sql
```

## 설치 방법

1. 가상환경 생성

```bash
python -m venv .venv
```

2. 가상환경 활성화

```bash
.venv\Scripts\activate
```

3. 의존성 설치

```bash
pip install -r requirements.txt
```

## 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 아래 값을 설정합니다.

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

## 실행 방법

서버를 실행하려면 다음 명령을 사용합니다.

```bash
uvicorn app.main:app --reload
```

이후 브라우저 또는 API 테스트 도구에서 아래 주소로 접근할 수 있습니다.

- http://127.0.0.1:8000/docs

## API 엔드포인트

### 채팅

- POST /chat/gemini
  - 요청 본문 예시

```json
{
  "user_id": "user-1",
  "prompt": "안녕"
}
```

### 상품

| 메서드 | 경로 | 설명 |
| --- | --- | --- |
| POST | `/product/create` | 상품 생성 |
| GET | `/product/get/{product_id}` | 상품 단건 조회 |
| GET | `/product/getall` | 상품 전체 조회 |
| PUT | `/product/{product_id}` | 상품 수정 |
| DELETE | `/product/delete/{product_id}` | 상품 삭제 |

상품 생성 요청 본문 예시입니다.

```json
{
  "name": "청바지",
  "price": 20000
}
```

## 테스트 실행

```bash
pytest
```

## 참고 사항

- 상품 API는 Supabase의 `products` 테이블을 사용합니다. 테이블 생성 및 예제 상품 10건은 [sql/product.sql](sql/product.sql)에 있습니다.
- `products` 테이블은 `id`(TEXT), `name`(TEXT), `price`(INTEGER, 0 이상), `created_at`(TIMESTAMP) 컬럼으로 구성됩니다.
- 현재 API 요청 검증은 가격을 1 이상으로 제한합니다. 데이터베이스 제약조건(`price >= 0`)과 정책을 통일하려면 이후 한쪽 기준을 조정해야 합니다.
- Gemini 응답은 환경 변수로 설정된 API 키를 사용합니다.
- `SUPABASE_SERVICE_ROLE_KEY`는 강한 권한을 가지므로 클라이언트 코드에 포함하거나 공개 저장소에 올리면 안 됩니다. `.env` 파일은 Git에 추가하지 마세요.
