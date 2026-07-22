from fastapi import APIRouter, HTTPException, status

from app.core.api_response import ApiResponse
from app.schemas.support_scheme import SupportCreate, SupportUpdate
from app.services.support_service import (
    support_create,
    support_delete,
    support_get,
    support_get_all,
    support_update,
)


support_router = APIRouter(prefix="/supports", tags=["Support"])


@support_router.post("", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
def create_support(support: SupportCreate) -> ApiResponse:
    created_support = support_create(support)
    if created_support is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="문의사항 등록에 실패했습니다.",
        )

    return ApiResponse(
        success=True,
        message="문의사항을 등록했습니다.",
        data=created_support,
    )


@support_router.get("", response_model=ApiResponse)
def get_all_supports() -> ApiResponse:
    supports = support_get_all()
    return ApiResponse(
        success=True,
        message="문의사항 목록을 조회했습니다.",
        data=supports,
    )


@support_router.get("/{support_id}", response_model=ApiResponse)
def get_support(support_id: int) -> ApiResponse:
    support = support_get(support_id)
    if support is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"문의사항 ID {support_id}를 찾을 수 없습니다.",
        )

    return ApiResponse(
        success=True,
        message="문의사항을 조회했습니다.",
        data=support,
    )


@support_router.put("/{support_id}", response_model=ApiResponse)
def update_support(support_id: int, support: SupportUpdate) -> ApiResponse:
    updated_support = support_update(support_id, support)
    if updated_support is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"문의사항 ID {support_id}를 찾을 수 없습니다.",
        )

    return ApiResponse(
        success=True,
        message="문의사항을 수정했습니다.",
        data=updated_support,
    )


@support_router.delete("/{support_id}", response_model=ApiResponse)
def delete_support(support_id: int) -> ApiResponse:
    deleted_support = support_delete(support_id)
    if deleted_support is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"문의사항 ID {support_id}를 찾을 수 없습니다.",
        )

    return ApiResponse(
        success=True,
        message="문의사항을 삭제했습니다.",
        data={"support_id": deleted_support.support_id},
    )
