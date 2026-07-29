from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.repositories.conversation_repository import (
    create_conversation,
    get_all_conversations,
    get_conversation,
    delete_conversation
)

from app.schemas.conversation_schema import (
    ConversationCreate,
    ConversationResponse,
    ConversationDetailResponse
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.post(
    "",
    response_model=ConversationResponse
)
def create_chat(
    data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_conversation(
        db=db,
        user_id=current_user.id,
        title=data.title
    )


@router.get(
    "",
    response_model=list[ConversationResponse]
)
def list_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_conversations(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationDetailResponse
)
def get_chat(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = get_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return conversation


@router.delete(
    "/{conversation_id}"
)
def delete_chat(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = delete_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.id
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return {
        "message": "Conversation deleted successfully"
    }