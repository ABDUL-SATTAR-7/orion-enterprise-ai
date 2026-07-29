from sqlalchemy.orm import Session

from app.models.conversation import Conversation


def create_conversation(
    db: Session,
    user_id: int,
    title: str = "New Chat"
):
    conversation = Conversation(
        title=title,
        user_id=user_id
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_all_conversations(
    db: Session,
    user_id: int
):
    return (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id
        )
        .order_by(
            Conversation.updated_at.desc()
        )
        .all()
    )


def get_conversation(
    db: Session,
    conversation_id: int,
    user_id: int
):
    return (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        .first()
    )


def update_conversation_title(
    db: Session,
    conversation_id: int,
    user_id: int,
    title: str
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        .first()
    )

    if conversation:
        conversation.title = title
        db.commit()
        db.refresh(conversation)

    return conversation


def delete_conversation(
    db: Session,
    conversation_id: int,
    user_id: int
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        .first()
    )

    if conversation:
        db.delete(conversation)
        db.commit()

    return conversation