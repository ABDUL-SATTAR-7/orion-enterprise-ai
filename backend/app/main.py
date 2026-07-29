from app.models.document import Document
from fastapi import FastAPI
from app.models.user import User
from app.database.database import Base, engine
from app.api.auth import router as auth_router

# Import models so SQLAlchemy registers them
from app.models.conversation import Conversation
from app.models.message import Message

# Import routers
from app.api.chat import router as chat_router
from app.api.conversation import router as conversation_router


app = FastAPI(
    title="Orion Enterprise AI",
    version="1.0.0"
)
app.include_router(auth_router)

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Orion Enterprise AI Backend Running 🚀"
    }


# Register routers
app.include_router(chat_router)
app.include_router(conversation_router)