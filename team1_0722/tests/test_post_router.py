"""Post CRUD 라우터 테스트입니다.

실행 방법(프로젝트 루트에서):
    pytest tests/test_post_router.py -v
"""

from datetime import datetime

from fastapi.testclient import TestClient

from app.routers import post_router
from app.schemes.post_scheme import PostResponse
from app.services.post_service import PostAuthorNotFoundError, PostDatabaseError
from app.sym import app


client = TestClient(app)


def make_post(post_id: int = 1) -> PostResponse:
    created_at = datetime.fromisoformat("2026-07-22T10:10:00+09:00")
    return PostResponse(
        post_id=post_id,
        user_id=1,
        title="FastAPI 프로젝트 시작",
        content="게시글 API를 구현합니다.",
        created_at=created_at,
        updated_at=created_at,
    )


def test_create_post(monkeypatch):
    monkeypatch.setattr(post_router, "create_post", lambda post: make_post())

    response = client.post(
        "/posts",
        json={"user_id": 1, "title": "FastAPI 프로젝트 시작", "content": "게시글 API를 구현합니다."},
    )

    assert response.status_code == 201
    assert response.json()["post_id"] == 1


def test_create_post_returns_404_when_user_is_missing(monkeypatch):
    def raise_missing_user(post):
        raise PostAuthorNotFoundError

    monkeypatch.setattr(post_router, "create_post", raise_missing_user)

    response = client.post(
        "/posts",
        json={"user_id": 999, "title": "테스트 제목", "content": "테스트 내용"},
    )

    assert response.status_code == 404
    assert "user_id 999" in response.json()["detail"]


def test_create_post_returns_explained_500_on_database_error(monkeypatch):
    def raise_database_error(post):
        raise PostDatabaseError("database error")

    monkeypatch.setattr(post_router, "create_post", raise_database_error)

    response = client.post(
        "/posts",
        json={"user_id": 1, "title": "테스트 제목", "content": "테스트 내용"},
    )

    assert response.status_code == 500
    assert "Supabase 연결 정보" in response.json()["detail"]


def test_get_posts(monkeypatch):
    monkeypatch.setattr(post_router, "get_posts", lambda: [make_post(1), make_post(2)])

    response = client.get("/posts")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_missing_post_returns_404(monkeypatch):
    monkeypatch.setattr(post_router, "get_post", lambda post_id: None)

    response = client.get("/posts/999")

    assert response.status_code == 404


def test_update_post(monkeypatch):
    monkeypatch.setattr(post_router, "update_post", lambda post_id, post: make_post(post_id))

    response = client.put(
        "/posts/1",
        json={"title": "수정된 제목", "content": "수정된 내용"},
    )

    assert response.status_code == 200
    assert response.json()["post_id"] == 1


def test_delete_post(monkeypatch):
    monkeypatch.setattr(post_router, "delete_post", lambda post_id: make_post(post_id))

    response = client.delete("/posts/1")

    assert response.status_code == 200
    assert response.json() == {"message": "게시글이 삭제되었습니다.", "post_id": 1}


def test_post_validation_returns_422():
    response = client.post("/posts", json={"user_id": 1, "title": "", "content": ""})

    assert response.status_code == 422
