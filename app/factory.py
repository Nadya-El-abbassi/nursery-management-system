"""Squelette — assemble l'application sans logique métier A/B."""

from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader

from app.config import Config
from app.database import close_db

BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "feature_m2_crud"
FRONTEND_DIR = BASE_DIR / "feature_m3_ai"


def create_base_app(config_class=Config):
    load_dotenv()

    app = Flask(
        __name__,
        static_folder=str(FRONTEND_DIR / "static"),
        static_url_path="/static",
    )
    app.config.from_object(config_class)

    data_dir = Path(app.config["DATABASE"]).parent
    data_dir.mkdir(parents=True, exist_ok=True)

    app.teardown_appcontext(close_db)

    @app.template_filter("mad")
    def format_mad(value):
        return f"{float(value):.2f} MAD".replace(".", ",")

    return app


def create_app(config_class=Config):
    app = create_base_app(config_class)

    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(str(FRONTEND_DIR / "templates")),
        FileSystemLoader(str(BACKEND_DIR / "templates")),
    ])

    from feature_m2_crud.register import register as register_m2_crud
    from feature_m3_ai.register import register as register_m3_ai

    register_m2_crud(app)
    register_m3_ai(app)

    return app
