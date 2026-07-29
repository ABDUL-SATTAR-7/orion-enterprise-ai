from pydantic import BaseModel
from datetime import datetime

from app.schemas.message_schema import MessageResponse


class ConversationCreate(BaseModel):
    title: str = "New Chat"


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class ConversationDetailResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    messages: list[MessageResponse]

    model_config = {
        "from_attributes": True
    }