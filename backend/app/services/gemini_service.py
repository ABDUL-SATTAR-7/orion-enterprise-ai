import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(messages) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=messages
        )

        return response.text

    except APIError as e:
        return f"Gemini API Error: {e}"


def generate_title(first_message: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=f"""
Generate a very short chat title.

Rules:
- Maximum 5 words
- No quotes
- No punctuation at the end
- Only return the title

Message:
{first_message}
"""
        )

        return response.text.strip()

    except APIError:
        return "New Chat"