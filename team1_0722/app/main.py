import logging

from fastapi import FastAPI
from app.routers.chat_router import chat_router
from app.routers.post_router import post_router
from app.routers.user_router import user_router
#from app.routers.product_router import product_router
import app.core.chat_config

logging.basicConfig(level=logging.INFO)


tags_metadata = [
    {
        "name": "Chat",
        "description": "Gemini 모델을 사용해 사용자 메시지에 답변합니다.",
    },
    {
        "name": "Post",
        "description": "Supabase에 저장된 게시글을 생성·조회·수정·삭제합니다.",
    },
    {
        "name": "User",
        "description": "Supabase에 저장된 회원 정보를 생성·조회·수정·삭제합니다.",
    },
    {
        "name": "Comment",
        "description": "Supabase에 저장된 댓글을 생성·조회·수정·삭제합니다.",
    },
]

app = FastAPI(title="Main App", openapi_tags=tags_metadata)

app.include_router(chat_router)
app.include_router(post_router)
app.include_router(user_router)
app.include_router(comment_router)
