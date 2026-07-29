from sqlalchemy.orm import Session

from app.models.user import User


def create_user(
    db: Session,
    name: str,
    email: str,
    password: str
):
    try:
        user = User(
            name=name,
            email=email,
            password=password
        )

        db.add(user)

        print("Before Commit")

        db.commit()

        print("After Commit")

        db.refresh(user)

        print("User Saved Successfully")
        print("ID:", user.id)
        print("EMAIL:", user.email)

        return user

    except Exception as e:
        db.rollback()

        print("ERROR SAVING USER")
        print(type(e))
        print(e)

        raise


def get_user_by_email(
    db: Session,
    email: str
):
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    print("Searching Email:", email)
    print("Found:", user)

    return user


def get_user_by_id(
    db: Session,
    user_id: int
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )