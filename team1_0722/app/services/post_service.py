"""Supabase의 posts 테이블을 처리하는 게시글 CRUD 서비스입니다.

실행 방법(프로젝트 루트에서):
    uvicorn app.sym:app --reload
테스트 방법:
    pytest tests/test_post_router.py -v
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.supabase_client import get_supabase
from app.schemes.post_scheme import PostCreate, PostResponse, PostUpdate


class PostAuthorNotFoundError(Exception):
    """게시글 작성자에 해당하는 사용자가 없을 때 발생합니다."""


class PostDatabaseError(Exception):
    """Supabase에서 게시글 데이터를 처리하지 못했을 때 발생합니다."""


def create_post(post: PostCreate) -> PostResponse | None:
    try:
        supabase = get_supabase()
        user_result = (
            supabase.table("users")
            .select("user_id")
            .eq("user_id", post.user_id)
            .execute()
        )
        if not user_result.data:
            raise PostAuthorNotFoundError

        result = supabase.table("posts").insert(post.model_dump()).execute()
    except PostAuthorNotFoundError:
        raise
    except Exception as exc:
        raise PostDatabaseError("게시글 생성 중 데이터베이스 오류가 발생했습니다.") from exc

    if not result.data:
        return None
    return PostResponse.model_validate(result.data[0])


def get_posts() -> list[PostResponse]:
    result = (
        get_supabase()
        .table("posts")
        .select("*")
        .order("post_id", desc=True)
        .execute()
    )
    return [PostResponse.model_validate(item) for item in result.data]


def get_post(post_id: int) -> PostResponse | None:
    result = (
        get_supabase()
        .table("posts")
        .select("*")
        .eq("post_id", post_id)
        .execute()
    )
    if not result.data:
        return None
    return PostResponse.model_validate(result.data[0])


def update_post(post_id: int, post: PostUpdate) -> PostResponse | None:
    update_data = post.model_dump()
    update_data["updated_at"] = datetime.now(ZoneInfo("Asia/Seoul")).isoformat()

    result = (
        get_supabase()
        .table("posts")
        .update(update_data)
        .eq("post_id", post_id)
        .execute()
    )
    if not result.data:
        return None
    return PostResponse.model_validate(result.data[0])


def delete_post(post_id: int) -> PostResponse | None:
    result = (
        get_supabase()
        .table("posts")
        .delete()
        .eq("post_id", post_id)
        .execute()
    )
    if not result.data:
        return None
    return PostResponse.model_validate(result.data[0])
