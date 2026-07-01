import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY fehlt. Kopiere .env.example zu .env und trage deinen Key ein "
        "(kostenlos erhältlich auf https://ai.google.dev)."
    )
