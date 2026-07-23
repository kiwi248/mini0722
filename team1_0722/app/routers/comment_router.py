"""댓글 CRUD API 주소와 HTTP 응답 처리를 담당합니다."""

from fastapi import APIRouter, HTTPException, Path, status

from app.schemes.comment_schema import (
    CommentCreate,
    CommentDeleteResponse,
    CommentResponse,
    CommentUpdate,
)
from app.services.comment_service import (
    comment_create,
    comment_delete,
    comment_get,
    comment_get_all,
    comment_get_by_post,
    comment_update,
)


comment_router = APIRouter()


# 특정 게시글에 새로운 댓글을 생성합니다.
@comment_router.post(
    "/posts/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Comment - Create"],
)
def create_comment(
    comment: CommentCreate,
    post_id: int = Path(gt=0),
) -> CommentResponse:
    created_comment = comment_create(post_id, comment)
    if created_comment is None:
        raise HTTPException(status_code=500, detail="댓글 생성에 실패했습니다.")
    return created_comment


# 저장된 모든 댓글을 조회합니다.
@comment_router.get(
    "/comments",
    response_model=list[CommentResponse],
    tags=["Comment - Read"],
)
def get_all_comments() -> list[CommentResponse]:
    return comment_get_all()


# 특정 게시글에 작성된 댓글만 조회합니다.
@comment_router.get(
    "/posts/{post_id}/comments",
    response_model=list[CommentResponse],
    tags=["Comment - Read"],
)
def get_comments_by_post(post_id: int = Path(gt=0)) -> list[CommentResponse]:
    return comment_get_by_post(post_id)


# 댓글 번호로 댓글 한 건을 조회합니다.
@comment_router.get(
    "/comments/{comment_id}",
    response_model=CommentResponse,
    tags=["Comment - Read"],
)
def get_comment(comment_id: int = Path(gt=0)) -> CommentResponse:
    comment = comment_get(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    return comment


# 댓글 번호에 해당하는 댓글 내용을 수정합니다.
@comment_router.put(
    "/comments/{comment_id}",
    response_model=CommentResponse,
    tags=["Comment - Update"],
)
def update_comment(
    comment: CommentUpdate,
    comment_id: int = Path(gt=0),
) -> CommentResponse:
    updated_comment = comment_update(comment_id, comment)
    if updated_comment is None:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    return updated_comment


# 댓글 번호에 해당하는 댓글을 삭제합니다.
@comment_router.delete(
    "/comments/{comment_id}",
    response_model=CommentDeleteResponse,
    tags=["Comment - Delete"],
)
def delete_comment(comment_id: int = Path(gt=0)) -> CommentDeleteResponse:
    deleted_comment = comment_delete(comment_id)
    if deleted_comment is None:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    return CommentDeleteResponse(
        message="댓글을 삭제했습니다.",
        comment_id=deleted_comment.comment_id,
    )
