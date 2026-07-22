"""게시글 API의 요청/응답 데이터 모델입니다.

실행 방법(프로젝트 루트에서):
    uvicorn app.sym:app --reload
실행 후 문서 확인:
    http://127.0.0.1:8000/docs
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    user_id: int = Field(gt=0, examples=[1])
    title: str = Field(min_length=1, max_length=200, examples=["FastAPI 프로젝트 시작"])
    content: str = Field(min_length=1, examples=["게시글 API를 구현합니다."])


class PostUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200, examples=["FastAPI 프로젝트 진행 중"])
    content: str = Field(min_length=1, examples=["게시글 CRUD를 구현하고 있습니다."])


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    post_id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class PostDeleteResponse(BaseModel):
    message: str
    post_id: int
