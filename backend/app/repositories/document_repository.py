from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    filename: str,
    filepath: str,
    content_type: str,
    user_id: int
):
    document = Document(
        filename=filename,
        filepath=filepath,
        content_type=content_type,
        user_id=user_id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_documents(
    db: Session,
    user_id: int
):
    return (
        db.query(Document)
        .filter(Document.user_id == user_id)
        .all()
    )