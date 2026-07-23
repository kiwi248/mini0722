"""Supabase comments 테이블의 댓글 생성, 조회, 수정, 삭제를 담당합니다."""

from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.supabase_client import get_supabase
from app.schemes.comment_schema import CommentCreate, CommentResponse, CommentUpdate


def _to_comment(data: dict) -> CommentResponse:
    """Supabase 응답 한 건을 댓글 응답 모델로 변환합니다."""

    return CommentResponse.model_validate(data)


def comment_create(post_id: int, comment: CommentCreate) -> CommentResponse | None:
    """특정 게시글에 댓글을 생성합니다."""

    result = (
        get_supabase()
        .table("comments")
        .insert(
            {
                "post_id": post_id,
                "user_id": comment.user_id,
                "content": comment.content,
            }
        )
        .execute()
    )
    return _to_comment(result.data[0]) if result.data else None


def comment_get_all() -> list[CommentResponse]:
    """모든 댓글을 최신 작성 순서로 조회합니다."""

    result = (
        get_supabase()
        .table("comments")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return [_to_comment(item) for item in result.data]


def comment_get_by_post(post_id: int) -> list[CommentResponse]:
    """특정 게시글에 작성된 댓글을 조회합니다."""

    result = (
        get_supabase()
        .table("comments")
        .select("*")
        .eq("post_id", post_id)
        .order("created_at")
        .execute()
    )
    return [_to_comment(item) for item in result.data]


def comment_get(comment_id: int) -> CommentResponse | None:
    """댓글 번호로 댓글 한 건을 조회합니다."""

    result = (
        get_supabase()
        .table("comments")
        .select("*")
        .eq("comment_id", comment_id)
        .limit(1)
        .execute()
    )
    return _to_comment(result.data[0]) if result.data else None


def comment_update(
    comment_id: int,
    comment: CommentUpdate,
) -> CommentResponse | None:
    """댓글 내용과 수정 시각을 갱신합니다."""

    result = (
        get_supabase()
        .table("comments")
        .update(
            {
                "content": comment.content,
                "updated_at": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
            }
        )
        .eq("comment_id", comment_id)
        .execute()
    )
    return _to_comment(result.data[0]) if result.data else None


def comment_delete(comment_id: int) -> CommentResponse | None:
    """댓글을 삭제하고 삭제된 댓글 정보를 반환합니다."""

    result = (
        get_supabase()
        .table("comments")
        .delete()
        .eq("comment_id", comment_id)
        .execute()
    )
    return _to_comment(result.data[0]) if result.data else None
