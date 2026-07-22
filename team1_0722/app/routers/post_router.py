"""게시글 CRUD HTTP 경로를 정의합니다.

실행 방법(프로젝트 루트에서):
    uvicorn app.sym:app --reload
Swagger UI:
    http://127.0.0.1:8000/docs
"""

from fastapi import APIRouter, HTTPException, status

from app.schemes.post_scheme import (
    PostCreate,
    PostDeleteResponse,
    PostResponse,
    PostUpdate,
)
from app.services.post_service import (
    PostAuthorNotFoundError,
    PostDatabaseError,
    create_post,
    delete_post,
    get_post,
    get_posts,
    update_post,
)


post_router = APIRouter(prefix="/posts", tags=["Post"])


@post_router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create(post: PostCreate) -> PostResponse:
    try:
        created_post = create_post(post)
    except PostAuthorNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"user_id {post.user_id}에 해당하는 사용자를 찾을 수 없습니다.",
        ) from exc
    except PostDatabaseError as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "게시글 생성 중 데이터베이스 오류가 발생했습니다. "
                "Supabase 연결 정보와 users/posts 테이블을 확인해 주세요."
            ),
        ) from exc

    if created_post is None:
        raise HTTPException(status_code=500, detail="게시글 생성에 실패했습니다.")
    return created_post


@post_router.get("", response_model=list[PostResponse])
def get_all() -> list[PostResponse]:
    try:
        return get_posts()
    except PostDatabaseError as exc:
        raise HTTPException(status_code=500, detail="게시글 목록을 조회하는 중 오류가 발생했습니다.") from exc


@post_router.get("/{post_id}", response_model=PostResponse)
def get_one(post_id: int) -> PostResponse:
    try:
        post = get_post(post_id)
    except PostDatabaseError as exc:
        raise HTTPException(status_code=500, detail="게시글을 조회하는 중 오류가 발생했습니다.") from exc
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return post


@post_router.put("/{post_id}", response_model=PostResponse)
def update(post_id: int, post: PostUpdate) -> PostResponse:
    try:
        updated_post = update_post(post_id, post)
    except PostDatabaseError as exc:
        raise HTTPException(status_code=500, detail="게시글을 수정하는 중 오류가 발생했습니다.") from exc
    if updated_post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return updated_post


@post_router.delete("/{post_id}", response_model=PostDeleteResponse)
def delete(post_id: int) -> PostDeleteResponse:
    try:
        deleted_post = delete_post(post_id)
    except PostDatabaseError as exc:
        raise HTTPException(status_code=500, detail="게시글을 삭제하는 중 오류가 발생했습니다.") from exc
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return PostDeleteResponse(message="게시글이 삭제되었습니다.", post_id=post_id)
