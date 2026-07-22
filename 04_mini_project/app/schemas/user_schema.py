from datetime import datetime
import re

from pydantic import BaseModel, Field, field_validator


EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class UserCreate(BaseModel):
    email: str = Field(
        max_length=254,
        description="필수. example@example.com 형식이며 중복될 수 없습니다.",
        examples=["user@example.com"],
    )
    password: str = Field(
        max_length=128,
        description="필수. 8자 이상 128자 이하로 입력합니다.",
        examples=["safe-password"],
    )
    name: str = Field(
        max_length=100,
        description="필수. 공백을 제외한 1자 이상 100자 이하로 입력합니다.",
        examples=["장상옥"],
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized_email = value.strip().lower()
        if not EMAIL_PATTERN.fullmatch(normalized_email):
            raise ValueError("이메일은 example@example.com 형식으로 입력해 주세요.")
        return normalized_email

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("비밀번호는 8자 이상 입력해 주세요.")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        stripped_name = value.strip()
        if not stripped_name:
            raise ValueError("이름은 공백을 제외하고 1자 이상 입력해 주세요.")
        return stripped_name


class UserUpdate(UserCreate):
    pass


class UserPublic(BaseModel):
    user_id: str = Field(
        description="생성 시각을 사용한 YYYYMMDDHHMMSSmmm 형식의 17자리 ID",
        examples=["20260722153045123"],
    )
    email: str
    name: str
    created_at: datetime
    updated_at: datetime
