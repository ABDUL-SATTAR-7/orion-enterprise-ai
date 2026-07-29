from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.user_schema import (
    UserRegister,
    UserResponse,
    TokenResponse
)

from app.repositories.user_repository import (
    create_user,
    get_user_by_email
)

from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ----------------------------
# REGISTER
# ----------------------------
@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    data: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(
        db=db,
        email=data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = create_user(
        db=db,
        name=data.name,
        email=data.email,
        password=hash_password(data.password)
    )

    return user


# ----------------------------
# LOGIN
# ----------------------------
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    print("\n========== LOGIN DEBUG ==========")
    print("USERNAME :", form_data.username)
    print("PASSWORD :", form_data.password)

    user = get_user_by_email(
        db=db,
        email=form_data.username
    )

    print("USER FOUND :", user)

    if user is None:
        print("RESULT : USER NOT FOUND")
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    print("HASH IN DATABASE :", user.password)

    password_ok = verify_password(
        form_data.password,
        user.password
    )

    print("PASSWORD MATCH :", password_ok)

    if not password_ok:
        print("RESULT : PASSWORD INCORRECT")
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    print("TOKEN GENERATED SUCCESSFULLY")
    print("================================\n")

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )