from __future__ import annotations

import base64
from datetime import datetime
import hashlib
import logging
import secrets
from typing import Any
from zoneinfo import ZoneInfo

from app.core.supabase_client import get_supabase
from app.schemes.user_schema import UserCreate, UserPublic, UserUpdate

logger = logging.getLogger(__name__)


class UserServiceError(Exception):
    """데이터베이스 처리 실패를 API 계층에 안전하게 전달합니다."""


class DuplicateEmailError(UserServiceError):
    pass


def _generate_user_id() -> str:
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    return now.strftime("%Y%m%d%H%M%S%f")[:17]


def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 600_000)
    return "pbkdf2_sha256$600000$" + base64.b64encode(salt).decode() + "$" + base64.b64encode(digest).decode()


def _to_public(row: dict[str, Any]) -> UserPublic:
    return UserPublic.model_validate(row)


def _email_exists(email: str, excluded_user_id: str | None = None) -> bool:
    query = get_supabase().table("users").select("user_id").eq("email", email)
    if excluded_user_id is not None:
        query = query.neq("user_id", excluded_user_id)
    return bool(query.limit(1).execute().data)


def user_create(user: UserCreate) -> UserPublic:
    try:
        if _email_exists(user.email):
            raise DuplicateEmailError
        result = (
            get_supabase()
            .table("users")
            .insert(
                {
                    "user_id": _generate_user_id(),
                    "email": user.email,
                    "password": _hash_password(user.password),
                    "name": user.name,
                }
            )
            .execute()
        )
        if not result.data:
            raise UserServiceError
        return _to_public(result.data[0])
    except DuplicateEmailError:
        raise
    except Exception as exc:
        logger.exception("user_create failed for email=%s", user.email)
        raise UserServiceError from exc


def user_get_all() -> list[UserPublic]:
    try:
        result = get_supabase().table("users").select("user_id,email,name,created_at,updated_at").execute()
        return [_to_public(row) for row in result.data]
    except Exception as exc:
        logger.exception("user_get_all failed")
        raise UserServiceError from exc


def user_get(user_id: str) -> UserPublic | None:
    try:
        result = (
            get_supabase()
            .table("users")
            .select("user_id,email,name,created_at,updated_at")
            .eq("user_id", user_id)
            .execute()
        )
        return _to_public(result.data[0]) if result.data else None
    except Exception as exc:
        logger.exception("user_get failed for user_id=%s", user_id)
        raise UserServiceError from exc


def user_update(user_id: str, user: UserUpdate) -> UserPublic | None:
    try:
        if user_get(user_id) is None:
            return None
        if _email_exists(user.email, excluded_user_id=user_id):
            raise DuplicateEmailError
        result = (
            get_supabase()
            .table("users")
            .update(
                {
                    "email": user.email,
                    "password": _hash_password(user.password),
                    "name": user.name,
                }
            )
            .eq("user_id", user_id)
            .execute()
        )
        return _to_public(result.data[0]) if result.data else None
    except (DuplicateEmailError, UserServiceError):
        raise
    except Exception as exc:
        logger.exception("user_update failed for user_id=%s", user_id)
        raise UserServiceError from exc


def user_delete(user_id: str) -> UserPublic | None:
    try:
        result = (
            get_supabase()
            .table("users")
            .delete()
            .eq("user_id", user_id)
            .execute()
        )
        return _to_public(result.data[0]) if result.data else None
    except Exception as exc:
        logger.exception("user_delete failed for user_id=%s", user_id)
        raise UserServiceError from exc
