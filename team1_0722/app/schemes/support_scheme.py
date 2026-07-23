from typing import Literal

from pydantic import BaseModel, Field


class SupportCreate(BaseModel):
    user_id: int
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class SupportUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    status: Literal["pending", "answered", "closed"]


class SupportResponse(BaseModel):
    support_id: int
    user_id: int
    title: str
    content: str
    status: str
    created_at: str
    updated_at: str
