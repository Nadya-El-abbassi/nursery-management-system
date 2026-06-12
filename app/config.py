import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "pepiniere.db"

load_dotenv(BASE_DIR / ".env", override=True)


def get_groq_api_key():
    load_dotenv(BASE_DIR / ".env", override=True)
    return (
        os.environ.get("GROQ_API_KEY") or os.environ.get("GROK_API_KEY", "")
    ).strip()


def get_groq_model():
    load_dotenv(BASE_DIR / ".env", override=True)
    return os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-pepiniere-secret")
    DATABASE = str(DATABASE_PATH)
    ENV_FILE = str(BASE_DIR / ".env")
    GROQ_API_KEY = get_groq_api_key()
    GROQ_MODEL = get_groq_model()
    GROQ_API_BASE_URL = os.environ.get("GROQ_API_BASE_URL", "https://api.groq.com/openai/v1")
