from app.services.gemini_service import ask_gemini


def chat_with_ai(message: str) -> str:
    return ask_gemini(message)