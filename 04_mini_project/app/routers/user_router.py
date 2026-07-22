from fastapi import APIRouter, HTTPException, status

from app.core.api_response import ApiResponse
from app.schemas.user_schema import UserCreate, UserUpdate
from app.services.user_service import (
    DuplicateEmailError,
    UserServiceError,
    user_create,
    user_delete,
    user_get,
    user_get_all,
    user_update,
)


user_router = APIRouter(prefix="/users", tags=["User"])


def _database_error() -> HTTPException:
    return HTTPException(status_code=500, detail="회원 정보를 처리하는 중 오류가 발생했습니다.")


@user_router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> ApiResponse:
    try:
        created_user = user_create(user)
    except DuplicateEmailError:
        raise HTTPException(status_code=409, detail="이미 사용 중인 이메일입니다.")
    except UserServiceError:
        raise _database_error()
    return ApiResponse(success=True, message="회원이 생성되었습니다.", data=created_user)


@user_router.get("")
def get_users() -> ApiResponse:
    try:
        users = user_get_all()
    except UserServiceError:
        raise _database_error()
    return ApiResponse(success=True, message="회원 목록을 조회했습니다.", data=users)


@user_router.get("/{user_id}")
def get_user(user_id: str) -> ApiResponse:
    try:
        user = user_get(user_id)
    except UserServiceError:
        raise _database_error()
    if user is None:
        raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다.")
    return ApiResponse(success=True, message="회원을 조회했습니다.", data=user)


@user_router.put("/{user_id}")
def update_user(user_id: str, user: UserUpdate) -> ApiResponse:
    try:
        updated_user = user_update(user_id, user)
    except DuplicateEmailError:
        raise HTTPException(status_code=409, detail="이미 사용 중인 이메일입니다.")
    except UserServiceError:
        raise _database_error()
    if updated_user is None:
        raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다.")
    return ApiResponse(success=True, message="회원 정보가 수정되었습니다.", data=updated_user)


@user_router.delete("/{user_id}")
def delete_user(user_id: str) -> ApiResponse:
    try:
        deleted_user = user_delete(user_id)
    except UserServiceError:
        raise _database_error()
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다.")
    return ApiResponse(success=True, message="회원이 삭제되었습니다.", data=deleted_user)
