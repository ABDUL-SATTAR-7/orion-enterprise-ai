from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.repositories.conversation_repository import (
    create_conversation,
    update_conversation_title,
    get_conversation
)

from app.repositories.message_repository import (
    create_message,
    get_messages_by_conversation
)

from app.schemas.chat_schema import (
    ChatRequest,
    ChatResponse
)

from app.services.chat_service import chat_with_ai
from app.services.gemini_service import generate_title

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Create new conversation
    if data.conversation_id is None:

        conversation = create_conversation(
            db=db,
            user_id=current_user.id
        )

        conversation_id = conversation.id

        title = generate_title(data.message)

        update_conversation_title(
            db=db,
            conversation_id=conversation_id,
            user_id=current_user.id,
            title=title
        )

    else:

        conversation = get_conversation(
            db=db,
            conversation_id=data.conversation_id,
            user_id=current_user.id
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )

        conversation_id = conversation.id

    # Save user message
    create_message(
        db=db,
        conversation_id=conversation_id,
        role="user",
        content=data.message
    )

    # Load conversation history
    messages = get_messages_by_conversation(
        db=db,
        conversation_id=conversation_id
    )

    history = []

    for message in messages:

        history.append(
            {
                "role": "model" if message.role == "assistant" else "user",
                "parts": [
                    {
                        "text": message.content
                    }
                ]
            }
        )

    # Ask Gemini
    response = chat_with_ai(history)

    # Save AI response
    create_message(
        db=db,
        conversation_id=conversation_id,
        role="assistant",
        content=response
    )

    return ChatResponse(
        response=response,
        conversation_id=conversation_id
    )