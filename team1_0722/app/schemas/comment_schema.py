"""댓글 생성, 수정, 응답에 사용하는 데이터 형식을 정의합니다."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


CommentContent = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=1000),
]


class CommentCreate(BaseModel):
    """댓글 생성 요청 본문입니다."""

    user_id: int = Field(gt=0, examples=[1])
    content: CommentContent = Field(examples=["댓글 테스트입니다."])


class CommentUpdate(BaseModel):
    """댓글 수정 요청 본문입니다."""

    content: CommentContent = Field(examples=["수정된 댓글입니다."])


class CommentResponse(BaseModel):
    """댓글 API가 반환하는 댓글 정보입니다."""

    comment_id: int
    post_id: int
    user_id: int
    content: str
    created_at: datetime
    updated_at: datetime


class CommentDeleteResponse(BaseModel):
    """댓글 삭제 성공 응답입니다."""

    message: str
    comment_id: int
