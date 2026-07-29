import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def classify_issue(issue: str):

    prompt = f"""
You are an AI civic issue classifier.

Analyze this complaint.

Complaint:
{issue}

Return ONLY valid JSON.

Format:

{{
"title":"",
"category":"",
"severity":"",
"department":"",
"description":"",
"confidence":0.95
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)