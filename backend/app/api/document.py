from app.services.pdf_service import extract_text
import os
import shutil
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.repositories.document_repository import (
    create_document,
    get_documents
)

from app.schemas.document_schema import (
    DocumentResponse
)

UPLOAD_FOLDER = "uploads"

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/upload",
    response_model=DocumentResponse
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    allowed_extensions = [
        ".pdf",
        ".docx",
        ".txt"
    ]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are allowed."
        )

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    document = create_document(
        db=db,
        filename=file.filename,
        filepath=filepath,
        content_type=file.content_type,
        user_id=current_user.id
    )

    return document


@router.get(
    "",
    response_model=list[DocumentResponse]
)
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_documents(
        db=db,
        user_id=current_user.id
    )