from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from app.config import Config
from app.database import close_db, get_db, init_db
from app.routes import categories


def create_app(config_class=Config):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_class)

    data_dir = Path(app.config["DATABASE"]).parent
    data_dir.mkdir(parents=True, exist_ok=True)

    from app.routes import ai, dashboard, plants, sales

    app.register_blueprint(dashboard.bp)
    app.register_blueprint(plants.bp)
    app.register_blueprint(sales.bp)
    app.register_blueprint(ai.bp)
    app.register_blueprint(categories.bp)

    app.teardown_appcontext(close_db)

    @app.template_filter("mad")
    def format_mad(value):
        return f"{float(value):.2f} MAD".replace(".", ",")

    with app.app_context():
        init_db()
        _seed_sample_data()

    return app


def _seed_sample_data():
    db = get_db()
    count = db.execute("SELECT COUNT(*) AS c FROM plants").fetchone()["c"]
    if count > 0:
        return

    samples = [
        ("Lavande", "Lavandula angustifolia", 45.00, 45, 10,
         "Plante aromatique, soleil, peu d'arrosage."),
        ("Rosier", "Rosa gallica", 120.00, 20, 5,
         "Fleurs parfumées, exposition ensoleillée."),
        ("Olivier", "Olea europaea", 350.00, 8, 3,
         "Arbre méditerranéen, résistant à la sécheresse."),
        ("Menthe", "Mentha spicata", 25.00, 60, 15,
         "Herbe aromatique, croissance rapide."),
        ("Géranium", "Pelargonium", 35.00, 12, 5,
         "Balcon et terrasse, floraison estivale."),
        ("Thym", "Thymus vulgaris", 30.00, 3, 5,
         "Condiment et ornement, sol drainé."),
    ]

    for name, species, price, qty, threshold, desc in samples:
        db.execute(
            """
            INSERT INTO plants (name, species, price, quantity, alert_threshold, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, species, price, qty, threshold, desc),
        )
    db.commit()
