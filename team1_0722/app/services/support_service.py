from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.supabase_client import get_supabase
from app.schemas.support_scheme import (
    SupportCreate,
    SupportResponse,
    SupportUpdate,
)


def support_create(support: SupportCreate) -> SupportResponse | None:
    supabase = get_supabase()
    result = (
        supabase.table("supports")
        .insert(
            {
                "user_id": support.user_id,
                "title": support.title,
                "content": support.content,
            }
        )
        .execute()
    )

    if not result.data:
        return None
    return SupportResponse.model_validate(result.data[0])


def support_get_all() -> list[SupportResponse]:
    supabase = get_supabase()
    result = (
        supabase.table("supports")
        .select("*")
        .order("support_id", desc=True)
        .execute()
    )
    return [SupportResponse.model_validate(item) for item in result.data]


def support_get(support_id: int) -> SupportResponse | None:
    supabase = get_supabase()
    result = (
        supabase.table("supports")
        .select("*")
        .eq("support_id", support_id)
        .execute()
    )

    if not result.data:
        return None
    return SupportResponse.model_validate(result.data[0])


def support_update(
    support_id: int,
    support: SupportUpdate,
) -> SupportResponse | None:
    supabase = get_supabase()
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    result = (
        supabase.table("supports")
        .update(
            {
                "title": support.title,
                "content": support.content,
                "status": support.status,
                "updated_at": now.isoformat(),
            }
        )
        .eq("support_id", support_id)
        .execute()
    )

    if not result.data:
        return None
    return SupportResponse.model_validate(result.data[0])


def support_delete(support_id: int) -> SupportResponse | None:
    supabase = get_supabase()
    result = (
        supabase.table("supports")
        .delete()
        .eq("support_id", support_id)
        .execute()
    )

    if not result.data:
        return None
    return SupportResponse.model_validate(result.data[0])
