import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "pepiniere.db"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-pepiniere-secret")
    DATABASE = str(DATABASE_PATH)
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
